import os
import time
import uuid
import json
import magic
import shutil

from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport

def log(message, prefix_newline=False):
  """Logging function, provides a hook to suppress or redirect log messages."""
  print(('\n' if prefix_newline else '') + 
    '{0:.2f}'.format(time.time()) + ': ' + str(message))

class UnpackFileUtil:

  def _file_to_staging(self, file_path_list, subdir_folder=None):
    """
    _file_to_staging: upload file(s) to staging area
    """
    subdir_folder_str = '' if not subdir_folder else '/{}'.format(subdir_folder)
    for file_path in file_path_list:
      log ("uploading [{}] to staging area".format(file_path))
      post_cmd = 'curl -H "Authorization: {}"\\\n'.format(self.token)
      post_cmd += ' -X POST\\\n'
      post_cmd += ' -F "destPath=/{}{}"\\\n'.format(self.user_id, subdir_folder_str)
      post_cmd += ' -F "uploads=@{}"\\\n'.format(file_path)
      post_cmd += ' https://ci.kbase.us/services/kb-ftp-api/v0/upload'
      return_code = os.popen(post_cmd).read()
      log ("return message from server:\n{}".format(return_code))

  def _remove_irrelevant_files(self, file_path):
    """
    _remove_irrelevant_files: remove irrelevant files
    """
    target_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    for dirpath, dirnames, filenames in os.walk(file_dir):
      for filename in filenames:
        if filename != target_name:
          irrelevant_file_path = os.sep.join([dirpath, filename])
          os.remove(irrelevant_file_path)
          log('removing irrelevant file: {}'.format(irrelevant_file_path))

  def _r_unpack(self, file_path, count):
    """
    _r_unpack: recursively unpack file_path
    """
    if count == 0:
      self._remove_irrelevant_files(file_path)

    count += 1
    if os.path.isfile(file_path):
      log('processing:      {}{}'.format('-' * count, file_path))
      t = magic.from_file(file_path, mime=True)

      if os.path.basename(file_path).endswith('.DS_Store'):
        os.remove(file_path)
        log('removing file:   {}{}'.format('-' * count, file_path))
      elif t in ['application/' + x for x in 
        'x-gzip', 'gzip', 'x-bzip', 'x-bzip2', 'bzip', 'bzip2',
        'x-tar', 'tar', 'x-gtar', 'zip', 'x-zip-compressed']:
        file_dir = os.path.dirname(file_path)
        files_before_unpack = os.listdir(file_dir)
        self.dfu.unpack_file({'file_path':file_path}).get('file_path')
        files_after_unpack = os.listdir(file_dir)
        new_files = [item for item in files_after_unpack 
                      if item not in files_before_unpack]
        for new_file in new_files:
          self._r_unpack(os.sep.join([file_dir, new_file]), count)
        os.remove(file_path)
        log('removing file:   {}{}'.format('-' * count, file_path))
      else:
        return file_path
    else:
      if os.path.basename(file_path).startswith('_'):
        shutil.rmtree(file_path, ignore_errors=True)
        log('removing folder: {}{}'.format('-' * count, file_path))
      else:
        for dirpath, dirnames, filenames in os.walk(file_path):
          for filename in filenames: 
            self._r_unpack(os.sep.join([dirpath, filename]), count)

  def __init__(self, config):
    self.callback_url = config['SDK_CALLBACK_URL']
    self.token = config['KB_AUTH_TOKEN']
    self.user_id = config['USER_ID']
    self.scratch = config['scratch']
    self.dfu = DataFileUtil(self.callback_url)

  def unpack_staging_file(self, params):
    """
    Unpack a staging area file

    params:
    staging_file_subdir_path: subdirectory file path 
      e.g.
            for file: /data/bulk/user_name/file_name 
            staging_file_subdir_path is file_name 
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name

    result:
    unpacked_file_path: unpacked file path(s) in staging area

    """

    log('--->\nrunning UnpackFileUtil.unpack_staging_file\n' +
       'params:\n{}'.format(json.dumps(params, indent=1)))

    scratch_file_path = self.dfu.download_staging_file(params).get(
                                                        'copy_file_path')

    self._r_unpack(scratch_file_path, 0)
    unpacked_file_path_list = []
    for dirpath, dirnames, filenames in os.walk(
                      os.path.dirname(scratch_file_path)):
      for filename in filenames:
        unpacked_file_path_list.append(
                      os.sep.join([dirpath, filename]))

    log ("Unpacked files:\n  {}".format(
                      '\n  '.join(unpacked_file_path_list)))

    self._file_to_staging(unpacked_file_path_list, os.path.dirname(
                                  params.get('staging_file_subdir_path')))
    unpacked_file_path = ','.join(unpacked_file_path_list)
    returnVal = {'unpacked_file_path': unpacked_file_path}
    
    return returnVal

  def unpack_web_file(self, params):
    """
    Download and unpack a web file to staging area

    params:
    file_url: file URL
    download_type: one of ['Direct Download', 'FTP', 
                'DropBox', 'Google Drive']

        result:
        unpacked_file_path: unpacked file path(s) in staging area

    """
    log('--->\nrunning UnpackFileUtil.unpack_web_file\n' +
       'params:\n{}'.format(json.dumps(params, indent=1)))

    scratch_file_path = self.dfu.download_web_file(params).get(
                                                        'copy_file_path')

    self._r_unpack(scratch_file_path, 0)
    unpacked_file_path_list = []
    for dirpath, dirnames, filenames in os.walk(
                      os.path.dirname(scratch_file_path)):
      for filename in filenames:
        unpacked_file_path_list.append(
                      os.sep.join([dirpath, filename]))

    log ("Unpacked files:\n  {}".format(
                      '\n  '.join(unpacked_file_path_list)))

    self._file_to_staging(unpacked_file_path_list)
    unpacked_file_path = ','.join(unpacked_file_path_list)
    returnVal = {'unpacked_file_path': unpacked_file_path}
    
    return returnVal

  def generate_report(self, unpacked_file_path, params):
    """
    generate_report: generate summary report

    unpacked_file_path: generated unpacked file path(s) in staging area. 
              (return of unpack_staging_file or unpack_web_file)

    """

    log ("generating report")
    uuid_string = str(uuid.uuid4())
    unpacked_file_path_list= unpacked_file_path.split(',')

    subdir = os.path.dirname(
                  params.get('staging_file_subdir_path')) + '/' if params.get(
                                            'staging_file_subdir_path') else '/'

    upload_message = 'Uploaded Files: {}\n'.format(
                                        len(unpacked_file_path_list))
    for file_path in unpacked_file_path_list:
      upload_message += subdir + os.path.basename(file_path) + '\n'

    report_params = { 
          'message': upload_message,
          'workspace_name' : params.get('workspace_name'),
          'report_object_name' : 'kb_upload_mothods_report_' + uuid_string}

    kbase_report_client = KBaseReport(self.callback_url, token=self.token)
    output = kbase_report_client.create_extended_report(report_params)

    report_output = {'report_name': output['name'], 
                      'report_ref': output['ref']}

    return report_output



