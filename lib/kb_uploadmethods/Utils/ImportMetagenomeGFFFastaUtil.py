import os
import time
import logging
import uuid
import collections

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from . import handler_utils


class ImportMetagenomeGFFFastaUtil:
    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.gfu = GenomeFileUtil(self.callback_url, service_ver='release')
        self.uploader_utils = UploaderUtil(config)
        self.scratch = os.path.join(config['scratch'], 'import_Metagenome_' + str(uuid.uuid4()))
        handler_utils._mkdir_p(self.scratch)

    def import_metagenome_gff_fasta_from_staging(self, params):
        """
        import_gff_fasta_from_staging: wrapper method for GenomeFileUtil.fasta_gff_to_genome

        required params:
        fasta_file: fasta file from user's staging area
        gff_file: gff file from user's staging area
        genome_name: output genome object name
        workspace_name: workspace name that genome will be stored to

        file paths for both fasta and gff files must be subdirectory file path in staging area
        e.g.
        for file: /data/bulk/user_name/file_name
        staging_file_subdir_path is file_name
        for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
        staging_file_subdir_path is subdir_1/subdir_2/file_name

        optional params:
        release: Release Or Version Of The Source Data
        genetic_code: Genetic Code For The Organism
        type: 'Reference', 'User upload', 'Representative'

        return:
        genome_ref: return object reference
        report_name: name of generated report (if any)
        report_ref: report reference (if any)
        """
        # logging.info('--->\nrunning ImportMetagenomeGFFFastaUtil.import_metagenome_gff_fasta_from_staging\n' +
        #              f'params:\n{json.dumps(params, indent=1)}')

        self.validate_import_metagenome_gff_fasta_from_staging_params(params)

        for key in ('fasta_file', 'gff_file'):
            file_path = params[key]
            download_staging_file_params = {'staging_file_subdir_path': file_path}
            dfu_returnVal = self.dfu.download_staging_file(download_staging_file_params)
            params[key] = {'path': dfu_returnVal['copy_file_path']}

        returnVal = self.gfu.fasta_gff_to_metagenome(params)

        """
        Update the workspace object related meta-data for staged file
        """
        # self.uploader_utils.update_staging_service(download_staging_file_params.get('staging_file_subdir_path'),
        #                                            returnVal['genome_ref'])
        return returnVal

    def validate_import_metagenome_gff_fasta_from_staging_params(self, params):
        """
        validate_import_metagenome_gff_fasta_from_staging_params:
                    validates params passed to import_gff_fasta_from_staging method
        """
        # check for required parameters

        for p in ['genome_name', 'workspace_name', 'fasta_file', 'gff_file']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')

        # for now must use workspace name, but no ws_id_to_name() function available
        if str(params["workspace_name"]).isdigit():
            error_msg = '"{}" parameter is a workspace id and workspace name is required'.format(
                                                                        params["workspace_name"])
            raise ValueError(error_msg)

    def generate_html_report(self, genome_ref, params):
        """
        _generate_html_report: generate html summary report
        """
        logging.info('start generating html report')
        genome_obj = self.dfu.get_objects({'object_refs': [genome_ref]})
        html_report = list()
        tmp_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        handler_utils._mkdir_p(tmp_dir)
        result_file_path = os.path.join(tmp_dir, 'report.html')

        genome_name = str(genome_obj.get('data')[0].get('info')[1])
        # genome_file = params.get('staging_file_subdir_path')

        genome_data = genome_obj.get('data')[0].get('data')
        genome_info = genome_obj.get('data')[0].get('info')
        genome_metadata = genome_info[10]

        source = genome_metadata.get('Source')
        num_contigs = genome_metadata.get('Number contigs')
        size = genome_metadata.get('Size')
        gc_content = genome_metadata.get('GC content')

        warnings = genome_data.get('warnings', [])
        feature_counts = sorted(list(genome_data.get('feature_counts', {}).items()))

        genome_overview_data = collections.OrderedDict()

        genome_overview_data['Name'] = '{} ({})'.format(genome_name, genome_ref)
        # genome_overview_data['Uploaded File'] = genome_file
        genome_overview_data['Date Uploaded'] = time.strftime("%c")
        genome_overview_data['Source'] = source
        genome_overview_data['Number of Contigs'] = num_contigs
        genome_overview_data['Size'] = size
        genome_overview_data['GC Content'] = gc_content
        genome_overview_data['Warnings'] = "\n".join(warnings)
        genome_overview_data.update(feature_counts)

        overview_content = '<br/><table>\n'
        for key, val in genome_overview_data.items():
            overview_content += '<tr><td><b>{}</b></td>'.format(key)
            overview_content += '<td>{}</td></tr>\n'.format(val)
        overview_content += '</table>'

        feature_content = str([[str(k), v] for k, v in
                               list(genome_data.get('feature_counts', {}).items())
                               if k != 'gene'])
        contig_content = str([[str(c), l] for c, l in
                              zip(genome_data.get('contig_ids', []),
                                  genome_data.get('contig_lengths', []))])

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template',
                                   'report_template_genome.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>Overview_Content</p>',
                                                          overview_content)
                report_template = report_template.replace('*FEATURE_DATA*',
                                                          feature_content)
                report_template = report_template.replace('*CONTIG_DATA*',
                                                          contig_content)
                result_file.write(report_template)

        report_shock_id = self.dfu.file_to_shock({'file_path': tmp_dir,
                                                  'pack': 'zip'})['shock_id']

        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for imported Annotated Metagenome Assembly'})
        return html_report

    def generate_report(self, genome_ref, params):
        """
        :param genome_ref:  Return Val from GenomeFileUtil for Uploaded metagenome
                            Need to get report warnings and message from it.
        :return:
        """
        uuid_string = str(uuid.uuid4())

        objects_created = [{'ref': genome_ref,
                            'description': 'Imported Annotated Metagenome Assembly'}]

        output_html_files = self.generate_html_report(genome_ref, params)
        report_params = {
            'message': '',
            'workspace_name': params.get('workspace_name'),
            'objects_created': objects_created,
            'html_links': output_html_files,
            'direct_html_link_index': 0,
            'html_window_height': 300,
            'report_object_name': 'kb_metagenome_upload_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output
