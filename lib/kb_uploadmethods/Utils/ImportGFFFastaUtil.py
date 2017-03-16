
import time
import json
import os

from kb_gffupload.kb_gffuploadClient import kb_gffupload
from DataFileUtil.DataFileUtilClient import DataFileUtil


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportGFFFastaUtil:
    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.gfu = kb_gffupload(self.callback_url,service_ver='dev')

    def import_gff_fasta_from_staging(self, params):
        '''
          import_gff_fasta_from_staging: wrapper method for kb_gffupload.fasta_gff_to_genome

          required params:
          fasta_file: fasta file from user's staging area
          gff_file: gff file from user's staging area
          genome_name: output genome object name
          workspace_name: workspace name that genome will be stored to

          file paths for both fasta and gff files must be subdirectory file path in staging area
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name

          return:
          genome_ref: return object reference
          report_name: name of generated report (if any)
          report_ref: report reference (if any)
        '''

        log('--->\nrunning ImportGFFFastaUtil.import_gff_fasta_from_staging\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_import_gff_fasta_from_staging_params(params)

        #If not testing, fetch from staging
        if('test' not in params or params['test'] != 1):
            for key in ('fasta_file','gff_file'):
                file_path = params[key]
                file = os.path.basename(file_path)
        
                download_staging_file_params = { 'staging_file_subdir_path': file }
                dfu_returnVal = self.dfu.download_staging_file(download_staging_file_params)
                params[key] = dfu_returnVal['copy_file_path']

        print params
        returnVal = self.gfu.fasta_gff_to_genome(params)
        return returnVal

    def validate_import_gff_fasta_from_staging_params(self, params):
        """
        validate_import_gff_fasta_from_staging_params: validates params passed to fasta_gff_to_genome method

        """

        # check for required parameters
        for p in ['genome_name', 'workspace_name', 'fasta_file', 'gff_file']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')  

        #for now must use workspace name, but no ws_id_to_name() function available
        if str(params["workspace_name"]).isdigit():
            raise ValueError('"' + params["workspace_name"] + '" parameter is a workspace id and workspace name is required')

    def validate_import_genbank_from_staging_params(self, params):
        """
        validate_import_genbank_from_staging_params:
                    validates params passed to import_genbank_from_staging method

        """

        # check for required parameters
        for p in ['staging_file_subdir_path', 'genome_name', 'workspace_name', 'source']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')
