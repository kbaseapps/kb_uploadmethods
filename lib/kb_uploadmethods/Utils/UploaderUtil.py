#Standard packages
import json,uuid,time

#KBase packages
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from kb_gffupload.kb_gffuploadClient import kb_gffupload
from ftp_service.ftp_serviceClient import ftp_service
from KBaseReport.KBaseReportClient import KBaseReport
from DataFileUtil.DataFileUtilClient import DataFileUtil

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + 
        '{0:.2f}'.format(time.time()) + ': ' + str(message))

class UploaderUtil:

  def __init__(self, config):
    self.callback_url = config['SDK_CALLBACK_URL']
    self.token = config['KB_AUTH_TOKEN']
    self.scratch = config['scratch']

  def upload_fastq_file(self, params):
    """
    upload_fastq_file: upload single-end fastq file or paired-end fastq files to workspace as read(s)
                       source file can be either from user's staging area or web

    params: 
    fwd_staging_file_name: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
    rev_staging_file_name: reverse/right paired-end fastq file name user's staging area
    sequencing_tech: sequencing technology
    name: output reads file name
    workspace_name: workspace name/ID that reads will be stored to
    download_type: download type for web source fastq file
    fwd_file_url: single-end fastq file URL or forward/left paired-end fastq file URL
    rev_file_url: reverse/right paired-end fastq file URL

    """
    log('--->\nrunning UploaderUtil.upload_fastq_file\n' + 
              'params:\n{}'.format(json.dumps(params, indent=1)))

    self.validate_upload_fastq_file_parameters(params)

    if 'fwd_staging_file_name' in params:
      # process single-end fastq file from user's staging area
      returnVal = self._upload_file_path(params)
    elif 'fwd_file_url' in params:
      # process single-end fastq file URL
      returnVal = self._upload_file_url(params)
    else:
      raise ValueError("Unexpected params: \n{}".format(
                                json.dumps(params, indent=1)))

    return returnVal

  def upload_gff_fasta_file(self, params):
      """
      upload_gff_fasta_file: load gff and fasta to workspace as genome using files from user's staging area
      
      params: 
      fasta_file: fasta file from user's staging area
      gff_file: gff file from user's staging area
      genome_name: output genome object name
      workspace_name: workspace name that genome will be stored to
      """
      log('--->\nrunning UploaderUtil.upload_gff_fasta_file\nparams:\n%s' % json.dumps(params, indent=1))
      
      #Test file availability
