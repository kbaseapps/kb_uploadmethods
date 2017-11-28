
import time
import json
import uuid

from KBaseFeatureValues.KBaseFeatureValuesClient import KBaseFeatureValues
from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportExpressionMatrixUtil:
    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.fv = KBaseFeatureValues(self.callback_url)
        self.uploader_utils = UploaderUtil(config)

    def import_tsv_as_expression_matrix_from_staging(self, params):
        '''
        import_tsv_as_expression_matrix_from_staging: wrapper method for
                                    KBaseFeatureValues.tsv_file_to_matrix

        required params:
            staging_file_subdir_path: subdirectory file path
              e.g.
                for file: /data/bulk/user_name/file_name
                staging_file_subdir_path is file_name
                for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
                staging_file_subdir_path is subdir_1/subdir_2/file_name
            matrix_name: output Expressin Matirx file name
            workspace_name: workspace name/ID of the object

        optional params:
            genome_ref: optional reference to a Genome object that will be
                  used for mapping feature IDs to
            fill_missing_values: optional flag for filling in missing
                    values in matrix (default value is false)
            data_type: optional filed, value is one of 'untransformed',
                    'log2_level', 'log10_level', 'log2_ratio', 'log10_ratio' or
                    'unknown' (last one is default value)
            data_scale: optional parameter (default value is '1.0')

        return:
            obj_ref: return object reference
        '''

        log('--->\nrunning ImportAssemblyUtil.import_tsv_as_expression_matrix_from_staging\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_import_tsv_as_expression_matrix_from_staging_params(params)

        download_staging_file_params = {
            'staging_file_subdir_path': params.get('staging_file_subdir_path')
        }
        scratch_file_path = self.dfu.download_staging_file(
                        download_staging_file_params).get('copy_file_path')

        import_matrix_params = params
        import_matrix_params['input_file_path'] = scratch_file_path
        import_matrix_params['output_ws_name'] = params.get('workspace_name')
        import_matrix_params['output_obj_name'] = params.get('matrix_name')

        ref = self.fv.tsv_file_to_matrix(import_matrix_params)
        """
        Update the workspace object related meta-data for staged file
        """
        self.uploader_utils.update_staging_service(params.get('staging_file_subdir_path'),
                                                   ref.get('output_matrix_ref'))
        returnVal = {'obj_ref': ref.get('output_matrix_ref')}

        return returnVal

    def validate_import_tsv_as_expression_matrix_from_staging_params(self, params):
        """
        validate_import_tsv_as_expression_matrix_from_staging_params:
                    validates params passed to import_tsv_as_expression_matrix_from_staging method

        """

        # check for required parameters
        for p in ['staging_file_subdir_path', 'workspace_name', 'matrix_name']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')

    def generate_report(self, obj_ref, params):
        """
        generate_report: generate summary report

        obj_ref: generated workspace object references. (return of
                                                         import_tsv_as_expression_matrix_from_staging)
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

        upload_message += "Expression Matrix Object Name: "
        upload_message += str(object_data.get('data')[0].get('info')[1]) + '\n'
        upload_message += 'Imported TSV File: {}\n'.format(
                              params.get('staging_file_subdir_path'))

        report_params = {
              'message': upload_message,
              'workspace_name': params.get('workspace_name'),
              'report_object_name': 'kb_upload_mothods_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output
