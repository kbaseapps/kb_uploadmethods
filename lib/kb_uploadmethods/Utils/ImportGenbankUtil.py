
import os
import time
import json
import uuid
import collections
from pprint import pprint

import handler_utils
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportGenbankUtil:
    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = os.path.join(config['scratch'], 'import_GenBank_' + str(uuid.uuid4()))
        handler_utils._mkdir_p(self.scratch)
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
        self.uploader_utils.update_staging_service(
            download_staging_file_params.get('staging_file_subdir_path'),
            returnVal['genome_ref'])
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

    def generate_html_report(self, genome_ref, gfu_report_ref, params):
        """
        _generate_html_report: generate html summary report
        """
        log('start generating html report')

        pprint(params)
        gfu_report_obj = self.dfu.get_objects({'object_refs': [gfu_report_ref]})
        pprint(gfu_report_obj)

        genome_obj = self.dfu.get_objects({'object_refs': [genome_ref]})

        html_report = list()

        result_file_path = os.path.join(self.scratch, 'report.html')

        genome_name = str(genome_obj.get('data')[0].get('info')[1])
        genome_file = params.get('staging_file_subdir_path')

        genome_data = genome_obj.get('data')[0].get('data')
        genome_info = genome_obj.get('data')[0].get('info')
        num_contigs = genome_info[10].get('Number contigs')
        gc_content = genome_info[10].get('GC content')
        warnings = gfu_report_obj.get('data')[0].get('info')[10].get('Warnings')

        genome_overview_data = collections.OrderedDict()

        genome_overview_data['Name'] = '{} ({})'.format(genome_name, genome_ref)
        genome_overview_data['Uploaded File'] = genome_file
        genome_overview_data['Date Uploaded'] = time.strftime("%c")
        genome_overview_data['Number of Contigs'] = num_contigs
        genome_overview_data['GC Content'] = gc_content
        genome_overview_data['Warnings'] = warnings

        overview_content = ''
        overview_content += '<br/><table>\n'
        for key, val in genome_overview_data.iteritems():
            overview_content += '<tr><td><b>{}</b></td>'.format(key)
            overview_content += '<td>{}</td>'.format(val)
            overview_content += '</tr>\n'
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
                            'description': 'HTML summary report for imported Genome'})
        return html_report

    def generate_report(self, genome_ref, gfu_report_ref, params):
        """
        :param genome_ref:  Return Val from GenomeFileUtil for Uploaded genome
                            Need to get report warnings and message from it.
        :return: 
        """
        uuid_string = str(uuid.uuid4())

        objects_created = [{'ref': genome_ref,
                            'description': 'Imported Genome'}]

        output_html_files = self.generate_html_report(genome_ref,
                                                      gfu_report_ref,
                                                      params)
        report_params = {
            'message': '',
            'workspace_name': params.get('workspace_name'),
            'objects_created': objects_created,
            'html_links': output_html_files,
            'direct_html_link_index': 0,
            'html_window_height': 270,
            'report_object_name': 'kb_genbank_upload_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

