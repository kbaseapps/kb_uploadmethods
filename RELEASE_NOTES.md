###Release Notes

**1.0.55**
Add `exact_match_on` field to the GFF Genome uploader.

**1.0.54**
Add `exact_match_on` field to the Genbank uploader.

**1.0.53**
Change casing of the `ui-name` field to sentence case for importers used by the Bulk Import cell.

**1.0.52**
Directly copy files in the scratch folder to staging image. Instead of using staging API.

**1.0.51**
Set valid_ws_types for SRA and interleaved reads import apps

**1.0.50**
Require at least one input file for SRA and non/interleaved reads

**1.0.49**
Add dynamic dropdown boxes for scientific_name ui input to address conflicting scientific_name/taxon_id issues. The dynamic dropdown will connect to the re_api_search service to match the ncbi_taxon_id for the scientific_name user types into the input box.

**1.0.48**
Fix `import_fastq_noninterleaved...` app always specifying `interleaved=true`

**1.0.47**
Add support for uploading files > 2GB to the staging service

**1.0.46**
Fix tests from new UIs for FASTQ/SRA Importers

**1.0.45**
Add github actions tests
Add new FASTQ/SRA Importers

**1.0.44**
fix Dockerfile for gcc error

**1.0.43**
update wrong description for FASTQ/SRA importer
Add file type checking to output of Import FASTQ/SRA file. This will enforce proper file names.

**1.0.42**
replace SBML model importer from fba_tools.sbml_file_to_model to SBMLTools.sbml_importer/integrate_model

**1.0.41**
Updated the contact information for the apps

**1.0.40**
Fixing algorithm to locate correct directory for fastq-dump result

**1.0.39**
Fixing metagenome gff fasta importer outputs and variable names

**1.0.34**
In the Batch Import apps, accept both /user_id and / as valid names of the root directory

**1.0.33**
restore visibility of Batch Import Apps up to beta

**1.0.32**
hiding Batch Import Apps so they can be backtracked to beta where they belong

**1.0.31**
Adding AnnotatedMetagenomeAssembly uploader

**1.0.22**:
Added KBase paper citation in PLOS format

**1.0.19**:
Convert  module to Python 3

**1.0.15**:
Add ConditionSet upload
Make all uploaders use dynamic_dropdown type for staging area uploads

**1.0.9**:
Added icons

**1.0.5**:
Add FBAModel import functions (tsv/excel/sbml)
added KBasePhenotypes.PhenotypeSet importer

**1.0.3**:
replace FBAFileUtil with fba_tools module
