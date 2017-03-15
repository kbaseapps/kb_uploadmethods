
import time
import json
import uuid

from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportAssemblyUtil:
    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.au = AssemblyUtil(self.callback_url)

    def import_fasta_as_assembly_from_staging(self, params):
        '''
          import_fasta_as_assembly_from_staging: wrapper method for
                                    AssemblyUtil.save_assembly_from_fasta

          required params:
          staging_file_subdir_path - subdirectory file path
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name
          assembly_name - output Assembly file name
          workspace_name - the name of the workspace it gets saved to.

          return:
          obj_ref: return object reference
        '''

        log('--->\nrunning ImportAssemblyUtil.import_fasta_as_assembly_from_staging\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_import_fasta_as_assembly_from_staging(params)

        download_staging_file_params = {
            'staging_file_subdir_path': params.get('staging_file_subdir_path')
        }
        scratch_file_path = self.dfu.download_staging_file(
                        download_staging_file_params).get('copy_file_path')

        file = {
            'path': scratch_file_path
        }

        import_assembly_params = params
        import_assembly_params['file'] = file

        ref = self.au.save_assembly_from_fasta(import_assembly_params)

        returnVal = {'obj_ref': ref}

        return returnVal

    def validate_import_fasta_as_assembly_from_staging(self, params):
        """
        validate_import_fasta_as_assembly_from_staging:
                    validates params passed to import_fasta_as_assembly_from_staging method

        """

        # check for required parameters
        for p in ['staging_file_subdir_path', 'workspace_name', 'assembly_name']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')

    def generate_report(self, obj_ref, params):
        """
        generate_report: generate summary report

        obj_ref: generated workspace object references. (return of
                                                         import_fasta_as_assembly_from_staging)
        params:
        staging_file_subdir_path: subdirectory file path
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name
        workspace_name: workspace name/ID that reads will be stored to

        """

        uuid_string = str(uuid.uuid4())
        upload_message = 'Import Finished\n'

        get_objects_params = {
            'object_refs': [obj_ref],
            'ignore_errors': False
        }

        object_data = self.dfu.get_objects(get_objects_params)
        base_count = object_data.get('data')[0].get('data').get('base_counts')
        dna_size = object_data.get('data')[0].get('data').get('dna_size')

        upload_message += "Assembly Object Name: "
        upload_message += str(object_data.get('data')[0].get('info')[1]) + '\n'
        upload_message += 'Imported Fasta File: {}\n'.format(
                              params.get('staging_file_subdir_path'))

        if isinstance(dna_size, (int, long)):
            upload_message += 'DNA Size: {:,}\n'.format(dna_size)

        if isinstance(base_count, dict):
            upload_message += 'Base Count:\n{}\n'.format(json.dumps(base_count, indent=1)[2:-2])

        report_params = {
              'message': upload_message,
              'workspace_name': params.get('workspace_name'),
              'report_object_name': 'kb_upload_mothods_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output
