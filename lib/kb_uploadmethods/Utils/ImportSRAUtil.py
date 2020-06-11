
import collections
import fnmatch
import json
import os
import re
import shutil
import subprocess
import time
import uuid

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.ReadsUtilsClient import ReadsUtils
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from . import handler_utils


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print((('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message)))


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
            log('Executed command:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running command:\n{}\n'.format(command)
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

        # PTV-1356 fix:  to try to make handing of output files from fastq-dump
        # more uniform for cases where there is an SRA extension or not

        # force an .sra extension if there isn't one already:

        if not re.match( ".*\.sra$", scratch_sra_file_path, re.IGNORECASE ):
            new_scratch_sra_file_path = scratch_sra_file_path + ".sra"
            os.symlink( scratch_sra_file_path, new_scratch_sra_file_path );
            log( "**** after symlink contents of . ****" )
            log( os.listdir() )
            scratch_sra_file_path = new_scratch_sra_file_path

        command = self.SRA_TOOLKIT_PATH + ' --split-3 -T -O '
        command += tmp_dir + ' ' + scratch_sra_file_path

        self._run_command(command)

        # next, remove the .sra extention to mimic what fastq-dump does

        sra_name = os.path.splitext( os.path.basename( scratch_sra_file_path ) )[0]
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
        self.uploader_utils = UploaderUtil(config)

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

        """
        Update the workspace object related meta-data for staged file
        """
        self.uploader_utils.update_staging_service(params.get('staging_file_subdir_path'),
                                                   returnVal['obj_ref'])
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
        uploaded_files = []

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
            uploaded_files.append(sra_url_to_add.get('file_url'))

        return {'obj_refs': obj_refs, 'uploaded_files': uploaded_files}

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

        objects_created = list()
        objects_data = list()

        for obj_ref in obj_refs_list:
            get_objects_params = {
                'object_refs': [obj_ref],
                'ignore_errors': False
            }
            objects_data.append(self.dfu.get_objects(get_objects_params))

            objects_created.append({'ref': obj_ref,
                                    'description': 'Imported Reads'})

        output_html_files = self.generate_html_report(objects_data, params, uuid_string)

        report_params = {
            'message': '',
            'workspace_name': params.get('workspace_name'),
            'objects_created': objects_created,
            'html_links': output_html_files,
            'direct_html_link_index': 0,
            'html_window_height': 460,
            'report_object_name': 'kb_sra_upload_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def generate_html_report(self, reads_objs, params, uuid_string):
        """
        _generate_html_report: generate html summary report
        """
        log('Start generating html report')

        tmp_dir = os.path.join(self.scratch, uuid_string)
        handler_utils._mkdir_p(tmp_dir)
        result_file_path = os.path.join(tmp_dir, 'report.html')
        html_report = list()
        objects_content = ''

        for index, reads_obj in enumerate(reads_objs):

            idx = str(index)
            reads_data = reads_obj.get('data')[0].get('data')
            reads_info = reads_obj.get('data')[0].get('info')
            reads_ref = str(reads_info[6]) + '/' + str(reads_info[0]) + '/' + str(reads_info[4])
            reads_obj_name = str(reads_info[1])

            with open(os.path.join(os.path.dirname(__file__), 'report_template_sra/table_panel.html'),
                      'r') as object_content_file:
                report_template = object_content_file.read()
                report_template = report_template.replace('_NUM', str(idx))
                report_template = report_template.replace('OBJECT_NAME', reads_obj_name)
                if index == 0:
                    report_template = report_template.replace('panel-collapse collapse', 'panel-collapse collapse in')

            objects_content += report_template
            base_percentages = ''
            for key, val in reads_data.get('base_percentages').items():
                base_percentages += '{}({}%) '.format(key, val)

            reads_overview_data = collections.OrderedDict()

            reads_overview_data['Name'] = '{} ({})'.format(reads_obj_name, reads_ref)
            reads_overview_data['Uploaded File'] = params.get('uploaded_files')[index]
            reads_overview_data['Date Uploaded'] = time.strftime("%c")
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
            reads_stats_data['Quality Score Mean'] = '{0:.2f}'.format(reads_data.get('qual_mean'))
            reads_stats_data['Quality Score (Min/Max)'] = '{}/{}'.format(str(reads_data.get('qual_min')),
                                                                         str(reads_data.get('qual_max')))
            reads_stats_data['GC Percentage'] = str(round(reads_data.get('gc_content') * 100, 2)) + '%'
            reads_stats_data['Base Percentages'] = base_percentages

            overview_content = ''
            for key, val in reads_overview_data.items():
                overview_content += '<tr><td><b>{}</b></td>'.format(key)
                overview_content += '<td>{}</td>'.format(val)
                overview_content += '</tr>'

            stats_content = ''
            for key, val in reads_stats_data.items():
                stats_content += '<tr><td><b>{}</b></td>'.format(key)
                stats_content += '<td>{}</td>'.format(val)
                stats_content += '</tr>'

            objects_content = objects_content.replace('###OVERVIEW_CONTENT###', overview_content)
            objects_content = objects_content.replace('###STATS_CONTENT###', stats_content)

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template_sra/report_head.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('###TABLE_PANELS_CONTENT###',
                                                          objects_content)
                result_file.write(report_template)
        result_file.close()

        shutil.copytree(os.path.join(os.path.dirname(__file__), 'report_template_sra/bootstrap-3.3.7'),
                        os.path.join(tmp_dir, 'bootstrap-3.3.7'))
        shutil.copy(os.path.join(os.path.dirname(__file__), 'report_template_sra/jquery-3.2.1.min.js'),
                    os.path.join(tmp_dir, 'jquery-3.2.1.min.js'))

        matched_files = []
        for root, dirnames, filenames in os.walk(tmp_dir):
            for filename in fnmatch.filter(filenames, '*.gz'):
                matched_files.append(os.path.join(root, filename))

        for gz_file in matched_files:
            print(('Removing ' + gz_file))
            os.remove(gz_file)

        report_shock_id = self.dfu.file_to_shock({'file_path': tmp_dir,
                                                  'pack': 'zip'})['shock_id']
        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for Imported Assembly'})
        return html_report
