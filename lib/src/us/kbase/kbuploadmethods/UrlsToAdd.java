
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
    "first_fastq_file_url",
    "second_fastq_file_url",
    "reads_file_name"
})
public class UrlsToAdd {

    @JsonProperty("first_fastq_file_url")
    private String firstFastqFileUrl;
    @JsonProperty("second_fastq_file_url")
    private String secondFastqFileUrl;
    @JsonProperty("reads_file_name")
    private String readsFileName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("first_fastq_file_url")
    public String getFirstFastqFileUrl() {
        return firstFastqFileUrl;
    }

    @JsonProperty("first_fastq_file_url")
    public void setFirstFastqFileUrl(String firstFastqFileUrl) {
        this.firstFastqFileUrl = firstFastqFileUrl;
    }

    public UrlsToAdd withFirstFastqFileUrl(String firstFastqFileUrl) {
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

    public UrlsToAdd withSecondFastqFileUrl(String secondFastqFileUrl) {
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

    public UrlsToAdd withReadsFileName(String readsFileName) {
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
        return ((((((((("UrlsToAdd"+" [firstFastqFileUrl=")+ firstFastqFileUrl)+", secondFastqFileUrl=")+ secondFastqFileUrl)+", readsFileName=")+ readsFileName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
