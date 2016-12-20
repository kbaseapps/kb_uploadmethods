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

    	self.validate_upload_fastq_file_parameters(params)

    	output_file = os.path.join(self.scratch, params['reads_file_name'] + '.fq')
    	log("--->\nOutput Reads File: \n %s" % output_file)

    	if 'first_fastq_file_name' in params:
    		file_path = self.get_file_path(params.get('first_fastq_file_name'))
    		#TODO: test file_path NEED TO DELETE
    		#/data/bulk/tgu2/interleaved.fastq
    		file_path = '/kb/module/work/tmp/SP1.fq'
    		upload_file_params = {
    			'fwd_file': file_path,
    			'sequencing_tech': 'tech1',
    			'name': params['reads_file_name']
    		}

    		ws_name_or_id = params['workspace_name']
    		if str(ws_name_or_id).isdigit():
    			upload_file_params['wsid'] = int(ws_name_or_id)
        	else:
        		upload_file_params['wsname'] = str(ws_name_or_id)

        	log('--->\nupload_file_params:\n')
        	pprint (upload_file_params)
        	print upload_file_params

        	ru = ReadsUtils(self.callback_url)
        	print 'xxxxxxxxxxxxxxxxxxx'
    		result = ru.upload_reads(upload_file_params)
    		print 'xxxxxxxxxxxxxxxxxxx'
    		print result

    	cmd = ''
    	cmd += 'curl -H "Authorization: '
    	cmd += self.token
    	cmd += '" '
    	cmd += 'https://ci.kbase.us/services/kb-ftp-api/v0/list/tgu2/'

    	cmd = 'pwd'
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
        

        # return the results
        returnVal = {'first_fastq_file_name': 'test'}
        return returnVal

    def validate_upload_fastq_file_parameters(self, params):

    	# check for required parameters
    	for p in ['reads_file_name', 'workspace_name']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')	
                
    	# check for file path parameters
    	if 'first_fastq_file_name' in params:
    		self._validate_upload_file_path_availability(params["first_fastq_file_name"])

    	# check for file URL parameters
    	if 'first_fastq_file_url' in params:
    		self._validate_upload_file_URL_availability(params["first_fastq_file_url"])

    def _validate_upload_file_path_availability(self, upload_file_name):
    	list = ftp_service(self.callback_url).list_files() #get available file list in user's staging area
    	if upload_file_name not in list:
    		raise ValueError("Target file: %s is NOT available. Available files: %s" % (upload_file_name, ",".join(list)))

    def _validate_upload_file_URL_availability(self, upload_file_URL):
    	pass

    def get_file_path(self, upload_file_name):
    	return '/data/bulk/%s/%s' % (self.token_user, upload_file_name)

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