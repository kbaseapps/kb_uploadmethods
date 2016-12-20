# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import shutil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
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
        fq_filename = "interleaved.fastq"
        fq_path = os.path.join(cls.cfg['scratch'], fq_filename)
        shutil.copy(os.path.join("data", fq_filename), fq_path)

        cls.default_input_params = {
            'first_fastq_file_name': 'interleaved.fastq',
            'reads_file_name': 'test_reads_file_name'
        }

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


        print '------------ Testing required params ------'
        invalidate_input_params = self.default_input_params.copy()
        del invalidate_input_params['reads_file_name']
        with self.assertRaisesRegexp(ValueError, '"reads_file_name" parameter is required, but missing'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)        
        print '------------ Testing required params OK------'

        print '------------ Testing _validate_upload_file_availability method ------'
        invalidate_input_params = self.default_input_params.copy()
        nonexistent_file_name = 'fake_file_0123456.fastq'
        invalidate_input_params['first_fastq_file_name'] = nonexistent_file_name
        with self.assertRaisesRegexp(ValueError, 'Target file: %s is NOT available.' % nonexistent_file_name):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)        
        print '------------ Testing _validate_upload_file_availability method OK------'


        print '------ Testing validate_upload_fastq_file_parameters Method OK ------'


    def test_upload_fastq_file(self):
        print '------ Testing upload_fastq_file Method ------'

        params = {
            'first_fastq_file_name': 'interleaved.fastq',
            'reads_file_name': 'test_reads_file_name'
        }

        ret = self.getImpl().upload_fastq_file(self.getContext(), params)


        print '------ Testing upload_fastq_file Method OK ------'

