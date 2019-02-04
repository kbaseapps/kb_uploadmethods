import json
import time
import uuid

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenericsApiClient import GenericsAPI
from installed_clients.KBaseReportClient import KBaseReport
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print((('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message)))


class ImportAttributeMappingUtil:

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.genapi = GenericsAPI(self.callback_url)
        self.uploader_utils = UploaderUtil(config)

    def import_attribute_mapping_from_staging(self, params):
        """
          import_attribute_mapping_from_staging: wrapper method for
                                    fba_tools.tsv_file_to_attribute_mapping

          required params:
          staging_file_subdir_path - subdirectory file path
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name
          attribute_mapping_name: output conditionSet object name
          workspace_name: workspace name/ID of the object

          return:
          obj_ref: return object reference
        """

        log('--->\nrunning ImportConditionSetUtil.import_attribute_mapping_from_staging\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_import_attribute_mapping_from_staging_params(params)

        download_staging_file_params = {
            'staging_file_subdir_path': params.get('staging_file_subdir_path')
        }
        scratch_file_path = self.dfu.download_staging_file(
                        download_staging_file_params).get('copy_file_path')
        ws_id = self.dfu.ws_name_to_id(params['workspace_name'])

        import_attribute_mapping_params = {
            'output_obj_name': params['attribute_mapping_name'],
            'output_ws_id': ws_id,
            'input_file_path': scratch_file_path
        }

        ref = self.genapi.file_to_attribute_mapping(import_attribute_mapping_params)

        # Update the workspace object related meta-data for staged file
        self.uploader_utils.update_staging_service(params.get('staging_file_subdir_path'),
                                                   ref.get('attribute_mapping_ref'))
        returnVal = {'obj_ref': ref.get('attribute_mapping_ref')}

        return returnVal

    @staticmethod
    def validate_import_attribute_mapping_from_staging_params(params):
        """
        validate_import_attribute_mapping_from_staging_params:
                    validates params passed to import_attribute_mapping_from_staging method
        """
        # check for required parameters
        for p in ['staging_file_subdir_path', 'workspace_name', 'attribute_mapping_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def generate_report(self, obj_ref, params):
        """
        generate_report: generate summary report

        obj_ref: generated workspace object references. (return of
                                                        import_attribute_mapping_from_staging)
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

        upload_message += "Attribute Mapping Name: "
        upload_message += str(object_data.get('data')[0].get('info')[1]) + '\n'
        upload_message += 'Imported File: {}\n'.format(params.get('staging_file_subdir_path'))
        report_params = {'message': upload_message,
                         'objects_created': [{'ref': obj_ref,
                                              'description': 'Imported Attribute Mapping'}],
                         'workspace_name': params['workspace_name'],
                         'report_object_name': 'kb_upload_methods_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output
