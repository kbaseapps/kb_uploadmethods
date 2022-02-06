import os
import shutil
import time
import unittest
from configparser import ConfigParser
from os import environ

from biokbase.workspace.client import Workspace as workspaceService
from mock import patch
import requests

from installed_clients.DataFileUtilClient import DataFileUtil
from kb_uploadmethods.Utils.BatchUtil import BatchUtil
from kb_uploadmethods.authclient import KBaseAuth as _KBaseAuth
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
from installed_clients.AbstractHandleClient import AbstractHandle as HandleService


class kb_uploadmethods_batchTest(unittest.TestCase):

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
        cls.hs = HandleService(url=cls.cfg['handle-service-url'],
                               token=cls.token)
        cls.scratch = cls.cfg['scratch']
        cls.shockURL = cls.cfg['shock-url']

        small_file = os.path.join(cls.scratch, 'test.txt')
        with open(small_file, "w") as f:
            f.write("empty content")
        cls.test_shock = cls.dfu.file_to_shock({'file_path': small_file, 'make_handle': True})
        cls.handles_to_delete = []
        cls.nodes_to_delete = []
        cls.handles_to_delete.append(cls.test_shock['handle']['hid'])
        cls.nodes_to_delete.append(cls.test_shock['shock_id'])

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')
        if hasattr(cls, 'nodes_to_delete'):
            for node in cls.nodes_to_delete:
                cls.delete_shock_node(node)
        if hasattr(cls, 'handles_to_delete'):
            cls.hs.delete_handles(cls.hs.hids_to_handles(cls.handles_to_delete))
            print('Deleted handles ' + str(cls.handles_to_delete))

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
        print('Mocking DataFileUtilClient.download_staging_file')
        print(params)

        staging_file_subdir_path = os.path.join('/kb/module/test/data',
                                                params.get('staging_file_subdir_path'))
        file_name = os.path.basename(staging_file_subdir_path)
        file_path = os.path.join('/kb/module/work/tmp', file_name)
        shutil.copy(staging_file_subdir_path, file_path)

        return {'copy_file_path': file_path}

    def mock_file_to_shock(params):
        print('Mocking DataFileUtilClient.file_to_shock')
        print(params)

        return kb_uploadmethods_batchTest().test_shock

    def test_bad_batch_import_genomes_from_staging_params(self):

        invalidate_input_params = {
            'missing_staging_subdir': 'staging_subdir',
            'workspace_name': 'workspace_name',
            'genome_set_name': 'genome_set_name'
        }
        with self.assertRaisesRegex(
                    ValueError,
                    '"staging_subdir" parameter is required, but missing'):
            self.getImpl().batch_import_genomes_from_staging(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
            'staging_subdir': 'staging_subdir',
            'missing_workspace_name': 'workspace_name',
            'genome_set_name': 'genome_set_name'
        }
        with self.assertRaisesRegex(
                ValueError,
                '"workspace_name" parameter is required, but missing'):
            self.getImpl().batch_import_genomes_from_staging(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
            'staging_subdir': 'staging_subdir',
            'workspace_name': 'workspace_name',
            'missing_genome_set_name': 'genome_set_name'
        }
        with self.assertRaisesRegex(
                ValueError,
                '"genome_set_name" parameter is required, but missing'):
            self.getImpl().batch_import_genomes_from_staging(self.getContext(), invalidate_input_params)

    @unittest.skip("inactive app")
    @patch.object(BatchUtil, "STAGING_USER_FILE_PREFIX", new='/kb/module/test/data/')
    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    def test_batch_import_genomes_from_staging(self, download_staging_file):
        input_params = {
            'staging_subdir': 'test_batch',
            'workspace_name': self.getWsName(),
            'genome_set_name': 'test_genome_set_name',
            'source': 'Other',
            'generate_missing_genes': 1
        }

        returnVal = self.getImpl().batch_import_genomes_from_staging(self.getContext(), input_params)[0]

        set_ref = returnVal.get('set_ref')

        set_obj = self.dfu.get_objects({'object_refs': [set_ref]})['data'][0]

        set_data = set_obj['data']
        set_info = set_obj['info']

        self.assertTrue('KBaseSearch.GenomeSet' in set_info[2])
        self.assertTrue(len(set_data['elements']) > 1)
        # self.assertEqual(len(set_data['elements']), 4)

    @patch.object(BatchUtil, "STAGING_USER_FILE_PREFIX", new='/kb/module/test/data/')
    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_batch_import_assemblies_from_staging(self, download_staging_file, file_to_shock):
        input_params = {
            'staging_subdir': '/test_batch',
            'workspace_name': self.getWsName(),
            'assembly_set_name': 'test_assembly_set_name'
        }
        returnVal = self.getImpl().batch_import_assemblies_from_staging(self.getContext(), input_params)[0]

        set_ref = returnVal.get('set_ref')

        set_data = self.dfu.get_objects({'object_refs': [set_ref]})['data'][0]['data']

        self.assertTrue(len(set_data['items']) > 1)
        # self.assertEqual(len(set_data['items']), 3)

    @patch.object(BatchUtil, "STAGING_USER_FILE_PREFIX", new='/kb/module/test/data/')
    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_batch_import_assemblies_from_staging2(self, download_staging_file, file_to_shock):
        input_params = {
            'staging_subdir': "/" + self.user_id + '/test_batch',
            'workspace_name': self.getWsName(),
            'assembly_set_name': 'test_assembly_set_name'
        }
        returnVal = self.getImpl().batch_import_assemblies_from_staging(self.getContext(), input_params)[0]

        set_ref = returnVal.get('set_ref')

        set_data = self.dfu.get_objects({'object_refs': [set_ref]})['data'][0]['data']

        self.assertTrue(len(set_data['items']) > 1)
        # self.assertEqual(len(set_data['items']), 2)
