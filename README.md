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
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2

### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
### Batch Import Assembly from Staging Area
**app_id**: batch_import_genome_from_staging
**entrypoint**: batch_import_assemblies_from_staging
**inputs**
* input 1
* input 2

**outputs**
* output 1
* output 2
