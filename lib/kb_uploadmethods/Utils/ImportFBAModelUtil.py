
import time
import json
import sys
import uuid

from fba_tools.fba_toolsClient import fba_tools
from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportFBAModelUtil:
    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.fba = fba_tools(self.callback_url)

    def import_fbamodel_from_staging(self, params):
        """

        """
        log('--->\nrunning {}.{}\n params:\n{}'
            .format(self.__class__.__name__, sys._getframe().f_code.co_name,
                    json.dumps(params, indent=1)))

        self._check_param(params, ['model_file', 'file_type', 'workspace_name',
                                   'model_name'],
                          ['biomass', 'genome', 'compounds_file'])
        if params['file_type'] == 'tsv' and params.get('compound_file', None):
            raise ValueError('A compound file is required for tsv upload.')

        fba_tools_params = params.copy()
        for infile in ['model_file', 'compounds_file']:
            if not params.get(infile, None):
                continue
            download_staging_file_params = {
                'staging_file_subdir_path': params[infile]
            }
            scratch_file_path = self.dfu.download_staging_file(
                            download_staging_file_params).get('copy_file_path')
            fba_tools_params[infile] = {'path': scratch_file_path}

        if params['file_type'] == 'sbml':
            res = self.fba.sbml_file_to_model(fba_tools_params)
        elif params['file_type'] == 'excel':
            res = self.fba.excel_file_to_model(fba_tools_params)
        elif params['file_type'] == 'tsv':
            res = self.fba.tsv_file_to_model(fba_tools_params)
        else:
            raise ValueError('"{}" is not a valid import file_type'
                             .format(params['file_type']))

        return_val = self.generate_report(res['ref'], params)
        return_val['obj_ref'] = res['ref']

        return return_val

    @staticmethod
    def _check_param(in_params, req_param, opt_param=list()):
        """
        Check if each of the params in the list are in the input params
        """
        for param in req_param:
            if param not in in_params:
                raise ValueError('Required parameter "{}" is missing'
                                 .format(param))
        defined_param = set(req_param + opt_param)
        for param in in_params:
            if param not in defined_param:
                print('WARNING: received unexpected parameter "{}"'
                      .format(param))

    def generate_report(self, obj_ref, params):
        """
        generate_report: generate summary report

        obj_ref: generated workspace object references. (return of
                                                        import_excel(tsv)_as_media_from_staging)
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

        upload_message += "FBAModel Object Name: "
        upload_message += params['model_name'] + '\n'
        upload_message += 'Imported File: {}\n'.format(
                              params.get('model_file'))

        report_params = {
              'message': upload_message,
              'objects_created': [{'ref': obj_ref,
                                   'description': 'Imported FBAModel'}],
              'workspace_name': params.get('workspace_name'),
              'report_object_name': 'kb_upload_methods_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output
