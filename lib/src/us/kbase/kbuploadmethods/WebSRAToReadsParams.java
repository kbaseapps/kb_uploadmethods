
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
 * <p>Original spec-file type: WebSRAToReadsParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "download_type",
    "sra_urls_to_add"
})
public class WebSRAToReadsParams {

    @JsonProperty("download_type")
    private String downloadType;
    /**
     * <p>Original spec-file type: sra_urls_to_add</p>
     * <pre>
     * download_type: download type for web source fastq file
     *                    ('Direct Download', 'FTP', 'DropBox', 'Google Drive')
     * sra_urls_to_add: dict of SRA file URLs
     *     required params:
     *     file_url: SRA file URL
     *     sequencing_tech: sequencing technology
     *     name: output reads file name
     *     workspace_name: workspace name/ID of the object
     *     Optional Params:
     *     single_genome: whether the reads are from a single genome or a metagenome.
     *     insert_size_mean: mean (average) insert length
     *     insert_size_std_dev: standard deviation of insert lengths
     *     read_orientation_outward: whether reads in a pair point outward
     * </pre>
     * 
     */
    @JsonProperty("sra_urls_to_add")
    private SraUrlsToAdd sraUrlsToAdd;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("download_type")
    public String getDownloadType() {
        return downloadType;
    }

    @JsonProperty("download_type")
    public void setDownloadType(String downloadType) {
        this.downloadType = downloadType;
    }

    public WebSRAToReadsParams withDownloadType(String downloadType) {
        this.downloadType = downloadType;
        return this;
    }

    /**
     * <p>Original spec-file type: sra_urls_to_add</p>
     * <pre>
     * download_type: download type for web source fastq file
     *                    ('Direct Download', 'FTP', 'DropBox', 'Google Drive')
     * sra_urls_to_add: dict of SRA file URLs
     *     required params:
     *     file_url: SRA file URL
     *     sequencing_tech: sequencing technology
     *     name: output reads file name
     *     workspace_name: workspace name/ID of the object
     *     Optional Params:
     *     single_genome: whether the reads are from a single genome or a metagenome.
     *     insert_size_mean: mean (average) insert length
     *     insert_size_std_dev: standard deviation of insert lengths
     *     read_orientation_outward: whether reads in a pair point outward
     * </pre>
     * 
     */
    @JsonProperty("sra_urls_to_add")
    public SraUrlsToAdd getSraUrlsToAdd() {
        return sraUrlsToAdd;
    }

    /**
     * <p>Original spec-file type: sra_urls_to_add</p>
     * <pre>
     * download_type: download type for web source fastq file
     *                    ('Direct Download', 'FTP', 'DropBox', 'Google Drive')
     * sra_urls_to_add: dict of SRA file URLs
     *     required params:
     *     file_url: SRA file URL
     *     sequencing_tech: sequencing technology
     *     name: output reads file name
     *     workspace_name: workspace name/ID of the object
     *     Optional Params:
     *     single_genome: whether the reads are from a single genome or a metagenome.
     *     insert_size_mean: mean (average) insert length
     *     insert_size_std_dev: standard deviation of insert lengths
     *     read_orientation_outward: whether reads in a pair point outward
     * </pre>
     * 
     */
    @JsonProperty("sra_urls_to_add")
    public void setSraUrlsToAdd(SraUrlsToAdd sraUrlsToAdd) {
        this.sraUrlsToAdd = sraUrlsToAdd;
    }

    public WebSRAToReadsParams withSraUrlsToAdd(SraUrlsToAdd sraUrlsToAdd) {
        this.sraUrlsToAdd = sraUrlsToAdd;
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
        return ((((((("WebSRAToReadsParams"+" [downloadType=")+ downloadType)+", sraUrlsToAdd=")+ sraUrlsToAdd)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
