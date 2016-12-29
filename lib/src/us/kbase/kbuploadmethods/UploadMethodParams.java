
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
 * <p>Original spec-file type: UploadMethodParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "first_fastq_file_name",
    "second_fastq_file_name",
    "download_type",
    "first_fastq_file_url",
    "second_fastq_file_url",
    "reads_file_name"
})
public class UploadMethodParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("first_fastq_file_name")
    private String firstFastqFileName;
    @JsonProperty("second_fastq_file_name")
    private String secondFastqFileName;
    @JsonProperty("download_type")
    private String downloadType;
    @JsonProperty("first_fastq_file_url")
    private String firstFastqFileUrl;
    @JsonProperty("second_fastq_file_url")
    private String secondFastqFileUrl;
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

    public UploadMethodParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("first_fastq_file_name")
    public String getFirstFastqFileName() {
        return firstFastqFileName;
    }

    @JsonProperty("first_fastq_file_name")
    public void setFirstFastqFileName(String firstFastqFileName) {
        this.firstFastqFileName = firstFastqFileName;
    }

    public UploadMethodParams withFirstFastqFileName(String firstFastqFileName) {
        this.firstFastqFileName = firstFastqFileName;
        return this;
    }

    @JsonProperty("second_fastq_file_name")
    public String getSecondFastqFileName() {
        return secondFastqFileName;
    }

    @JsonProperty("second_fastq_file_name")
    public void setSecondFastqFileName(String secondFastqFileName) {
        this.secondFastqFileName = secondFastqFileName;
    }

    public UploadMethodParams withSecondFastqFileName(String secondFastqFileName) {
        this.secondFastqFileName = secondFastqFileName;
        return this;
    }

    @JsonProperty("download_type")
    public String getDownloadType() {
        return downloadType;
    }

    @JsonProperty("download_type")
    public void setDownloadType(String downloadType) {
        this.downloadType = downloadType;
    }

    public UploadMethodParams withDownloadType(String downloadType) {
        this.downloadType = downloadType;
        return this;
    }

    @JsonProperty("first_fastq_file_url")
    public String getFirstFastqFileUrl() {
        return firstFastqFileUrl;
    }

    @JsonProperty("first_fastq_file_url")
    public void setFirstFastqFileUrl(String firstFastqFileUrl) {
        this.firstFastqFileUrl = firstFastqFileUrl;
    }

    public UploadMethodParams withFirstFastqFileUrl(String firstFastqFileUrl) {
        this.firstFastqFileUrl = firstFastqFileUrl;
        return this;
    }

    @JsonProperty("second_fastq_file_url")
    public String getSecondFastqFileUrl() {
        return secondFastqFileUrl;
    }

    @JsonProperty("second_fastq_file_url")
    public void setSecondFastqFileUrl(String secondFastqFileUrl) {
        this.secondFastqFileUrl = secondFastqFileUrl;
    }

    public UploadMethodParams withSecondFastqFileUrl(String secondFastqFileUrl) {
        this.secondFastqFileUrl = secondFastqFileUrl;
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

    public UploadMethodParams withReadsFileName(String readsFileName) {
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
        return ((((((((((((((((("UploadMethodParams"+" [workspaceName=")+ workspaceName)+", firstFastqFileName=")+ firstFastqFileName)+", secondFastqFileName=")+ secondFastqFileName)+", downloadType=")+ downloadType)+", firstFastqFileUrl=")+ firstFastqFileUrl)+", secondFastqFileUrl=")+ secondFastqFileUrl)+", readsFileName=")+ readsFileName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
