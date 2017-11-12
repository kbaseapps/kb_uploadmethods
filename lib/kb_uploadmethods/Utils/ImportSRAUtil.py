
import json
import uuid
import time
import os
import fnmatch
import errno
import glob
import subprocess
from pprint import pprint
import collections

import handler_utils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ftp_service.ftp_serviceClient import ftp_service
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportSRAUtil:

    SRA_TOOLKIT_PATH = '/kb/deployment/bin/fastq-dump'

    def _run_command(self, command):
        """
        _run_command: run command and print result
        """

        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            log('Executed commend:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running commend:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
            raise ValueError(error_msg)

    def _check_fastq_dump_result(self, tmp_dir, sra_name):
        """
        _check_fastq_dump_result: check fastq_dump result is PE or SE
        """
        return os.path.exists(tmp_dir + '/' + sra_name + '/1')

    def _sra_to_fastq(self, scratch_sra_file_path, params):
        """
        _sra_to_fastq: convert SRA file to FASTQ file(s)
        """

        tmp_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        handler_utils._mkdir_p(tmp_dir)

        command = self.SRA_TOOLKIT_PATH + ' --split-3 -T -O '
        command += tmp_dir + ' ' + scratch_sra_file_path

        self._run_command(command)

        sra_name = os.path.basename(scratch_sra_file_path).partition('.')[0]
        paired_end = self._check_fastq_dump_result(tmp_dir, sra_name)

        if paired_end:
            self._validate_paired_end_advanced_params(params)
            fwd_file = os.path.join(tmp_dir, sra_name, '1', 'fastq')
            os.rename(fwd_file, fwd_file + '.fastq')
            fwd_file = fwd_file + '.fastq'

            rev_file = os.path.join(tmp_dir, sra_name, '2', 'fastq')
            os.rename(rev_file, rev_file + '.fastq')
            rev_file = rev_file + '.fastq'
        else:
            self._validate_single_end_advanced_params(params)
            fwd_file = os.path.join(tmp_dir, sra_name, 'fastq')
            os.rename(fwd_file, fwd_file + '.fastq')
            fwd_file = fwd_file + '.fastq'
            rev_file = None

        fastq_file_path = {
            'fwd_file': fwd_file,
            'rev_file': rev_file
        }
        return fastq_file_path

    def _validate_single_end_advanced_params(self, params):
        """
        _validate_single_end_advanced_params: validate advanced params for single end reads
        """
        if (params.get('insert_size_mean')
           or params.get('insert_size_std_dev')
           or params.get('read_orientation_outward')):
            error_msg = 'Advanced params "Mean Insert Size", "St. Dev. of Insert Size" or '
            error_msg += '"Reads Orientation Outward" is Paried End Reads specific'
            raise ValueError(error_msg)

        if 'interleaved' in params:
            del params['interleaved']

    def _validate_paired_end_advanced_params(self, params):
        """
        _validate_paired_end_advanced_params: validate advanced params for paired end reads

        """
        sequencing_tech = params.get('sequencing_tech')

        if sequencing_tech in ['PacBio CCS', 'PacBio CLR']:
            error_msg = 'Sequencing Technology: "PacBio CCS" or "PacBio CLR" '
            error_msg += 'is Single End Reads specific'
            raise ValueError(error_msg)

    def _validate_upload_staging_file_availability(self, staging_file_subdir_path):
        """
        _validate_upload_file_path_availability: validates file availability in user's staging area

        """
        pass
        # TODO ftp_server needs to be fixed for subdir
        # list = ftp_service(self.callback_url).list_files()
        # if staging_file_subdir_path not in list:
        #     error_msg = 'Target file: {} is NOT available.\n'.format(
        #                                         staging_file_subdir_path.rpartition('/')[-1])
        #     error_msg += 'Available files:\n {}'.format("\n".join(list))
        #     raise ValueError(error_msg)

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = os.path.join(config['scratch'], 'import_SRA_' + str(uuid.uuid4()))
        handler_utils._mkdir_p(self.scratch)
        self.dfu = DataFileUtil(self.callback_url)
        self.ru = ReadsUtils(self.callback_url)

    def import_sra_from_staging(self, params):
        '''
          import_sra_from_staging: wrapper method for GenomeFileUtil.genbank_to_genome

          required params:
          staging_file_subdir_path: subdirectory file path
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name
          sequencing_tech: sequencing technology
          name: output reads file name
          workspace_name: workspace name/ID of the object

          Optional Params:
          single_genome: whether the reads are from a single genome or a metagenome.
          insert_size_mean: mean (average) insert length
          insert_size_std_dev: standard deviation of insert lengths
          read_orientation_outward: whether reads in a pair point outward

          return:
          obj_ref: return object reference
        '''

        log('--->\nrunning ImportSRAUtil.import_sra_from_staging\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_import_sra_from_staging_params(params)

        download_staging_file_params = {
            'staging_file_subdir_path': params.get('staging_file_subdir_path')
        }
        scratch_sra_file_path = self.dfu.download_staging_file(
                        download_staging_file_params).get('copy_file_path')
        log('Downloaded staging file to: {}'.format(scratch_sra_file_path))

        fastq_file_path = self._sra_to_fastq(scratch_sra_file_path, params)

        import_sra_reads_params = params
        import_sra_reads_params.update(fastq_file_path)

        workspace_name_or_id = params.get('workspace_name')
        if str(workspace_name_or_id).isdigit():
            import_sra_reads_params['wsid'] = int(workspace_name_or_id)
        else:
            import_sra_reads_params['wsname'] = str(workspace_name_or_id)

        log('--->\nrunning ReadsUtils.upload_reads\nparams:\n{}'.format(
                                        json.dumps(import_sra_reads_params, indent=1)))
        returnVal = self.ru.upload_reads(import_sra_reads_params)

        return returnVal

    def import_sra_from_web(self, params):
        '''
        import_sra_from_web: wrapper method for GenomeFileUtil.genbank_to_genome

        required params:
        download_type: download type for web source fastq file
                       ('Direct Download', 'FTP', 'DropBox', 'Google Drive')
        workspace_name: workspace name/ID of the object

        sra_urls_to_add: dict of SRA file URLs
            required params:
            file_url: SRA file URL
            sequencing_tech: sequencing technology
            name: output reads file name

            Optional Params:
            single_genome: whether the reads are from a single genome or a metagenome.
            insert_size_mean: mean (average) insert length
            insert_size_std_dev: standard deviation of insert lengths
            read_orientation_outward: whether reads in a pair point outward

        return:
        obj_ref: return object reference
        '''

        log('--->\nrunning ImportSRAUtil.import_sra_from_web\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self.validate_import_sra_from_web_params(params)

        download_type = params.get('download_type')
        workspace_name = params.get('workspace_name')
        obj_refs = []

        for sra_url_to_add in params.get('sra_urls_to_add'):
            download_web_file_params = {
                'download_type': download_type,
                'file_url': sra_url_to_add.get('file_url')
            }
            scratch_sra_file_path = self.dfu.download_web_file(
                        download_web_file_params).get('copy_file_path')
            log('Downloaded web file to: {}'.format(scratch_sra_file_path))

            fastq_file_path = self._sra_to_fastq(scratch_sra_file_path, sra_url_to_add)

            import_sra_reads_params = sra_url_to_add
            import_sra_reads_params.update(fastq_file_path)

            workspace_name_or_id = workspace_name
            if str(workspace_name_or_id).isdigit():
                import_sra_reads_params['wsid'] = int(workspace_name_or_id)
            else:
                import_sra_reads_params['wsname'] = str(workspace_name_or_id)

            log('--->\nrunning ReadsUtils.upload_reads\nparams:\n{}'.format(
                                            json.dumps(import_sra_reads_params, indent=1)))
            obj_ref = self.ru.upload_reads(import_sra_reads_params).get('obj_ref')
            obj_refs.append(obj_ref)

        return {'obj_refs': obj_refs}

    def validate_import_sra_from_staging_params(self, params):
        """
        validate_import_genbank_from_staging_params:
                    validates params passed to import_genbank_from_staging method
        """
        # check for required parameters
        for p in ['staging_file_subdir_path', 'sequencing_tech', 'name', 'workspace_name']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')

        self._validate_upload_staging_file_availability(params.get('staging_file_subdir_path'))

    def validate_import_sra_from_web_params(self, params):
        """
        validate_import_genbank_from_staging_params:
                    validates params passed to import_genbank_from_staging method

        """
        # check for required parameters
        for p in ['download_type', 'workspace_name', 'sra_urls_to_add']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        if not isinstance(params.get('sra_urls_to_add'), list):
            raise ValueError('sra_urls_to_add is not type list as required')

        for sra_url_to_add in params.get('sra_urls_to_add'):
            for p in ['file_url', 'sequencing_tech', 'name']:
                if p not in sra_url_to_add:
                    raise ValueError('"{}" parameter is required, but missing'.format(p))

    def generate_html_report(self, reads_objs, params, uuid_string):
        """
        _generate_html_report: generate html summary report
        """
        log('start generating html report')

        result_file_path = os.path.join(self.scratch, 'report.html')
        html_report = list()
        objects_content = ''

        for index, reads_obj in enumerate(reads_objs):
            idx = str(index)

            reads_data = reads_obj.get('data')[0].get('data')
            reads_info = reads_obj.get('data')[0].get('info')
            reads_ref = str(reads_info[6]) + '/' + str(reads_info[0]) + '/' + str(reads_info[4])
            reads_obj_name = str(reads_info[1])

            objects_content += '<div data-tabpanel="object' + idx + '" class="tabpanel">'
            objects_content += '<div class="tabtoggle" title="Click for more info" href="#" '
            objects_content += 'onclick="toggleTabpanel(\'object' + idx + '\')">' + reads_obj_name + '</div>'
            objects_content += '<div data-tabset="object' + idx + '" class="tabset">'
            objects_content += '<div class="tabs">'
            objects_content += '<button class="tab" data-tab="overview" onclick="openTab(\'object' + idx + \
                               '\',\'overview\')">Overview</button>'
            objects_content += '<button class="tab" data-tab="stats" onclick="openTab(\'object' + idx + \
                               '\', \'stats\')">Stats</button></div>'

            base_percentages = ''
            for key, val in reads_data.get('base_percentages').iteritems():
                base_percentages += '{}({}%) '.format(key, val)

            reads_overview_data = collections.OrderedDict()

            reads_overview_data['Reads Object'] = '{} ({})'.format(reads_obj_name, reads_ref)
            reads_overview_data['Number of Reads'] = '{:,}'.format(reads_data.get('read_count'))

            reads_type = reads_info[2].lower()
            if 'single' in reads_type:
                reads_overview_data['Type'] = 'Single End'
            elif 'paired' in reads_type:
                reads_overview_data['Type'] = 'Paired End'
            else:
                reads_overview_data['Type'] = 'Unknown'

            reads_overview_data['Platform'] = reads_data.get('sequencing_tech', 'Unknown')

            reads_single_genome = str(reads_data.get('single_genome', 'Unknown'))
            if '0' in reads_single_genome:
                reads_overview_data['Single Genome'] = 'No'
            elif '1' in reads_single_genome:
                reads_overview_data['Single Genome'] = 'Yes'
            else:
                reads_overview_data['Single Genome'] = 'Unknown'

            insert_size_mean = params.get('insert_size_mean', 'Not Specified')
            if insert_size_mean is not None:
                reads_overview_data['Insert Size Mean'] = str(insert_size_mean)
            else:
                reads_overview_data['Insert Size Mean'] = 'Not Specified'

            insert_size_std_dev = params.get('insert_size_std_dev', 'Not Specified')
            if insert_size_std_dev is not None:
                reads_overview_data['Insert Size Std Dev'] = str(insert_size_std_dev)
            else:
                reads_overview_data['Insert Size Std Dev'] = 'Not Specified'

            reads_outward_orientation = str(reads_data.get('read_orientation_outward', 'Unknown'))
            if '0' in reads_outward_orientation:
                reads_overview_data['Outward Read Orientation'] = 'No'
            elif '1' in reads_outward_orientation:
                reads_overview_data['Outward Read Orientation'] = 'Yes'
            else:
                reads_overview_data['Outward Read Orientation'] = 'Unknown'

            reads_stats_data = collections.OrderedDict()

            reads_stats_data['Number of Reads'] = '{:,}'.format(reads_data.get('read_count'))
            reads_stats_data['Total Number of Bases'] = '{:,}'.format(reads_data.get('total_bases'))
            reads_stats_data['Mean Read Length'] = str(reads_data.get('read_length_mean'))
            reads_stats_data['Read Length Std Dev'] = str(reads_data.get('read_length_stdev'))
            dup_reads_percent = '{:.2f}'.format(float(reads_data.get('number_of_duplicates') * 100) / \
                                                reads_data.get('read_count'))
            reads_stats_data['Number of Duplicate Reads(%)'] = '{} ({}%)' \
                .format(str(reads_data.get('number_of_duplicates')),
                        dup_reads_percent)
            reads_stats_data['Phred Type'] = str(reads_data.get('phred_type'))
            reads_stats_data['Quality Score Mean'] = str(reads_data.get('qual_mean'))
            reads_stats_data['Quality Score (Min/Max)'] = '{}/{}'.format(str(reads_data.get('qual_min')),
                                                                         str(reads_data.get('qual_max')))
            reads_stats_data['GC Percentage'] = str(round(reads_data.get('gc_content') * 100, 2)) + '%'
            reads_stats_data['Base Percentages'] = base_percentages

            objects_content += '<div data-tabpane="overview" class="tabcontent"><br/><table>'

            for key, val in reads_overview_data.iteritems():
                objects_content += '<tr><td><b>{}</b></td>'.format(key)
                objects_content += '<td>{}</td>'.format(val)
                objects_content += '</tr>'

            objects_content += '</table></div>'
            objects_content += '<div data-tabpane="stats" class="tabcontent"><br/><table><br/><table>'

            for key, val in reads_stats_data.iteritems():
                objects_content += '<tr><td><b>{}</b></td>'.format(key)
                objects_content += '<td>{}</td>'.format(val)
                objects_content += '</tr>'

            objects_content += '</table></div></div></div>'

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'multi_obj_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>OBJECTS_DATA_TO_FILL</p>',
                                                          objects_content)
                result_file.write(report_template)
        result_file.close()

        matched_files = []
        for root, dirnames, filenames in os.walk(self.scratch):
            for filename in fnmatch.filter(filenames, '*.gz'):
                matched_files.append(os.path.join(root, filename))

        for gz_file in matched_files:
            print('Removing ' + gz_file)
            os.remove(gz_file)

        report_shock_id = self.dfu.file_to_shock({'file_path': self.scratch,
                                                  'pack': 'zip'})['shock_id']
        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for Imported Assembly'})
        return html_report


    def generate_report(self, obj_refs_list, params):
        """
        generate_report: generate summary report

        obj_refs: generated workspace object references. (return of import_sra_from_staging/web)
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

        if isinstance(obj_refs_list, list):
            obj_refs = obj_refs_list
        else:
            obj_refs = [obj_refs_list]

        objects_created = list()
        objects_data = list()

        for obj_ref in obj_refs:
            get_objects_params = {
                'object_refs': [obj_ref],
                'ignore_errors': False
            }
            objects_data.append(self.dfu.get_objects(get_objects_params))

            objects_created.append({'ref': obj_ref,
                                    'description': 'Imported Reads'})

        output_html_files = self.generate_html_report_NEW(objects_data, params, uuid_string)

        report_params = {
            'message': '',
            'workspace_name': params.get('workspace_name'),
            'objects_created': objects_created,
            'html_links': output_html_files,
            'direct_html_link_index': 0,
            'html_window_height': 333,
            'report_object_name': 'kb_upload_mothods_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output
