
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
 * <p>Original spec-file type: inputParamUploadFile</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "fastq_file_name",
    "secondary_fastq_file_name",
    "fastq_file_url",
    "secondary_fastq_file_url",
    "reads_file_name"
})
public class InputParamUploadFile {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("fastq_file_name")
    private String fastqFileName;
    @JsonProperty("secondary_fastq_file_name")
    private String secondaryFastqFileName;
    @JsonProperty("fastq_file_url")
    private String fastqFileUrl;
    @JsonProperty("secondary_fastq_file_url")
    private String secondaryFastqFileUrl;
    @JsonProperty("reads_file_name")
    private String readsFileName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public InputParamUploadFile withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("fastq_file_name")
    public String getFastqFileName() {
        return fastqFileName;
    }

    @JsonProperty("fastq_file_name")
    public void setFastqFileName(String fastqFileName) {
        this.fastqFileName = fastqFileName;
    }

    public InputParamUploadFile withFastqFileName(String fastqFileName) {
        this.fastqFileName = fastqFileName;
        return this;
    }

    @JsonProperty("secondary_fastq_file_name")
    public String getSecondaryFastqFileName() {
        return secondaryFastqFileName;
    }

    @JsonProperty("secondary_fastq_file_name")
    public void setSecondaryFastqFileName(String secondaryFastqFileName) {
        this.secondaryFastqFileName = secondaryFastqFileName;
    }

    public InputParamUploadFile withSecondaryFastqFileName(String secondaryFastqFileName) {
        this.secondaryFastqFileName = secondaryFastqFileName;
        return this;
    }

    @JsonProperty("fastq_file_url")
    public String getFastqFileUrl() {
        return fastqFileUrl;
    }

    @JsonProperty("fastq_file_url")
    public void setFastqFileUrl(String fastqFileUrl) {
        this.fastqFileUrl = fastqFileUrl;
    }

    public InputParamUploadFile withFastqFileUrl(String fastqFileUrl) {
        this.fastqFileUrl = fastqFileUrl;
        return this;
    }

    @JsonProperty("secondary_fastq_file_url")
    public String getSecondaryFastqFileUrl() {
        return secondaryFastqFileUrl;
    }

    @JsonProperty("secondary_fastq_file_url")
    public void setSecondaryFastqFileUrl(String secondaryFastqFileUrl) {
        this.secondaryFastqFileUrl = secondaryFastqFileUrl;
    }

    public InputParamUploadFile withSecondaryFastqFileUrl(String secondaryFastqFileUrl) {
        this.secondaryFastqFileUrl = secondaryFastqFileUrl;
        return this;
    }

    @JsonProperty("reads_file_name")
    public String getReadsFileName() {
        return readsFileName;
    }

    @JsonProperty("reads_file_name")
    public void setReadsFileName(String readsFileName) {
        this.readsFileName = readsFileName;
    }

    public InputParamUploadFile withReadsFileName(String readsFileName) {
        this.readsFileName = readsFileName;
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
        return ((((((((((((((("InputParamUploadFile"+" [workspaceName=")+ workspaceName)+", fastqFileName=")+ fastqFileName)+", secondaryFastqFileName=")+ secondaryFastqFileName)+", fastqFileUrl=")+ fastqFileUrl)+", secondaryFastqFileUrl=")+ secondaryFastqFileUrl)+", readsFileName=")+ readsFileName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
