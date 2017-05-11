
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
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "file_url",
    "sequencing_tech",
    "name",
    "workspace_name",
    "single_genome",
    "insert_size_mean",
    "insert_size_std_dev",
    "read_orientation_outward"
})
public class SraUrlsToAdd {

    @JsonProperty("file_url")
    private String fileUrl;
    @JsonProperty("sequencing_tech")
    private String sequencingTech;
    @JsonProperty("name")
    private String name;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("single_genome")
    private String singleGenome;
    @JsonProperty("insert_size_mean")
    private String insertSizeMean;
    @JsonProperty("insert_size_std_dev")
    private String insertSizeStdDev;
    @JsonProperty("read_orientation_outward")
    private String readOrientationOutward;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("file_url")
    public String getFileUrl() {
        return fileUrl;
    }

    @JsonProperty("file_url")
    public void setFileUrl(String fileUrl) {
        this.fileUrl = fileUrl;
    }

    public SraUrlsToAdd withFileUrl(String fileUrl) {
        this.fileUrl = fileUrl;
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

    public SraUrlsToAdd withSequencingTech(String sequencingTech) {
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

    public SraUrlsToAdd withName(String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public SraUrlsToAdd withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
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

    public SraUrlsToAdd withSingleGenome(String singleGenome) {
        this.singleGenome = singleGenome;
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

    public SraUrlsToAdd withInsertSizeMean(String insertSizeMean) {
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

    public SraUrlsToAdd withInsertSizeStdDev(String insertSizeStdDev) {
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

    public SraUrlsToAdd withReadOrientationOutward(String readOrientationOutward) {
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
        return ((((((((((((((((((("SraUrlsToAdd"+" [fileUrl=")+ fileUrl)+", sequencingTech=")+ sequencingTech)+", name=")+ name)+", workspaceName=")+ workspaceName)+", singleGenome=")+ singleGenome)+", insertSizeMean=")+ insertSizeMean)+", insertSizeStdDev=")+ insertSizeStdDev)+", readOrientationOutward=")+ readOrientationOutward)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
