
import time
import json
import uuid
import os
from pprint import pprint

import handler_utils
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))

class ImportAssemblyUtil:

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = os.path.join(config['scratch'], 'import_assembly_' + str(uuid.uuid4()))
        handler_utils._mkdir_p(self.scratch)
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.au = AssemblyUtil(self.callback_url)
        self.uploader_utils = UploaderUtil(config)

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

        """
        Update the workspace object related meta-data for staged file
        """
        self.uploader_utils.update_staging_service(params.get('staging_file_subdir_path'), ref)

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

    def generate_html_report(self, assembly_ref, assembly_data, params):
        """
        _generate_html_report: generate html summary report
        """
        log('start generating html report')
        html_report = list()

        result_file_path = os.path.join(self.scratch, 'report.html')

        assembly_name = str(assembly_data.get('data')[0].get('info')[1])
        assembly_file = params.get('staging_file_subdir_path')

        base_count = assembly_data.get('data')[0].get('data').get('base_counts')
        base_count_str = ''
        for base, count in base_count.iteritems():
            base_count_str += '{}({:,}) '.format(base, count)

        dna_size = assembly_data.get('data')[0].get('data').get('dna_size')

        overview_content = ''

        overview_content += '<br/><table><tr><th>Imported Assembly'
        overview_content += '</th><th></th><th></th><th></th></tr>'

        overview_content += '<br/><table><tr><td><b>Assembly Object:</b></td>'
        overview_content += '<td>{} ({})'.format(assembly_name,
                                                 assembly_ref)
        overview_content += '</td>'
        overview_content += '</tr>'

        overview_content += '<tr><td><b>{}</b></td>'.format('Fasta File:')
        overview_content += '<td>{}</td>'.format(assembly_file)
        overview_content += '</tr>'

        overview_content += '<tr><td><b>{}</b></td>'.format('DNA Size:')
        overview_content += '<td>{:,}</td>'.format(dna_size)
        overview_content += '</tr>'

        overview_content += '<tr><td><b>{}</b></td>'.format('Base Counts:')
        overview_content += '<td>{}</td>'.format(base_count_str)
        overview_content += '</tr>'

        overview_content += '</table>'

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>Overview_Content</p>',
                                                          overview_content)
                result_file.write(report_template)
        result_file.close()

        report_shock_id = self.dfu.file_to_shock({'file_path': self.scratch,
                                                  'pack': 'zip'})['shock_id']

        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for Imported Assembly'})
        return html_report

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

        get_objects_params = {
            'object_refs': [obj_ref],
            'ignore_errors': False
        }
        object_data = self.dfu.get_objects(get_objects_params)
        objects_created = [{'ref': obj_ref,
                            'description': 'Imported Assembly'}]

        output_html_files = self.generate_html_report(obj_ref, object_data, params)

        report_params = {
                'message': '',
                'workspace_name': params.get('workspace_name'),
                'objects_created': objects_created,
                'html_links': output_html_files,
                'direct_html_link_index': 0,
                'html_window_height': 270,
                'report_object_name': 'kb_upload_mothods_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

