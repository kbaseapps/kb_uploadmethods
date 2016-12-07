# -*- coding: utf-8 -*-
#BEGIN_HEADER
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
    GIT_COMMIT_HASH = "355bb67bfc40d97a5ad97a5610db063417a2fcdc"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
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