#      self._validate_upload_file_path_availability(params["fasta_file"])
#      self._validate_upload_file_path_availability(params["gff_file"])
      
      returnVal = self._load_gff_fasta_file_path(params)
      return returnVal

  def generate_report(self, obj_refs, params):
      """
      generate_report: generate summary report

       
      obj_refs: generated workspace object references. (return of upload_fastq_file)
      params:
      fwd_staging_file_name: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
      rev_staging_file_name: reverse/right paired-end fastq file name user's staging area
      workspace_name: workspace name/ID that reads will be stored to

      """

      uuid_string = str(uuid.uuid4())
      obj_refs_list = obj_refs.split(',')

      dfu = DataFileUtil(self.callback_url)

      reads_number = 1 if 'urls_to_add' not in params else len(params['urls_to_add'])

      upload_message = 'Import Finished\nImported Reads: {}\n'.format(reads_number)

      for obj_ref in obj_refs_list:
        get_objects_params = {
            'object_refs': [obj_ref],
            'ignore_errors': False
        }

        object_data = dfu.get_objects(get_objects_params)
        number_of_reads = object_data.get('data')[0].get('data').get('read_count')
        
        upload_message += "Reads Name: "
        upload_message += str(object_data.get('data')[0].get('info')[1]) + '\n'
        if params.get('fwd_staging_file_name'):
          if params.get('rev_staging_file_name'):
            upload_message += 'Imported Reads Files:\n'
            upload_message += 'Forward: {}\n'.format(
                              params.get('fwd_staging_file_name'))
            upload_message += 'Reverse: {}\n'.format(
                              params.get('rev_staging_file_name'))
          else:
            upload_message += 'Imported Reads File: {}\n'.format(
                              params.get('fwd_staging_file_name'))
          if isinstance(number_of_reads, (int, long)):
            upload_message += 'Number of Reads: {:,}\n'.format(number_of_reads)
        else:
          reads_info = object_data.get('data')[0].get('info')[-1]
          if isinstance(reads_info, dict):
            upload_message += "Reads Info: "
            upload_message += json.dumps(reads_info, indent=1)[1:-1] + '\n'

      report_params = { 
              'message': upload_message,
              'workspace_name' : params.get('workspace_name'),
              'report_object_name' : 'kb_upload_mothods_report_' + uuid_string }

      kbase_report_client = KBaseReport(self.callback_url, token=self.token)
      output = kbase_report_client.create_extended_report(report_params)

      report_output = { 'report_name': output['name'], 
                        'report_ref': output['ref'] }

      return report_output

  def validate_upload_fastq_file_parameters(self, params):
      """
      validate_upload_fastq_file_parameters: validates params passed to upload_fastq_file method

      """

      # check for required parameters
      for p in ['name', 'workspace_name']:
        if p not in params:
          raise ValueError('"' + p + '" parameter is required, but missing')  

      # check for invalidate both file path and file URL parameters
      upload_file_path = False
      upload_file_URL = False

      if params.get('fwd_staging_file_name') or params.get('rev_staging_file_name'):
        upload_file_path = True

      if params.get('fwd_file_url') or params.get('rev_file_url'):
        upload_file_URL = True

      if upload_file_path and upload_file_URL:
        raise ValueError('Cannot upload Reads for both file path and file URL') 

      if (upload_file_path and 
              (params.get('fwd_staging_file_name') == params.get('rev_staging_file_name'))):
        error_msg = 'Same file [{}] is used for forward and reverse. '.format(
                                                      params.get('fwd_staging_file_name'))
        error_msg += 'Please select different files and try again.'
        raise ValueError(error_msg)

      if (upload_file_URL and 
              (params.get('fwd_file_url') == params.get('rev_file_url'))):
        error_msg = 'Same URL\n {}\nis used for forward and reverse. '.format(
                                                      params.get('fwd_file_url'))
        error_msg += 'Please select different files and try again.'
        raise ValueError(error_msg)

      # check for file path parameters
      if params.get('rev_staging_file_name'):
        self._validate_upload_file_path_availability(params["rev_staging_file_name"])
      elif params.get('fwd_staging_file_name'):
        self._validate_upload_file_path_availability(params["fwd_staging_file_name"])
      
      # check for file URL parameters
      if upload_file_URL:
        self._validate_upload_file_URL_availability(params)

  def _validate_upload_file_path_availability(self, upload_file_name):
      """
      _validate_upload_file_path_availability: validates file availability in user's staging area

      """
      list = ftp_service(self.callback_url).list_files() #get available file list in user's staging area
      if upload_file_name.rpartition('/')[-1] not in list:
        error_msg = 'Target file: {} is NOT available. '.format(
                                                upload_file_name.rpartition('/')[-1])
        error_msg += 'Available files: {}'.format(",".join(list))
        raise ValueError(error_msg)

  def _validate_upload_file_URL_availability(self, params):
      """
      _validate_upload_file_URL_availability: validates param URL format/connection 

      """

      if 'download_type' not in params:
        raise ValueError("Download type parameter is required, but missing")

      # parse URL prefix
      if params.get('rev_file_url'):
        first_url_prefix = params['fwd_file_url'][:5].lower()
        second_url_prefix = params['rev_file_url'][:5].lower()
      elif params.get('fwd_file_url') and not params.get('rev_file_url'):
        url_prefix = params['fwd_file_url'][:5].lower()

      # check URL prefix
      if params.get('rev_file_url'):
        if (params['download_type'] == 'Direct Download' 
                and (first_url_prefix[:4] != 'http' or second_url_prefix[:4] != 'http')):
          raise ValueError("Download type and URL prefix do NOT match")
        elif (params['download_type'] in ['DropBox', 'Google Drive']  
                and (first_url_prefix != 'https' or second_url_prefix != 'https')):
          raise ValueError("Download type and URL prefix do NOT match")
        elif (params['download_type'] == 'FTP' 
                and (first_url_prefix[:3] != 'ftp' or second_url_prefix[:3] != 'ftp')):
          raise ValueError("Download type and URL prefix do NOT match")
      elif params.get('fwd_file_url') and not params.get('rev_file_url'):
        if params['download_type'] == 'Direct Download' and url_prefix[:4] != 'http':
          raise ValueError("Download type and URL prefix do NOT match")
        elif (params['download_type'] in ['DropBox', 'Google Drive'] 
                                                            and url_prefix != 'https'):
          raise ValueError("Download type and URL prefix do NOT match")
        elif params['download_type'] == 'FTP' and url_prefix[:3] != 'ftp':
          raise ValueError("Download type and URL prefix do NOT match")

  def _upload_file_path(self, params):
      """
      _upload_file_path: upload fastq file as reads from user's staging area

      params:
      fwd_staging_file_name: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
      sequencing_tech: sequencing technology
      name: output reads file name
      workspace_name: workspace name/ID that reads will be stored to

      optional params:
      rev_staging_file_name: reverse/right paired-end fastq file name user's staging area
      single_genome: whether the reads are from a single genome or a metagenome
      insert_size_mean: mean (average) insert length
      insert_size_std_dev: standard deviation of insert lengths
      read_orientation_outward: whether reads in a pair point outward
      interleaved: whether reads is interleaved

      """
      log ('---> running UploaderUtil._upload_file_path')

      upload_file_params = params

      workspace_name_or_id = params.get('workspace_name')

      if str(workspace_name_or_id).isdigit():
        upload_file_params['wsid'] = int(workspace_name_or_id)
      else:
        upload_file_params['wsname'] = str(workspace_name_or_id)

      log('--->\nrunning ReadsUtils.upload_reads\nparams:\n{}'.format(
                                          json.dumps(upload_file_params, indent=1)))
      ru = ReadsUtils(self.callback_url)
      result = ru.upload_reads(upload_file_params)

      return result

  def _load_gff_fasta_file_path(self, params):
      """
      _load_gff_fasta_file_path: load gff and fasta to workspace as genome using files from user's staging area
      
      fasta_file: fasta file from user's staging area
      gff_file: gff file from user's staging area
      genome_name: output genome object name
      workspace_name: workspace name that genome will be stored to
      """
      log ('---> running UploaderUtil._load_gff_fasta_file_path')
      
      workspace_name_or_id = params.get('workspace_name')
      
      #for now must use workspace name, but no ws_id_to_name() function available
      if str(workspace_name_or_id).isdigit():
          raise ValueError('"' + workspace_name_or_id + '" parameter is a workspace id and workspace name is required')

      log('--->\nrunning kb_gffupload.fasta_gff_to_genome\nparams:\n%s' % json.dumps(params, indent=1))
      gff_upload = kb_gffupload(self.callback_url,service_ver='dev')
      result = gff_upload.fasta_gff_to_genome(params)
      
      return result

  def _upload_file_url(self, params):
      """
      _upload_file_url: upload fastq file as reads from web

      params:
      download_type: download type for web source fastq file
      fwd_file_url: single-end fastq file URL or forward/left paired-end fastq file URL
      sequencing_tech: sequencing technology
      name: output reads file name
      workspace_name: workspace name/ID that reads will be stored to

      optional params:
      rev_file_url: reverse/right paired-end fastq file URL
      single_genome: whether the reads are from a single genome or a metagenome
      insert_size_mean: mean (average) insert length
      insert_size_std_dev: standard deviation of insert lengths
      read_orientation_outward: whether reads in a pair point outward
      interleaved: whether reads is interleaved
      
      """
      log ('---> running UploaderUtil._upload_file_url')

      upload_file_params = params

      workspace_name_or_id = params.get('workspace_name')

      if str(workspace_name_or_id).isdigit():
        upload_file_params['wsid'] = int(workspace_name_or_id)
      else:
        upload_file_params['wsname'] = str(workspace_name_or_id)

      log('--->\nrunning ReadsUtils.upload_reads\nparams:\n{}'.format(
                                          json.dumps(upload_file_params, indent=1)))
      ru = ReadsUtils(self.callback_url)
      result = ru.upload_reads(upload_file_params)

      return result

