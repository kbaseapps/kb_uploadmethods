# -*- coding: utf-8 -*-
import hashlib
import os  # noqa: F401
import shutil
import time
import unittest
from configparser import ConfigParser
from os import environ

import requests
from biokbase.workspace.client import Workspace as workspaceService
from mock import patch

from installed_clients.DataFileUtilClient import DataFileUtil
from kb_uploadmethods.Utils.ImportSRAUtil import ImportSRAUtil
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from kb_uploadmethods.authclient import KBaseAuth as _KBaseAuth
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
from installed_clients.AbstractHandleClient import AbstractHandle as HandleService


class kb_uploadmethods_reads_Test(unittest.TestCase):

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
        print(('Deleted shock node ' + node_id))

    @classmethod
    def make_ref(self, objinfo):
        return str(objinfo[6]) + '/' + str(objinfo[0]) + '/' + str(objinfo[4])

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

    def check_lib(self, lib, size, filename, md5):
        shock_id = lib["file"]["id"]
        print("LIB: {}".format(str(lib)))
        print("Shock ID: {}".format(str(shock_id)))
        fileinput = [{
                    'shock_id': shock_id,
                    'file_path': self.scratch + '/temp',
                    'unpack': 'uncompress'}]
        print("File Input: {}".format(str(fileinput)))
        files = self.dfu.shock_to_file_mass(fileinput)
        path = files[0]["file_path"]
        file_md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
        libfile = lib['file']
        self.assertEqual(file_md5, md5)
        self.assertEqual(lib['size'], size)
        self.assertEqual(lib['type'], 'fq')
        self.assertEqual(lib['encoding'], 'ascii')

        self.assertEqual(libfile['file_name'], filename)
        self.assertEqual(libfile['hid'].startswith('KBH_'), True)

        self.assertEqual(libfile['type'], 'shock')
        self.assertEqual(libfile['url'], self.shockURL)

    def mock_download_staging_file(params):
        print('Mocking DataFileUtilClient.download_staging_file')
        print(params)

        fq_filename = params.get('staging_file_subdir_path')
        fq_path = os.path.join('/kb/module/work/tmp', fq_filename)
        shutil.copy(os.path.join("data", fq_filename), fq_path)

        return {'copy_file_path': fq_path}

    def mock_file_to_shock(params):
        print('Mocking DataFileUtilClient.file_to_shock')
        print(params)

        return kb_uploadmethods_reads_Test().test_shock

    def mock_validate_upload_staging_file_availability(staging_file_subdir_path):
        print('Mocking ImportSRAUtil._validate_upload_staging_file_availability')
        print(staging_file_subdir_path)

    def mock_run_command_pe(command):
        print('Mocking ImportSRAUtil._run_command')

        tmp_dir = command.split(' ')[-2]
        scratch_sra_file_path = command.split(' ')[-1]

        sra_name = os.path.basename(scratch_sra_file_path).partition('.')[0]

        fwd_file_path = os.path.join(tmp_dir, sra_name, '1')
        os.makedirs(fwd_file_path)
        rev_file_path = os.path.join(tmp_dir, sra_name, '2')
        os.makedirs(rev_file_path)

        fwd_filename = 'small.forward.fq'
        shutil.copy(os.path.join("data", fwd_filename), fwd_file_path)
        os.rename(os.path.join(fwd_file_path, fwd_filename), os.path.join(fwd_file_path, 'fastq'))

        rev_filename = 'small.reverse.fq'
        shutil.copy(os.path.join("data", rev_filename), rev_file_path)
        os.rename(os.path.join(rev_file_path, rev_filename), os.path.join(rev_file_path, 'fastq'))

    def mock_run_command_se(command):
        print('Mocking ImportSRAUtil._run_command')

        tmp_dir = command.split(' ')[-2]
        scratch_sra_file_path = command.split(' ')[-1]

        sra_name = os.path.basename(scratch_sra_file_path).partition('.')[0]

        fwd_file_path = os.path.join(tmp_dir, sra_name)
        os.makedirs(fwd_file_path)

        fq_filename = 'Sample1.fastq'
        shutil.copy(os.path.join("data", fq_filename), fwd_file_path)
        os.rename(os.path.join(fwd_file_path, fq_filename), os.path.join(fwd_file_path, 'fastq'))

    def test_bad_import_reads_from_staging_params(self):
        invalidate_input_params = {
          'missing_import_type': 'import_type',
          'sequencing_tech': 'sequencing_tech',
          'workspace_name': 'workspace_name',
          'name': 'name'
        }
        with self.assertRaisesRegex(
                    ValueError,
                    '"import_type" parameter is required, but missing'):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)

        invalidate_input_params = {
          'import_type': 'import_type',
          'missing_sequencing_tech': 'sequencing_tech',
          'workspace_name': 'workspace_name',
          'name': 'name'
        }
        with self.assertRaisesRegex(
                    ValueError,
                    '"sequencing_tech" parameter is required, but missing'):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)
        invalidate_input_params = {
          'import_type': 'import_type',
          'sequencing_tech': 'sequencing_tech',
          'missing_workspace_name': 'workspace_name',
          'name': 'name'
        }
        with self.assertRaisesRegex(
                ValueError,
                '"workspace_name" parameter is required, but missing'):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)

        invalidate_input_params = {
          'import_type': 'import_type',
          'sequencing_tech': 'sequencing_tech',
          'workspace_name': 'workspace_name',
          'missing_name': 'name'
        }
        with self.assertRaisesRegex(
                ValueError,
                '"name" parameter is required, but missing'):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)

        invalidate_input_params = {
          'import_type': 'invalide_import_type',
          'sequencing_tech': 'sequencing_tech',
          'workspace_name': 'workspace_name',
          'name': 'name'
        }
        error_msg = "Import file type \[invalide_import_type\] is not supported. "
        error_msg += "Please select one of \['FASTQ/FASTA', 'SRA'\]"
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)

        invalidate_input_params = {
          'import_type': 'FASTQ/FASTA',
          'sra_staging_file_name': 'sra_staging_file_name',
          'sequencing_tech': 'sequencing_tech',
          'workspace_name': 'workspace_name',
          'name': 'name'
        }
        with self.assertRaisesRegex(
                ValueError,
                'FASTQ/FASTA input file type selected. But missing FASTQ/FASTA file.'):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)

        invalidate_input_params = {
          'import_type': 'SRA',
          'fastq_fwd_staging_file_name': 'fastq_fwd_staging_file_name',
          'sequencing_tech': 'sequencing_tech',
          'workspace_name': 'workspace_name',
          'name': 'name'
        }
        with self.assertRaisesRegex(
                ValueError,
                'SRA input file type selected. But missing SRA file.'):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)

        invalidate_input_params = {
          'import_type': 'FASTQ/FASTA',
          'fastq_fwd_staging_file_name': 'fastq_fwd_staging_file_name',
          'sra_staging_file_name': 'sra_staging_file_name',
          'sequencing_tech': 'sequencing_tech',
          'workspace_name': 'workspace_name',
          'name': 'name'
        }
        with self.assertRaisesRegex(
                ValueError,
                'Both SRA and FASTQ/FASTA file given. Please provide one file type only.'):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)

        invalidate_input_params = {
          'import_type': 'SRA',
          'fastq_rev_staging_file_name': 'fastq_rev_staging_file_name',
          'sra_staging_file_name': 'sra_staging_file_name',
          'sequencing_tech': 'sequencing_tech',
          'workspace_name': 'workspace_name',
          'name': 'name'
        }
        with self.assertRaisesRegex(
                ValueError,
                'Both SRA and FASTQ/FASTA file given. Please provide one file type only.'):
            self.getImpl().import_reads_from_staging(self.getContext(),
                                                     invalidate_input_params)

    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    @patch.object(ImportSRAUtil, "_validate_upload_staging_file_availability",
                  side_effect=mock_validate_upload_staging_file_availability)
    @patch.object(ImportSRAUtil, "_run_command", side_effect=mock_run_command_pe)
    @patch.object(UploaderUtil, "update_staging_service", return_value=None)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_import_sra_reads_paired_end(self, download_staging_file,
                                         _validate_upload_staging_file_availability,
                                         _run_command, update_staging_service, file_to_shock):

        sra_path = 'empty.sra'
        ws_obj_name = 'MyReads'

        params = {
            'import_type': 'SRA',
            'sra_staging_file_name': sra_path,
            'name': ws_obj_name,
            'workspace_name': self.getWsName(),
            'sequencing_tech': 'Unknown',
            'single_genome': 0,
            'insert_size_mean': 99.9,
            'insert_size_std_dev': 10.1,
            'read_orientation_outward': 1
        }

        ref = self.getImpl().import_reads_from_staging(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/MyReads']})['data'][0]
        self.assertEqual(ref[0]['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.PairedEndLibrary'), True)

        d = obj['data']
        file_name = d["lib1"]["file"]["file_name"]
        self.assertTrue(file_name.endswith(".inter.fastq.gz"))
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 0)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.assertEqual(d['interleaved'], 1)
        self.assertEqual(d['read_orientation_outward'], 1)
        self.assertEqual(d['insert_size_mean'], 99.9)
        self.assertEqual(d['insert_size_std_dev'], 10.1)
        self.check_lib(d['lib1'], 2696029, file_name,
                       '1c58d7d59c656db39cedcb431376514b')
        node = d['lib1']['file']['id']
        self.nodes_to_delete.append(node)

    @unittest.skip("duplicate test")
    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    @patch.object(ImportSRAUtil, "_validate_upload_staging_file_availability",
                  side_effect=mock_validate_upload_staging_file_availability)
    @patch.object(ImportSRAUtil, "_run_command", side_effect=mock_run_command_se)
    @patch.object(UploaderUtil, "update_staging_service", return_value=None)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_import_sra_reads_single_end(self, download_staging_file,
                                         _validate_upload_staging_file_availability,
                                         _run_command, update_staging_service, file_to_shock):

        sra_path = 'empty.sra'
        ws_obj_name = 'MyReads'

        params = {
            'import_type': 'SRA',
            'sra_staging_file_name': sra_path,
            'name': ws_obj_name,
            'workspace_name': self.getWsName(),
            'sequencing_tech': 'Unknown',
            'single_genome': 1
        }

        ref = self.getImpl().import_reads_from_staging(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/MyReads']})['data'][0]
        self.assertEqual(ref[0]['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2964, 'fastq.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.nodes_to_delete.append(node)
