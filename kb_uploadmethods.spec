/*
A KBase module: kb_uploadmethods
*/

module kb_uploadmethods {

	/* indicates true or false values, false <= 0, true >=1 */
	typedef int uploaded;

	/* workspace name of the object */
	typedef string workspace_name;

	/* input and output file path/url */
	typedef string fastq_file_name;
    typedef string secondary_fastq_file_name;
    typedef string fastq_file_url;
    typedef string secondary_fastq_file_url;
    typedef string reads_file_name;

	typedef structure {
		workspace_name workspace_name;
		fastq_file_name fastq_file_name;
		secondary_fastq_file_name secondary_fastq_file_name;
		fastq_file_url fastq_file_url;
		secondary_fastq_file_url secondary_fastq_file_url;
		reads_file_name reads_file_name;
	} inputParamUploadFile;

	typedef structure {
		uploaded uploaded;
	} outParam; 

    funcdef upload_fastq_file(inputParamUploadFile)
    	returns (outParam) authentication required;
};
