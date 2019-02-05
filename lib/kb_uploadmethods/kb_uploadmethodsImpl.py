# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json
import sys
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from kb_uploadmethods.Utils.UnpackFileUtil import UnpackFileUtil
from kb_uploadmethods.Utils.ImportGenbankUtil import ImportGenbankUtil
from kb_uploadmethods.Utils.ImportGFFFastaUtil import ImportGFFFastaUtil
from kb_uploadmethods.Utils.ImportSRAUtil import ImportSRAUtil
from kb_uploadmethods.Utils.ImportAssemblyUtil import ImportAssemblyUtil
from kb_uploadmethods.Utils.ImportMediaUtil import ImportMediaUtil
from kb_uploadmethods.Utils.ImportFBAModelUtil import ImportFBAModelUtil
from kb_uploadmethods.Utils.ImportExpressionMatrixUtil import ImportExpressionMatrixUtil
from kb_uploadmethods.Utils.ImportReadsUtil import ImportReadsUtil
from kb_uploadmethods.Utils.ImportPhenotypeSetUtil import ImportPhenotypeSetUtil
from kb_uploadmethods.Utils.ImportAttributeMappingUtil import ImportAttributeMappingUtil
from kb_uploadmethods.Utils.BatchUtil import BatchUtil
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
    VERSION = "1.0.25"
    GIT_URL = "git@github.com:Tianhao-Gu/kb_uploadmethods.git"
    GIT_COMMIT_HASH = "2f21fdb4ce631405258cd96304f454b87a3a7c05"

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
        print('--->\nRunning uploadmethods.upload_fastq_file\nparams:')
        print((json.dumps(params, indent=1)))

        if params.get('urls_to_add'):
            returnVal = {'obj_ref': ''}
            for params_item in params.get('urls_to_add'):
                params_item['workspace_name'] = params.get('workspace_name')
                params_item['download_type'] = params.get('download_type')
                params_item['sequencing_tech'] = params.get('sequencing_tech')
                params_item['interleaved'] = params.get('interleaved')
                for key, value in list(params_item.items()):
                    if isinstance(value, str):
                        params_item[key] = value.strip()
                fastqUploader = UploaderUtil(self.config)
                itemReturnVal = fastqUploader.upload_fastq_file(params_item)
                returnVal['obj_ref'] += itemReturnVal['obj_ref'] + ','
            returnVal['obj_ref'] = returnVal['obj_ref'][:-1]
        else:
            for key, value in list(params.items()):
                if isinstance(value, str):
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
           (Required: genome_name: output genome object name workspace_name:
           workspace name/ID of the object For staging area: fasta_file:
           fasta file containing assembled contigs/chromosomes gff_file: gff
           file containing predicted gene models and corresponding features
           Optional params: scientific_name: proper name for species, key for
           taxonomy lookup. Default to 'unknown_taxon' source: Source Of The
           GFF File. Default to 'User' taxon_wsname - where the reference
           taxons are. Default to 'ReferenceTaxons' taxon_reference - if
           defined, will try to link the Genome to the specified taxonomy
           object release: Release Or Version Of The Source Data
           genetic_code: Genetic Code For The Organism type: 'Reference',
           'User upload', 'Representative') -> structure: parameter
           "fasta_file" of String, parameter "gff_file" of String, parameter
           "genome_name" of String, parameter "workspace_name" of type
           "workspace_name" (workspace name of the object), parameter
           "genome_type" of String, parameter "scientific_name" of String,
           parameter "source" of String, parameter "taxon_wsname" of String,
           parameter "taxon_reference" of String, parameter "release" of
           String, parameter "genetic_code" of Long, parameter "type" of
           String, parameter "generate_missing_genes" of String
        :returns: instance of type "UploadFastaGFFMethodResult" -> structure:
           parameter "genome_ref" of String, parameter "genome_info" of
           String, parameter "report_name" of type "report_name", parameter
           "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN upload_fasta_gff_file

        print('--->\nRunning uploadmethods.upload_fasta_gff_file\nparams:')
        print((json.dumps(params, indent=1)))

        for key in list(params.keys()):
            value = params[key]
            if value is None:
                del params[key]
            else:
                if isinstance(value, str):
                    if value.strip() == '':
                        params[key] = None
                    else:
                        params[key] = value.strip()

        uploader = ImportGFFFastaUtil(self.config)
        returnVal = uploader.import_gff_fasta_from_staging(params)
        # reuse logic from genbank report rather than replicate
        genbank_import = ImportGenbankUtil(self.config)
        reportVal = genbank_import.generate_report(returnVal['genome_ref'],
                                                   params)
        returnVal.update(reportVal)
        #END upload_fasta_gff_file

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method upload_fasta_gff_file return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def batch_import_genomes_from_staging(self, ctx, params):
        """
        :param params: instance of type "BatchGenomeImporterParams" ->
           structure: parameter "staging_subdir" of String, parameter
           "genome_set_name" of String, parameter "workspace_name" of type
           "workspace_name" (workspace name of the object), parameter
           "genome_type" of String, parameter "source" of String, parameter
           "taxon_wsname" of String, parameter "taxon_reference" of String,
           parameter "release" of String, parameter "genetic_code" of Long,
           parameter "generate_missing_genes" of String
        :returns: instance of type "BatchGenomeImporterResult" -> structure:
           parameter "genome_set_ref" of String, parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN batch_import_genomes_from_staging

        print('--->\nRunning uploadmethods.batch_import_genomes_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        self.config['USER_ID'] = ctx['user_id']

        batch_util = BatchUtil(self.config)
        returnVal = batch_util.batch_import_genomes_from_staging(params)
        #END batch_import_genomes_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method batch_import_genomes_from_staging return value ' +
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
        print('--->\nRunning uploadmethods.unpack_staging_file\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
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
        print('--->\nRunning uploadmethods.unpack_web_file\nparams:')
        print((json.dumps(params, indent=1)))

        self.config['USER_ID'] = ctx['user_id']

        if params.get('urls_to_add_web_unpack'):
            returnVal = {'unpacked_file_path': ''}
            download_type = params.get('download_type')
            workspace_name = params.get('workspace_name')
            for params_item in params.get('urls_to_add_web_unpack'):
                params_item['download_type'] = download_type
                params_item['workspace_name'] = workspace_name
                for key, value in list(params_item.items()):
                    if isinstance(value, str):
                        params_item[key] = value.strip()
                unpacker = UnpackFileUtil(self.config)
                itemReturnVal = unpacker.unpack_web_file(params_item)
                returnVal['unpacked_file_path'] += itemReturnVal['unpacked_file_path'] + ','
            returnVal['unpacked_file_path'] = returnVal['unpacked_file_path'][:-1]
        else:
            for key, value in list(params.items()):
                if isinstance(value, str):
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
           generate_missing_genes - Generate gene feature for CDSs that do
           not have a parent in file genetic_code - Genetic code of organism.
           Overwrites determined GC from taxon object type - Reference,
           Representative or User upload) -> structure: parameter
           "staging_file_subdir_path" of String, parameter "genome_name" of
           String, parameter "workspace_name" of String, parameter "source"
           of String, parameter "genome_type" of String, parameter "release"
           of String, parameter "genetic_code" of Long, parameter "type" of
           String, parameter "generate_ids_if_needed" of String, parameter
           "generate_missing_genes" of String
        :returns: instance of type "GenomeSaveResult" -> structure: parameter
           "genome_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_genbank_from_staging
        for key, value in list(params.items()):
            if isinstance(value, str):
                params[key] = value.strip()

        importer = ImportGenbankUtil(self.config)
        returnVal = importer.import_genbank_from_staging(params)
        reportVal = importer.generate_report(returnVal['genome_ref'], params)
        returnVal.update(reportVal)
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
        print('--->\nRunning uploadmethods.import_sra_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
                params[key] = value.strip()

        importer = ImportSRAUtil(self.config)
        returnVal = importer.import_sra_from_staging(params)
        params['uploaded_files'] = [params.get('staging_file_subdir_path')]
        reportVal = importer.generate_report([returnVal['obj_ref']], params)
        returnVal.update(reportVal)
        #END import_sra_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_sra_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_sra_from_web(self, ctx, params):
        """
        :param params: instance of type "WebSRAToReadsParams" -> structure:
           parameter "download_type" of String, parameter "sra_urls_to_add"
           of type "sra_urls_to_add" (download_type: download type for web
           source fastq file ('Direct Download', 'FTP', 'DropBox', 'Google
           Drive') sra_urls_to_add: dict of SRA file URLs required params:
           file_url: SRA file URL sequencing_tech: sequencing technology
           name: output reads file name workspace_name: workspace name/ID of
           the object Optional Params: single_genome: whether the reads are
           from a single genome or a metagenome. insert_size_mean: mean
           (average) insert length insert_size_std_dev: standard deviation of
           insert lengths read_orientation_outward: whether reads in a pair
           point outward) -> structure: parameter "file_url" of String,
           parameter "sequencing_tech" of type "sequencing_tech", parameter
           "name" of type "name", parameter "single_genome" of type
           "single_genome", parameter "insert_size_mean" of type
           "insert_size_mean", parameter "insert_size_std_dev" of type
           "insert_size_std_dev", parameter "read_orientation_outward" of
           type "read_orientation_outward", parameter "workspace_name" of
           type "workspace_name" (workspace name of the object)
        :returns: instance of type "WebSRAToReadsResult" -> structure:
           parameter "obj_refs" of list of String, parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_sra_from_web
        print('--->\nRunning uploadmethods.import_sra_from_web\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
                params[key] = value.strip()

        importer = ImportSRAUtil(self.config)
        returnVal = importer.import_sra_from_web(params)
        params['uploaded_files'] = returnVal.get('uploaded_files')
        reportVal = importer.generate_report(returnVal['obj_refs'], params)
        returnVal.update(reportVal)
        #END import_sra_from_web

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_sra_from_web return value ' +
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
           (workspace name of the object), parameter "min_contig_length" of
           Long, parameter "type" of String
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_fasta_as_assembly_from_staging
        print('--->\nRunning uploadmethods.import_fasta_as_assembly_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
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
        print('--->\nRunning uploadmethods.import_tsv_as_media_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
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
        print('--->\nRunning uploadmethods.import_excel_as_media_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
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
        print('--->\nRunning uploadmethods.import_tsv_or_excel_as_media_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
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

    def import_file_as_fba_model_from_staging(self, ctx, params):
        """
        :param params: instance of type "FileToFBAModelParams" (required
           params: model_file: subdirectory file path for model file e.g. for
           file: /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           compounds_file: same as above for compound (only used for tsv)
           file_type: one of "tsv", "excel", "sbml" genome: the associated
           species genome biomasses: one or more biomass reactions in model
           model_name: output FBAModel object name workspace_name: workspace
           name/ID of the object) -> structure: parameter "model_file" of
           String, parameter "compounds_file" of String, parameter
           "file_type" of String, parameter "genome" of String, parameter
           "biomass" of String, parameter "model_name" of String, parameter
           "workspace_name" of type "workspace_name" (workspace name of the
           object)
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_file_as_fba_model_from_staging
        print(('--->\nrunning {}.{}\n params:\n{}'
            .format(self.__class__.__name__, sys._getframe().f_code.co_name,
                    json.dumps(params, indent=1))))

        importer = ImportFBAModelUtil(self.config)
        returnVal = importer.import_fbamodel_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_file_as_fba_model_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_file_as_fba_model_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_tsv_as_expression_matrix_from_staging(self, ctx, params):
        """
        :param params: instance of type "FileToMatrixParams" (required
           params: staging_file_subdir_path: subdirectory file path e.g. for
           file: /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           matrix_name: output Expressin Matirx file name workspace_name:
           workspace name/ID of the object genome_ref: optional reference to
           a Genome object that will be used for mapping feature IDs to
           fill_missing_values: optional flag for filling in missing values
           in matrix (default value is false) data_type: optional filed,
           value is one of 'untransformed', 'log2_level', 'log10_level',
           'log2_ratio', 'log10_ratio' or 'unknown' (last one is default
           value) data_scale: optional parameter (default value is '1.0')) ->
           structure: parameter "staging_file_subdir_path" of String,
           parameter "workspace_name" of type "workspace_name" (workspace
           name of the object), parameter "matrix_name" of String, parameter
           "genome_ref" of String, parameter "fill_missing_values" of type
           "boolean" (Indicates true or false values, false = 0, true = 1
           @range [0,1]), parameter "data_type" of String, parameter
           "data_scale" of String
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_tsv_as_expression_matrix_from_staging
        print('--->\nRunning uploadmethods.import_tsv_as_expression_matrix_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
                params[key] = value.strip()

        importer = ImportExpressionMatrixUtil(self.config)
        returnVal = importer.import_tsv_as_expression_matrix_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_tsv_as_expression_matrix_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_tsv_as_expression_matrix_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_reads_from_staging(self, ctx, params):
        """
        :param params: instance of type "UploadReadsParams" (sequencing_tech:
           sequencing technology name: output reads file name workspace_name:
           workspace name/ID of the object import_type: either FASTQ or SRA
           For files in user's staging area:
           fastq_fwd_or_sra_staging_file_name: single-end fastq file name Or
           forward/left paired-end fastq file name from user's staging area
           Or SRA staging file fastq_rev_staging_file_name: reverse/right
           paired-end fastq file name user's staging area e.g. for file:
           /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name Optional
           Params: single_genome: whether the reads are from a single genome
           or a metagenome. interleaved: whether reads is interleaved
           insert_size_mean: mean (average) insert length
           insert_size_std_dev: standard deviation of insert lengths
           read_orientation_outward: whether reads in a pair point outward)
           -> structure: parameter "import_type" of String, parameter
           "fastq_fwd_staging_file_name" of String, parameter
           "fastq_rev_staging_file_name" of String, parameter
           "sra_staging_file_name" of String, parameter "sequencing_tech" of
           type "sequencing_tech", parameter "workspace_name" of type
           "workspace_name" (workspace name of the object), parameter "name"
           of String, parameter "single_genome" of type "single_genome",
           parameter "interleaved" of type "interleaved", parameter
           "insert_size_mean" of type "insert_size_mean", parameter
           "insert_size_std_dev" of type "insert_size_std_dev", parameter
           "read_orientation_outward" of type "read_orientation_outward"
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_reads_from_staging
        print('--->\nRunning uploadmethods.import_reads_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
                params[key] = value.strip()

        importer = ImportReadsUtil(self.config)
        returnVal = importer.import_reads_from_staging(params)
        #END import_reads_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_reads_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_tsv_as_phenotype_set_from_staging(self, ctx, params):
        """
        :param params: instance of type "FileToPhenotypeSetParams" (required
           params: staging_file_subdir_path: subdirectory file path e.g. for
           file: /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           phenotype_set_name: output PhenotypeSet object name
           workspace_name: workspace name/ID of the object optional: genome:
           Genome object that contains features referenced by the Phenotype
           Set) -> structure: parameter "staging_file_subdir_path" of String,
           parameter "workspace_name" of type "workspace_name" (workspace
           name of the object), parameter "phenotype_set_name" of String,
           parameter "genome" of type "obj_ref"
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_tsv_as_phenotype_set_from_staging
        print('--->\nRunning uploadmethods.import_tsv_as_phenotype_set_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
                params[key] = value.strip()

        importer = ImportPhenotypeSetUtil(self.config)
        returnVal = importer.import_phenotype_set_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_tsv_as_phenotype_set_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_tsv_as_phenotype_set_from_staging return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def import_attribute_mapping_from_staging(self, ctx, params):
        """
        :param params: instance of type "FileToConditionSetParams" (required
           params: staging_file_subdir_path: subdirectory file path e.g. for
           file: /data/bulk/user_name/file_name staging_file_subdir_path is
           file_name for file:
           /data/bulk/user_name/subdir_1/subdir_2/file_name
           staging_file_subdir_path is subdir_1/subdir_2/file_name
           attribute_mapping_name: output ConditionSet object name
           workspace_id: workspace name/ID of the object) -> structure:
           parameter "staging_file_subdir_path" of String, parameter
           "workspace_name" of type "workspace_name" (workspace name of the
           object), parameter "attribute_mapping_name" of String
        :returns: instance of type "UploadMethodResult" -> structure:
           parameter "obj_ref" of type "obj_ref", parameter "report_name" of
           type "report_name", parameter "report_ref" of type "report_ref"
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN import_attribute_mapping_from_staging
        print('--->\nRunning uploadmethods.import_attribute_mapping_from_staging\nparams:')
        print((json.dumps(params, indent=1)))

        for key, value in list(params.items()):
            if isinstance(value, str):
                params[key] = value.strip()

        importer = ImportAttributeMappingUtil(self.config)
        returnVal = importer.import_attribute_mapping_from_staging(params)

        reportVal = importer.generate_report(returnVal['obj_ref'], params)
        returnVal.update(reportVal)
        #END import_attribute_mapping_from_staging

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method import_attribute_mapping_from_staging return value ' +
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
