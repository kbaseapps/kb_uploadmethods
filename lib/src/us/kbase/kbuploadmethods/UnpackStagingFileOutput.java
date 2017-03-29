
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
 * <p>Original spec-file type: UnpackStagingFileOutput</p>
 * <pre>
 * Results from the unpack_staging_file function.
 *     unpacked_file_path: unpacked file path(s) in staging area
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "unpacked_file_path"
})
public class UnpackStagingFileOutput {

    @JsonProperty("unpacked_file_path")
    private String unpackedFilePath;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("unpacked_file_path")
    public String getUnpackedFilePath() {
        return unpackedFilePath;
    }

    @JsonProperty("unpacked_file_path")
    public void setUnpackedFilePath(String unpackedFilePath) {
        this.unpackedFilePath = unpackedFilePath;
    }

    public UnpackStagingFileOutput withUnpackedFilePath(String unpackedFilePath) {
        this.unpackedFilePath = unpackedFilePath;
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
        return ((((("UnpackStagingFileOutput"+" [unpackedFilePath=")+ unpackedFilePath)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
