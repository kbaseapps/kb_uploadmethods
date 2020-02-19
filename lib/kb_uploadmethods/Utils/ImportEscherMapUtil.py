import json
import uuid
import logging
import copy

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport


class ImportEscherMapUtil:

    @staticmethod
    def validate_eschermap_params(params, expected, opt_param=set()):
        """
        Validates that required parameters are present.
        Warns if unexpected parameters appear
        """
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logging.warning("Unexpected parameter {} supplied".format(param))

    def _save_escher_map(self, escher_data, workspace_id, escher_map_name):
        """
        save KBaseFBA.EscherMap to workspace
        """

        logging.info('start saving KBaseFBA.EscherMap')

        if not isinstance(workspace_id, int):
            logging.warning('Invalid workspace ID: {}'.format(workspace_id))

            try:
                workspace_id = self.dfu.ws_name_to_id(workspace_id)
            except Exception:
                raise ValueError('Cannot convert {} to valid workspace id'.format(workspace_id))

        info = self.dfu.save_objects({'id': workspace_id,
                                      'objects': [{'type': 'KBaseFBA.EscherMap',
                                                   'data': escher_data,
                                                   'name': escher_map_name}]})[0]

        return "%s/%s/%s" % (info[6], info[0], info[4])

    def _refactor_escher_data(self, escher_data):
        """
        refactor escher data to better fit KBaseFBA.EscherMap object
        """
        logging.info('start refactoring escher data')
        refactored_escher_data = copy.deepcopy(escher_data)

        if refactored_escher_data == escher_data:
            logging.warning('No changes in escher data')

        return refactored_escher_data

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)

    def import_eschermap_from_staging(self, params):
        """
          import_attribute_mapping_from_staging: import a JSON file as KBaseFBA.EscherMap

          required params:
          staging_file_subdir_path - subdirectory file path
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name
          escher_map_name: output KBaseFBA.EscherMap object name
          workspace_id: workspace ID

          return:
          obj_ref: return object reference
        """

        self.validate_eschermap_params(params, ['staging_file_subdir_path', 'escher_map_name',
                                                'workspace_id'])

        download_staging_file_params = {
            'staging_file_subdir_path': params.get('staging_file_subdir_path')
        }
        scratch_file_path = self.dfu.download_staging_file(
                                               download_staging_file_params).get('copy_file_path')

        try:
            with open(scratch_file_path) as f:
                escher_data = json.load(f)
        except Exception:
            raise ValueError('Failed to parse JSON file.')

        escher_data = self._refactor_escher_data(escher_data)

        obj_ref = self._save_escher_map(escher_data,
                                        params['workspace_id'],
                                        params['escher_map_name'])

        returnVal = {'obj_ref': obj_ref}

        return returnVal

    def generate_report(self, obj_ref, params):
        """
        generate_report: generate summary report

        obj_ref: generated workspace object references.
        """
        logging.info('start generating report')

        upload_message = 'Import Finished\n'

        get_objects_params = {'object_refs': [obj_ref],
                              'ignore_errors': False}

        object_data = self.dfu.get_objects(get_objects_params)

        upload_message += "Imported Escher Map Name: "
        upload_message += str(object_data.get('data')[0].get('info')[1]) + '\n'
        upload_message += 'Imported File: {}\n'.format(params['staging_file_subdir_path'])
        report_params = {'message': upload_message,
                         'objects_created': [{'ref': obj_ref,
                                              'description': 'Imported Escher Map'}],
                         'workspace_id': params['workspace_id'],
                         'report_object_name': 'kb_upload_methods_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output
