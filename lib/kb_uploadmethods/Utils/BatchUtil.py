
import logging
import json
import os
import uuid
from copy import deepcopy
import traceback
import itertools

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.SetAPIServiceClient import SetAPI
from kb_uploadmethods.Utils.ImportGenbankUtil import ImportGenbankUtil
from kb_uploadmethods.Utils.ImportGFFFastaUtil import ImportGFFFastaUtil
from kb_uploadmethods.Utils.ImportAssemblyUtil import ImportAssemblyUtil


class BatchUtil:

    # staging file prefix
    STAGING_FILE_PREFIX = '/data/bulk/'
    GENBANK_FILE_EXT = ['gbk', 'genbank', 'gbff', 'gb', 'gbf', 'dat']
    GFF_FILE_EXT = ['gff', 'gff3']
    FASTA_FILE_EXT = ['fna', 'fasta', 'fa']

    def _generate_report(self, set_object, sub_objects, workspace_name, failed_files=[],
                         object_type=''):
        """
        _generate_report: generate summary report
        """

        logging.info('start generating report widget')

        objects_created = list()

        if set_object:
            objects_created.append({'ref': set_object,
                                    'description': 'Imported {}Set'.format(object_type)})

        if sub_objects:
            objects_created.extend([{
                'ref': generated_object,
                'description': 'Imported {}Object'.format(object_type)} for generated_object in sub_objects])

        message = ''
        if failed_files:
            message = 'Failed files:\n{}'.format('\n'.join(list(itertools.chain.from_iterable(failed_files))))

        report_params = {'message': message,
                         'objects_created': objects_created,
                         'workspace_name': workspace_name,
                         'report_object_name': 'batch_importer_from_staging_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

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
                    matching_files = [os.path.join(root, file).split('/', 4)[-1]]
                    if associate_file_exts:
                        for associate_file in os.listdir(root):
                            associate_file_name, associate_file_extension = os.path.splitext(
                                                                                associate_file)
                            if (file_name == associate_file_name and
                                    associate_file_extension[1:].lower() in associate_file_exts):
                                matching_files.append(os.path.join(root, associate_file).split('/', 4)[-1])
                    current_dir = root.split('/', 4)[-1].replace('/', '_')
                    found_files.update({file_name + '_' + current_dir: matching_files})

        return found_files

    def _fetch_assembly_files(self, staging_subdir):
        logging.info('start fetching assembly files')
        assembly_files = dict()

        sub_dir = self._get_staging_file_path(self.user_id, staging_subdir)

        fasta_files = self._find_files_end_with(sub_dir, self.FASTA_FILE_EXT)
        assembly_files.update({'fasta': fasta_files})

        return assembly_files

    def _fetch_genome_files(self, staging_subdir):
        logging.info('start fetching genome files')
        genome_files = dict()

        sub_dir = self._get_staging_file_path(self.user_id, staging_subdir)

        genbank_files = self._find_files_end_with(sub_dir, self.GENBANK_FILE_EXT)
        genome_files.update({'genbank': genbank_files})

        gff_fasta_files = self._find_files_end_with(sub_dir, self.GFF_FILE_EXT,
                                                    associate_file_exts=self.FASTA_FILE_EXT)
        genome_files.update({'gff_fasta': gff_fasta_files})

        return genome_files

    def _generate_set_object(self, workspace_name, obj_refs, set_name, set_type):

        logging.info('start saving {} set object'.format(set_type))

        set_ref = None

        if not obj_refs:
            logging.info('skip generating Set due to no sub-object generated')
            return set_ref

        items = [{'ref': obj_ref} for obj_ref in obj_refs]
        set_data = {'description': '{} set generated by batch importer'.format(set_type),
                    'items': items}

        set_save_params = {'data': set_data,
                           'workspace': workspace_name,
                           'output_object_name': set_name}

        try:
            set_ref = getattr(self.set_client,
                              'save_{}_set_v1'.format(set_type))(set_save_params)['set_ref']
        except Exception as e:
            logging.info('caught exception in saving set')
            error_msg = 'ERROR -- {}:\n{}'.format(
                            e,
                            ''.join(traceback.format_exception(None, e, e.__traceback__)))
            raise ValueError(error_msg)

        return set_ref

    def _call_importer(self, params, importer_type):

        obj_ref = None
        try:
            if importer_type == 'genbank':
                obj_ref = self.genbank_import.import_genbank_from_staging(params)['genome_ref']
            elif importer_type == 'gff_fasta':
                obj_ref = self.gff_fasta_import.import_gff_fasta_from_staging(params)['genome_ref']
            elif importer_type == 'assembly':
                obj_ref = self.fasta_import.import_fasta_as_assembly_from_staging(params)['obj_ref']
            else:
                return obj_ref
        except Exception as e:
            logging.info('caught exception in worker')

            error_msg = 'ERROR -- {}:\n{}'.format(
                            e,
                            ''.join(traceback.format_exception(None, e, e.__traceback__)))
            logging.info(error_msg)
        else:
            return obj_ref

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.scratch = config['scratch']
        self.user_id = config['USER_ID']
        self.dfu = DataFileUtil(self.callback_url)
        self.genbank_import = ImportGenbankUtil(config)
        self.gff_fasta_import = ImportGFFFastaUtil(config)
        self.fasta_import = ImportAssemblyUtil(config)
        self.set_client = SetAPI(config['srv-wiz-url'])

    def batch_import_genomes_from_staging(self, params):
        logging.info('--->\nstart importing genomes\n' +
                     'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_batch_import_genomes_from_staging_params(params)

        staging_subdir = params.get('staging_subdir')
        workspace_name = params.get('workspace_name')
        genome_set_name = params.get('genome_set_name')

        genome_files = self._fetch_genome_files(staging_subdir)

        genome_objects = list()
        failed_files = list()

        # import genbank genome
        genbank_files = genome_files.get('genbank')
        if genbank_files:
            for genome_name, genbank_file in genbank_files.items():
                genbank_params = deepcopy(params)
                genbank_params['staging_file_subdir_path'] = genbank_file[0]
                genbank_params['genome_name'] = genome_name

                genome_ref = self._call_importer(genbank_params, 'genbank')

                if genome_ref:
                    genome_objects.append(genome_ref)
                else:
                    failed_files.append(genbank_file)

        # import gff + fasta genome
        gff_fasta_files = genome_files.get('gff_fasta')
        if gff_fasta_files:
            for genome_name, gff_fasta_file in gff_fasta_files.items():
                gff_fasta_params = deepcopy(params)
                gff_file = gff_fasta_file[0]
                gff_fasta_params['gff_file'] = gff_file
                gff_fasta_params['genome_name'] = genome_name
                try:
                    gff_fasta_params['fasta_file'] = gff_fasta_file[1]
                except Exception as e:
                    logging.info('caught exception in worker')
                    logging.info('Unable to find matching FASTA file for: {}'.format(gff_file))
                    failed_files.append(gff_fasta_file)
                else:
                    genome_ref = self._call_importer(gff_fasta_params, 'gff_fasta')

                    if genome_ref:
                        genome_objects.append(genome_ref)
                    else:
                        failed_files.append(gff_fasta_file)

        genome_set_ref = self._generate_set_object(workspace_name, genome_objects,
                                                   genome_set_name, 'genome')

        report_output = self._generate_report(genome_set_ref, genome_objects, workspace_name,
                                              failed_files=failed_files, object_type='Genome ')

        returnVal = {'set_ref': genome_set_ref}

        returnVal.update(report_output)

        return returnVal

    def batch_import_assemblies_from_staging(self, params):
        logging.info('--->\nstart importing assembly\n' +
                     'params:\n{}'.format(json.dumps(params, indent=1)))

        staging_subdir = params.get('staging_subdir')
        workspace_name = params.get('workspace_name')
        assembly_set_name = params.get('assembly_set_name')

        assembly_files = self._fetch_assembly_files(staging_subdir)

        assembly_objects = list()
        failed_files = list()

        # import fasta assembly
        fasta_files = assembly_files.get('fasta')
        if fasta_files:
            for assembly_name, fasta_file in fasta_files.items():
                fasta_params = deepcopy(params)
                fasta_params['staging_file_subdir_path'] = fasta_file[0]
                fasta_params['assembly_name'] = assembly_name

                assembly_ref = self._call_importer(fasta_params, 'assembly')

                if assembly_ref:
                    assembly_objects.append(assembly_ref)
                else:
                    failed_files.append(fasta_file)

        assembly_set_ref = self._generate_set_object(workspace_name, assembly_objects,
                                                     assembly_set_name, 'assembly')

        report_output = self._generate_report(assembly_set_ref, assembly_objects, workspace_name,
                                              failed_files=failed_files, object_type='Assembly ')

        returnVal = {'set_ref': assembly_set_ref}

        returnVal.update(report_output)

        return returnVal
