/*
A KBase module: kb_uploadmethods
*/

module kb_uploadmethods {

	/* workspace name of the object */
	typedef string workspace_name;

	/* input and output file path/url */
	typedef string fwd_staging_file_name;
	typedef string rev_staging_file_name;
	typedef string download_type;
	typedef string fwd_file_url;
	typedef string rev_file_url;
	typedef string sequencing_tech;
	typedef string name;
	typedef string single_genome;
	typedef string interleaved;
	typedef string insert_size_mean;
	typedef string insert_size_std_dev;
	typedef string read_orientation_outward;
	typedef string obj_ref;
	typedef string report_name;
	typedef string report_ref;

	typedef structure {
		fwd_file_url fwd_file_url;
		rev_file_url rev_file_url;
		name name;
		single_genome single_genome;
		interleaved interleaved;
		insert_size_mean insert_size_mean;
		insert_size_std_dev insert_size_std_dev;
		read_orientation_outward read_orientation_outward;
	} urls_to_add;

	/*
	    sequencing_tech: sequencing technology
	    name: output reads file name
	    workspace_name: workspace name/ID of the object
	    
	    For files in user's staging area:
	    fwd_staging_file_name: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
	    rev_staging_file_name: reverse/right paired-end fastq file name user's staging area
	    
	    For files from web:
	    download_type: download type for web source fastq file ('Direct Download', 'FTP', 'DropBox', 'Google Drive')
	    fwd_file_url: single-end fastq file URL or forward/left paired-end fastq file URL
	    rev_file_url: reverse/right paired-end fastq file URL
	     
	    urls_to_add: used for parameter-groups. dict of {fwd_file_url, rev_file_url, name,
	    			single_genome, interleaved, insert_size_mean and read_orientation_outward}

	    Optional Params:
	    single_genome: whether the reads are from a single genome or a metagenome.
		interleaved: whether reads is interleaved
		insert_size_mean: mean (average) insert length
		insert_size_std_dev: standard deviation of insert lengths
		read_orientation_outward: whether reads in a pair point outward
    */
	typedef structure {
		workspace_name workspace_name;
		fwd_staging_file_name fwd_staging_file_name;
		rev_staging_file_name rev_staging_file_name;
		download_type download_type;
		fwd_file_url fwd_file_url;
		rev_file_url rev_file_url;
		sequencing_tech sequencing_tech;
		name name;
		urls_to_add urls_to_add;
		single_genome single_genome;
		interleaved interleaved;
		insert_size_mean insert_size_mean;
		insert_size_std_dev insert_size_std_dev;
		read_orientation_outward read_orientation_outward;
	} UploadMethodParams;

	typedef structure {
		obj_ref obj_ref;
		report_name report_name;
		report_ref report_ref;
	} UploadMethodResult;

	funcdef upload_fastq_file(UploadMethodParams params)
		returns (UploadMethodResult returnVal) authentication required;

	/* Input parameters for the "unpack_staging_file" function.

      Required parameters:
      staging_file_subdir_path: subdirectory file path
      e.g. 
        for file: /data/bulk/user_name/file_name
        staging_file_subdir_path is file_name
        for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
        staging_file_subdir_path is subdir_1/subdir_2/file_name
      workspace_name: workspace name/ID of the object
    */
    typedef structure {
      workspace_name workspace_name;
      string staging_file_subdir_path;
    }UnpackStagingFileParams;

    /* Results from the unpack_staging_file function.

      unpacked_file_path: unpacked file path(s) in staging area
    */
    typedef structure {
      string unpacked_file_path;
    }UnpackStagingFileOutput;

    /* Unpack a staging area file */
    funcdef unpack_staging_file(UnpackStagingFileParams params)
        returns(UnpackStagingFileOutput returnVal) authentication required;

    typedef structure{
    	string file_url;
    }urls_to_add_web_unpack;

    /* Input parameters for the "unpack_web_file" function.

      Required parameters:
      workspace_name: workspace name/ID of the object
      file_url: file URL
      download_type: one of ['Direct Download', 'FTP', 'DropBox', 'Google Drive']

      Optional:
      urls_to_add_web_unpack: used for parameter-groups. dict of {file_url}

    */
    typedef structure {
      workspace_name workspace_name;
      string file_url;
      string download_type;
      urls_to_add_web_unpack urls_to_add_web_unpack;
    }UnpackWebFileParams;

    /* Results from the unpack_web_file function.

      unpacked_file_path: unpacked file path(s) in staging area
    */
    typedef structure {
      string unpacked_file_path;
    }UnpackWebFileOutput;

    /* Download and unpack a web file to staging area */
    funcdef unpack_web_file(UnpackWebFileParams params)
        returns(UnpackWebFileOutput returnVal) authentication required;


    /* 
    import_genbank_from_staging: wrapper method for GenomeFileUtil.genbank_to_genome
    
      required params:
      staging_file_subdir_path - subdirectory file path
      e.g. 
        for file: /data/bulk/user_name/file_name
        staging_file_subdir_path is file_name
        for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
        staging_file_subdir_path is subdir_1/subdir_2/file_name
      genome_name - becomes the name of the object
      workspace_name - the name of the workspace it gets saved to.
      source - Source of the file typically something like RefSeq or Ensembl

      optional params:
      release - Release or version number of the data 
          per example Ensembl has numbered releases of all their data: Release 31
      generate_ids_if_needed - If field used for feature id is not there, 
          generate ids (default behavior is raising an exception)
      genetic_code - Genetic code of organism. Overwrites determined GC from 
          taxon object
      type - Reference, Representative or User upload
    */
    typedef structure {
      string staging_file_subdir_path;
      string genome_name;
      string workspace_name;
      string source;

      string release;
      int    genetic_code;
      string type;
      string generate_ids_if_needed;
      string exclude_ontologies;
    } GenbankToGenomeParams;

    typedef structure {
        string genome_ref;
    } GenomeSaveResult;

    funcdef import_genbank_from_staging(GenbankToGenomeParams params)
            returns (GenomeSaveResult returnVal) authentication required;

    /*
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
    */
    typedef structure {
      string staging_file_subdir_path;
      sequencing_tech sequencing_tech;
      name name;
      workspace_name workspace_name;

      single_genome single_genome;
      insert_size_mean insert_size_mean;
      insert_size_std_dev insert_size_std_dev;
      read_orientation_outward read_orientation_outward;
    } SRAToReadsParams;

    funcdef import_sra_from_staging(SRAToReadsParams params)
            returns (UploadMethodResult returnVal) authentication required;

    /*
      required params:
      staging_file_subdir_path: subdirectory file path
      e.g. 
        for file: /data/bulk/user_name/file_name
        staging_file_subdir_path is file_name
        for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
        staging_file_subdir_path is subdir_1/subdir_2/file_name
      assembly_name: output Assembly file name
      workspace_name: workspace name/ID of the object
    */
    typedef structure {
      string staging_file_subdir_path;
      string assembly_name;
      workspace_name workspace_name;
    } FastaToAssemblyParams;

    funcdef import_fasta_as_assembly_from_staging(FastaToAssemblyParams params)
            returns (UploadMethodResult returnVal) authentication required;

};
