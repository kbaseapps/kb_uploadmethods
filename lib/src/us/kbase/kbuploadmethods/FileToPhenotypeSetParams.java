
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
 * <p>Original spec-file type: FileToPhenotypeSetParams</p>
 * <pre>
 * required params:
 * staging_file_subdir_path: subdirectory file path
 * e.g.
 *   for file: /data/bulk/user_name/file_name
 *   staging_file_subdir_path is file_name
 *   for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
 *   staging_file_subdir_path is subdir_1/subdir_2/file_name
 * phenotype_set_name: output PhenotypeSet object name
 * workspace_name: workspace name/ID of the object
 * optional:
 * genome: Genome object that contains features referenced by the Phenotype Set
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "staging_file_subdir_path",
    "workspace_name",
    "phenotype_set_name",
    "genome"
})
public class FileToPhenotypeSetParams {

    @JsonProperty("staging_file_subdir_path")
    private String stagingFileSubdirPath;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("phenotype_set_name")
    private String phenotypeSetName;
    @JsonProperty("genome")
    private String genome;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("staging_file_subdir_path")
    public String getStagingFileSubdirPath() {
        return stagingFileSubdirPath;
    }

    @JsonProperty("staging_file_subdir_path")
    public void setStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
    }

    public FileToPhenotypeSetParams withStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
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

    public FileToPhenotypeSetParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("phenotype_set_name")
    public String getPhenotypeSetName() {
        return phenotypeSetName;
    }

    @JsonProperty("phenotype_set_name")
    public void setPhenotypeSetName(String phenotypeSetName) {
        this.phenotypeSetName = phenotypeSetName;
    }

    public FileToPhenotypeSetParams withPhenotypeSetName(String phenotypeSetName) {
        this.phenotypeSetName = phenotypeSetName;
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

    public FileToPhenotypeSetParams withGenome(String genome) {
        this.genome = genome;
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
        return ((((((((((("FileToPhenotypeSetParams"+" [stagingFileSubdirPath=")+ stagingFileSubdirPath)+", workspaceName=")+ workspaceName)+", phenotypeSetName=")+ phenotypeSetName)+", genome=")+ genome)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
