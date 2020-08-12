
import time
import json
import sys
import uuid

from installed_clients.fba_toolsClient import fba_tools
from installed_clients.SBMLToolsClient import SBMLTools
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print((('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message)))


class ImportFBAModelUtil:

    def _call_sbml_tools(self, params):

        try:
            # calling SBMLTools.sbml_importer without genome
            sbml_importer_params = dict()
            sbml_importer_params['sbml_local_path'] = params.get('model_file').get('path')
            sbml_importer_params['automatically_integrate'] = 1
            sbml_importer_params['remove_boundary'] = 1
            for param_name in ['workspace_name', 'model_name', 'biomass']:
                sbml_importer_params[param_name] = params.get(param_name)
            log('start executing SBMLTools.sbml_importer with {}'.format(sbml_importer_params))
            sbml_importer_ret = self.SBMLTools.sbml_importer(sbml_importer_params)
            log('SBMLTools.sbml_importer returned {}'.format(sbml_importer_ret))
        except Exception:
            raise ValueError('Unexpected error calling SBMLTools.sbml_importer')

        try:
            # calling SBMLTools.integrate_model
            integrate_model_params = dict()
            integrate_model_params['biomass_reactions'] = ''
            integrate_model_params['compartment_translation'] = list()
            integrate_model_params['compound_mappings'] = ''
            integrate_model_params['create_extracellular'] = 0
            integrate_model_params['fill_metadata'] = 1
            integrate_model_params['gene_mappings'] = ''
            integrate_model_params['remove_boundary'] = 1
            integrate_model_params['template_id'] = 'gramneg'
            integrate_model_params['translate_database'] = 'modelseed'

            integrate_model_params['model_name'] = params.get('model_name')
            integrate_model_params['output_model_name'] = params.get('model_name')
            integrate_model_params['output_media_name'] = params.get('model_name') + '.media'
            integrate_model_params['genome_id'] = params.get('genome')

            log('start executing SBMLTools.integrate_model with {}'.format(integrate_model_params))
            sbml_integrate_model_ret = self.SBMLTools.integrate_model(integrate_model_params)
            log('SBMLTools.integrate_model returned {}'.format(sbml_integrate_model_ret))

            fbamodel_id = sbml_integrate_model_ret['fbamodel_id']
            report_name = sbml_integrate_model_ret['report_name']
            report_ref = sbml_integrate_model_ret['report_ref']
        except Exception:
            raise ValueError('Unexpected error calling SBMLTools.integrate_model')

        return fbamodel_id, report_name, report_ref

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.fba = fba_tools(self.callback_url)
        self.SBMLTools = SBMLTools(self.callback_url)
        self.uploader_utils = UploaderUtil(config)

    def import_fbamodel_from_staging(self, params):

        log('--->\nrunning {}.{}\n params:\n{}'
            .format(self.__class__.__name__, sys._getframe().f_code.co_name,
                    json.dumps(params, indent=1)))

        self._check_param(params, ['model_file', 'file_type', 'workspace_name',
                                   'model_name', 'biomass'],
                                  ['genome', 'compounds_file'])
        if params['file_type'] == 'tsv' and not params.get('compounds_file', None):
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

        report_name = None
        report_ref = None
        if params['file_type'] == 'sbml':
            fbamodel_id, report_name, report_ref = self._call_sbml_tools(fba_tools_params)
            res = dict()
            res['ref'] = fbamodel_id
            # res = self.fba.sbml_file_to_model(fba_tools_params)
        elif params['file_type'] == 'excel':
            res = self.fba.excel_file_to_model(fba_tools_params)
        elif params['file_type'] == 'tsv':
            res = self.fba.tsv_file_to_model(fba_tools_params)
        else:
            raise ValueError('"{}" is not a valid import file_type'
                             .format(params['file_type']))

        return {'obj_ref': res['ref'], 'report_name': report_name, 'report_ref': report_ref}

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
                print(('WARNING: received unexpected parameter "{}"'
                      .format(param)))

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
