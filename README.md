# kb_uploadmethods

[![Build Status](https://travis-ci.org/tgu/kb_uploadmethods.svg?branch=master)](https://travis-ci.org/tgu/kb_uploadmethods)  
[Release Notes](RELEASE_NOTES.md)

## Description
This module implements [KBase](https://www.kbase.us) apps that are used to transform data files into KBase data objects for use in analysis. This also includes a few apps for adding external files to the user's [staging area](https://docs.kbase.us/getting-started/narrative/add-data#uploading-data-from-external-sources), and manipulating them there.

See [here](https://docs.kbase.us/data/upload-download-guide/uploads) for more information on uploading data to KBase.

## Development
This module was created using the KBase SDK. See the [documentation](https://kbase.github.io/kb_sdk_docs/) for more detail. Apps are mostly broken down into submodules. Instructions for setting up a local development environment can be found [here](https://kbase.github.io/kb_sdk_docs/tutorial/2_install.html) (note that [Docker](https://www.docker.com) is required).

The main entrypoint is in `lib/kb_uploadmethods/kb_uploadmethodsImpl.py`. Individual apps in that module use one or more utility module to handle different file types. These are all under `lib/kb_uploadmethods/Utils`. Add a new Util module if you're adding an uploader for a new data type.

## Testing
This module can be tested with the following steps, common to all KBase SDK modules.
1. Install the [KBase SDK](https://kbase.github.io/kb_sdk_docs/).
2. Fetch this module and navigate to it from the console.
3. Run `kb-sdk test` once - this will initialize the `test_local/test.cfg` file.
4. Populate the `test_local/test.cfg` file with a KBase authentication token (see [here](https://kbase.github.io/kb_sdk_docs/tutorial/3_initialize.html?highlight=token#set-up-your-developer-credentials) for details). 
5. Run `kb-sdk test` again.

Once steps 1-4 have been run once, you can just run `kb-sdk test` to run the test suite any time.

## Apps

Each app is listed below with the following format:
**Display name** - what the user sees - links to module doc page, if available
**app id**: id - how the app is identified to the system, including the directory under ui/narrative/methods  
**entrypoint**: function - name of the function that gets run in this module, as described in `kb_uploadmethods.spec`  
**output type**: typed object(s) created  

### [Batch Import Assembly from Staging Area](https://narrative.kbase.us/#catalog/apps/kb_uploadmethods/batch_import_assembly_from_staging)
* **app id**: batch_import_assembly_from_staging  
* **entrypoint**: batch_import_assemblies_from_staging  
* **description**: Import FASTA files from your staging area into your Narrative as an Assembly data object.  
* **input file type**: FASTA
* **output type**: KBaseSets.AssemblySet

### [Batch Import Genome from Staging Area](https://narrative.kbase.us/#catalog/apps/kb_uploadmethods/batch_import_genome_from_staging)
* **app id**: batch_import_genome_from_staging  
* **entrypoint**: batch_import_genomes_from_staging  
* **description:**: Import files (Genbank or GFF + FASTA) from your staging area into your Narrative as a Genome data object  
* **input file types**: Genbank, GFF with FASTA
* **output type**: KBaseSearch.GenomeSet

### [Import TSV/Excel File as Attribute Mapping from Staging Area](https://narrative.kbase.us/#catalog/apps/kb_uploadmethods/import_attribute_mapping_from_staging)
* **app id**: import_attribute_mapping_from_staging  
* **entrypoint**: import_attribute_mapping_from_staging  
* **description**: Import a TSV or Excel file from your staging area into your Narrative as an Attribute Mapping data object.
* **input file types**: TSV, Excel
* **output type**: KBaseExperiments.AttributeMapping

### [Import JSON File as EscherMap from Staging Area](https://narrative.kbase.us/#catalog/apps/kb_uploadmethods/import_eschermap_from_staging)
* **app id**: import_eschermap_from_staging
* **entrypoint**: import_eschermap_from_staging
* **description**: Import a JSON file from your staging area into your Narrative as an KBaseFBA.EscherMap data object.
* **input file type**: JSON (format not specified)
* **output type**: KBaseFBA.EscherMap

### [Import FASTA File as Assembly from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_fasta_as_assembly_from_staging)
* **app id**: import_fasta_as_assembly_from_staging
* **entrypoint**: import_fasta_as_assembly_from_staging
* **description**: Import a FASTA file from your staging area into your Narrative as an Assembly data object.
* **input file type**: FASTA
* **output type**: KBaseGenomeAnnotations.Assembly

### [Import FASTQ/SRA File as Reads from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_fastq_sra_as_reads_from_staging)
* **app id**: import_fastq_sra_as_reads_from_staging
* **entrypoint**: import_reads_from_staging
* **description**: Import a FASTQ or SRA file into your Narrative as a Reads data object.
* **input file types**: FASTQ, SRA
* **output type**: KBaseFile.SingleEndLibrary or KBaseFile.PairedEndLibrary

### [Import TSV/XLS/SBML File as an FBAModel from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_file_as_fba_model_from_staging)
* **app id**: import_file_as_fba_model_from_staging
* **entrypoint**: import_file_as_fba_model_from_staging
* **description**: Import a file in TSV, XLS (Excel) or SBML format from your staging area into your Narrative as an FBAModel.
* **input file types**: TSV, Excel, SBML
* **output type**: KBaseFBA.FBAModel

### [Import GenBank File as Genome from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_genbank_as_genome_from_staging)
* **app id**: import_genbank_as_genome_from_staging
* **entrypoint**: import_genbank_from_staging
* **description**: Import a GenBank file from your staging area into your Narrative as a Genome data object.
* **input file types**: Genbank
* **output type**: KBaseGenomes.Genome

### [Import GFF3/FASTA file as Genome from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_gff_fasta_as_genome_from_staging)
* **app id**: import_gff_fasta_as_genome_from_staging
* **entrypoint**: upload_fasta_gff_file
* **description**: Import a GFF or FASTA file from your staging area into your Narrative as a Genome data object. 
* **input file types**: GFF3 and FASTA
* **output type**: KBaseGenomes.Genome

### [Import GFF3/FASTA file as Annotated Metagenome Assembly from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_gff_fasta_as_metagenome_from_staging)
* **app id**: import_gff_fasta_as_metagenome_from_staging
* **entrypoint**: upload_metagenome_fasta_gff_file
* **description**: Import a GFF or FASTA file from your staging area into your Narrative as an annotated metagenome data object.
* **input file types**: GFF3 and FASTA
* **output type**: KBaseMetagenomes.AnnotatedMetagenomeAssembly

### [Import SRA File as Reads From Web - v1.0.7](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_sra_as_reads_from_web)
* **app id**: import_sra_as_reads_from_web
* **entrypoint**: import_sra_from_web
* **description**: This App allows the user to load SRA format read libraries directly into the workspace from sources on the web. In addition to standard HTTP and anonymous FTP links, the user may also obtain files from Google drive and Dropbox links.
* **input file type**: SRA
* **output type**: KBaseFile.SingleEndLibrary or KBaseFile.PairedEndLibrary

### [Import TSV File as Expression Matrix From Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_tsv_as_expression_matrix_from_staging)
* **app id**: import_tsv_as_expression_matrix_from_staging
* **entrypoint**: import_tsv_as_expression_matrix_from_staging
* **description**: Import a tab-delimited file from your staging area into your Narrative as an Expression Matrix.
* **input file type**: TSV
* **output type**: KBaseFeatureValues.ExpressionMatrix

### [Import TSV File as Phenotype Set from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_tsv_as_phenotype_set_from_staging)
* **app id**: import_tsv_as_phenotype_set_from_staging
* **entrypoint**: import_tsv_as_phenotype_set_from_staging
* **description**: Import a tab-delimited file in your staging area as a Phenotype Set.
* **input file type**: TSV
* **output type**: KBasePhenotypes.PhenotypeSet

### [Import Media file (TSV/Excel) from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_tsv_excel_as_media_from_staging)
* **app id**: import_tsv_excel_as_media_from_staging
* **entrypoint**: import_tsv_or_excel_as_media_from_staging
* **description**: Import Media file (TSV/Excel) from your staging area.
* **input file types**: TSV, Excel
* **output type**: KBaseBiochem.Media

### [Import Paired-End Reads from Web - v1.0.12](https://narrative.kbase.us/#catalog/apps/kb_uploadmethods/load_paired_end_reads_from_URL)
* **app id**: load_paired_end_reads_from_URL
* **entrypoint**: upload_fastq_file
* **description**: This App allows users to load FASTQ format paired-end read libraries directly into the workspace from sources on the web. In addition to standard HTTP and anonymous FTP links, the user may also obtain files from Google drive and Dropbox links.
* **input file types**: FASTQ, FASTA
* **output type**: KBaseFile.PairedEndLibrary 

### [Import Single-End Reads from Web - v1.0.12](https://narrative.kbase.us/#catalog/apps/kb_uploadmethods/load_single_end_reads_from_URL)
* **app id**: load_single_end_reads_from_URL
* **entrypoint**: upload_fastq_file
* **description**: This App allows users to load FASTQ format single-end read libraries directly into the workspace from sources on the web. In addition to standard HTTP and anonymous FTP links, the user may also obtain files from Google drive and Dropbox links.
* **input file types**: FASTQ, FASTA
* **output type**: KBaseFile.SingleEndLibrary

### [Unpack a Compressed File in Staging Area - v1.0.12](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/unpack_staging_file)
* **app id**: unpack_staging_file
* **entrypoint**: unpack_staging_file
* **description**: This App allows users to unpack a compressed file in the staging area. Recognizable compressed files include .zip, .gz, .bz2, .tar, .tar.gz, and .tar.bz2.
* **input file types**: any compressed file
* **output type**: none, this creates one or more new files in the staging area

### [Upload File to Staging from Web - v1.0.12](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/upload_web_file)
* **app id**: upload_web_file
* **entrypoint**: unpack_web_file
* **description**: This App allows users to upload a data file (which may be compressed) from a web URL to the staging area. If the file is compressed (.gz or .zip), it will automatically be uncompressed. It is possible, and indeed encouraged to make use of folders when uploading compressed archives of files. These folders are leveraged by downstream batch processing Apps and enable users to run tools on every file in the folder. We strongly recommend using this method to move large amounts of data easily into KBase because the transfer mechanism is less likely to be interrupted (versus uploading directly from your laptop). Note that both Box and DropBox offer a mechanism to share private files temporarily using links that are only accessible to someone who know what the link address is.
* **input file types**: any
* **output type**: none, adds one or more files to the staging area

### (not in use) [Import SRA File as Reads from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/import_sra_as_reads_from_staging)
* replaced by the "Import FASTQ/SRA File as Reads from Staging Area" app
* **app id**: import_sra_as_reads_from_staging
* **entrypoint**: import_sra_from_staging
* **description**: Import an SRA file from your staging area into your Narrative as a Reads object.
* **input file type**: SRA
* **output type**: KBaseFile.SingleEndLibrary or KBaseFile.PairedEndLibrary

### (not in use) [Import Paired-End Reads from Staging Area](https://narrative.kbase.us/#appcatalog/app/kb_uploadmethods/load_paired_end_reads_from_file)
* replaced by the "Import FASTQ/SRA File as Reads from Staging Area" app
* **app id**: load_paired_end_reads_from_file
* **entrypoint**: upload_fastq_file
* **description**: Import FASTA or FASTQ files as paired-end reads from your staging area.
* **input file types**: FASTA, FASTQ
* **output type**: KBaseFile.PairedEndLibrary

### (not in use) [Load Single-End Reads From Staging Area](https://narrative.kbase.us/#catalog/apps/kb_uploadmethods/load_single_end_reads_from_file)
* replaced by the "Import FASTQ/SRA File as Reads from Staging Area" app
* **app id**: load_single_end_reads_from_file
* **entrypoint**: upload_fastq_file
* **description**: Upload a single-end reads library from a FASTQ or FASTA file in your staging area.
* **input file types**: FASTA, FASTQ
* **output type**: KBaseFile.SingleEndLibrary
