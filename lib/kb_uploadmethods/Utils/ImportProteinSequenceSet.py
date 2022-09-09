
import collections
import json
import logging
import os
import time
import uuid

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from kb_uploadmethods.Utils.UploaderUtil import UploaderUtil
from . import handler_utils

#Additional imports eventually to move to library layer
#import json
#import os
import os.path
from pathlib import Path
import sys
#import uuid
from typing import List, Callable
from collections import Counter
from hashlib import md5

from Bio import SeqIO

#from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace

_WSID = 'workspace_id'
_INPUTS = 'inputs'
_GENOME_REFS = 'genome_refs'
_DESCRIPTION = 'description'
_LOOKUP_GENE_MATCHES = 'lookup_gene_matches'
_MIN_SIMILARITY_THRESHOLD = 'min_similarity_threshold'
_FILTER_NOMATCH = 'filter_nomatch'
_PROTSEQSET_NAME = 'protseqset_name'
_FILE = 'file'
_NODE = 'node'

def _ref(object_info):
    return f'{object_info[6]}/{object_info[0]}/{object_info[4]}'

class ImportProteinSequenceSet:

    def __init__(self, config):
        self.callback_url = config['SDK_CALLBACK_URL']
        self.scratch = os.path.join(config['scratch'], 'import_protseqset_' + str(uuid.uuid4()))
        handler_utils._mkdir_p(self.scratch)
        self.token = config['KB_AUTH_TOKEN']
        self.dfu = DataFileUtil(self.callback_url)
        self.uploader_utils = UploaderUtil(config)
        #Library properties
        self._ws = Workspace()
        self._uuid_gen = Callable[[], uuid.UUID] = lambda: uuid.uuid4()):
        
    def import_fasta_as_protseqset_from_staging(self, params):
        """
          import_fasta_as_protseqset_from_staging: importer for protein sequence set

          required params:
          staging_file_subdir_path - subdirectory file path
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name
          protseqset_name - output ProteinSequenceSet file name
          workspace_name - the name of the workspace it gets saved to.
          
          optional params:
          genome_refs - array of genomes or genome sets whose genes should be mapped to proteins
          lookup_gene_matches - boolean lookup matching genes within KBase reference data
          min_similarity_threshold - minimum identity a gene must have to be mapped
          description - description of the protein sequence set
          filter_nomatch - boolean indicating if proteins for which matches cannot be found should be removed from the set

          return:
          obj_ref: return object reference
        """
        logging.info('--->\nrunning ImportProteinSequenceSet.import_fasta_as_protseqset_from_staging\n'
                     f'params:\n{json.dumps(params, indent=1)}')

        params = self.validate_import_fasta_as_protseqset_from_staging(params)

        download_staging_file_params = {
            'staging_file_subdir_path': params.get('staging_file_subdir_path')
        }
        scratch_file_path = self.dfu.download_staging_file(
                            download_staging_file_params).get('copy_file_path')

        with open(scratch_file_path, 'r') as fasta_file:
            first_line = fasta_file.readline()

        if not first_line.startswith('>'):
            raise ValueError("Expected FASTA record with a '>' as the first character on the first line.")

        file = {
            'path': scratch_file_path
        }
        import_protseqset_params = params
        import_protseqset_params['file'] = file

        ref = self.import_fasta(import_protseqset_params)

        """
        Update the workspace object related meta-data for staged file
        """
        # self.uploader_utils.update_staging_service(params.get('staging_file_subdir_path'), ref)

        returnVal = {'obj_ref': ref}
        return returnVal

    def validate_import_fasta_as_protseqset_from_staging(self, params):
        """
        validate_import_fasta_as_protseqset_from_staging:
                    validates params passed to import_fasta_as_protseqset_from_staging method
        """
        # check for required parameters
        for p in ['staging_file_subdir_path', 'workspace_name', 'protseqset_name']:
            if p not in params:
                raise ValueError(f'"{p}" parameter is required, but missing')
        optional = {
            "genome_refs":[],
            "lookup_gene_matches":1,
            "min_similarity_threshold":1,
            "description":"None",
            "filter_nomatch":0
        }
        for p in optional:
            if p not in params:
                params[p] = optional[p]
        return params

    def generate_html_report(self, protseqset_ref, protseqset_object, params):#CHRIS-TODO
        """
        _generate_html_report: generate html summary report
        """
        logging.info('start generating html report')
        html_report = list()

        tmp_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        handler_utils._mkdir_p(tmp_dir)
        result_file_path = os.path.join(tmp_dir, 'report.html')

        assembly_name = str(assembly_info[1])
        assembly_file = params.get('staging_file_subdir_path')

        overview_data = {
            "ID":protseqset_object["id"],
            "Description":protseqset_object["description"],
            "Protein count":len(protseqset_object["sequences"])
        }
        overview_content = ['<br/><table>\n']
        for key, val in overview_data.items():
            overview_content.append(f'<tr><td><b>{key}</b></td>')
            overview_content.append(f'<td>{val}</td></tr>\n')
        overview_content.append('</table>')
        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template',
                                   'report_template_protseqset.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>*Overview_Content*</p>',''.join(overview_content))
                #report_template = report_template.replace('*PROTSEQSET_DATA*',contig_content)
                result_file.write(report_template)
        result_file.close()
        report_shock_id = self.dfu.file_to_shock({'file_path': tmp_dir,
                                                  'pack': 'zip'})['shock_id']
        html_report.append({'shock_id': report_shock_id,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for Imported Assembly'})
        return html_report

    def generate_report(self, obj_ref, params):
        """
        generate_report: generate summary report

        obj_ref: generated workspace object references. (return of
                                                         import_fasta_as_protseqset_from_staging)
        params:
        staging_file_subdir_path: subdirectory file path
          e.g.
            for file: /data/bulk/user_name/file_name
            staging_file_subdir_path is file_name
            for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
            staging_file_subdir_path is subdir_1/subdir_2/file_name
        workspace_name: workspace name/ID that reads will be stored to

        """
        object_data = self.dfu.get_objects({'object_refs': [obj_ref]})

        report_params = {
            'workspace_name': params.get('workspace_name'),
            'objects_created': [{'ref': obj_ref,
                                 'description': 'Imported Protein Sequence Set'}],
            'report_object_name': f'kb_upload_protseqset_report_{uuid.uuid4()}'}
        
        output_html_files = self.generate_html_report(obj_ref, object_data, params)
        report_params.update({
            'html_links': output_html_files,
            'direct_html_link_index': 0,
            'html_window_height': 375,
        })

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

#####################--Library code starts here--####################
    _VALID_CHARS = "-ACGTUWSMKRYBDHVNX"
    _AMINO_ACID_SPECIFIC_CHARACTERS = "PLIFQE"
    
    def import_fasta(self, params):
        print('validating parameters')
        mass_params = self._set_up_single_params(params)
        return self._import_fasta_mass(mass_params)[0]

    def import_fasta_mass(self, params):
        print('validating parameters')
        self._validate_mass_params(params)
        return self._import_fasta_mass(params)

    def _import_fasta_mass(self, params):
        # TODO TEST with muliple files
        # TODO check that inputs are all either files or shock nodes
        # TODO check inputs generally
        # TODO expose in API
        # For now this is completely serial, but theoretically we could start uploading
        # Blobstore nodes when some fraction of the initial checks are done, start uploading
        # Workspace obects when some fraction of the Blobstore nodes are done, parallelize
        # the file filtering / parsing, etc.
        # For now keep it simple
        # Also note all the assembly data is kept in memory once parsed, but it contains
        # no sequence info and so shouldn't be too huge. Could push to KBase in batches or
        # save to disk if that's an issue
        # We also probably want to add some retries for saving data, but that should go
        # in DataFileUtils if it's not there already
        # Finally, if more than 1G worth of assembly object data is sent to the workspace at once,
        # the call will fail. May need to add some checking / splitting code around this.
        if _FILE in params[_INPUTS][0]:
            input_files = self._stage_file_inputs(params[_INPUTS])
        else:
            input_files = self._stage_blobstore_inputs(params[_INPUTS])

        protseqset_objects = []
        for i in range(len(input_files)):
            # Hmm, all through these printouts we should really put the blobstore node here as
            # well as the file if it exists... wait and see if that code path is still actually
            # used
            print(f'parsing FASTA file: {input_files[i]}')
            data = self._parse_fasta(input_files[i],params[_INPUTS][i])
            print(f' - parsed {len(data["sequences"]} proteins')
            if len(data["sequences"]):
                raise ValueError("The FASTA file contained no valid sequences "
                                 + f"parameter for file {input_files[i]}")
            protseqset_objects.append(data)

        # save to WS and return
        protseqset_infos = self._save_protseqset_objects(params[_WSID],protseqset_objects)
        return [_ref(ai) for ai in protseqset_infos]

    def _parse_fasta(self, fasta_file_path: Path,params):
        """ Parsing protein FASTA and building Protein Set object """

        # TODO TEST this needs more extensive unit testing
        # variables to store running counts of things
        md5_list = []
        object = {
            "description":params["description"],
            "id":params["protseqset_name"],
            "sequence_set_id":params["protseqset_name"],
            "sequences":[],
            "ontology_events":[]
        }
        for record in SeqIO.parse(str(fasta_file_path), "fasta"):
            # SeqRecord(seq=Seq('TTAT...', SingleLetterAlphabet()),
            #           id='gi|113968346|ref|NC_008321.1|',
            #           name='gi|113968346|ref|NC_008321.1|',
            #           description='gi|113968346|ref|NC_008321.1| Shewanella sp. MR-4 chromosome, complete genome',
            #           dbxrefs=[])

            sequence = str(record.seq).upper()
            prot_obj = {
                "id":record.id,
                "sequence_id":record.id,
                "description":record.description[len(record.id):].strip(),
                "sequence":sequence,
                "md5":md5(sequence.encode()).hexdigest(),
                "ontology_terms":[]
            }
            object["sequences"].append(prot_obj)
            md5_list.append(prot_obj["md5"])
            #object_ref
            #object_feature_id
        object["md5"] = md5(",".join(sorted(md5_list)).encode()).hexdigest()
        return object

    def _save_protseqset_objects(self, workspace_id, objects):
        print('Saving Protein Sequence Sets to Workspace')
        sys.stdout.flush()
        ws_inputs = []
        for obj in objects:
            ws_inputs.append({
                'type': 'KBaseSequences.SequenceSet',  #Replace with: KBaseSequences.ProteinSequenceSet
                'data': obj,
                'name': obj["id"]
            })
        return self.dfu.save_objects({'id': workspace_id, 'objects': ws_inputs})

    def _save_files_to_blobstore(self, files: List[Path]):
        print(f'Uploading FASTA files to the Blobstore')
        sys.stdout.flush()
        blob_input = [{'file_path': str(fp), 'make_handle': 1} for fp in files]
        return self.dfu.file_to_shock_mass(blob_input)

    def _stage_file_inputs(self, inputs) -> List[Path]:
        in_files = []
        for inp in inputs:
            if not os.path.isfile(inp[_FILE]):
                raise ValueError(
                    "KBase Sequence Set Utils tried to save an protein sequence set, but the calling "
                    + f"application specified a file ('{inp[_FILE]}') that is missing. "
                    + "Please check the application logs for details.")
            # Ideally we'd have some sort of security check here but the DTN files could
            # be mounted anywhere...
            # TODO check with sysadmin about this - checked, waiting on clear list of safedirs
            fp = Path(inp[_FILE]).resolve(strict=True)
            # make the downstream unpack call unpack into scratch rather than wherever the
            # source file might be
            file_path = self._create_temp_dir() / fp.name
            # symlink doesn't work, because in DFU filemagic doesn't follow symlinks, and so
            # DFU won't unpack symlinked files
            os.link(fp, file_path)
            in_files.append(file_path)
        # extract the file if it is compressed
        # could add a target dir argument to unpack_files, not sure how much work that might be
        fs = [{'file_path': str(fp), 'unpack': 'uncompress'} for fp in in_files]
        unpacked_files = self.dfu.unpack_files(fs)
        return [Path(uf['file_path']) for uf in unpacked_files]

    def _stage_blobstore_inputs(self, inputs) -> List[Path]:
        blob_params = []
        for inp in inputs:
            blob_params.append({
                'shock_id': inp[_NODE],
                'file_path': str(self._create_temp_dir()),
                'unpack': 'uncompress'  # Will throw an error for archives
            })
        dfu_res = self.dfu.shock_to_file_mass(blob_params)
        return [Path(dr['file_path']) for dr in dfu_res]

    def _create_temp_dir(self):
        tmpdir = self.scratch / ("import_fasta_" + str(self._uuid_gen()))
        os.makedirs(tmpdir, exist_ok=True)
        return tmpdir

    def _set_up_single_params(self, params):
        inputs = dict(params)
        ws_id = self._get_int(inputs.pop(_WSID, None), _WSID)
        ws_name = inputs.pop('workspace_name', None)
        if (bool(ws_id) == bool(ws_name)):  # xnor
            raise ValueError(f"Exactly one of a {_WSID} or a workspace_name must be provided")
        if not ws_id:
            print(f"Translating workspace name {ws_name} to a workspace ID. Prefer submitting "
                  + "a workspace ID over a mutable workspace name that may cause race conditions")
            ws_id = self.dfu.ws_name_to_id(params['workspace_name'])

        if not inputs.get(_PROTSEQSET_NAME):
            raise ValueError(f"Required parameter {_PROTSEQSET_NAME} was not defined")

        # one and only one of either 'file' or 'shock_id' is required
        file_ = inputs.pop(_FILE, None)
        shock_id = inputs.pop('shock_id', None)
        if (bool(file_) == bool(shock_id)):  # xnor
            raise ValueError(f"Exactly one of {_FILE} or shock_id is required")
        if file_:
            if not isinstance(file_, dict) or 'path' not in file_:
                raise ValueError('When specifying a FASTA file input, "path" field was '
                                 + f'not defined in "{_FILE}"')
        mass_params = {
            _WSID: ws_id,
            _INPUTS: [inputs]
        }
        if file_:
            inputs[_FILE] = params[_FILE]['path']
        else:
            inputs[_NODE] = params['shock_id']
        return mass_params

    def _validate_mass_params(self, params):
        ws_id = self._get_int(params.get(_WSID), _WSID)
        if not ws_id:
            raise ValueError(f"{_WSID} is required")
        inputs = params.get(_INPUTS)
        if not inputs or type(inputs) != list:
            raise ValueError(f"{_INPUTS} field is required and must be a non-empty list")
        for i, inp in enumerate(inputs, start=1):
            if type(inp) != dict:
                raise ValueError(f"Entry #{i} in {_INPUTS} field is not a mapping as required")
        file_ = inputs[0].get(_FILE)
        if bool(file_) == bool(inputs[0].get(_NODE)):  # xnor
            raise ValueError(f"Entry #1 in {_INPUTS} field must have exactly one of "
                             + f"{_FILE} or {_NODE} specified")
        field = _FILE if file_ else _NODE
        for i, inp in enumerate(inputs, start=1):
            if not inp.get(field):
                raise ValueError(
                    f"Entry #{i} in {_INPUTS} must have a {field} field to match entry #1")
            if not inp.get(_PROTSEQSET_NAME):
                raise ValueError(f"Missing {_PROTSEQSET_NAME} field in {_INPUTS} entry #{i}")

    def _get_int(self, putative_int, name):
        if putative_int is not None:
            if type(putative_int) != int:
                raise ValueError(f"{name} must be an integer, got: {putative_int}")
            if putative_int < 1:
                raise ValueError(f"{name} must be an integer > 0")
        return putative_int