import os
from pprint import pprint
import subprocess
import shutil
import urllib2
from contextlib import closing
import ftplib
import re
from ReadsUtils.ReadsUtilsClient import ReadsUtils
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
		log(params)

		self.validate_upload_fastq_file_parameters(params)

		if 'second_fastq_file_name' in params:
			pass
		elif 'first_fastq_file_name' in params:
			returnVal = self._upload_file_path(
							file_name=params.get('first_fastq_file_name'), 
							sequencing_tech=params.get('sequencing_tech'),
							output_file_name=params['reads_file_name'],
							workspace_name_or_id=params['workspace_name'])
		
		if 'second_fastq_file_url' in params:
			pass
		elif 'first_fastq_file_url' in params:
			returnVal = self._upload_file_url(
							download_type=params.get('download_type'),
							file_url=params.get('first_fastq_file_url'), 
							sequencing_tech=params.get('sequencing_tech'),
							output_file_name=params['reads_file_name'],
							workspace_name_or_id=params['workspace_name'])

		return returnVal

	def validate_upload_fastq_file_parameters(self, params):

		# check for required parameters
		for p in ['reads_file_name', 'workspace_name']:
			if p not in params:
				raise ValueError('"' + p + '" parameter is required, but missing')	

		# check for invalidate both file path and file URL parameters
		upload_file_path = False
		upload_file_URL = False

		if 'first_fastq_file_name' in params or 'second_fastq_file_name' in params:
			upload_file_path = True

		if 'first_fastq_file_url' in params or 'second_fastq_file_url' in params:
			upload_file_URL = True

		if upload_file_path and upload_file_URL:
			raise ValueError('Cannot upload Reads for both file path and file URL')	

		# check for file path parameters
		if 'second_fastq_file_name' in params:
			self._validate_upload_file_path_availability(params["second_fastq_file_name"])
		elif 'first_fastq_file_name' in params:
			self._validate_upload_file_path_availability(params["first_fastq_file_name"])
		
		# check for file URL parameters
		if 'first_fastq_file_url' in params:
			self._validate_upload_file_URL_availability(params)

	def _validate_upload_file_path_availability(self, upload_file_name):
		list = ftp_service(self.callback_url).list_files() #get available file list in user's staging area
		if upload_file_name not in list:
			raise ValueError("Target file: %s is NOT available. Available files: %s" % (upload_file_name, ",".join(list)))

	def _validate_upload_file_URL_availability(self, params):
		if 'download_type' not in params:
			raise ValueError("Download type parameter is required, but missing")

		if 'second_fastq_file_url' in params:
			first_url_prefix = params['first_fastq_file_url'][:5].lower()
			second_url_prefix = params['second_fastq_file_url'][:5].lower()
		elif 'first_fastq_file_url' in params:
			url_prefix = params['first_fastq_file_url'][:5].lower()

		if 'second_fastq_file_url' in params:
			if params['download_type'] == 'Direct Download' and (first_url_prefix[:4] != 'http' or second_url_prefix[:4] != 'http'):
				raise ValueError("Download type and URL prefix do NOT match")
			elif params['download_type'] in ['DropBox', 'Google Drive']  and (first_url_prefix != 'https' or second_url_prefix != 'https'):
				raise ValueError("Download type and URL prefix do NOT match")
			elif params['download_type'] == 'FTP':
				if first_url_prefix[:3] != 'ftp' or second_url_prefix[:3] != 'ftp':
					raise ValueError("Download type and URL prefix do NOT match")
				else:
					first_ftp_url_format = re.match(r'ftp://.*:.*@.*/.*', params['first_fastq_file_url'])
					second_ftp_url_format = re.match(r'ftp://.*:.*@.*/.*', params['second_fastq_file_url'])
					if not first_ftp_url_format:
						raise ValueError("FTP Link: %s does NOT match format: 'ftp://user_name:password@domain/file_path'" % params['first_fastq_file_url'])
					if not second_ftp_url_format:
						raise ValueError("FTP Link: %s does NOT match format: 'ftp://user_name:password@domain/file_path'" % params['second_fastq_file_url'])
		elif 'first_fastq_file_url' in params:
			if params['download_type'] == 'Direct Download' and url_prefix[:4] != 'http':
				raise ValueError("Download type and URL prefix do NOT match")
			elif params['download_type'] in ['DropBox', 'Google Drive'] and url_prefix != 'https':
				raise ValueError("Download type and URL prefix do NOT match")
			elif params['download_type'] == 'FTP': 
				if url_prefix[:3] != 'ftp':
					raise ValueError("Download type and URL prefix do NOT match")
				else:
					ftp_url_format = re.match(r'ftp://.*:.*@.*/.*', params['first_fastq_file_url'])
					if not ftp_url_format:
						raise ValueError("FTP Link: %s does NOT match format: 'ftp://user_name:password@domain/file_path'" % params['first_fastq_file_url'])

	def _get_file_path(self, upload_file_name):
		return '/data/bulk/%s/%s' % (self.token_user, upload_file_name)

	def _upload_file_path(self, file_name, sequencing_tech, output_file_name, workspace_name_or_id):
		file_path = self._get_file_path(file_name)
		log('--->\nstart copying file to local:\n')
		dstdir = os.path.join(self.scratch, 'tmp')
		if not os.path.exists(dstdir):
			os.makedirs(dstdir)
		shutil.copy2(file_path, dstdir)
		copy_file_path = os.path.join(dstdir, file_name)
		log('--->\ncopied file from: %s to: %s\n' % (file_path, copy_file_path))

		upload_file_params = {
			'fwd_file': copy_file_path,
			'sequencing_tech': sequencing_tech,
			'name': output_file_name
		}

		if str(workspace_name_or_id).isdigit():
			upload_file_params['wsid'] = int(workspace_name_or_id)
		else:
			upload_file_params['wsname'] = str(workspace_name_or_id)

		log('--->\nupload_file_params:\n')
		log(upload_file_params)

		ru = ReadsUtils(self.callback_url)
		result = ru.upload_reads(upload_file_params)

		log('--->\nremoving folder: %s' % dstdir)
		shutil.rmtree(dstdir)

		return result

	def _upload_file_url(self, download_type, file_url, sequencing_tech, output_file_name, workspace_name_or_id):

		log('--->\nFile URL:\n')
		log(file_url)
		file_name = 'tmp_fastq.fq'

		# Prepare copy file path
		dstdir = os.path.join(self.scratch, 'tmp')
		if not os.path.exists(dstdir):
			os.makedirs(dstdir)
		copy_file_path = os.path.join(dstdir, file_name)

		if download_type == 'Direct Download':
			try: online_file = urllib2.urlopen(file_url)
			except urllib2.HTTPError as e:
				raise ValueError("The server couldn\'t fulfill the request.\n(Is link publicaly accessable?)\nError code: %s" % e.code)
			except urllib2.URLError as e:
				raise ValueError("Failed to reach a server\nReason: %s" % e.reason)
			else:
				with closing(online_file):
					with open(copy_file_path, 'wb') as output:
						shutil.copyfileobj(online_file, output)
		elif download_type == 'DropBox':
			if "?" not in file_url:
				force_download_link = file_url + '?raw=1'
			else:
				force_download_link = file_url.partition('?')[0] + '?raw=1'

			try: online_file = urllib2.urlopen(force_download_link)
			except urllib2.HTTPError as e:
				raise ValueError("The server couldn\'t fulfill the request.\n(Is link publicaly accessable?)\nError code: %s" % e.code)
			except urllib2.URLError as e:
				raise ValueError("Failed to reach a server\nReason: %s" % e.reason)
			else:
				with closing(online_file):
					with open(copy_file_path, 'wb') as output:
						shutil.copyfileobj(online_file, output)
		elif download_type == 'FTP':
			
			self.ftp_user_name = re.search('ftp://(.+?):', file_url).group(1)
			self.ftp_password = file_url.rpartition('@')[0].rpartition(':')[-1]
			self.ftp_domain = re.search('ftp://.*:.*@(.+?)/', file_url).group(1)
			self.ftp_file_path = file_url.partition('ftp://')[-1].partition('/')[-1].rpartition('/')[0]
			self.ftp_file_name = re.search('ftp://.*:.*@.*/(.+$)', file_url).group(1)

			self._check_ftp_connection(self.ftp_user_name, self.ftp_password, self.ftp_domain, self.ftp_file_path, self.ftp_file_name)
			
			ftp_connection = ftplib.FTP(self.ftp_domain)
			ftp_connection.login(self.ftp_user_name, self.ftp_password)
			ftp_connection.cwd(self.ftp_file_path)

			with open(copy_file_path, 'wb') as output:
				ftp_connection.retrbinary('RETR %s' % self.ftp_file_name, output.write)
		elif download_type == 'Google Drive':
			force_download_link_prefix = 'https://drive.google.com/uc?export=download&id='
			file_id = file_url.partition('/d/')[-1].partition('/')[0]
			force_download_link = force_download_link_prefix + file_id
			try: online_file = urllib2.urlopen(force_download_link)
			except urllib2.HTTPError as e:
				raise ValueError("The server couldn\'t fulfill the request.\n(Is link publicaly accessable?)\nError code: %s" % e.code)
			except urllib2.URLError as e:
				raise ValueError("Failed to reach a server\nReason: %s" % e.reason)
			else:
				with closing(online_file):
					with open(copy_file_path, 'wb') as output:
						shutil.copyfileobj(online_file, output)

		upload_file_params = {
			'fwd_file': copy_file_path,
			'sequencing_tech': sequencing_tech,
			'name': output_file_name
		}

		if str(workspace_name_or_id).isdigit():
			upload_file_params['wsid'] = int(workspace_name_or_id)
		else:
			upload_file_params['wsname'] = str(workspace_name_or_id)

		log('--->\nupload_file_params:\n')
		log(upload_file_params)

		ru = ReadsUtils(self.callback_url)
		result = ru.upload_reads(upload_file_params)

		log('--->\nremoving folder: %s' % dstdir)
		shutil.rmtree(dstdir)

		return result

	def _check_ftp_connection(self, user_name, password, domain, file_path, file_name):

		try: ftp = ftplib.FTP(domain)
		except ftplib.all_errors, error:
			raise ValueError("Cannot connect: %s" % error)
		else:
			try: ftp.login(user_name, password)
			except ftplib.all_errors, error:
				raise ValueError("Cannot login: %s" % error)
			else:
				ftp.cwd(file_path)
				if file_name in ftp.nlst():
					pass
				else:
					raise ValueError("File %s does NOT exist in FTP path: %s" % (file_name, domain + '/' + file_path))


		