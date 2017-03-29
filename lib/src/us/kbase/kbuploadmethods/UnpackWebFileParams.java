
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
 * <p>Original spec-file type: UnpackWebFileParams</p>
 * <pre>
 * Input parameters for the "unpack_web_file" function.
 *     Required parameters:
 *     workspace_name: workspace name/ID of the object
 *     file_url: file URL
 *     download_type: one of ['Direct Download', 'FTP', 'DropBox', 'Google Drive']
 *     Optional:
 *     urls_to_add_web_unpack: used for parameter-groups. dict of {file_url}
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "file_url",
    "download_type",
    "urls_to_add_web_unpack"
})
public class UnpackWebFileParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("file_url")
    private String fileUrl;
    @JsonProperty("download_type")
    private String downloadType;
    /**
     * <p>Original spec-file type: urls_to_add_web_unpack</p>
     * 
     * 
     */
    @JsonProperty("urls_to_add_web_unpack")
    private UrlsToAddWebUnpack urlsToAddWebUnpack;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public UnpackWebFileParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("file_url")
    public String getFileUrl() {
        return fileUrl;
    }

    @JsonProperty("file_url")
    public void setFileUrl(String fileUrl) {
        this.fileUrl = fileUrl;
    }

    public UnpackWebFileParams withFileUrl(String fileUrl) {
        this.fileUrl = fileUrl;
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

    public UnpackWebFileParams withDownloadType(String downloadType) {
        this.downloadType = downloadType;
        return this;
    }

    /**
     * <p>Original spec-file type: urls_to_add_web_unpack</p>
     * 
     * 
     */
    @JsonProperty("urls_to_add_web_unpack")
    public UrlsToAddWebUnpack getUrlsToAddWebUnpack() {
        return urlsToAddWebUnpack;
    }

    /**
     * <p>Original spec-file type: urls_to_add_web_unpack</p>
     * 
     * 
     */
    @JsonProperty("urls_to_add_web_unpack")
    public void setUrlsToAddWebUnpack(UrlsToAddWebUnpack urlsToAddWebUnpack) {
        this.urlsToAddWebUnpack = urlsToAddWebUnpack;
    }

    public UnpackWebFileParams withUrlsToAddWebUnpack(UrlsToAddWebUnpack urlsToAddWebUnpack) {
        this.urlsToAddWebUnpack = urlsToAddWebUnpack;
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
        return ((((((((((("UnpackWebFileParams"+" [workspaceName=")+ workspaceName)+", fileUrl=")+ fileUrl)+", downloadType=")+ downloadType)+", urlsToAddWebUnpack=")+ urlsToAddWebUnpack)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
