
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
 * <pre>
 * sequencing_tech: sequencing technology
 * name: output reads file name
 * workspace_name: workspace name/ID of the object
 * For files in user's staging area:
 * fwd_staging_file_name: single-end fastq file name or forward/left paired-end fastq file name from user's staging area
 * rev_staging_file_name: reverse/right paired-end fastq file name user's staging area
 * For files from web:
 * download_type: download type for web source fastq file ('Direct Download', 'FTP', 'DropBox', 'Google Drive')
 * fwd_file_url: single-end fastq file URL or forward/left paired-end fastq file URL
 * rev_file_url: reverse/right paired-end fastq file URL
 *  
 * urls_to_add: used for parameter-groups. dict of {fwd_file_url, rev_file_url, name}
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "fwd_staging_file_name",
    "rev_staging_file_name",
    "download_type",
    "fwd_file_url",
    "rev_file_url",
    "sequencing_tech",
    "name",
    "urls_to_add"
})
public class UploadMethodParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("fwd_staging_file_name")
    private String fwdStagingFileName;
    @JsonProperty("rev_staging_file_name")
    private String revStagingFileName;
    @JsonProperty("download_type")
    private String downloadType;
    @JsonProperty("fwd_file_url")
    private String fwdFileUrl;
    @JsonProperty("rev_file_url")
    private String revFileUrl;
    @JsonProperty("sequencing_tech")
    private String sequencingTech;
    @JsonProperty("name")
    private String name;
    /**
     * <p>Original spec-file type: urls_to_add</p>
     * 
     * 
     */
    @JsonProperty("urls_to_add")
    private UrlsToAdd urlsToAdd;
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

    @JsonProperty("fwd_staging_file_name")
    public String getFwdStagingFileName() {
        return fwdStagingFileName;
    }

    @JsonProperty("fwd_staging_file_name")
    public void setFwdStagingFileName(String fwdStagingFileName) {
        this.fwdStagingFileName = fwdStagingFileName;
    }

    public UploadMethodParams withFwdStagingFileName(String fwdStagingFileName) {
        this.fwdStagingFileName = fwdStagingFileName;
        return this;
    }

    @JsonProperty("rev_staging_file_name")
    public String getRevStagingFileName() {
        return revStagingFileName;
    }

    @JsonProperty("rev_staging_file_name")
    public void setRevStagingFileName(String revStagingFileName) {
        this.revStagingFileName = revStagingFileName;
    }

    public UploadMethodParams withRevStagingFileName(String revStagingFileName) {
        this.revStagingFileName = revStagingFileName;
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

    @JsonProperty("fwd_file_url")
    public String getFwdFileUrl() {
        return fwdFileUrl;
    }

    @JsonProperty("fwd_file_url")
    public void setFwdFileUrl(String fwdFileUrl) {
        this.fwdFileUrl = fwdFileUrl;
    }

    public UploadMethodParams withFwdFileUrl(String fwdFileUrl) {
        this.fwdFileUrl = fwdFileUrl;
        return this;
    }

    @JsonProperty("rev_file_url")
    public String getRevFileUrl() {
        return revFileUrl;
    }

    @JsonProperty("rev_file_url")
    public void setRevFileUrl(String revFileUrl) {
        this.revFileUrl = revFileUrl;
    }

    public UploadMethodParams withRevFileUrl(String revFileUrl) {
        this.revFileUrl = revFileUrl;
        return this;
    }

    @JsonProperty("sequencing_tech")
    public String getSequencingTech() {
        return sequencingTech;
    }

    @JsonProperty("sequencing_tech")
    public void setSequencingTech(String sequencingTech) {
        this.sequencingTech = sequencingTech;
    }

    public UploadMethodParams withSequencingTech(String sequencingTech) {
        this.sequencingTech = sequencingTech;
        return this;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    @JsonProperty("name")
    public void setName(String name) {
        this.name = name;
    }

    public UploadMethodParams withName(String name) {
        this.name = name;
        return this;
    }

    /**
     * <p>Original spec-file type: urls_to_add</p>
     * 
     * 
     */
    @JsonProperty("urls_to_add")
    public UrlsToAdd getUrlsToAdd() {
        return urlsToAdd;
    }

    /**
     * <p>Original spec-file type: urls_to_add</p>
     * 
     * 
     */
    @JsonProperty("urls_to_add")
    public void setUrlsToAdd(UrlsToAdd urlsToAdd) {
        this.urlsToAdd = urlsToAdd;
    }

    public UploadMethodParams withUrlsToAdd(UrlsToAdd urlsToAdd) {
        this.urlsToAdd = urlsToAdd;
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
        return ((((((((((((((((((((("UploadMethodParams"+" [workspaceName=")+ workspaceName)+", fwdStagingFileName=")+ fwdStagingFileName)+", revStagingFileName=")+ revStagingFileName)+", downloadType=")+ downloadType)+", fwdFileUrl=")+ fwdFileUrl)+", revFileUrl=")+ revFileUrl)+", sequencingTech=")+ sequencingTech)+", name=")+ name)+", urlsToAdd=")+ urlsToAdd)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
