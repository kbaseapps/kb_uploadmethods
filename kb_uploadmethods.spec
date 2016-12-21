/*
A KBase module: kb_uploadmethods
*/

module kb_uploadmethods {

	/* workspace name of the object */
	typedef string workspace_name;

	/* input and output file path/url */
	typedef string first_fastq_file_name;
    typedef string second_fastq_file_name;
    typedef string first_fastq_file_url;
    typedef string second_fastq_file_url;
    typedef string reads_file_name;
    typedef string obj_ref;

	typedef structure {
		workspace_name workspace_name;
		first_fastq_file_name first_fastq_file_name;
		second_fastq_file_name second_fastq_file_name;
		first_fastq_file_url first_fastq_file_url;
		second_fastq_file_url second_fastq_file_url;
		reads_file_name reads_file_name;
	} UploadMethodParams;

	typedef structure {
		obj_ref obj_ref;
	} UploadMethodResult;

    funcdef upload_fastq_file(UploadMethodParams params)
    	returns (UploadMethodResult returnVal) authentication required;
};
