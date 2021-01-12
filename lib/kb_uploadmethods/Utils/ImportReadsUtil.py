import time

from kb_uploadmethods.Utils.ImportSRAUtil import ImportSRAUtil
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print((('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message)))


class ImportReadsUtil:
    def __init__(self, config):
        self.uploader_utils = UploaderUtil(config)
        self.sra_importer = ImportSRAUtil(config)

    def _run_fastq_importer(self, params):
        fastq_importer_params = params
        fastq_importer_params['fwd_staging_file_name'] = params.get(
            'fastq_fwd_staging_file_name')
        fastq_importer_params['rev_staging_file_name'] = params.get(
            'fastq_rev_staging_file_name')

        return_val = self.uploader_utils.upload_fastq_file(fastq_importer_params)

        uploaded_file = params.get('fastq_fwd_staging_file_name')
        if params.get('fastq_rev_staging_file_name') is not None:
            uploaded_file += '\n' + params.get('fastq_rev_staging_file_name')
        fastq_importer_params['uploaded_files'] = [uploaded_file]

        """
        Update the workspace object related meta-data for staged file
        """
        self.uploader_utils.update_staging_service(params.get('fastq_fwd_staging_file_name'),
                                                   return_val['obj_ref'])

        if params.get('fastq_rev_staging_file_name') is not None:
            self.uploader_utils.update_staging_service(params.get('fastq_rev_staging_file_name'),
                                                       return_val['obj_ref'])

        report_val = self.sra_importer.generate_report([return_val['obj_ref']],
                                                       fastq_importer_params)
        return_val.update(report_val)
        return return_val

    def _run_sra_importer(self, params):
        sra_importer_params = params
        sra_importer_params['staging_file_subdir_path'] = params.get(
            'sra_staging_file_name')

        return_val = self.sra_importer.import_sra_from_staging(sra_importer_params)

        sra_importer_params['uploaded_files'] = [params.get('sra_staging_file_name')]

        """
        Update the workspace object related meta-data for staged file
        """
        self.uploader_utils.update_staging_service(params.get('sra_staging_file_name'),
                                                   return_val['obj_ref'])

        report_val = self.sra_importer.generate_report([return_val['obj_ref']],
                                                       sra_importer_params)
        return_val.update(report_val)
        return return_val

    def import_reads_from_staging(self, params):
        """
        Check to see if the params are valid and then run the correct importer
        based on the import type
        """
        self._validate_import_reads_from_staging_params(params)
        if params.get('import_type') == 'FASTQ/FASTA':
            return self._run_fastq_importer(params)
        elif params.get('import_type') == 'SRA':
            return self._run_sra_importer(params)
        else:
            raise Exception("Unrecognized type. Must be one of FASTQ/FASTA, or SRA")

    def _validate_import_reads_from_staging_params(self, params):
        """
        _validate_import_reads_from_staging_params:
                    validates params passed to import_reads_from_staging method

        """
        # check for required parameters
        for p in ['import_type', 'sequencing_tech', 'name', 'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        valid_import_types = ['FASTQ/FASTA', 'SRA']
        if params.get('import_type') not in valid_import_types:
            error_msg = 'Import file type [{}] is not supported. '.format(params.get('import_type'))
            error_msg += 'Please select one of {}'.format(valid_import_types)
            raise ValueError(error_msg)

        if (params.get('import_type') == 'FASTQ/FASTA' and
                not params.get('fastq_fwd_staging_file_name')):
            error_msg = 'FASTQ/FASTA input file type selected. But missing FASTQ/FASTA file.'
            raise ValueError(error_msg)

        if (params.get('import_type') == 'SRA' and
                not params.get('sra_staging_file_name')):
            error_msg = 'SRA input file type selected. But missing SRA file.'
            raise ValueError(error_msg)

        if ((params.get('fastq_fwd_staging_file_name') and params.get('sra_staging_file_name')) or
                (params.get('fastq_rev_staging_file_name') and params.get(
                    'sra_staging_file_name'))):
            error_msg = 'Both SRA and FASTQ/FASTA file given. Please provide one file type only.'
            raise ValueError(error_msg)
