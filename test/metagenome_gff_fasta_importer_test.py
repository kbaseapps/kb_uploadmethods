import os
import re
import shutil
import time
import unittest
from configparser import ConfigParser
from os import environ
import requests

from biokbase.workspace.client import Workspace as workspaceService
from mock import patch

from installed_clients.DataFileUtilClient import DataFileUtil
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from kb_uploadmethods.authclient import KBaseAuth as _KBaseAuth
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
from installed_clients.AbstractHandleClient import AbstractHandle as HandleService


class kb_metagenome_uploadmethodsTest(unittest.TestCase):

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

        fq_filename = params.get('staging_file_subdir_path')
        fq_path = os.path.join('/kb/module/work/tmp', fq_filename)
        shutil.copy(os.path.join("data/test_Metagenome", fq_filename), fq_path)

        return {'copy_file_path': fq_path}

    def mock_file_to_shock(params):
        print('Mocking DataFileUtilClient.file_to_shock')
        print(params)

        return kb_metagenome_uploadmethodsTest().test_shock

    # def test_bad_upload_fasta_gff_file_params(self):

    #     invalidate_input_params = {
    #         'missing_fasta_file': 'fasta_file',
    #         'gff_file': 'gff_file',
    #         'workspace_name': 'workspace_name',
    #         'genome_name': 'genome_name'
    #     }
    #     with self.assertRaisesRegex(
    #                 ValueError,
    #                 '"fasta_file" parameter is required, but missing'):
    #         self.getImpl().upload_fasta_gff_file(self.getContext(), invalidate_input_params)

    #     invalidate_input_params = {
    #         'fasta_file': 'fasta_file',
    #         'missing_gff_file': 'gff_file',
    #         'workspace_name': 'workspace_name',
    #         'genome_name': 'genome_name'
    #     }
    #     with self.assertRaisesRegex(
    #             ValueError,
    #             '"gff_file" parameter is required, but missing'):
    #         self.getImpl().upload_fasta_gff_file(self.getContext(), invalidate_input_params)

    #     invalidate_input_params = {
    #         'fasta_file': 'fasta_file',
    #         'gff_file': 'gff_file',
    #         'missing_workspace_name': 'workspace_name',
    #         'genome_name': 'genome_name'
    #     }
    #     with self.assertRaisesRegex(
    #             ValueError,
    #             '"workspace_name" parameter is required, but missing'):
    #         self.getImpl().upload_fasta_gff_file(self.getContext(), invalidate_input_params)

    #     invalidate_input_params = {
    #         'fasta_file': 'fasta_file',
    #         'gff_file': 'gff_file',
    #         'workspace_name': 'workspace_name',
    #         'missing_genome_name': 'genome_name'
    #     }
    #     with self.assertRaisesRegex(
    #             ValueError,
    #             '"genome_name" parameter is required, but missing'):
    #         self.getImpl().upload_fasta_gff_file(self.getContext(), invalidate_input_params)

    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    @patch.object(UploaderUtil, "update_staging_service", return_value=None)
    def test_upload_metagenome_fasta_gff_file(self, download_staging_file,
                                              update_staging_service):

        fasta_file = "metagenome.fa"
        gff_file = "metagenome.gff"
        ws_obj_name = 'MyMetagenome'
        scientific_name = "Garbage trashus"

        params = {
            "fasta_file": fasta_file,
            "gff_file": gff_file,
            "workspace_name": self.getWsName(),
            "genome_name": ws_obj_name,
            "scientific_name": scientific_name,
            "genetic_code": None,
            "source": None,
            "taxon_wsname": None,
            "release": None,
            "type": "User upload",
            "generate_missing_genes": True
        }

        ref = self.getImpl().upload_metagenome_fasta_gff_file(self.getContext(), params)

        self.assertTrue('metagenome_ref' in ref[0])
        self.assertTrue('metagenome_info' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])

        metagenome_info = ref[0]['metagenome_info']
        metagenome_metadata = metagenome_info[10]

        self.assertEqual(metagenome_metadata['Source'], 'User')
        self.assertTrue('GC content' in metagenome_metadata)
        self.assertEqual(metagenome_info[2], 'KBaseMetagenomes.AnnotatedMetagenomeAssembly-1.0')
        self.assertTrue(re.match("^\d+?\.\d+?$", metagenome_metadata['GC content']) is not None)
        self.assertTrue('Size' in metagenome_metadata)
        self.assertTrue(metagenome_metadata['Size'].isdigit())

        # self.assertEqual(metagenome_metadata['Domain'], 'Eukaryota')
        # self.assertEqual(metagenome_metadata['Genetic code'], '11')
        # self.assertEqual(metagenome_metadata['Name'], 'Populus trichocarpa')
        # self.assertEqual(metagenome_metadata['Taxonomy'],
        #                   'cellular organisms; Eukaryota; Viridiplantae; Streptophyta; ' +
        #                   'Streptophytina; Embryophyta; Tracheophyta; Euphyllophyta; ' +
        #                   'Spermatophyta; Magnoliophyta; Mesangiospermae; eudicotyledons; ' +
        #                   'Gunneridae; Pentapetalae; rosids; fabids; Malpighiales; Salicaceae; ' +
        #                   'Saliceae; Populus')
