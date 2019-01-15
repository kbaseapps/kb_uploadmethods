# -*- coding: utf-8 -*-
import os  # noqa: F401
import shutil
import time
import unittest
from configparser import ConfigParser
from os import environ

import requests
from biokbase.workspace.client import Workspace as workspaceService
from mock import patch

from DataFileUtil.DataFileUtilClient import DataFileUtil
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from kb_uploadmethods.authclient import KBaseAuth as _KBaseAuth
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext


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
        cls.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=cls.token)
        cls.scratch = cls.cfg['scratch']
        cls.shockURL = cls.cfg['shock-url']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def make_ref(self, objinfo):
        return str(objinfo[6]) + '/' + str(objinfo[0]) + '/' + str(objinfo[4])

    @classmethod
    def delete_shock_node(cls, node_id):
        header = {'Authorization': 'Oauth {0}'.format(cls.token)}
        requests.delete(cls.shockURL + '/node/' + node_id, headers=header,
                        allow_redirects=True)
        print(('Deleted shock node ' + node_id))

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
        print('Mocking DataFileUtilClient.download_staging_file')
        print(params)

        fq_filename = params.get('staging_file_subdir_path')
        fq_path = os.path.join('/kb/module/work/tmp', fq_filename)
        shutil.copy(os.path.join("data", fq_filename), fq_path)

        return {'copy_file_path': fq_path}

    def test_bad_import_genbank_from_staging_params(self):
        invalidate_input_params = {
          'missing_staging_file_subdir_path': 'staging_file_subdir_path',
          'genome_name': 'genome_name',
          'workspace_name': 'workspace_name',
          'source': 'source'
        }
        with self.assertRaisesRegex(
                    ValueError,
                    '"staging_file_subdir_path" parameter is required, but missing'):
            self.getImpl().import_genbank_from_staging(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'staging_file_subdir_path': 'staging_file_subdir_path',
          'missing_genome_name': 'genome_name',
          'workspace_name': 'workspace_name',
          'source': 'source'
        }
        with self.assertRaisesRegex(
                    ValueError,
                    '"genome_name" parameter is required, but missing'):
            self.getImpl().import_genbank_from_staging(self.getContext(), invalidate_input_params)
        invalidate_input_params = {
          'staging_file_subdir_path': 'staging_file_subdir_path',
          'genome_name': 'genome_name',
          'missing_workspace_name': 'workspace_name',
          'source': 'source'
        }
        with self.assertRaisesRegex(
                ValueError,
                '"workspace_name" parameter is required, but missing'):
            self.getImpl().import_genbank_from_staging(self.getContext(), invalidate_input_params)
        invalidate_input_params = {
          'staging_file_subdir_path': 'staging_file_subdir_path',
          'genome_name': 'genome_name',
          'workspace_name': 'workspace_name',
          'missing_source': 'source'
        }
        with self.assertRaisesRegex(
                ValueError,
                '"source" parameter is required, but missing'):
            self.getImpl().import_genbank_from_staging(self.getContext(), invalidate_input_params)

    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    @patch.object(UploaderUtil, "update_staging_service", return_value=None)
    def test_genbank_to_genome(self, download_staging_file, update_staging_service):

        gbk_path = 'small_genbank.gbff'
        ws_obj_name = 'MyGenome'

        params = {
          'staging_file_subdir_path': gbk_path,
          'genome_name': ws_obj_name,
          'workspace_name': self.getWsName(),
          'source': 'RefSeq'
        }

        ref = self.getImpl().import_genbank_from_staging(self.getContext(), params)
        self.assertTrue('genome_ref' in ref[0])
        self.assertTrue('genome_info' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
