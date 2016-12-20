import os
from pprint import pprint
import subprocess
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from ftp_service.ftp_serviceClient import ftp_service

def log(message):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(message)

class FastqUploaderUtil:

    def __init__(self, config):
    	log('--->\nInitializing FastqUploaderUtil instance:\n config:')
        log(config)
        self.scratch = config['scratch']
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.token_user = self.token.split('client_id=')[1].split('|')[0]

    def upload_fastq_file(self, params):
    	log('--->\nrunning upload_fastq_file:\nparams:\n')

    	fs = ftp_service(self.callback_url)
    	list = fs.list_files()
    	print 'xxxxxxxxxxxxxxxxxxx'
    	print list
    	print 'xxxxxxxxxxxxxxxxxxx'

    	self.validate_upload_fastq_file_parameters(params)

    	output_file = os.path.join(self.scratch, params['reads_file_name'] + '.fq')
    	log("--->\nOutput Reads File: \n %s" % output_file)


    	ru = ReadsUtils(self.callback_url)

    	upload_params = {
    		'fwd_file': output_file,
    		'name': params['reads_file_name']
    	}

    	cmd = ''
    	cmd += 'curl -H "Authorization: '
    	cmd += self.token
    	cmd += '" '
    	cmd += 'https://ci.kbase.us/services/kb-ftp-api/v0/list/tgu2/'

    	
    	#data/bulk/tgu2/interleaved.fastq
    	# cmd = 'find -name "interleaved.fastq"'
    	# self.scratch = '/data/bulk/tgu2'
    	# cmd = 'ls'
        log('    ' + ''.join(cmd))

    	p = subprocess.Popen(cmd, cwd=self.scratch, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    	report = ''
        while True:
            line = p.stdout.readline()
            if not line:
                break
            report += line
            log(line.replace('\n', ''))

        p.stdout.close()
        p.wait()
        report += "\n\n"
       	log('process return code: ' + str(p.returncode))
        if p.returncode != 0:
            raise ValueError('Error running upload_fastq_file, return code: ' +
                             str(p.returncode) + '\n')
        print report
        print 'xxxxxxxxxxxxxxxxxxx'

    	# ru_return = ru.upload_reads(upload_params)
    	# print ru_return

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
        #                             params['output_worksspace'],
        #                             input_file_info,
        #                             report)
    	returnVal = {'first_fastq_file_name': 'test'}
        # return the results
        return returnVal

    # def _get_file_path(self, token_user, file_name):


    def validate_upload_fastq_file_parameters(self, params):
        # check for required parameters
        # for p in ['input_reads', 'output_workspace', 'output_object_name']:
        #     if p not in params:
        #         raise ValueError('"' + p + '" parameter is required, but missing')

        # if 'five_prime' in params:
        #     if 'adapter_sequence_5P' not in params['five_prime']:
        #         raise ValueError('"five_prime.adapter_sequence_5P" was not defined')
        #     if 'anchored_5P' in params['five_prime']:
        #         if params['five_prime']['anchored_5P'] not in [0, 1]:
        #             raise ValueError('"five_prime.anchored_5P" must be either 0 or 1')

        # if 'three_prime' in params:
        #     if 'adapter_sequence_3P' not in params['three_prime']:
        #         raise ValueError('"three_prime.adapter_sequence_3P" was not defined')
        #     if 'anchored_3P' in params['three_prime']:
        #         if params['three_prime']['anchored_3P'] not in [0, 1]:
        #             raise ValueError('"three_prime.anchored_3P" must be either 0 or 1')
        self._validate_upload_file_availability(params["first_fastq_file_name"])
        # self._validate_upload_file_availability('as')

    def _validate_upload_file_availability(self, upload_file_name):
    	list = ftp_service(self.callback_url).list_files() #get available file list in user's staging area
    	if upload_file_name not in list:
    		raise ValueError("Target file: %s is NOT available. Available files: %s" % (upload_file_name, ",".join(list)))

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