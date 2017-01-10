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
    GIT_URL = "git@github.com:Tianhao-Gu/uk_uploadmethods.git"
    GIT_COMMIT_HASH = "d2d60b113676883396e72cbde28f424d7e69f4f3"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        #END_CONSTRUCTOR
        pass


    def upload_fastq_file(self, ctx, params):
        """
        :param params:
            sequencing_tech: sequencing technology
            reads_file_name: output reads file name
            workspace_name: workspace name/ID of the object
            
            For files in user's staging area:
            first_fastq_file_name: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
            second_fastq_file_name: reverse/right paired-end fastq file name user's staging area
            
            For files from web:
            download_type: download type for web source fastq file ('Direct Download', 'FTP', 'DropBox', 'Google Drive')
            first_fastq_file_url: single-end fastq file URL or forward/left paired-end fastq file URL
            second_fastq_file_url: reverse/right paired-end fastq file URL
             
            urls_to_add: used for parameter-groups. dict of {first_fastq_file_url, second_fastq_file_url, reads_file_name}

        :returns: 
            obj_ref: return object(s) ref
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
