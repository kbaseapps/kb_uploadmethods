
import logging
import json
import os

from installed_clients.DataFileUtilClient import DataFileUtil


class BatchUtil:

    # staging file prefix
    STAGING_FILE_PREFIX = '/data/bulk/'
    GENBANK_FILE_EXT = ['gbk', 'genbank', 'gbff']
    GFF_FILE_EXT = ['gff']
    FASTA_FILE_EXT = ['fna', 'fasta', 'fa']

    def _get_staging_file_path(self, token_user, staging_file_subdir_path):
        """
        _get_staging_file_path: return staging area file path

        directory pattern: /data/bulk/user_name/file_name

        """

        return os.path.join(self.STAGING_FILE_PREFIX, token_user,
                            staging_file_subdir_path.strip('/'))

    def _validate_batch_import_genomes_from_staging_params(self, params):
        """
        _validate_batch_import_genomes_from_staging_params:
                    validates params passed to batch_import_genomes_from_staging method
        """
        # check for required parameters
        for p in ['staging_subdir', 'workspace_name', 'genome_set_name']:
            if p not in params:
                raise ValueError('"' + p + '" parameter is required, but missing')

    def _find_files_end_with(self, sub_dir, file_exts, associate_file_exts=[]):
        found_files = dict()

        for root, dirs, files in os.walk(sub_dir):
            for file in files:
                file_name, file_extension = os.path.splitext(file)
                if file_extension[1:].lower() in file_exts:
                    matching_files = [os.path.join(root, file)]
                    if associate_file_exts:
                        print(os.listdir(root))
                        for associate_file in os.listdir(root):
                            associate_file_name, associate_file_extension = os.path.splitext(
                                                                                associate_file)
                            if (file_name == associate_file_name and
                                associate_file_extension[1:].lower() in associate_file_exts):
                                matching_files.append(os.path.join(root, associate_file))

                    found_files.update({file_name: matching_files})

        return found_files

    def _fetch_genome_files(self, staging_subdir):
        genome_files = dict()

        sub_dir = self._get_staging_file_path(self.user_id, staging_subdir)

        genbank_files = self._find_files_end_with(sub_dir, self.GENBANK_FILE_EXT)
        genome_files.update({'genbank': genbank_files})

        gff_fasta_files = self._find_files_end_with(sub_dir, self.GFF_FILE_EXT,
                                                    associate_file_ext=self.FASTA_FILE_EXT)
        genome_files.update({'gff_fasta': gff_fasta_files})

        return genome_files

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = config['scratch']
        self.user_id = config['USER_ID']
        self.dfu = DataFileUtil(self.callback_url)

    def batch_import_genomes_from_staging(self, params):
        logging.info('--->\nstart importing genomes\n' +
                     'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_batch_import_genomes_from_staging_params(params)

        staging_subdir = params.get('staging_subdir')

        genome_files = self._fetch_genome_files(staging_subdir)

        reportVal = dict()

        return reportVal
