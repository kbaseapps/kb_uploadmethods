# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import shutil
from mock import patch

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
from kb_uploadmethods.authclient import KBaseAuth as _KBaseAuth
from DataFileUtil.DataFileUtilClient import DataFileUtil
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil


class kb_uploadmethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_uploadmethods'):
            cls.cfg[nameval[0]] = nameval[1]
        authServiceUrl = cls.cfg.get('auth-service-url',
                                     "https://kbase.us/services/authorization/Sessions/Login")
        auth_client = _KBaseAuth(authServiceUrl)
        cls.user_id = auth_client.get_user(cls.token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': cls.token,
                        'user_id': cls.user_id,
                        'provenance': [
                            {'service': 'kb_uploadmethods',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=cls.token)
        cls.serviceImpl = kb_uploadmethods(cls.cfg)
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.scratch = cls.cfg['scratch']
        cls.shockURL = cls.cfg['shock-url']
        cls.prepare_data()

    @classmethod
    def prepare_data(cls):
        # upload genome object
        genbank_file_name = 'small_genbank.gbff'
        genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
        shutil.copy(os.path.join('data', genbank_file_name), genbank_file_path)

        genome_object_name = 'test_Genome'
        cls.genome_ref = cls.gfu.genbank_to_genome(
            {'file': {'path': genbank_file_path}, 'workspace_name': cls.getWsName(),
             'genome_name': genome_object_name})['genome_ref']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def delete_shock_node(cls, node_id):
        header = {'Authorization': 'Oauth {0}'.format(cls.token)}
        requests.delete(cls.shockURL + '/node/' + node_id, headers=header,
                        allow_redirects=True)
        print('Deleted shock node ' + node_id)

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

    def mock_download_staging_file(params):
        print 'Mocking DataFileUtilClient.download_staging_file'
        print params

        fq_filename = params.get('staging_file_subdir_path')
        fq_path = os.path.join('/kb/module/work/tmp', fq_filename)
        shutil.copy(os.path.join("data", fq_filename), fq_path)

        return {'copy_file_path': fq_path}

    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    def test_bad_as_media_from_staging(self):
        invalid_params = {
            'file_type': 'sbml',
            'workspace_name': self.getWsName(),
            'model_name': 'MyModel'
        }
        with self.assertRaisesRegexp(
                    ValueError, 'Required parameter "model_file" is missing'):
            self.getImpl().import_file_as_fba_model_from_staging(
                self.getContext(), invalid_params)

        invalid_params = {
            'model_file': 'test_model-reactions.tsv',
            'file_type': 'tsv',
            'workspace_name': self.getWsName(),
            'model_name': 'MyModel'
        }
        with self.assertRaisesRegexp(
                ValueError, 'A compound file is required for tsv upload.'):
            self.getImpl().import_file_as_fba_model_from_staging(
                self.getContext(), invalid_params)

        invalid_params = {
            'model_file': 'test_model-reactions.tsv',
            'file_type': 'csv',
            'workspace_name': self.getWsName(),
            'model_name': 'MyModel'
        }
        with self.assertRaisesRegexp(
                ValueError, '"csv" is not a valid import file_type'):
            self.getImpl().import_file_as_fba_model_from_staging(
                self.getContext(), invalid_params)

    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    def test_import_as_media_from_staging(self, download_staging_file):

        params = {
          'model_file': 'test_model.sbml',
          'file_type': 'sbml',
          'workspace_name': self.getWsName(),
          'model_name': 'MyModel'
        }

        ref = self.getImpl().import_file_as_fba_model_from_staging(
            self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])

        params = {
            'model_file': 'test_model.xlsx',
            'file_type': 'excel',
            'genome': self.genome_ref,
            'biomass': ['bio1'],
            'workspace_name': self.getWsName(),
            'model_name': 'MyModel'
        }

        ref = self.getImpl().import_file_as_fba_model_from_staging(
            self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])

        params = {
            'model_file': 'test_model-reactions.tsv',
            'compound_file': 'test_model-compounds.tsv',
            'file_type': 'tsv',
            'genome': self.genome_ref,
            'biomass': ['bio1'],
            'workspace_name': self.getWsName(),
            'model_name': 'MyModel'
        }

        ref = self.getImpl().import_file_as_fba_model_from_staging(
            self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
