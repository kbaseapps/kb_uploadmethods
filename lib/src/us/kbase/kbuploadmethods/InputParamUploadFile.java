
package us.kbase.kbuploadmethods;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: inputParamUploadFile</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "fastq_file_path",
    "secondary_fastq_file_path",
    "reads_file_name"
})
public class InputParamUploadFile {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("fastq_file_path")
    private List<String> fastqFilePath;
    @JsonProperty("secondary_fastq_file_path")
    private List<String> secondaryFastqFilePath;
    @JsonProperty("reads_file_name")
    private java.lang.String readsFileName;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public InputParamUploadFile withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("fastq_file_path")
    public List<String> getFastqFilePath() {
        return fastqFilePath;
    }

    @JsonProperty("fastq_file_path")
    public void setFastqFilePath(List<String> fastqFilePath) {
        this.fastqFilePath = fastqFilePath;
    }

    public InputParamUploadFile withFastqFilePath(List<String> fastqFilePath) {
        this.fastqFilePath = fastqFilePath;
        return this;
    }

    @JsonProperty("secondary_fastq_file_path")
    public List<String> getSecondaryFastqFilePath() {
        return secondaryFastqFilePath;
    }

    @JsonProperty("secondary_fastq_file_path")
    public void setSecondaryFastqFilePath(List<String> secondaryFastqFilePath) {
        this.secondaryFastqFilePath = secondaryFastqFilePath;
    }

    public InputParamUploadFile withSecondaryFastqFilePath(List<String> secondaryFastqFilePath) {
        this.secondaryFastqFilePath = secondaryFastqFilePath;
        return this;
    }

    @JsonProperty("reads_file_name")
    public java.lang.String getReadsFileName() {
        return readsFileName;
    }

    @JsonProperty("reads_file_name")
    public void setReadsFileName(java.lang.String readsFileName) {
        this.readsFileName = readsFileName;
    }

    public InputParamUploadFile withReadsFileName(java.lang.String readsFileName) {
        this.readsFileName = readsFileName;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((("InputParamUploadFile"+" [workspaceName=")+ workspaceName)+", fastqFilePath=")+ fastqFilePath)+", secondaryFastqFilePath=")+ secondaryFastqFilePath)+", readsFileName=")+ readsFileName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
