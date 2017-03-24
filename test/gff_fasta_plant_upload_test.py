import unittest
import os
import time
import shutil
import requests
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
        shutil.copy(os.path.join("data/Test_Plant", fq_filename), fq_path)

        return {'copy_file_path': fq_path}

    def test_bad_upload_fasta_gff_file_params(self):

        invalidate_input_params = {
            'missing_fasta_file': 'fasta_file',
            'gff_file': 'gff_file',
            'workspace_name': 'workspace_name',
            'genome_name': 'genome_name',
            'scientific_name': 'scientific_name'
        }
        with self.assertRaisesRegexp(
                    ValueError,
                    '"fasta_file" parameter is required, but missing'):
            self.getImpl().upload_fasta_gff_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
            'fasta_file': 'fasta_file',
            'missing_gff_file': 'gff_file',
            'workspace_name': 'workspace_name',
            'genome_name': 'genome_name',
            'scientific_name': 'scientific_name'
        }
        with self.assertRaisesRegexp(
                ValueError,
                '"gff_file" parameter is required, but missing'):
            self.getImpl().upload_fasta_gff_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
            'fasta_file': 'fasta_file',
            'gff_file': 'gff_file',
            'missing_workspace_name': 'workspace_name',
            'genome_name': 'genome_name',
            'scientific_name': 'scientific_name'
        }
        with self.assertRaisesRegexp(
                ValueError,
                '"workspace_name" parameter is required, but missing'):
            self.getImpl().upload_fasta_gff_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
            'fasta_file': 'fasta_file',
            'gff_file': 'gff_file',
            'workspace_name': 'workspace_name',
            'missing_genome_name': 'genome_name',
            'scientific_name': 'scientific_name'
        }
        with self.assertRaisesRegexp(
                ValueError,
                '"genome_name" parameter is required, but missing'):
            self.getImpl().upload_fasta_gff_file(self.getContext(), invalidate_input_params)

    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    def test_simple_upload(self, download_staging_file):

        fasta_file = "Test_v1.0.fa"
        gff_file = "Test_v1.0.gene.gff3"
        ws_obj_name = 'MyGenome'
        scientific_name = "Populus trichocarpa"

        params = {
            'fasta_file': fasta_file,
            'gff_file': gff_file,
            'workspace_name': self.getWsName(),
            'genome_name': ws_obj_name,
            'scientific_name': scientific_name
        }

        ref = self.getImpl().upload_fasta_gff_file(self.getContext(), params)

        self.assertTrue('genome_ref' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
