
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
 * <p>Original spec-file type: UnpackStagingFileParams</p>
 * <pre>
 * Input parameters for the "unpack_staging_file" function.
 *       Required parameters:
 *       staging_file_subdir_path: subdirectory file path
 *       e.g. 
 *         for file: /data/bulk/user_name/file_name
 *         staging_file_subdir_path is file_name
 *         for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
 *         staging_file_subdir_path is subdir_1/subdir_2/file_name
 *       workspace_name: workspace name/ID of the object
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "staging_file_subdir_path"
})
public class UnpackStagingFileParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("staging_file_subdir_path")
    private String stagingFileSubdirPath;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public UnpackStagingFileParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("staging_file_subdir_path")
    public String getStagingFileSubdirPath() {
        return stagingFileSubdirPath;
    }

    @JsonProperty("staging_file_subdir_path")
    public void setStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
    }

    public UnpackStagingFileParams withStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
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
        return ((((((("UnpackStagingFileParams"+" [workspaceName=")+ workspaceName)+", stagingFileSubdirPath=")+ stagingFileSubdirPath)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
