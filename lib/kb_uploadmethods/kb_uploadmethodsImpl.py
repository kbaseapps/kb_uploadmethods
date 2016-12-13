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
    GIT_COMMIT_HASH = "e234459ebf252aaac7f44ea0f958bc2160d3ba3c"

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

    def __upload_single_end_reads_from_file(self, ctx, inputParamUploadFile)

        uploaded_first_file = False
        returnVal = dict([('uploaded_first_file', uploaded_first_file)])
        first_fastq_file_name = inputParamUploadFile.get('first_fastq_file_name')
        reads_file_name = inputParamUploadFile.get('reads_file_name')

        ru = ReadsUtils(self.callback_url, token=ctx['token'])
        fs = ftp_service(self.callback_url, token=ctx['token'])
        dfu = DataFileUtil(self.callback_url, token=ctx['token'])

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_fastq_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def __upload_paired_end_reads_from_file(self, ctx, inputParamUploadFile)

        uploaded_first_file = False
        uploaded_second_file = False
        returnVal = dict([('uploaded_first_file', uploaded_first_file), 
                        ('uploaded_second_file', uploaded_second_file)])
        first_fastq_file_name = inputParamUploadFile.get('first_fastq_file_name')
        second_file_name = inputParamUploadFile.get('second_fastq_file_name')
        reads_file_name = inputParamUploadFile.get('reads_file_name')

        ru = ReadsUtils(self.callback_url, token=ctx['token'])
        fs = ftp_service(self.callback_url, token=ctx['token'])
        dfu = DataFileUtil(self.callback_url, token=ctx['token'])

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_fastq_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]


    def upload_fastq_file(self, ctx, inputParamUploadFile):
        """
        :param inputParamUploadFile: instance of type "inputParamUploadFile"
           -> structure: parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "first_fastq_file_name"
           of type "first_fastq_file_name" (input and output file path/url),
           parameter "second_fastq_file_name" of type
           "second_fastq_file_name", parameter "first_fastq_file_url" of type
           "first_fastq_file_url", parameter "second_fastq_file_url" of type
           "second_fastq_file_url", parameter "reads_file_name" of type
           "reads_file_name"
        :returns: instance of type "outParam" -> structure: parameter
           "uploaded" of type "uploaded" (indicates true or false values,
           false <= 0, true >=1)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_fastq_file

        if inputParamUploadFile.get('second_fastq_file_name'):
            returnVal = __upload_paired_end_reads_from_file(ctx, inputParamUploadFile)
        elif inputParamUploadFile.get('first_fastq_file_name'):
            returnVal = __upload_single_end_reads_from_file(ctx, inputParamUploadFile)

        #END upload_fastq_file

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_fastq_file return value ' +
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
