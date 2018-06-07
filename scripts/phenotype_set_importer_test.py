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
from fba_tools.fba_toolsClient import fba_tools
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil


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
        cls.gfu = GenomeFileUtil(os.environ['SDK_CALLBACK_URL'], token=cls.token)
        cls.fba_tools = fba_tools(os.environ['SDK_CALLBACK_URL'], token=cls.token)
        cls.scratch = cls.cfg['scratch']
        cls.shockURL = cls.cfg['shock-url']

        suffix = int(time.time() * 1000)
        cls.wsName = "test_kb_uploadmethods_phenotype_set" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})

        cls.prepare_data()

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

    @classmethod
    def prepare_data(cls):
        # upload genome object
        genbank_file_name = 'minimal.gbff'
        genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
        shutil.copy(os.path.join('data', genbank_file_name), genbank_file_path)

        cls.genome_object_name = 'test_Genome'
        cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
                                                    'workspace_name': cls.wsName,
                                                    'genome_name': cls.genome_object_name,
                                                    'generate_missing_genes': 1,
                                                    })['genome_ref']

        # upload media object
        media_file_name = 'media_example.txt'
        media_file_path = os.path.join(cls.scratch, media_file_name)
        shutil.copy(os.path.join('data', media_file_name), media_file_path)
        cls.media_object_name = 'test_Media'
        cls.media_ref = cls.fba_tools.tsv_file_to_media({'media_file': {'path': media_file_path},
                                                         'workspace_name': cls.wsName,
                                                         'media_name': cls.media_object_name
                                                         })['ref']

        cls.tsv_filename = 'phenotype_set_example.tsv'
        cls.tsv_file_path = os.path.join('/kb/module/work/tmp', cls.tsv_filename)
        with open(cls.tsv_file_path, 'w') as output:
            output.write("geneko\tmediaws\tmedia\taddtlCpd;addtlCpdBounds;customReactionBounds\tgrowth\n")
            line = "none\t{}\t{}\t".format(cls.wsName, cls.media_object_name)
            line += "L-Isoleucine;NH3;Phosphate;Sulfate\t1\n"
            output.write(line)

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @property
    def mock_download_staging_file(params):
        print('Mocking DataFileUtilClient.download_staging_file')
        print(params)

        tsv_file_path = params.get('staging_file_subdir_path')

        return {'copy_file_path': tsv_file_path}

    def test_bad_import_phenotype_set_from_staging_params(self):
        invalidate_input_params = {
          'missing_staging_file_subdir_path': 'staging_file_subdir_path',
          'workspace_name': 'workspace_name',
          'phenotype_set_name': 'phenotype_set_name',
          'genome': 'genome'
        }
        with self.assertRaisesRegexp(
                    ValueError,
                    '"staging_file_subdir_path" parameter is required, but missing'):
            self.getImpl().import_tsv_as_phenotype_set_from_staging(self.getContext(),
                                                                    invalidate_input_params)

        invalidate_input_params = {
          'staging_file_subdir_path': 'staging_file_subdir_path',
          'missing_workspace_name': 'workspace_name',
          'phenotype_set_name': 'phenotype_set_name',
          'genome': 'genome'
        }
        with self.assertRaisesRegexp(
                    ValueError,
                    '"workspace_name" parameter is required, but missing'):
            self.getImpl().import_tsv_as_phenotype_set_from_staging(self.getContext(),
                                                                    invalidate_input_params)

        invalidate_input_params = {
          'staging_file_subdir_path': 'staging_file_subdir_path',
          'workspace_name': 'workspace_name',
          'missing_phenotype_set_name': 'phenotype_set_name',
          'genome': 'genome'
        }
        with self.assertRaisesRegexp(
                ValueError,
                '"phenotype_set_name" parameter is required, but missing'):
            self.getImpl().import_tsv_as_phenotype_set_from_staging(self.getContext(),
                                                                    invalidate_input_params)

        invalidate_input_params = {
          'staging_file_subdir_path': 'staging_file_subdir_path',
          'workspace_name': 'workspace_name',
          'phenotype_set_name': 'phenotype_set_name',
          'missing_genome': 'genome'
        }
        with self.assertRaisesRegexp(
                ValueError,
                '"genome" parameter is required, but missing'):
            self.getImpl().import_tsv_as_phenotype_set_from_staging(self.getContext(),
                                                                    invalidate_input_params)

    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    @patch.object(UploaderUtil, "update_staging_service", return_value=None)
    def test_import_phenotype_set_from_staging(self, download_staging_file,
                                               update_staging_service):

        ws_obj_name = 'MyPhenotypeSet'

        params = {'staging_file_subdir_path': self.tsv_file_path,
                  'workspace_name': self.getWsName(),
                  'phenotype_set_name': ws_obj_name,
                  'genome': self.genome_object_name}

        ref = self.getImpl().import_tsv_as_phenotype_set_from_staging(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
