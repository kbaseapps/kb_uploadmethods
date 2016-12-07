
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
 * <p>Original spec-file type: outParam</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "uploaded"
})
public class OutParam {

    @JsonProperty("uploaded")
    private Long uploaded;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("uploaded")
    public Long getUploaded() {
        return uploaded;
    }

    @JsonProperty("uploaded")
    public void setUploaded(Long uploaded) {
        this.uploaded = uploaded;
    }

    public OutParam withUploaded(Long uploaded) {
        this.uploaded = uploaded;
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
        return ((((("OutParam"+" [uploaded=")+ uploaded)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
