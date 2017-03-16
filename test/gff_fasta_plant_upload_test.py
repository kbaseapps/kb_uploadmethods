import unittest
import os
import time
import shutil
import requests
import json

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
from DataFileUtil.DataFileUtilClient import DataFileUtil

class kb_uploadmethodsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        cls.user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(cls.token)).json()['user_id']
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
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_uploadmethods'):
            cls.cfg[nameval[0]] = nameval[1]
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

    def test_simple_upload(self):
        # fetch the test files and set things up
        kb_uploadmethods = self.getImpl()
        data_dir="data/Test_Plant"
        scratch_data_dir = os.path.join(self.scratch,data_dir)
        shutil.copytree(data_dir, scratch_data_dir)

        fasta_file = "Test_v1.0.fa.gz"
        gff_file = "Test_v1.0.gene.gff3.gz"

        fasta_path = scratch_data_dir+"/"+fasta_file
        gff_path = scratch_data_dir+"/"+gff_file

        shutil.copy(data_dir+"/"+fasta_file, fasta_path)
        shutil.copy(data_dir+"/"+gff_file, gff_path)

        fasta_path=self.dfu.unpack_file({'file_path':fasta_path}).get('file_path')
        gff_path=self.dfu.unpack_file({'file_path':gff_path}).get('file_path')
        
        pprint([fasta_path,gff_path])

        ws_obj_name = 'MyGenome'
        ws_name = self.getWsName()
        scientific_name = "Populus trichocarpa"

        ### Test for a Local Function Call
        print('attempting upload via local function directly')

        result = kb_uploadmethods.upload_fasta_gff_file(self.getContext(), 
            {
                'fasta_file' : fasta_path,
                'gff_file' : gff_path,
                'workspace_name':ws_name,
                'genome_name':ws_obj_name,
                'scientific_name':scientific_name,
                'test':1
            })[0]
        pprint(result)
        #self.assertIsNotNone(result['genome_ref'])

        shutil.rmtree(scratch_data_dir)

