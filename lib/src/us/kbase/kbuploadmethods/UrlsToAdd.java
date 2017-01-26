
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
    "name",
    "single_genome",
    "interleaved",
    "insert_size_mean",
    "insert_size_std_dev",
    "read_orientation_outward"
})
public class UrlsToAdd {

    @JsonProperty("fwd_file_url")
    private String fwdFileUrl;
    @JsonProperty("rev_file_url")
    private String revFileUrl;
    @JsonProperty("name")
    private String name;
    @JsonProperty("single_genome")
    private String singleGenome;
    @JsonProperty("interleaved")
    private String interleaved;
    @JsonProperty("insert_size_mean")
    private String insertSizeMean;
    @JsonProperty("insert_size_std_dev")
    private String insertSizeStdDev;
    @JsonProperty("read_orientation_outward")
    private String readOrientationOutward;
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

    @JsonProperty("single_genome")
    public String getSingleGenome() {
        return singleGenome;
    }

    @JsonProperty("single_genome")
    public void setSingleGenome(String singleGenome) {
        this.singleGenome = singleGenome;
    }

    public UrlsToAdd withSingleGenome(String singleGenome) {
        this.singleGenome = singleGenome;
        return this;
    }

    @JsonProperty("interleaved")
    public String getInterleaved() {
        return interleaved;
    }

    @JsonProperty("interleaved")
    public void setInterleaved(String interleaved) {
        this.interleaved = interleaved;
    }

    public UrlsToAdd withInterleaved(String interleaved) {
        this.interleaved = interleaved;
        return this;
    }

    @JsonProperty("insert_size_mean")
    public String getInsertSizeMean() {
        return insertSizeMean;
    }

    @JsonProperty("insert_size_mean")
    public void setInsertSizeMean(String insertSizeMean) {
        this.insertSizeMean = insertSizeMean;
    }

    public UrlsToAdd withInsertSizeMean(String insertSizeMean) {
        this.insertSizeMean = insertSizeMean;
        return this;
    }

    @JsonProperty("insert_size_std_dev")
    public String getInsertSizeStdDev() {
        return insertSizeStdDev;
    }

    @JsonProperty("insert_size_std_dev")
    public void setInsertSizeStdDev(String insertSizeStdDev) {
        this.insertSizeStdDev = insertSizeStdDev;
    }

    public UrlsToAdd withInsertSizeStdDev(String insertSizeStdDev) {
        this.insertSizeStdDev = insertSizeStdDev;
        return this;
    }

    @JsonProperty("read_orientation_outward")
    public String getReadOrientationOutward() {
        return readOrientationOutward;
    }

    @JsonProperty("read_orientation_outward")
    public void setReadOrientationOutward(String readOrientationOutward) {
        this.readOrientationOutward = readOrientationOutward;
    }

    public UrlsToAdd withReadOrientationOutward(String readOrientationOutward) {
        this.readOrientationOutward = readOrientationOutward;
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
        return ((((((((((((((((((("UrlsToAdd"+" [fwdFileUrl=")+ fwdFileUrl)+", revFileUrl=")+ revFileUrl)+", name=")+ name)+", singleGenome=")+ singleGenome)+", interleaved=")+ interleaved)+", insertSizeMean=")+ insertSizeMean)+", insertSizeStdDev=")+ insertSizeStdDev)+", readOrientationOutward=")+ readOrientationOutward)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
