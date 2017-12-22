
import time
import json
from pprint import pprint

from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from DataFileUtil.DataFileUtilClient import DataFileUtil
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportGenbankUtil:
    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.gfu = GenomeFileUtil(self.callback_url, service_ver='dev')
        self.uploader_utils = UploaderUtil(config)

    def import_genbank_from_staging(self, params):
        '''
          import_genbank_from_staging: wrapper method for GenomeFileUtil.genbank_to_genome

          required params:
          staging_file_subdir_path - subdirectory file path
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name
          genome_name - becomes the name of the object
          workspace_name - the name of the workspace it gets saved to.
          source - Source of the file typically something like RefSeq or Ensembl

          optional params:
          release - Release or version number of the data
              per example Ensembl has numbered releases of all their data: Release 31
          generate_ids_if_needed - If field used for feature id is not there,
              generate ids (default behavior is raising an exception)
          genetic_code - Genetic code of organism. Overwrites determined GC from
              taxon object
          type - Reference, Representative or User upload

          return:
          genome_ref: return object reference
        '''

        log('--->\nrunning ImportGenbankUtil.import_genbank_from_staging\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_import_genbank_from_staging_params(params)

        download_staging_file_params = {
            'staging_file_subdir_path': params.get('staging_file_subdir_path')
        }
        scratch_file_path = self.dfu.download_staging_file(
                                 download_staging_file_params).get('copy_file_path')
        file = {
            'path': scratch_file_path
        }
        import_genbank_params = params
        import_genbank_params['file'] = file
        del import_genbank_params['staging_file_subdir_path']

        returnVal = self.gfu.genbank_to_genome(import_genbank_params)

        """
        Update the workspace object related meta-data for staged file
        """
        self.uploader_utils.update_staging_service(download_staging_file_params.get('staging_file_subdir_path'),
                                                   returnVal['genome_ref'])

        reportVal = {'report_name': returnVal['report_name'],
                     'report_ref': returnVal['report_ref']}
        returnVal.update(reportVal)
        return returnVal

    def validate_import_genbank_from_staging_params(self, params):
        """
        validate_import_genbank_from_staging_params:
                    validates params passed to import_genbank_from_staging method
        """
        # check for required parameters
        for p in ['staging_file_subdir_path', 'genome_name', 'workspace_name', 'source']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')

    def generate_report(self, genome_ref, report_ref_in):
        """
        :param genome_ref:  Uploaded genome ref
        :param report_ref_in: Report object from GenomeFileUtil. need to get warnings and message from it.
        :return: 
        """
        report_obj_in = self.dfu.get_objects({'object_refs': [report_ref_in]})
        pprint(report_obj_in)
