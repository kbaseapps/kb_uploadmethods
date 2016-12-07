# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from ftp_service.ftp_serviceClient import ftp_service
#END_HEADER


class kb_uploadmethods:
    '''
    Module Name:
    kb_uploadmethods

    Module Description:
    A KBase module: kb_uploadmethods
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:Tianhao-Gu/uk_uploadmethods.git"
    GIT_COMMIT_HASH = "faf8bbdf0da8eff85b2ee2729b94107ba31898c6"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.scratch = config['scratch']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        #END_CONSTRUCTOR
        pass


    def upload_fastq_file(self, ctx, inputParamUploadFile):
        """
        :param inputParamUploadFile: instance of type "inputParamUploadFile"
           -> structure: parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "fastq_file_path" of
           type "fastq_file_path" (input and output file path/url), parameter
           "secondary_fastq_file_path" of type "secondary_fastq_file_path",
           parameter "reads_file_name" of type "reads_file_name"
        :returns: instance of type "outParam" -> structure: parameter
           "uploaded" of type "uploaded" (indicates true or false values,
           false <= 0, true >=1)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_fastq_file

        fastq_file_path = inputParamUploadFile.get('fastq_file_path')
        secondary_file_path = inputParamUploadFile.get('secondary_fastq_file_path')
        reads_file_name = inputParamUploadFile.get('reads_file_name')


        ru = ReadsUtils(self.callback_url, token=ctx['token'])
        fs = ftp_service(self.callback_url, token=ctx['token'])
        dfu = DataFileUtil(self.callback_url, token=ctx['token'])
        #END upload_fastq_file

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_fastq_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def upload_fastq_url(self, ctx, inputParamUploadURL):
        """
        :param inputParamUploadURL: instance of type "inputParamUploadURL" ->
           structure: parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "fastq_file_url" of type
           "fastq_file_url", parameter "secondary_fastq_file_url" of type
           "secondary_fastq_file_url", parameter "reads_file_name" of type
           "reads_file_name"
        :returns: instance of type "outParam" -> structure: parameter
           "uploaded" of type "uploaded" (indicates true or false values,
           false <= 0, true >=1)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_fastq_url
        #END upload_fastq_url

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_fastq_url return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
