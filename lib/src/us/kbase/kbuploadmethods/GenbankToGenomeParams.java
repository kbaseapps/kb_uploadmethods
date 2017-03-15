
package us.kbase.kbuploadmethods;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: GenbankToGenomeParams</p>
 * <pre>
 * import_genbank_from_staging: wrapper method for GenomeFileUtil.genbank_to_genome
 *   required params:
 *   staging_file_subdir_path - subdirectory file path
 *   e.g. 
 *     for file: /data/bulk/user_name/file_name
 *     staging_file_subdir_path is file_name
 *     for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
 *     staging_file_subdir_path is subdir_1/subdir_2/file_name
 *   genome_name - becomes the name of the object
 *   workspace_name - the name of the workspace it gets saved to.
 *   source - Source of the file typically something like RefSeq or Ensembl
 *   optional params:
 *   release - Release or version number of the data 
 *       per example Ensembl has numbered releases of all their data: Release 31
 *   generate_ids_if_needed - If field used for feature id is not there, 
 *       generate ids (default behavior is raising an exception)
 *   genetic_code - Genetic code of organism. Overwrites determined GC from 
 *       taxon object
 *   type - Reference, Representative or User upload
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "staging_file_subdir_path",
    "genome_name",
    "workspace_name",
    "source",
    "release",
    "genetic_code",
    "type",
    "generate_ids_if_needed",
    "exclude_ontologies"
})
public class GenbankToGenomeParams {

    @JsonProperty("staging_file_subdir_path")
    private String stagingFileSubdirPath;
    @JsonProperty("genome_name")
    private String genomeName;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("source")
    private String source;
    @JsonProperty("release")
    private String release;
    @JsonProperty("genetic_code")
    private Long geneticCode;
    @JsonProperty("type")
    private String type;
    @JsonProperty("generate_ids_if_needed")
    private String generateIdsIfNeeded;
    @JsonProperty("exclude_ontologies")
    private String excludeOntologies;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("staging_file_subdir_path")
    public String getStagingFileSubdirPath() {
        return stagingFileSubdirPath;
    }

    @JsonProperty("staging_file_subdir_path")
    public void setStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
    }

    public GenbankToGenomeParams withStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
        return this;
    }

    @JsonProperty("genome_name")
    public String getGenomeName() {
        return genomeName;
    }

    @JsonProperty("genome_name")
    public void setGenomeName(String genomeName) {
        this.genomeName = genomeName;
    }

    public GenbankToGenomeParams withGenomeName(String genomeName) {
        this.genomeName = genomeName;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public GenbankToGenomeParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("source")
    public String getSource() {
        return source;
    }

    @JsonProperty("source")
    public void setSource(String source) {
        this.source = source;
    }

    public GenbankToGenomeParams withSource(String source) {
        this.source = source;
        return this;
    }

    @JsonProperty("release")
    public String getRelease() {
        return release;
    }

    @JsonProperty("release")
    public void setRelease(String release) {
        this.release = release;
    }

    public GenbankToGenomeParams withRelease(String release) {
        this.release = release;
        return this;
    }

    @JsonProperty("genetic_code")
    public Long getGeneticCode() {
        return geneticCode;
    }

    @JsonProperty("genetic_code")
    public void setGeneticCode(Long geneticCode) {
        this.geneticCode = geneticCode;
    }

    public GenbankToGenomeParams withGeneticCode(Long geneticCode) {
        this.geneticCode = geneticCode;
        return this;
    }

    @JsonProperty("type")
    public String getType() {
        return type;
    }

    @JsonProperty("type")
    public void setType(String type) {
        this.type = type;
    }

    public GenbankToGenomeParams withType(String type) {
        this.type = type;
        return this;
    }

    @JsonProperty("generate_ids_if_needed")
    public String getGenerateIdsIfNeeded() {
        return generateIdsIfNeeded;
    }

    @JsonProperty("generate_ids_if_needed")
    public void setGenerateIdsIfNeeded(String generateIdsIfNeeded) {
        this.generateIdsIfNeeded = generateIdsIfNeeded;
    }

    public GenbankToGenomeParams withGenerateIdsIfNeeded(String generateIdsIfNeeded) {
        this.generateIdsIfNeeded = generateIdsIfNeeded;
        return this;
    }

    @JsonProperty("exclude_ontologies")
    public String getExcludeOntologies() {
        return excludeOntologies;
    }

    @JsonProperty("exclude_ontologies")
    public void setExcludeOntologies(String excludeOntologies) {
        this.excludeOntologies = excludeOntologies;
    }

    public GenbankToGenomeParams withExcludeOntologies(String excludeOntologies) {
        this.excludeOntologies = excludeOntologies;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((("GenbankToGenomeParams"+" [stagingFileSubdirPath=")+ stagingFileSubdirPath)+", genomeName=")+ genomeName)+", workspaceName=")+ workspaceName)+", source=")+ source)+", release=")+ release)+", geneticCode=")+ geneticCode)+", type=")+ type)+", generateIdsIfNeeded=")+ generateIdsIfNeeded)+", excludeOntologies=")+ excludeOntologies)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
