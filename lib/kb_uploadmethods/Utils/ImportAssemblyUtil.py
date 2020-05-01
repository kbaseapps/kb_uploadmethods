
import collections
import json
import logging
import os
import time
import uuid

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from . import handler_utils


class ImportAssemblyUtil:

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = os.path.join(config['scratch'], 'import_assembly_' + str(uuid.uuid4()))
        handler_utils._mkdir_p(self.scratch)
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.au = AssemblyUtil(self.callback_url)
        self.uploader_utils = UploaderUtil(config)
        self.max_contigs_for_report = 200

    def import_fasta_as_assembly_from_staging(self, params):
        """
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
        """
        logging.info('--->\nrunning ImportAssemblyUtil.import_fasta_as_assembly_from_staging\n'
                     f'params:\n{json.dumps(params, indent=1)}')

        self.validate_import_fasta_as_assembly_from_staging(params)

        download_staging_file_params = {
            'staging_file_subdir_path': params.get('staging_file_subdir_path')
        }
        scratch_file_path = self.dfu.download_staging_file(
                            download_staging_file_params).get('copy_file_path')

        with open(scratch_file_path, 'r') as fasta_file:
            first_line = fasta_file.readline()

        if not first_line.startswith('>'):
            raise ValueError("Expected FASTA record with a '>' as the first character on the first line.")

        file = {
            'path': scratch_file_path
        }
        import_assembly_params = params
        import_assembly_params['file'] = file

        ref = self.au.save_assembly_from_fasta(import_assembly_params)

        """
        Update the workspace object related meta-data for staged file
        """
        # self.uploader_utils.update_staging_service(params.get('staging_file_subdir_path'), ref)

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
                raise ValueError(f'"{p}" parameter is required, but missing')

    def generate_html_report(self, assembly_ref, assembly_object, params):
        """
        _generate_html_report: generate html summary report
        """
        logging.info('start generating html report')
        html_report = list()

        assembly_data = assembly_object.get('data')[0].get('data')
        assembly_info = assembly_object.get('data')[0].get('info')

        tmp_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        handler_utils._mkdir_p(tmp_dir)
        result_file_path = os.path.join(tmp_dir, 'report.html')

        assembly_name = str(assembly_info[1])
        assembly_file = params.get('staging_file_subdir_path')

        dna_size = assembly_data.get('dna_size')
        num_contigs = assembly_data.get('num_contigs')

        assembly_overview_data = collections.OrderedDict()

        assembly_overview_data['Name'] = '{} ({})'.format(assembly_name, assembly_ref)
        assembly_overview_data['Uploaded File'] = assembly_file
        assembly_overview_data['Date Uploaded'] = time.strftime("%c")
        assembly_overview_data['DNA Size'] = dna_size
        assembly_overview_data['Number of Contigs'] = num_contigs

        overview_content = ['<br/><table>\n']
        for key, val in assembly_overview_data.items():
            overview_content.append(f'<tr><td><b>{key}</b></td>')
            overview_content.append(f'<td>{val}</td></tr>\n')
        overview_content.append('</table>')

        contig_data = assembly_data.get('contigs').values()
        contig_content = str([str(e['contig_id']), e['length']] for e in contig_data)

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template',
                                   'report_template_assembly.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>*Overview_Content*</p>',
                                                          ''.join(overview_content))
                report_template = report_template.replace('*CONTIG_DATA*',
                                                          contig_content)
                result_file.write(report_template)
        result_file.close()

        report_shock_id = self.dfu.file_to_shock({'file_path': tmp_dir,
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
        object_data = self.dfu.get_objects({'object_refs': [obj_ref]})

        report_params = {
            'workspace_name': params.get('workspace_name'),
            'objects_created': [{'ref': obj_ref,
                                 'description': 'Imported Assembly'}],
            'report_object_name': f'kb_upload_assembly_report_{uuid.uuid4()}'}

        num_contigs = object_data['data'][0]['data']['num_contigs']
        if num_contigs > self.max_contigs_for_report:
            report_params['message'] = ("The uploaded assembly has too many contigs to display "
                                        "here. Click on the object for a dedicated viewer")
        else:
            output_html_files = self.generate_html_report(obj_ref, object_data, params)
            report_params.update({
                'html_links': output_html_files,
                'direct_html_link_index': 0,
                'html_window_height': 375,
            })

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

