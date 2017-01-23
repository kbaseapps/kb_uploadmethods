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
	typedef string obj_ref;

	typedef structure {
		fwd_file_url fwd_file_url;
		rev_file_url rev_file_url;
		name name;
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
	     
	    urls_to_add: used for parameter-groups. dict of {fwd_file_url, rev_file_url, name}
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
	} UploadMethodParams;

	typedef structure {
		obj_ref obj_ref;
	} UploadMethodResult;

	funcdef upload_fastq_file(UploadMethodParams params)
		returns (UploadMethodResult returnVal) authentication required;
};
