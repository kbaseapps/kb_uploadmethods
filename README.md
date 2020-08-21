# kb_uploadmethods

[![Build Status](https://travis-ci.org/tgu/kb_uploadmethods.svg?branch=master)](https://travis-ci.org/tgu/kb_uploadmethods)  
[Release Notes](RELEASE_NOTES.md)

## Description
This module implements [KBase](https://www.kbase.us) apps that are used to transform data files into KBase data objects for use in analysis.

See [here](https://docs.kbase.us/data/upload-download-guide/uploads) for more information on uploading data to KBase.

There are three types of apps described here:
* Staging - these apps take files from the user's staging area - the filesystem where users can upload raw data files before transforming them. 
* URL - these apps take a URL as a parameter and will automatically download the files hosted there. These URLs must be publically accessible.

Each app is listed below with the following format:
### Display name - what the user sees
**app_id**: id - how the app is identified to the system, including the directory under ui/narrative/methods  
**entrypoint**: function - name of the function that gets run in this module (for developer use)  
**inputs** - bulleted list of input parameters  
**outputs** - generated data type and report (if created)

## Development
This module was created using the [KBase SDK](https://kbase.github.io/kb_sdk_docs/)

## Testing
This module can be tested with the following steps, common to all KBase SDK modules.
1. Install the [KBase SDK](https://kbase.github.io/kb_sdk_docs/).
2. Fetch this module and navigate to it from the console.
3. Run `kb-sdk test` once - this will initialize the `test_local/test.cfg` file.
4. Populate the `test_local/test.cfg` file with a KBase authentication token.
5. Run `kb-sdk test` again.

Once steps 1-4 have been run once, you can just run `kb-sdk test` to run the test suite any time.

## Apps and Usage

### Batch Import Assembly from Staging Area
**app_id**: batch_import_assembly_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Batch Import Genome from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_genomes_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import TSV/Excel File as Attribute Mapping from Staging Area
**app_id**: import_attribute_mapping_from_staging
**entrypoint**: import_attribute_mapping_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import JSON File as EscherMap from Staging Area
**app_id**: import_eschermap_from_staging
**entrypoint**: import_eschermap_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import FASTA File as Assembly from Staging Area
**app_id**: import_fasta_as_assembly_from_staging
**entrypoint**: import_fasta_as_assembly_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import FASTQ/SRA File as Reads from Staging Area
**app_id**: import_fastq_sra_as_reads_from_staging
**entrypoint**: import_reads_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import TSV/XLS/SBML File as an FBAModel from Staging Area
**app_id**: import_file_as_fba_model_from_staging
**entrypoint**: import_file_as_fba_model_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import GenBank File as Genome from Staging Area
**app_id**: import_genbank_as_genome_from_staging
**entrypoint**: import_genbank_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import GFF3/FASTA file as Genome from Staging Area
**app_id**: import_gff_fasta_as_genome_from_staging
**entrypoint**: upload_fasta_gff_file
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import GFF3/FASTA file as Annotated Metagenome Assembly from Staging Area
**app_id**: import_gff_fasta_as_metagenome_from_staging
**entrypoint**: upload_metagenome_fasta_gff_file
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import SRA File as Reads from Staging Area
**app_id**: import_sra_as_reads_from_staging
**entrypoint**: import_sra_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import SRA File as Reads From Web - v1.0.7
**app_id**: import_sra_as_reads_from_web
**entrypoint**: import_sra_from_web
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import TSV File as Expression Matrix From Staging Area
**app_id**: import_tsv_as_expression_matrix_from_staging
**entrypoint**: import_tsv_as_expression_matrix_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import TSV File as Phenotype Set from Staging Area
**app_id**: import_tsv_as_phenotype_set_from_staging
**entrypoint**: import_tsv_as_phenotype_set_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import Media file (TSV/Excel) from Staging Area
**app_id**: import_tsv_excel_as_media_from_staging
**entrypoint**: import_tsv_or_excel_as_media_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import Paired-End Reads from Staging Area
**app_id**: load_paired_end_reads_from_file
**entrypoint**: upload_fastq_file
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import Paired-End Reads from Web - v1.0.12
**app_id**: load_paired_end_reads_from_URL
**entrypoint**: upload_fastq_file
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Load Single-End Reads From Staging Area
**app_id**: load_single_end_reads_from_file
**entrypoint**: upload_fastq_file
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Import Single-End Reads from Web - v1.0.12
**app_id**: load_single_end_reads_from_URL
**entrypoint**: upload_fastq_file
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Unpack a Compressed File in Staging Area - v1.0.12
**app_id**: unpack_staging_file
**entrypoint**: unpack_staging_file
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Upload File to Staging from Web - v1.0.12
**app_id**: upload_web_file
**entrypoint**: unpack_web_file
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

