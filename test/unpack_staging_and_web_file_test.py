# -*- coding: utf-8 -*-
import ftplib
import os  # noqa: F401
import shutil
import time
import unittest
from configparser import ConfigParser
from os import environ

import requests
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
import threading
import socket
from biokbase.workspace.client import Workspace as workspaceService
from mock import patch

from installed_clients.DataFileUtilClient import DataFileUtil
from kb_uploadmethods.Utils.UnpackFileUtil import UnpackFileUtil
from kb_uploadmethods.authclient import KBaseAuth as _KBaseAuth
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
from installed_clients.AbstractHandleClient import AbstractHandle as HandleService


class kb_uploadmethods_unpack_Test(unittest.TestCase):

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

        cls.ftp_domain = socket.gethostbyname(socket.gethostname())
        cls.ftp_port = 21
        thread = threading.Thread(target=cls.start_ftp_service,
                                  args=(cls.ftp_domain, cls.ftp_port))
        thread.daemon = True
        thread.start()
        time.sleep(5)

        small_file = os.path.join(cls.scratch, 'test.txt')
        with open(small_file, "w") as f:
            f.write("empty content")
        cls.test_shock = cls.dfu.file_to_shock({'file_path': small_file, 'make_handle': True})
        cls.handles_to_delete = []
        cls.nodes_to_delete = []
        cls.handles_to_delete.append(cls.test_shock['handle']['hid'])
        cls.nodes_to_delete.append(cls.test_shock['shock_id'])

    @classmethod
    def start_ftp_service(cls, domain, port):

        print('starting ftp service')
        authorizer = DummyAuthorizer()
        authorizer.add_anonymous(os.getcwd(), perm='elradfmwMT')

        handler = FTPHandler
        handler.authorizer = authorizer

        address = (domain, port)
        with ThreadedFTPServer(address, handler) as server:
            server.serve_forever()

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

    def mock_file_to_staging(file_path_list, subdir_folder=None):
        print('Mocking _file_to_staging')
        print("Mocking uploaded files to staging area:\n{}".format('\n'.join(file_path_list)))

    def mock_file_to_staging_direct(file_path_list, subdir_folder=''):
        print('Mocking _file_to_staging_direct')
        print("Mocking uploaded files to staging area:\n{}".format('\n'.join(file_path_list)))

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

        return kb_uploadmethods_unpack_Test().test_shock

    @patch.object(UnpackFileUtil, "_file_to_staging_direct", side_effect=mock_file_to_staging_direct)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_unpack_web_file_direct_download_trailing_space(self, _file_to_staging_direct,
                                                            file_to_shock):
        file_url = 'https://anl.box.com/shared/static/'
        file_url += 'g0064wasgaoi3sax4os06paoyxay4l3r.zip   '

        params = {
            'download_type': 'Direct Download',
            'file_url': file_url,
            'workspace_name': self.getWsName()
        }

        ref = self.getImpl().unpack_web_file(self.getContext(), params)
        self.assertTrue('unpacked_file_path' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
        self.assertEqual(6, len(ref[0].get('unpacked_file_path').split(',')))
        for file_path in ref[0].get('unpacked_file_path').split(','):
            self.assertRegex(
                                os.path.basename(file_path),
                                'file[1-6]\.txt')

    @patch.object(UnpackFileUtil, "_file_to_staging_direct", side_effect=mock_file_to_staging_direct)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_unpack_web_file_direct_download_multiple_urls(self, _file_to_staging_direct,
                                                           file_to_shock):
        file_url = '  https://anl.box.com/shared/static/'
        file_url += 'g0064wasgaoi3sax4os06paoyxay4l3r.zip'
        params = {
          'download_type': 'Direct Download',
          'workspace_name': self.getWsName(),
          'urls_to_add_web_unpack': [
            {
                'file_url': file_url
            },
            {
                'file_url': file_url
            }
          ]
        }

        ref = self.getImpl().unpack_web_file(self.getContext(), params)
        self.assertTrue('unpacked_file_path' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
        self.assertEqual(12, len(ref[0].get('unpacked_file_path').split(',')))
        for file_path in ref[0].get('unpacked_file_path').split(','):
            self.assertRegex(
                            os.path.basename(file_path),
                            'file[1-6]\.txt')

    @patch.object(UnpackFileUtil, "_file_to_staging_direct", side_effect=mock_file_to_staging_direct)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_unpack_web_file_dropbox(self, _file_to_staging_direct, file_to_shock):
        params = {
            'download_type': 'DropBox',
            'file_url': 'https://www.dropbox.com/s/cbiywh2aihjxdf5/Archive.zip?dl=0',
            'workspace_name': self.getWsName()
        }

        ref = self.getImpl().unpack_web_file(self.getContext(), params)
        self.assertTrue('unpacked_file_path' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
        self.assertEqual(6, len(ref[0].get('unpacked_file_path').split(',')))
        for file_path in ref[0].get('unpacked_file_path').split(','):
            self.assertRegex(
                                os.path.basename(file_path),
                                'file[1-6]\.txt')

    @patch.object(UnpackFileUtil, "_file_to_staging_direct", side_effect=mock_file_to_staging_direct)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_unpack_web_file_ftp(self, _file_to_staging_direct, file_to_shock):
        # copy test file to FTP
        fq_filename = "Archive.zip"
        with ftplib.FTP(self.ftp_domain) as ftp_connection:
            ftp_connection.login('anonymous', 'anonymous@domain.com')
            if fq_filename not in ftp_connection.nlst():
                with open(os.path.join("data", fq_filename), 'rb') as fh:
                    ftp_connection.storbinary('STOR {}'.format(fq_filename), fh)

        params = {
            'download_type': 'FTP',
            'file_url': 'ftp://{}/{}    '.format(self.ftp_domain, fq_filename),
            'workspace_name': self.getWsName()
        }

        ref = self.getImpl().unpack_web_file(self.getContext(), params)
        self.assertTrue('unpacked_file_path' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
        self.assertEqual(6, len(ref[0].get('unpacked_file_path').split(',')))
        for file_path in ref[0].get('unpacked_file_path').split(','):
            self.assertRegex(
                        os.path.basename(file_path),
                        'file[1-6]\.txt')

    @patch.object(UnpackFileUtil, "_file_to_staging_direct", side_effect=mock_file_to_staging_direct)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_unpack_web_file_google_drive(self, _file_to_staging_direct, file_to_shock):
        file_url = 'https://drive.google.com/open?id=0B0exSa7ebQ0qSlJiWEVWYU5rYWM'
        params = {
            'download_type': 'Google Drive',
            'file_url': file_url,
            'workspace_name': self.getWsName()
        }

        ref = self.getImpl().unpack_web_file(self.getContext(), params)
        self.assertTrue('unpacked_file_path' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
        self.assertEqual(6, len(ref[0].get('unpacked_file_path').split(',')))
        for file_path in ref[0].get('unpacked_file_path').split(','):
            self.assertRegex(
                            os.path.basename(file_path),
                            'file[1-6]\.txt')

    @patch.object(DataFileUtil, "download_staging_file", side_effect=mock_download_staging_file)
    @patch.object(UnpackFileUtil, "_file_to_staging_direct", side_effect=mock_file_to_staging_direct)
    @patch.object(DataFileUtil, "file_to_shock", side_effect=mock_file_to_shock)
    def test_unpack_staging_file(self, _file_to_staging_direct, download_staging_file,
                                 file_to_shock):
        params = {
          'staging_file_subdir_path': 'Archive.zip',
          'workspace_name': self.getWsName()
        }

        ref = self.getImpl().unpack_staging_file(self.getContext(), params)
        self.assertTrue('unpacked_file_path' in ref[0])
        self.assertTrue('report_ref' in ref[0])
        self.assertTrue('report_name' in ref[0])
        self.assertEqual(6, len(ref[0].get('unpacked_file_path').split(',')))
        for file_path in ref[0].get('unpacked_file_path').split(','):
            self.assertRegex(
                        os.path.basename(file_path),
                        'file[1-6]\.txt')
