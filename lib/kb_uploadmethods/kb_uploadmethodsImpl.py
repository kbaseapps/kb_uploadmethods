# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
from pprint import pprint
import json
from kb_uploadmethods.FastqUploaderUtil import FastqUploaderUtil
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
    GIT_URL = "git@github.com:Tianhao-Gu/kb_uploadmethods.git"
    GIT_COMMIT_HASH = "fd901fdac12fe74d0159b94ba127094aac757dcf"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        #END_CONSTRUCTOR
        pass


    def upload_fastq_file(self, ctx, params):
        """
        :param params: instance of type "UploadMethodParams"
           (sequencing_tech: sequencing technology name: output reads file
           name workspace_name: workspace name/ID of the object For files in
           user's staging area: fwd_staging_file_name: single-end fastq file
           name or forward/left paired-end fastq file name from user's
           staging area rev_staging_file_name: reverse/right paired-end fastq
           file name user's staging area For files from web: download_type:
           download type for web source fastq file ('Direct Download', 'FTP',
           'DropBox', 'Google Drive') fwd_file_url: single-end fastq file URL
           or forward/left paired-end fastq file URL rev_file_url:
           reverse/right paired-end fastq file URL urls_to_add: used for
           parameter-groups. dict of {fwd_file_url, rev_file_url, name}) ->
           structure: parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "fwd_staging_file_name"
           of type "fwd_staging_file_name" (input and output file path/url),
           parameter "rev_staging_file_name" of type "rev_staging_file_name",
           parameter "download_type" of type "download_type", parameter
           "fwd_file_url" of type "fwd_file_url", parameter "rev_file_url" of
           type "rev_file_url", parameter "sequencing_tech" of type
           "sequencing_tech", parameter "name" of type "name", parameter
           "urls_to_add" of type "urls_to_add" -> structure: parameter
           "fwd_file_url" of type "fwd_file_url", parameter "rev_file_url" of
           type "rev_file_url", parameter "name" of type "name"
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_fastq_file
        print '--->\nRunning uploadmethods.upload_fastq_file\nparams:'
        print json.dumps(params, indent=1)

        if params.get('urls_to_add'):
            returnVal = {'obj_ref': ''}
            for params_item in params.get('urls_to_add'):
                params_item['workspace_name'] = params.get('workspace_name')
                params_item['download_type'] = params.get('download_type')
                params_item['sequencing_tech'] = params.get('sequencing_tech')
                fastqUploader = FastqUploaderUtil(self.config)
                itemReturnVal = fastqUploader.upload_fastq_file(params_item) 
                returnVal['obj_ref'] += itemReturnVal['obj_ref'] + ',' 
            returnVal['obj_ref'] = returnVal['obj_ref'][:-1]
        else:
            fastqUploader = FastqUploaderUtil(self.config)
            returnVal = fastqUploader.upload_fastq_file(params)

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
