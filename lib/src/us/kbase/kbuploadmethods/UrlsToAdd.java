
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
 * <p>Original spec-file type: urls_to_add</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "fwd_file_url",
    "rev_file_url",
    "name"
})
public class UrlsToAdd {

    @JsonProperty("fwd_file_url")
    private String fwdFileUrl;
    @JsonProperty("rev_file_url")
    private String revFileUrl;
    @JsonProperty("name")
    private String name;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("fwd_file_url")
    public String getFwdFileUrl() {
        return fwdFileUrl;
    }

    @JsonProperty("fwd_file_url")
    public void setFwdFileUrl(String fwdFileUrl) {
        this.fwdFileUrl = fwdFileUrl;
    }

    public UrlsToAdd withFwdFileUrl(String fwdFileUrl) {
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

    public UrlsToAdd withRevFileUrl(String revFileUrl) {
        this.revFileUrl = revFileUrl;
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

    public UrlsToAdd withName(String name) {
        this.name = name;
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
        return ((((((((("UrlsToAdd"+" [fwdFileUrl=")+ fwdFileUrl)+", revFileUrl=")+ revFileUrl)+", name=")+ name)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
