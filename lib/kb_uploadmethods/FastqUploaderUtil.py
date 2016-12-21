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

		if 'first_fastq_file_name' in params:
			returnVal = self._upload_file_path(file_name=params.get('first_fastq_file_name'), 
							sequencing_tech='tech1', 
							output_file_name=params['reads_file_name'],
							workspace_name_or_id=params['workspace_name'])

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

	def _get_file_path(self, upload_file_name):
		return '/data/bulktest/%s/%s' % (self.token_user, upload_file_name)

	def _upload_file_path(self, file_name, sequencing_tech, output_file_name, workspace_name_or_id):
		file_path = self._get_file_path(file_name)
		#TODO: test file_path NEED TO DELETE
		#/data/bulk/tgu2/interleaved.fastq
		# file_path = '/kb/module/work/tmp/SP1.fq'
		upload_file_params = {
			'fwd_file': file_path,
			'sequencing_tech': sequencing_tech,
			'name': output_file_name
		}

		if str(workspace_name_or_id).isdigit():
			upload_file_params['wsid'] = int(workspace_name_or_id)
		else:
			upload_file_params['wsname'] = str(workspace_name_or_id)

		log('--->\nupload_file_params:\n')
		pprint (upload_file_params)
		print upload_file_params

		ru = ReadsUtils(self.callback_url)
		result = ru.upload_reads(upload_file_params)

		return result


