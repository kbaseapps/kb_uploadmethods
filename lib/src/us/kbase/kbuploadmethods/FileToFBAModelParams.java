
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
 * <p>Original spec-file type: FileToFBAModelParams</p>
 * <pre>
 * required params:
 * model_file: subdirectory file path for model file
 * e.g.
 *   for file: /data/bulk/user_name/file_name
 *   staging_file_subdir_path is file_name
 *   for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
 *   staging_file_subdir_path is subdir_1/subdir_2/file_name
 * compounds_file: same as above for compound (only used for tsv)
 * file_type: one of "tsv", "excel", "sbml"
 * genome: the associated species genome
 * biomasses: one or more biomass reactions in model
 * model_name: output FBAModel object name
 * workspace_name: workspace name/ID of the object
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "model_file",
    "compounds_file",
    "file_type",
    "genome",
    "biomass",
    "model_name",
    "workspace_name"
})
public class FileToFBAModelParams {

    @JsonProperty("model_file")
    private String modelFile;
    @JsonProperty("compounds_file")
    private String compoundsFile;
    @JsonProperty("file_type")
    private String fileType;
    @JsonProperty("genome")
    private String genome;
    @JsonProperty("biomass")
    private String biomass;
    @JsonProperty("model_name")
    private String modelName;
    @JsonProperty("workspace_name")
    private String workspaceName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("model_file")
    public String getModelFile() {
        return modelFile;
    }

    @JsonProperty("model_file")
    public void setModelFile(String modelFile) {
        this.modelFile = modelFile;
    }

    public FileToFBAModelParams withModelFile(String modelFile) {
        this.modelFile = modelFile;
        return this;
    }

    @JsonProperty("compounds_file")
    public String getCompoundsFile() {
        return compoundsFile;
    }

    @JsonProperty("compounds_file")
    public void setCompoundsFile(String compoundsFile) {
        this.compoundsFile = compoundsFile;
    }

    public FileToFBAModelParams withCompoundsFile(String compoundsFile) {
        this.compoundsFile = compoundsFile;
        return this;
    }

    @JsonProperty("file_type")
    public String getFileType() {
        return fileType;
    }

    @JsonProperty("file_type")
    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public FileToFBAModelParams withFileType(String fileType) {
        this.fileType = fileType;
        return this;
    }

    @JsonProperty("genome")
    public String getGenome() {
        return genome;
    }

    @JsonProperty("genome")
    public void setGenome(String genome) {
        this.genome = genome;
    }

    public FileToFBAModelParams withGenome(String genome) {
        this.genome = genome;
        return this;
    }

    @JsonProperty("biomass")
    public String getBiomass() {
        return biomass;
    }

    @JsonProperty("biomass")
    public void setBiomass(String biomass) {
        this.biomass = biomass;
    }

    public FileToFBAModelParams withBiomass(String biomass) {
        this.biomass = biomass;
        return this;
    }

    @JsonProperty("model_name")
    public String getModelName() {
        return modelName;
    }

    @JsonProperty("model_name")
    public void setModelName(String modelName) {
        this.modelName = modelName;
    }

    public FileToFBAModelParams withModelName(String modelName) {
        this.modelName = modelName;
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

    public FileToFBAModelParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
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
        return ((((((((((((((((("FileToFBAModelParams"+" [modelFile=")+ modelFile)+", compoundsFile=")+ compoundsFile)+", fileType=")+ fileType)+", genome=")+ genome)+", biomass=")+ biomass)+", modelName=")+ modelName)+", workspaceName=")+ workspaceName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
