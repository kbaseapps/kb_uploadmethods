# # -*- coding: utf-8 -*-
# import unittest
# import os  # noqa: F401
# import json  # noqa: F401
# import time
# import requests

# from os import environ
# try:
#     from ConfigParser import ConfigParser  # py2
# except:
#     from configparser import ConfigParser  # py3

# from pprint import pprint  # noqa: F401

# from biokbase.workspace.client import Workspace as workspaceService
# from kb_uploadmethods.kb_uploadmethodsImpl import kb_uploadmethods
# from kb_uploadmethods.kb_uploadmethodsServer import MethodContext
# from kb_uploadmethods.authclient import KBaseAuth as _KBaseAuth
# from DataFileUtil.DataFileUtilClient import DataFileUtil


# class kb_uploadmethodsTest(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.token = environ.get('KB_AUTH_TOKEN', None)
#         config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
#         cls.cfg = {}
#         config = ConfigParser()
#         config.read(config_file)
#         for nameval in config.items('kb_uploadmethods'):
#             cls.cfg[nameval[0]] = nameval[1]
#         authServiceUrl = cls.cfg.get('auth-service-url',
#                                      "https://kbase.us/services/authorization/Sessions/Login")
#         auth_client = _KBaseAuth(authServiceUrl)
#         cls.user_id = auth_client.get_user(cls.token)
#         # WARNING: don't call any logging methods on the context object,
#         # it'll result in a NoneType error
#         cls.ctx = MethodContext(None)
#         cls.ctx.update({'token': cls.token,
#                         'user_id': cls.user_id,
#                         'provenance': [
#                             {'service': 'kb_uploadmethods',
#                              'method': 'please_never_use_it_in_production',
#                              'method_params': []
#                              }],
#                         'authenticated': 1})
#         cls.wsURL = cls.cfg['workspace-url']
#         cls.wsClient = workspaceService(cls.wsURL, token=cls.token)
#         cls.serviceImpl = kb_uploadmethods(cls.cfg)
#         cls.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=cls.token)
#         cls.scratch = cls.cfg['scratch']
#         cls.shockURL = cls.cfg['shock-url']

#     @classmethod
#     def tearDownClass(cls):
#         if hasattr(cls, 'wsName'):
#             cls.wsClient.delete_workspace({'workspace': cls.wsName})
#             print('Test workspace was deleted')

#     @classmethod
#     def make_ref(self, objinfo):
#         return str(objinfo[6]) + '/' + str(objinfo[0]) + '/' + str(objinfo[4])

#     @classmethod
#     def delete_shock_node(cls, node_id):
#         header = {'Authorization': 'Oauth {0}'.format(cls.token)}
#         requests.delete(cls.shockURL + '/node/' + node_id, headers=header,
#                         allow_redirects=True)
#         print('Deleted shock node ' + node_id)

#     def getWsClient(self):
#         return self.__class__.wsClient

#     def getWsName(self):
#         if hasattr(self.__class__, 'wsName'):
#             return self.__class__.wsName
#         suffix = int(time.time() * 1000)
#         wsName = "test_kb_uploadmethods_" + str(suffix)
#         ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
#         self.__class__.wsName = wsName
#         return wsName

#     def getImpl(self):
#         return self.__class__.serviceImpl

#     def getContext(self):
#         return self.__class__.ctx

#     def test_contructor(self):
#         ret = self.getImpl()
#         print 'self.config: %s' % ret.config
#         print 'self.callback_url: %s' % ret.config['SDK_CALLBACK_URL']
#         self.assertIsNotNone(ret.config)
#         self.assertIsNotNone(ret.config['SDK_CALLBACK_URL'])
