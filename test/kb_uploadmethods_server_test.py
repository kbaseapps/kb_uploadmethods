# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import shutil
from mock import patch
import mock
import ftplib

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
from kb_uploadmethods.FastqUploaderUtil import FastqUploaderUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils

class kb_uploadmethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_uploadmethods',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_uploadmethods'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = kb_uploadmethods(cls.cfg)

        # copy test file to scratch area
        fq_filename = "SP1.fq"
        fq_path = os.path.join(cls.cfg['scratch'], fq_filename)
        shutil.copy(os.path.join("data", fq_filename), fq_path)

        ftp_connection = ftplib.FTP('ftp.swfwmd.state.fl.us')
        ftp_connection.login('Anonymous', 'fake_email@hotmail.com')
        ftp_connection.cwd("/pub/incoming/")
        if fq_filename not in ftp_connection.nlst():
            fh = open(os.path.join("data", fq_filename), 'rb')
            ftp_connection.storbinary('STOR SP1.fq', fh)
            fh.close()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_uploadmethods_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def getDefaultParams(self, file_path=True):
        if file_path:
            default_input_params = {
                'first_fastq_file_name': 'SP1.fq',
                'sequencing_tech': 'Unknown',
                'reads_file_name': 'test_reads_file_name.reads',
                'workspace_name': self.getWsName()
            }
        else:
            default_input_params = {
                'download_type': 'Direct Download',
                'first_fastq_file_url': 'http://molb7621.github.io/workshop/_downloads/SP1.fq',
                'sequencing_tech': 'Unknown',
                'reads_file_name': 'test_reads_file_name.reads',
                'workspace_name': self.getWsName()
            }
        return default_input_params

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), paramPeters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass

    def test_contructor(self):
        print '------ Testing Contructor Method ------'
        ret = self.getImpl()
        print 'self.config: %s' % ret.config
        print 'self.callback_url: %s' % ret.config['SDK_CALLBACK_URL']
        self.assertIsNotNone(ret.config)
        self.assertIsNotNone(ret.config['SDK_CALLBACK_URL'])
        print '------ Testing Contructor Method OK ------'

    def test_validate_upload_fastq_file_parameters(self):
        print '------ Testing validate_upload_fastq_file_parameters Method ------'

        # Testing required params
        invalidate_input_params = self.getDefaultParams()
        del invalidate_input_params['reads_file_name']
        with self.assertRaisesRegexp(ValueError, '"reads_file_name" parameter is required, but missing'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)
        invalidate_input_params = self.getDefaultParams()
        del invalidate_input_params['workspace_name']
        with self.assertRaisesRegexp(ValueError, '"workspace_name" parameter is required, but missing'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params) 
        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['first_fastq_file_url'] = 'https://fake_url'
        with self.assertRaisesRegexp(ValueError, 'Cannot upload Reads for both file path and file URL'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)          

        # Testing _validate_upload_file_availability
        invalidate_input_params = self.getDefaultParams()
        nonexistent_file_name = 'fake_file_0123456.fastq'
        invalidate_input_params['first_fastq_file_name'] = nonexistent_file_name
        with self.assertRaisesRegexp(ValueError, 'Target file: %s is NOT available.' % nonexistent_file_name):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)    

        # Testing URL prefix
        invalidate_input_params = self.getDefaultParams(file_path=False) 
        invalidate_input_params['first_fastq_file_url'] = 'ftp://Anonymous:fake_email@hotmail.com@ftp.swfwmd.state.fl.us/pub/incoming/SP1.fq' 
        with self.assertRaisesRegexp(ValueError, 'Download type and URL prefix do NOT match'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)   

        invalidate_input_params = self.getDefaultParams(file_path=False) 
        invalidate_input_params['download_type'] = 'DropBox' 
        with self.assertRaisesRegexp(ValueError, 'Download type and URL prefix do NOT match'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)  

        invalidate_input_params = self.getDefaultParams(file_path=False) 
        invalidate_input_params['download_type'] = 'FTP' 
        with self.assertRaisesRegexp(ValueError, 'Download type and URL prefix do NOT match'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)   

        invalidate_input_params = self.getDefaultParams(file_path=False) 
        del invalidate_input_params['download_type']
        with self.assertRaisesRegexp(ValueError, 'Download type parameter is required, but missing'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)  

        print '------ Testing validate_upload_fastq_file_parameters Method OK ------'

    @patch.object(FastqUploaderUtil, '_get_file_path')
    def test_upload_fastq_file_path(self, mock_get_file_path):
        print '------ Testing upload_fastq_file for file path Method ------'
        mock_get_file_path.return_value = '/kb/module/work/tmp/SP1.fq'
        params = self.getDefaultParams()
        ret = self.getImpl().upload_fastq_file(self.getContext(), params)

        print '------ Testing upload_fastq_file for file path Method OK ------'

    def test_upload_fastq_file_url_direct_download(self):
        print '------ Testing upload_fastq_file for Direct Download Link Method ------'
        params = self.getDefaultParams(file_path=False)
        ret = self.getImpl().upload_fastq_file(self.getContext(), params)

        print '------ Testing upload_fastq_file for Direct Download Link Method OK ------'

    def test_upload_fastq_file_url_dropbox(self):
        print '------ Testing upload_fastq_file for DropBox Download Link Method ------'
        params = self.getDefaultParams(file_path=False)
        params['first_fastq_file_url'] = 'https://www.dropbox.com/s/mcl7mual35c5p7s/SP1.fq?dl=0'
        params['download_type'] = 'DropBox'
        ret = self.getImpl().upload_fastq_file(self.getContext(), params)

        print '------ Testing upload_fastq_file for DropBox Download Link Method OK ------'

    def test_upload_fastq_file_url_ftp(self):
        print '------ Testing upload_fastq_file for FTP Link Method ------'
       
        fake_ftp_domain_params = self.getDefaultParams(file_path=False)
        fake_ftp_domain_params['first_fastq_file_url'] = 'ftp://Anonymous:fake_email@hotmail.com@fake_ftp.fake_ftp/pub/incoming/SP1.fq'
        fake_ftp_domain_params['download_type'] = 'FTP'
        with self.assertRaisesRegexp(ValueError, 'Cannot connect:'):
            self.getImpl().upload_fastq_file(self.getContext(), fake_ftp_domain_params)

        fake_ftp_user_params = self.getDefaultParams(file_path=False)
        fake_ftp_user_params['first_fastq_file_url'] = 'ftp://fake_user:fake_email@hotmail.com@ftp.swfwmd.state.fl.us/pub/incoming/SP1.fq'
        fake_ftp_user_params['download_type'] = 'FTP'
        with self.assertRaisesRegexp(ValueError, 'Cannot login:'):
            self.getImpl().upload_fastq_file(self.getContext(), fake_ftp_user_params)

        params = self.getDefaultParams(file_path=False)
        params['first_fastq_file_url'] = 'ftp://Anonymous:fake_email@hotmail.com@ftp.swfwmd.state.fl.us/pub/incoming/SP1.fq'
        params['download_type'] = 'FTP'
        ret = self.getImpl().upload_fastq_file(self.getContext(), params)

        print '------ Testing upload_fastq_file for FTP Link Method OK ------'

