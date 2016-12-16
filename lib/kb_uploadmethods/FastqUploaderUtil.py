import os
from pprint import pprint
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from ftp_service.ftp_serviceClient import ftp_service

class FastqUploaderUtil:

    def __init__(self, config):
        # pprint(config)
        self.scratch = config['scratch']
        self.callback_url = config['SDK_CALLBACK_URL']

    def upload_fastq_file(self, params):
    	fs = ftp_service(self.callback_url)
    	list = fs.list_files()
    	print 'xxxxxxxxxxxxxxxxxxx'
    	print list
    	print 'xxxxxxxxxxxxxxxxxxx'

    	# self.validate_upload_fastq_file_parameters(params)

    	output_file = os.path.join(self.scratch, params['output_object_name'] + '.fq')

    	# if params.get('second_fastq_file_name'):
     #        returnVal = _upload_paired_end_reads_from_file(params)
     #    elif params.get('first_fastq_file_name'):
     #        returnVal = _upload_single_end_reads_from_file(params)

        # ca = CutadaptRunner(self.scratch)
        # input_file_info = self._stage_input_file(ca, params['input_reads'])
        # output_file = os.path.join(self.scratch, params['output_object_name'] + '.fq')
        # ca.set_output_file(output_file)
        # self._build_run(ca, params)
        # report = ca.run()

        # return self._package_result(output_file,
        #                             params['output_object_name'],
        #                             params['output_workspace'],
        #                             input_file_info,
        #                             report)
    	returnVal = {'first_fastq_file_name': 'test'}
        # return the results
        return returnVal

    def validate_remove_adapters_parameters(self, params):
        # check for required parameters
        for p in ['input_reads', 'output_workspace', 'output_object_name']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')

        if 'five_prime' in params:
            if 'adapter_sequence_5P' not in params['five_prime']:
                raise ValueError('"five_prime.adapter_sequence_5P" was not defined')
            if 'anchored_5P' in params['five_prime']:
                if params['five_prime']['anchored_5P'] not in [0, 1]:
                    raise ValueError('"five_prime.anchored_5P" must be either 0 or 1')

        if 'three_prime' in params:
            if 'adapter_sequence_3P' not in params['three_prime']:
                raise ValueError('"three_prime.adapter_sequence_3P" was not defined')
            if 'anchored_3P' in params['three_prime']:
                if params['three_prime']['anchored_3P'] not in [0, 1]:
                    raise ValueError('"three_prime.anchored_3P" must be either 0 or 1')

        # TODO: validate values of error_tolerance and min_overlap_length

    def _upload_single_end_reads_from_file(self, params):

        uploaded_first_file = False
        returnVal = dict([('uploaded_first_file', uploaded_first_file)])

        first_fastq_file_name = params.get('first_fastq_file_name')
        reads_file_name = params.get('reads_file_name')

        ru = ReadsUtils(self.callback_url)
        fs = ftp_service(self.callback_url)
        dfu = DataFileUtil(self.callback_url)

        # return the results
        return returnVal

    def _upload_paired_end_reads_from_file(self, params):

        uploaded_first_file = False
        uploaded_second_file = False
        returnVal = dict([('uploaded_first_file', uploaded_first_file), 
                        ('uploaded_second_file', uploaded_second_file)])

        first_fastq_file_name = params.get('first_fastq_file_name')
        second_file_name = params.get('second_fastq_file_name')
        reads_file_name = params.get('reads_file_name')

        ru = ReadsUtils(self.callback_url)
        fs = ftp_service(self.callback_url)
        dfu = DataFileUtil(self.callback_url)

        # return the results
        return returnVal