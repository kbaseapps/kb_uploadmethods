import time

from kb_uploadmethods.Utils.ImportSRAUtil import ImportSRAUtil
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class ImportReadsUtil:
    def __init__(self, config):
        self.fastq_importer = UploaderUtil(config)
        self.sra_importer = ImportSRAUtil(config)

    def import_reads_from_staging(self, params):
        self._validte_import_reads_from_staging_params(params)

        if params.get('import_type') == 'FASTQ/FASTA':
            fastq_importer_params = params
            fastq_importer_params['fwd_staging_file_name'] = params.get(
                                                        'fastq_fwd_staging_file_name')
            fastq_importer_params['rev_staging_file_name'] = params.get(
                                                        'fastq_rev_staging_file_name')

            returnVal = self.fastq_importer.upload_fastq_file(fastq_importer_params)
            reportVal = self.sra_importer.generate_report(returnVal['obj_ref'],
                                                            fastq_importer_params)
            returnVal.update(reportVal)
        elif params.get('import_type') == 'SRA':
            sra_importer_params = params
            sra_importer_params['staging_file_subdir_path'] = params.get(
                                                        'sra_staging_file_name')

            returnVal = self.sra_importer.import_sra_from_staging(sra_importer_params)
            reportVal = self.sra_importer.generate_report(returnVal['obj_ref'],
                                                          sra_importer_params)
            returnVal.update(reportVal)

        return returnVal

    def _validte_import_reads_from_staging_params(self, params):
        """
        _validte_import_reads_from_staging_params:
                    validates params passed to import_reads_from_staging method

        """

        # check for required parameters
        for p in ['import_type', 'sequencing_tech', 'name', 'workspace_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

        valide_import_type = ['FASTQ/FASTA', 'SRA']
        if params.get('import_type') not in valide_import_type:
            error_msg = 'Import file type [{}] is not supported. '.format(params.get('import_type'))
            error_msg += 'Please selet one of {}'.format(valide_import_type)
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
           (params.get('fastq_rev_staging_file_name') and params.get('sra_staging_file_name'))):
            error_msg = 'Both SRA and FASTQ/FASTA file given. Please provide one file type only.'
            raise ValueError(error_msg)
