# -*- coding: utf-8 -*-
import ftplib
import hashlib
import os
import time
import unittest
from configparser import ConfigParser
from os import environ

import requests
from biokbase.workspace.client import Workspace as workspaceService

from installed_clients.DataFileUtilClient import DataFileUtil
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

    def getDefaultParams(self, file_path=True):
        if file_path:
            default_input_params = {
                'fwd_staging_file_name': 'SP1.fq',
                'sequencing_tech': 'Unknown',
                'name': 'test_reads_file_name.reads',
                'workspace_name': self.getWsName()
            }
        else:
            default_input_params = {
                'download_type': 'Direct Download',
                'fwd_file_url': 'http://molb7621.github.io/workshop/_downloads/SP1.fq',
                'sequencing_tech': 'Unknown',
                'name': 'test_reads_file_name.reads',
                'workspace_name': self.getWsName()
            }
        return default_input_params

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

    def test_validate_upload_fastq_file_parameters(self):

        # Testing required params
        invalidate_input_params = self.getDefaultParams()
        del invalidate_input_params['name']
        with self.assertRaisesRegex(
                            ValueError,
                            '"name" parameter is required, but missing'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)
        invalidate_input_params = self.getDefaultParams()
        del invalidate_input_params['workspace_name']
        with self.assertRaisesRegex(
                            ValueError,
                            '"workspace_name" parameter is required, but missing'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)
        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['fwd_file_url'] = 'https://fake_url'
        with self.assertRaisesRegex(
                            ValueError,
                            'Cannot upload Reads for both file path and file URL'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        # Testing _validate_upload_file_availability
        # invalidate_input_params = self.getDefaultParams()
        # nonexistent_file_name = 'fake_file_0123456.fastq'
        # invalidate_input_params['fwd_staging_file_name'] = nonexistent_file_name
        # with self.assertRaisesRegexp(ValueError,
        #                 'Target file: {} is NOT available.'.format(nonexistent_file_name)):
        #     self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        # Testing duplicate forward/reverse
        invalidate_input_params = self.getDefaultParams()
        rev_staging_file_name = invalidate_input_params['fwd_staging_file_name']
        invalidate_input_params['rev_staging_file_name'] = rev_staging_file_name
        error_msg = 'Same file \[{}\] is used for forward and reverse. '.format(
                                            invalidate_input_params['rev_staging_file_name'])
        error_msg += 'Please select different files and try again.'
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams(file_path=False)
        invalidate_input_params['rev_file_url'] = invalidate_input_params['fwd_file_url']
        error_msg = 'Same URL\n {}\nis used for forward and reverse. '.format(
                                                      invalidate_input_params['rev_file_url'])
        error_msg += 'Please select different files and try again.'
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        # Testing URL prefix
        invalidate_input_params = self.getDefaultParams(file_path=False)
        invalidate_input_params['fwd_file_url'] = 'ftp://ftp.dlptest.com/24_Hour/SP1.fq'
        with self.assertRaisesRegex(
                            ValueError,
                            'Download type and URL prefix do NOT match'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams(file_path=False)
        invalidate_input_params['download_type'] = 'DropBox'
        with self.assertRaisesRegex(
                            ValueError,
                            'Download type and URL prefix do NOT match'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams(file_path=False)
        invalidate_input_params['download_type'] = 'FTP'
        with self.assertRaisesRegex(
                            ValueError,
                            'Download type and URL prefix do NOT match'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams(file_path=False)
        del invalidate_input_params['download_type']
        with self.assertRaisesRegex(
                        ValueError,
                        'Download type parameter is required, but missing'):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        error_msg = 'Advanced params "Mean Insert Size", "St. Dev. of Insert Size" or '
        error_msg += '"Reads Orientation Outward" is Paried End Reads specific'

        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['insert_size_mean'] = 10
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['insert_size_std_dev'] = 0.4
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['read_orientation_outward'] = 1
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        error_msg = 'Sequencing Technology: "PacBio CCS" or "PacBio CLR" '
        error_msg += 'is Single End Reads specific'

        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['sequencing_tech'] = 'PacBio CCS'
        invalidate_input_params['rev_staging_file_name'] = 'rev_staging_file_name'
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['sequencing_tech'] = 'PacBio CLR'
        invalidate_input_params['rev_staging_file_name'] = 'rev_staging_file_name'
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['sequencing_tech'] = 'PacBio CCS'
        invalidate_input_params['interleaved'] = 1
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams()
        invalidate_input_params['sequencing_tech'] = 'PacBio CLR'
        invalidate_input_params['interleaved'] = 1
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams(file_path=False)
        invalidate_input_params['sequencing_tech'] = 'PacBio CCS'
        invalidate_input_params['rev_file_url'] = 'rev_file_url'
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams(file_path=False)
        invalidate_input_params['sequencing_tech'] = 'PacBio CLR'
        invalidate_input_params['rev_file_url'] = 'rev_file_url'
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams(file_path=False)
        invalidate_input_params['sequencing_tech'] = 'PacBio CCS'
        invalidate_input_params['interleaved'] = 1
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

        invalidate_input_params = self.getDefaultParams(file_path=False)
        invalidate_input_params['sequencing_tech'] = 'PacBio CLR'
        invalidate_input_params['interleaved'] = 1
        with self.assertRaisesRegex(ValueError, error_msg):
            self.getImpl().upload_fastq_file(self.getContext(), invalidate_input_params)

    def test_upload_fastq_file_url_direct_download(self):
        fwd_file_url = 'https://anl.box.com/shared/static/'
        fwd_file_url += 'qwadp20dxtwnhc8r3sjphen6h0k1hdyo.fastq'
        params = {
          'download_type': 'Direct Download',
          'fwd_file_url': fwd_file_url,
          'sequencing_tech': 'Unknown',
          'name': 'test_reads_file_name.reads',
          'workspace_name': self.getWsName()
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
          {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
        self.assertEqual(ref[0]['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_direct_download_interleaved(self):
        fwd_file_url = 'https://anl.box.com/shared/static/'
        fwd_file_url += 'pf0d0d7torv07qh2nogaay073udmiacr.fastq'
        params = {
          'download_type': 'Direct Download',
          'fwd_file_url': fwd_file_url,
          'sequencing_tech': 'seqtech-pr2',
          'name': 'pairedreads2',
          'workspace_name': self.getWsName(),
          'insert_size_mean': 72.1,
          'insert_size_std_dev': 84.0,
          'read_orientation_outward': 1,
          'interleaved': 1
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/pairedreads2']})['data'][0]

        self.assertEqual(ref[0]['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.PairedEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'seqtech-pr2')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.assertEqual(d['interleaved'], 1)
        self.assertEqual(d['read_orientation_outward'], 1)
        self.assertEqual(d['insert_size_mean'], 72.1)
        self.assertEqual(d['insert_size_std_dev'], 84.0)
        self.assertNotIn('lib2', d)
        self.assertEqual(d['read_count'], 4)
        self.assertEqual(d['total_bases'], 1004)
        self.assertEqual(d['number_of_duplicates'], 0)
        self.assertEqual(d['base_percentages']['A'], 20)
        self.assertEqual(d['base_percentages']['T'], 20)
        self.assertEqual(d['base_percentages']['N'], 0)
        self.assertEqual(d['base_percentages']['C'], 26.4286)
        self.assertEqual(d['base_percentages']['G'], 33.5714)
        self.assertEqual(d["phred_type"], "33")
        self.assertEqual(d["qual_mean"], 25.1143)
        self.assertEqual(d["qual_min"], 10)
        self.assertEqual(d["qual_max"], 40)
        self.assertEqual(d["qual_stdev"], 10.081)
        self.assertEqual(d["gc_content"], 0.6)
        self.assertEqual(d["read_length_mean"], 251)
        self.assertEqual(d["read_length_stdev"], 0)
        self.check_lib(d['lib1'], 1063, 'Sample5_interleaved.fastq.gz',
                       '971a5f445055c85fd45b17459e15e3ed')
        node = d['lib1']['file']['id']
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_direct_download_paired_end(self):
        fwd_file_url = 'https://anl.box.com/shared/static/'
        fwd_file_url += 'lph9l0ye6yqetnbk04cx33mqgrj4b85j.fq'
        rev_file_url = 'https://anl.box.com/shared/static/'
        rev_file_url += '1u9fi158vquyrh9qt7l04t71eqbpvyrr.fq'
        params = {
          'download_type': 'Direct Download',
          'fwd_file_url': fwd_file_url,
          'rev_file_url': rev_file_url,
          'sequencing_tech': 'Unknown',
          'name': 'test_reads_file_name.reads',
          'workspace_name': self.getWsName(),
          'single_genome': 0,
          'insert_size_mean': 99.9,
          'insert_size_std_dev': 10.1,
          'read_orientation_outward': 1,
          'interleaved': 0
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
          {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
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
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_dropbox(self):
        fwd_file_url = 'https://www.dropbox.com/s/'
        fwd_file_url += 'lv7jx1vh6yky3o0/Sample1.fastq?dl=0'
        params = {
          'download_type': 'DropBox',
          'fwd_file_url': fwd_file_url,
          'sequencing_tech': 'Unknown',
          'name': 'test_reads_file_name.reads',
          'workspace_name': self.getWsName()
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
        self.assertEqual(ref[0]['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_dropbox_paired_end(self):
        fwd_file_url = 'https://www.dropbox.com/s/'
        fwd_file_url += 'pgtja4btj62ctkx/small.forward.fq?dl=0'
        rev_file_url = 'https://www.dropbox.com/s/'
        rev_file_url += 'hh55x00qluhfhr8/small.reverse.fq?dl=0'
        params = {
          'download_type': 'DropBox',
          'fwd_file_url': fwd_file_url,
          'rev_file_url': rev_file_url,
          'sequencing_tech': 'Unknown',
          'name': 'test_reads_file_name.reads',
          'workspace_name': self.getWsName(),
          'single_genome': 0,
          'insert_size_mean': 99.9,
          'insert_size_std_dev': 10.1,
          'read_orientation_outward': 1,
          'interleaved': 0
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
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
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_google_drive(self):
        fwd_file_url = 'https://drive.google.com/file/d/'
        fwd_file_url += '0B0exSa7ebQ0qcHdNS2NEYjJOTTg/view?usp=sharing'
        params = {
          'download_type': 'Google Drive',
          'fwd_file_url': fwd_file_url,
          'sequencing_tech': 'Unknown',
          'name': 'test_reads_file_name.reads',
          'workspace_name': self.getWsName()
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
        self.assertEqual(ref[0]['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_google_drive_paired_end(self):
        fwd_file_url = 'https://drive.google.com/open?'
        fwd_file_url += 'id=0B0exSa7ebQ0qSGlmVzIwNXV5OWc'
        rev_file_url = 'https://drive.google.com/file/d/'
        rev_file_url += '0B0exSa7ebQ0qYml1c1BXTEhtR00/view?usp=sharing'
        params = {
          'download_type': 'Google Drive',
          'fwd_file_url': fwd_file_url,
          'rev_file_url': rev_file_url,
          'sequencing_tech': 'Unknown',
          'name': 'test_reads_file_name.reads',
          'workspace_name': self.getWsName(),
          'single_genome': 0,
          'insert_size_mean': 99.9,
          'insert_size_std_dev': 10.1,
          'read_orientation_outward': 1,
          'interleaved': 0
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
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
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_ftp(self):
        # copy test file to FTP
        fq_filename = "Sample1.fastq"
        ftp_connection = ftplib.FTP('ftp.uconn.edu')
        ftp_connection.login('anonymous', 'anonymous@domain.com')
        ftp_connection.cwd("/48_hour/")

        if fq_filename not in ftp_connection.nlst():
            fh = open(os.path.join("data", fq_filename), 'rb')
            ftp_connection.storbinary('STOR Sample1.fastq', fh)
            fh.close()

        params = {
          'download_type': 'FTP',
          'fwd_file_url': 'ftp://ftp.uconn.edu/48_hour/Sample1.fastq',
          'sequencing_tech': 'Unknown',
          'name': 'test_reads_file_name.reads',
          'workspace_name': self.getWsName()
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
        self.assertEqual(ref[0]['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_ftp_paired(self):
        # copy test file to FTP
        fq_filename = "small.forward.fq"
        ftp_connection = ftplib.FTP('ftp.uconn.edu')
        ftp_connection.login('anonymous', 'anonymous@domain.com')
        ftp_connection.cwd("/48_hour/")

        if fq_filename not in ftp_connection.nlst():
            fh = open(os.path.join("data", fq_filename), 'rb')
            ftp_connection.storbinary('STOR small.forward.fq', fh)
            fh.close()

        fq_filename = "small.reverse.fq"

        if fq_filename not in ftp_connection.nlst():
            fh = open(os.path.join("data", fq_filename), 'rb')
            ftp_connection.storbinary('STOR small.reverse.fq', fh)
            fh.close()

        params = {
            'download_type': 'FTP',
            'fwd_file_url': 'ftp://ftp.uconn.edu/48_hour/small.forward.fq',
            'rev_file_url': 'ftp://ftp.uconn.edu/48_hour/small.reverse.fq',
            'sequencing_tech': 'Unknown',
            'name': 'test_reads_file_name.reads',
            'workspace_name': self.getWsName(),
            'single_genome': 0,
            'insert_size_mean': 99.9,
            'insert_size_std_dev': 10.1,
            'interleaved': 0
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
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
        self.assertEqual(d['read_orientation_outward'], 0)
        self.assertEqual(d['insert_size_mean'], 99.9)
        self.assertEqual(d['insert_size_std_dev'], 10.1)
        self.check_lib(d['lib1'], 2696029, file_name,
                       '1c58d7d59c656db39cedcb431376514b')
        node = d['lib1']['file']['id']
        self.delete_shock_node(node)

    def test_urls_to_add_direct_download(self):
        fwd_file_url = 'https://anl.box.com/shared/static/'
        fwd_file_url += 'qwadp20dxtwnhc8r3sjphen6h0k1hdyo.fastq'
        params = {
          'download_type': 'Direct Download',
          'workspace_name': self.getWsName(),
          'sequencing_tech': 'Unknown',
          'urls_to_add': [
            {
                'fwd_file_url': fwd_file_url,
                'name': 'test_reads_file_name_1.reads',
                'single_genome': 1
            },
            {
                'fwd_file_url': fwd_file_url,
                'name': 'test_reads_file_name_2.reads',
                'single_genome': 1
            }
          ]
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertEqual(2, len(ref[0].get('obj_ref').split(',')))

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name_1.reads']})['data'][0]
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name_2.reads']})['data'][0]
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)

    def test_urls_to_add_dropbox_paired_end(self):
        fwd_file_url = 'https://www.dropbox.com/s/pgtja4btj62ctkx/small.forward.fq?dl=0'
        rev_file_url = 'https://www.dropbox.com/s/hh55x00qluhfhr8/small.reverse.fq?dl=0'
        params = {
          'download_type': 'DropBox',
          'sequencing_tech': 'Unknown',
          'workspace_name': self.getWsName(),
          'urls_to_add': [
            {
              'fwd_file_url': fwd_file_url,
              'rev_file_url': rev_file_url,
              'name': 'test_reads_file_name_1.reads',
              'single_genome': 0,
              'insert_size_mean': 99.9,
              'insert_size_std_dev': 10.1,
              'read_orientation_outward': 1,
              'interleaved': 0
            },
            {
              'fwd_file_url': fwd_file_url,
              'rev_file_url': rev_file_url,
              'name': 'test_reads_file_name_2.reads',
              'single_genome': 0,
              'insert_size_mean': 99.9,
              'insert_size_std_dev': 10.1,
              'read_orientation_outward': 1,
              'interleaved': 0
            }
          ]
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertEqual(2, len(ref[0].get('obj_ref').split(',')))

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name_1.reads']})['data'][0]
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
        self.delete_shock_node(node)

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name_2.reads']})['data'][0]
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
        self.delete_shock_node(node)

    def test_urls_to_add_direct_download_leading_space(self):
        fwd_file_url = '      https://anl.box.com/shared/static/'
        fwd_file_url += 'qwadp20dxtwnhc8r3sjphen6h0k1hdyo.fastq'
        params = {
          'download_type': 'Direct Download',
          'workspace_name': self.getWsName(),
          'sequencing_tech': 'Unknown',
          'urls_to_add': [
            {
                'fwd_file_url': fwd_file_url,
                'name': 'test_reads_file_name_1.reads',
                'single_genome': 1
            },
            {
                'fwd_file_url': fwd_file_url,
                'name': 'test_reads_file_name_2.reads',
                'single_genome': 1
            }
          ]
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])
        self.assertEqual(2, len(ref[0].get('obj_ref').split(',')))

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name_1.reads']})['data'][0]
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name_2.reads']})['data'][0]
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)

    def test_upload_fastq_file_url_ftp_trailing_space(self):
        # copy test file to FTP
        fq_filename = "Sample1.fastq"
        ftp_connection = ftplib.FTP('ftp.uconn.edu')
        ftp_connection.login('anonymous', 'anonymous@domain.com')
        ftp_connection.cwd("/48_hour/")

        if fq_filename not in ftp_connection.nlst():
            fh = open(os.path.join("data", fq_filename), 'rb')
            ftp_connection.storbinary('STOR Sample1.fastq', fh)
            fh.close()

        params = {
            'download_type': 'FTP',
            'fwd_file_url': 'ftp://ftp.uconn.edu/48_hour/Sample1.fastq   ',
            'sequencing_tech': 'Unknown',
            'name': 'test_reads_file_name.reads',
            'workspace_name': self.getWsName()
        }
        ref = self.getImpl().upload_fastq_file(self.getContext(), params)
        self.assertTrue('obj_ref' in ref[0])

        obj = self.dfu.get_objects(
            {'object_refs': [self.getWsName() + '/test_reads_file_name.reads']})['data'][0]
        self.assertEqual(ref[0]['obj_ref'], self.make_ref(obj['info']))
        self.assertEqual(obj['info'][2].startswith(
            'KBaseFile.SingleEndLibrary'), True)
        d = obj['data']
        self.assertEqual(d['sequencing_tech'], 'Unknown')
        self.assertEqual(d['single_genome'], 1)
        self.assertEqual('source' not in d, True)
        self.assertEqual('strain' not in d, True)
        self.check_lib(d['lib'], 2966, 'Sample1.fastq.gz',
                       'f118ee769a5e1b40ec44629994dfc3cd')
        node = d['lib']['file']['id']
        self.delete_shock_node(node)
