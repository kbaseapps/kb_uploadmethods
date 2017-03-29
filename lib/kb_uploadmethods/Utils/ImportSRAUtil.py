
import json
import uuid
import time
import os
import errno
import subprocess

from DataFileUtil.DataFileUtilClient import DataFileUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ftp_service.ftp_serviceClient import ftp_service
from KBaseReport.KBaseReportClient import KBaseReport


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportSRAUtil:

    SRA_TOOLKIT_PATH = '/kb/deployment/bin/fastq-dump'

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

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
        self._mkdir_p(tmp_dir)

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

        sequencing_tech = params.get('sequencing_tech')

        if sequencing_tech in ['']:
            error_msg = ''
            raise ValueError(error_msg)

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
        self.scratch = config['scratch']

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

    def generate_report(self, obj_ref, params):
        """
        generate_report: generate summary report


        obj_ref: generated workspace object references. (return of import_sra_from_staging)
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
        number_of_reads = object_data.get('data')[0].get('data').get('read_count')

        upload_message += "Reads Name: "
        upload_message += str(object_data.get('data')[0].get('info')[1]) + '\n'
        upload_message += 'Imported Reads File: {}\n'.format(
                              params.get('staging_file_subdir_path'))
        if isinstance(number_of_reads, (int, long)):
            upload_message += 'Number of Reads: {:,}\n'.format(number_of_reads)

        report_params = {
              'message': upload_message,
              'workspace_name': params.get('workspace_name'),
              'report_object_name': 'kb_upload_mothods_report_' + uuid_string}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output
