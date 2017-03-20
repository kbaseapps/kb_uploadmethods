# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from kb_uploadmethods.Utils.UnpackFileUtil import UnpackFileUtil
from kb_uploadmethods.Utils.ImportGenbankUtil import ImportGenbankUtil
from kb_uploadmethods.Utils.ImportGFFFastaUtil import ImportGFFFastaUtil
from kb_uploadmethods.Utils.ImportSRAUtil import ImportSRAUtil
from kb_uploadmethods.Utils.ImportAssemblyUtil import ImportAssemblyUtil
from kb_uploadmethods.Utils.ImportMediaUtil import ImportMediaUtil
#END_HEADER


class kb_uploadmethods:
    '''
    Module Name:
    kb_uploadmethods

    Module Description:
    A KBase module: kb_uploadmethods
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.1.10"
    GIT_URL = "git@github.com:Tianhao-Gu/kb_uploadmethods.git"
    GIT_COMMIT_HASH = "039f023b778eecd0c95e5e2dbaba2cf172eacd40"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        #END_CONSTRUCTOR
        pass


    def upload_fastq_file(self, ctx, params):
        """
        :param params: instance of type "UploadMethodParams"
           (sequencing_tech: sequencing technology name: output reads file
           name workspace_name: workspace name/ID of the object For files in
           user's staging area: fwd_staging_file_name: single-end fastq file
           name or forward/left paired-end fastq file name from user's
           staging area rev_staging_file_name: reverse/right paired-end fastq
           file name user's staging area For files from web: download_type:
           download type for web source fastq file ('Direct Download', 'FTP',
           'DropBox', 'Google Drive') fwd_file_url: single-end fastq file URL
           or forward/left paired-end fastq file URL rev_file_url:
           reverse/right paired-end fastq file URL urls_to_add: used for
           parameter-groups. dict of {fwd_file_url, rev_file_url, name,
           single_genome, interleaved, insert_size_mean and
           read_orientation_outward} Optional Params: single_genome: whether
           the reads are from a single genome or a metagenome. interleaved:
           whether reads is interleaved insert_size_mean: mean (average)
           insert length insert_size_std_dev: standard deviation of insert
           lengths read_orientation_outward: whether reads in a pair point
           outward) -> structure: parameter "workspace_name" of type
           "workspace_name" (workspace name of the object), parameter
           "fwd_staging_file_name" of type "fwd_staging_file_name" (input and
           output file path/url), parameter "rev_staging_file_name" of type
           "rev_staging_file_name", parameter "download_type" of type
           "download_type", parameter "fwd_file_url" of type "fwd_file_url",
           parameter "rev_file_url" of type "rev_file_url", parameter
           "sequencing_tech" of type "sequencing_tech", parameter "name" of
           type "name", parameter "urls_to_add" of type "urls_to_add" ->
           structure: parameter "fwd_file_url" of type "fwd_file_url",
           parameter "rev_file_url" of type "rev_file_url", parameter "name"
           of type "name", parameter "single_genome" of type "single_genome",
           parameter "interleaved" of type "interleaved", parameter
           "insert_size_mean" of type "insert_size_mean", parameter
           "insert_size_std_dev" of type "insert_size_std_dev", parameter
           "read_orientation_outward" of type "read_orientation_outward",
           parameter "single_genome" of type "single_genome", parameter
           "interleaved" of type "interleaved", parameter "insert_size_mean"
           of type "insert_size_mean", parameter "insert_size_std_dev" of
           type "insert_size_std_dev", parameter "read_orientation_outward"
           of type "read_orientation_outward"
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_fastq_file
        print '--->\nRunning uploadmethods.upload_fastq_file\nparams:'
        print json.dumps(params, indent=1)

        if params.get('urls_to_add'):
            returnVal = {'obj_ref': ''}
            for params_item in params.get('urls_to_add'):
                params_item['workspace_name'] = params.get('workspace_name')
                params_item['download_type'] = params.get('download_type')
                params_item['sequencing_tech'] = params.get('sequencing_tech')
                params_item['interleaved'] = params.get('interleaved')
                for key, value in params_item.iteritems():
                    if isinstance(value, basestring):
                        params_item[key] = value.strip()
                fastqUploader = UploaderUtil(self.config)
                itemReturnVal = fastqUploader.upload_fastq_file(params_item)
                returnVal['obj_ref'] += itemReturnVal['obj_ref'] + ','
            returnVal['obj_ref'] = returnVal['obj_ref'][:-1]
        else:
            for key, value in params.iteritems():
                if isinstance(value, basestring):
                    params[key] = value.strip()
            fastqUploader = UploaderUtil(self.config)
            returnVal = fastqUploader.upload_fastq_file(params)

        reportVal = fastqUploader.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END upload_fastq_file

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_fastq_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def upload_fasta_gff_file(self, ctx, params):
        """
        :param params: instance of type "UploadFastaGFFMethodParams"
           (genome_name: output genome object name workspace_name: workspace
           name/ID of the object scientific_name: proper name for species,
           key for taxonomy lookup For staging area: fasta_file: fasta file
           containing assembled contigs/chromosomes gff_file: gff file
           containing predicted gene models and corresponding features) ->
           structure: parameter "fasta_file" of String, parameter "gff_file"
           of String, parameter "genome_name" of String, parameter
           "scientific_name" of String, parameter "workspace_name" of type
           "workspace_name" (workspace name of the object)
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_fasta_gff_file

        print '--->\nRunning uploadmethods.upload_fasta_gff_file\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        uploader = ImportGFFFastaUtil(self.config)
        returnVal = uploader.import_gff_fasta_from_staging(params)

        #END upload_fasta_gff_file

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_fasta_gff_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def unpack_staging_file(self, ctx, params):
        """
        Unpack a staging area file
        :param params: instance of type "UnpackStagingFileParams" (Input
           parameters for the "unpack_staging_file" function. Required
           parameters: staging_file_subdir_path: subdirectory file path e.g.
           for file: /data/bulk/user_name/file_name staging_file_subdir_path
           is file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           workspace_name: workspace name/ID of the object) -> structure:
           parameter "workspace_name" of type "workspace_name" (workspace
           name of the object), parameter "staging_file_subdir_path" of String
        :returns: instance of type "UnpackStagingFileOutput" (Results from
           the unpack_staging_file function. unpacked_file_path: unpacked
           file path(s) in staging area) -> structure: parameter
           "unpacked_file_path" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN unpack_staging_file
        print '--->\nRunning uploadmethods.unpack_staging_file\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        self.config['USER_ID'] = ctx['user_id']
        unpacker = UnpackFileUtil(self.config)
        returnVal = unpacker.unpack_staging_file(params)

        reportVal = unpacker.generate_report(returnVal['unpacked_file_path'], params)
        returnVal.update(reportVal)

        #END unpack_staging_file

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method unpack_staging_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def unpack_web_file(self, ctx, params):
        """
        Download and unpack a web file to staging area
        :param params: instance of type "UnpackWebFileParams" (Input
           parameters for the "unpack_web_file" function. Required
           parameters: workspace_name: workspace name/ID of the object
           file_url: file URL download_type: one of ['Direct Download',
           'FTP', 'DropBox', 'Google Drive'] Optional:
           urls_to_add_web_unpack: used for parameter-groups. dict of
           {file_url}) -> structure: parameter "workspace_name" of type
           "workspace_name" (workspace name of the object), parameter
           "file_url" of String, parameter "download_type" of String,
           parameter "urls_to_add_web_unpack" of type
           "urls_to_add_web_unpack" -> structure: parameter "file_url" of
           String
        :returns: instance of type "UnpackWebFileOutput" (Results from the
           unpack_web_file function. unpacked_file_path: unpacked file
           path(s) in staging area) -> structure: parameter
           "unpacked_file_path" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN unpack_web_file
        print '--->\nRunning uploadmethods.unpack_web_file\nparams:'
        print json.dumps(params, indent=1)

        self.config['USER_ID'] = ctx['user_id']

        if params.get('urls_to_add_web_unpack'):
            returnVal = {'unpacked_file_path': ''}
            download_type = params.get('download_type')
            workspace_name = params.get('workspace_name')
            for params_item in params.get('urls_to_add_web_unpack'):
                params_item['download_type'] = download_type
                params_item['workspace_name'] = workspace_name
                for key, value in params_item.iteritems():
                    if isinstance(value, basestring):
                        params_item[key] = value.strip()
                unpacker = UnpackFileUtil(self.config)
                itemReturnVal = unpacker.unpack_web_file(params_item)
                returnVal['unpacked_file_path'] += itemReturnVal['unpacked_file_path'] + ','
            returnVal['unpacked_file_path'] = returnVal['unpacked_file_path'][:-1]
        else:
            for key, value in params.iteritems():
                if isinstance(value, basestring):
                    params[key] = value.strip()
            unpacker = UnpackFileUtil(self.config)
            returnVal = unpacker.unpack_web_file(params)

        reportVal = unpacker.generate_report(returnVal['unpacked_file_path'], params)
        returnVal.update(reportVal)

        #END unpack_web_file

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method unpack_web_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_genbank_from_staging(self, ctx, params):
        """
        :param params: instance of type "GenbankToGenomeParams"
           (import_genbank_from_staging: wrapper method for
           GenomeFileUtil.genbank_to_genome required params:
           staging_file_subdir_path - subdirectory file path e.g. for file:
           /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           genome_name - becomes the name of the object workspace_name - the
           name of the workspace it gets saved to. source - Source of the
           file typically something like RefSeq or Ensembl optional params:
           release - Release or version number of the data per example
           Ensembl has numbered releases of all their data: Release 31
           generate_ids_if_needed - If field used for feature id is not
           there, generate ids (default behavior is raising an exception)
           genetic_code - Genetic code of organism. Overwrites determined GC
           from taxon object type - Reference, Representative or User upload)
           -> structure: parameter "staging_file_subdir_path" of String,
           parameter "genome_name" of String, parameter "workspace_name" of
           String, parameter "source" of String, parameter "release" of
           String, parameter "genetic_code" of Long, parameter "type" of
           String, parameter "generate_ids_if_needed" of String, parameter
           "exclude_ontologies" of String
        :returns: instance of type "GenomeSaveResult" -> structure: parameter
           "genome_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_genbank_from_staging
        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        importer = ImportGenbankUtil(self.config)
        returnVal = importer.import_genbank_from_staging(params)
        #END import_genbank_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_genbank_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_sra_from_staging(self, ctx, params):
        """
        :param params: instance of type "SRAToReadsParams" (required params:
           staging_file_subdir_path: subdirectory file path e.g. for file:
           /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           sequencing_tech: sequencing technology name: output reads file
           name workspace_name: workspace name/ID of the object Optional
           Params: single_genome: whether the reads are from a single genome
           or a metagenome. insert_size_mean: mean (average) insert length
           insert_size_std_dev: standard deviation of insert lengths
           read_orientation_outward: whether reads in a pair point outward)
           -> structure: parameter "staging_file_subdir_path" of String,
           parameter "sequencing_tech" of type "sequencing_tech", parameter
           "name" of type "name", parameter "workspace_name" of type
           "workspace_name" (workspace name of the object), parameter
           "single_genome" of type "single_genome", parameter
           "insert_size_mean" of type "insert_size_mean", parameter
           "insert_size_std_dev" of type "insert_size_std_dev", parameter
           "read_orientation_outward" of type "read_orientation_outward"
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_sra_from_staging
        print '--->\nRunning uploadmethods.import_sra_from_staging\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        importer = ImportSRAUtil(self.config)
        returnVal = importer.import_sra_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_sra_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_sra_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_fasta_as_assembly_from_staging(self, ctx, params):
        """
        :param params: instance of type "FastaToAssemblyParams" (required
           params: staging_file_subdir_path: subdirectory file path e.g. for
           file: /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           assembly_name: output Assembly file name workspace_name: workspace
           name/ID of the object) -> structure: parameter
           "staging_file_subdir_path" of String, parameter "assembly_name" of
           String, parameter "workspace_name" of type "workspace_name"
           (workspace name of the object)
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_fasta_as_assembly_from_staging
        print '--->\nRunning uploadmethods.import_fasta_as_assembly_from_staging\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        importer = ImportAssemblyUtil(self.config)
        returnVal = importer.import_fasta_as_assembly_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_fasta_as_assembly_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_fasta_as_assembly_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_tsv_as_media_from_staging(self, ctx, params):
        """
        :param params: instance of type "FileToMediaParams" (required params:
           staging_file_subdir_path: subdirectory file path e.g. for file:
           /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           media_name: output Media file name workspace_name: workspace
           name/ID of the object) -> structure: parameter
           "staging_file_subdir_path" of String, parameter "media_name" of
           String, parameter "workspace_name" of type "workspace_name"
           (workspace name of the object)
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_tsv_as_media_from_staging
        print '--->\nRunning uploadmethods.import_tsv_as_media_from_staging\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        importer = ImportMediaUtil(self.config)
        returnVal = importer.import_tsv_as_media_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_tsv_as_media_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_tsv_as_media_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_excel_as_media_from_staging(self, ctx, params):
        """
        :param params: instance of type "FileToMediaParams" (required params:
           staging_file_subdir_path: subdirectory file path e.g. for file:
           /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           media_name: output Media file name workspace_name: workspace
           name/ID of the object) -> structure: parameter
           "staging_file_subdir_path" of String, parameter "media_name" of
           String, parameter "workspace_name" of type "workspace_name"
           (workspace name of the object)
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_excel_as_media_from_staging
        print '--->\nRunning uploadmethods.import_excel_as_media_from_staging\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        importer = ImportMediaUtil(self.config)
        returnVal = importer.import_excel_as_media_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_excel_as_media_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_excel_as_media_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_tsv_or_excel_as_media_from_staging(self, ctx, params):
        """
        :param params: instance of type "FileToMediaParams" (required params:
           staging_file_subdir_path: subdirectory file path e.g. for file:
           /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           media_name: output Media file name workspace_name: workspace
           name/ID of the object) -> structure: parameter
           "staging_file_subdir_path" of String, parameter "media_name" of
           String, parameter "workspace_name" of type "workspace_name"
           (workspace name of the object)
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_tsv_or_excel_as_media_from_staging
        print '--->\nRunning uploadmethods.import_tsv_or_excel_as_media_from_staging\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        importer = ImportMediaUtil(self.config)
        returnVal = importer.import_media_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_tsv_or_excel_as_media_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_tsv_or_excel_as_media_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
