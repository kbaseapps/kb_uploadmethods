
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
 * <p>Original spec-file type: UploadReadsParams</p>
 * <pre>
 * sequencing_tech: sequencing technology
 * name: output reads file name
 * workspace_name: workspace name/ID of the object
 * import_type: either FASTQ or SRA
 * For files in user's staging area:
 * fastq_fwd_or_sra_staging_file_name: single-end fastq file name Or forward/left paired-end fastq file name from user's staging area Or SRA staging file 
 * fastq_rev_staging_file_name: reverse/right paired-end fastq file name user's staging area
 * e.g. 
 *   for file: /data/bulk/user_name/file_name
 *   staging_file_subdir_path is file_name
 *   for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
 *   staging_file_subdir_path is subdir_1/subdir_2/file_name
 * Optional Params:
 * single_genome: whether the reads are from a single genome or a metagenome.
 * interleaved: whether reads is interleaved
 * insert_size_mean: mean (average) insert length
 * insert_size_std_dev: standard deviation of insert lengths
 * read_orientation_outward: whether reads in a pair point outward
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "import_type",
    "fastq_fwd_staging_file_name",
    "fastq_rev_staging_file_name",
    "sra_staging_file_name",
    "sequencing_tech",
    "workspace_name",
    "name",
    "single_genome",
    "interleaved",
    "insert_size_mean",
    "insert_size_std_dev",
    "read_orientation_outward"
})
public class UploadReadsParams {

    @JsonProperty("import_type")
    private String importType;
    @JsonProperty("fastq_fwd_staging_file_name")
    private String fastqFwdStagingFileName;
    @JsonProperty("fastq_rev_staging_file_name")
    private String fastqRevStagingFileName;
    @JsonProperty("sra_staging_file_name")
    private String sraStagingFileName;
    @JsonProperty("sequencing_tech")
    private String sequencingTech;
    @JsonProperty("workspace_name")
    private String workspaceName;
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

    @JsonProperty("import_type")
    public String getImportType() {
        return importType;
    }

    @JsonProperty("import_type")
    public void setImportType(String importType) {
        this.importType = importType;
    }

    public UploadReadsParams withImportType(String importType) {
        this.importType = importType;
        return this;
    }

    @JsonProperty("fastq_fwd_staging_file_name")
    public String getFastqFwdStagingFileName() {
        return fastqFwdStagingFileName;
    }

    @JsonProperty("fastq_fwd_staging_file_name")
    public void setFastqFwdStagingFileName(String fastqFwdStagingFileName) {
        this.fastqFwdStagingFileName = fastqFwdStagingFileName;
    }

    public UploadReadsParams withFastqFwdStagingFileName(String fastqFwdStagingFileName) {
        this.fastqFwdStagingFileName = fastqFwdStagingFileName;
        return this;
    }

    @JsonProperty("fastq_rev_staging_file_name")
    public String getFastqRevStagingFileName() {
        return fastqRevStagingFileName;
    }

    @JsonProperty("fastq_rev_staging_file_name")
    public void setFastqRevStagingFileName(String fastqRevStagingFileName) {
        this.fastqRevStagingFileName = fastqRevStagingFileName;
    }

    public UploadReadsParams withFastqRevStagingFileName(String fastqRevStagingFileName) {
        this.fastqRevStagingFileName = fastqRevStagingFileName;
        return this;
    }

    @JsonProperty("sra_staging_file_name")
    public String getSraStagingFileName() {
        return sraStagingFileName;
    }

    @JsonProperty("sra_staging_file_name")
    public void setSraStagingFileName(String sraStagingFileName) {
        this.sraStagingFileName = sraStagingFileName;
    }

    public UploadReadsParams withSraStagingFileName(String sraStagingFileName) {
        this.sraStagingFileName = sraStagingFileName;
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

    public UploadReadsParams withSequencingTech(String sequencingTech) {
        this.sequencingTech = sequencingTech;
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

    public UploadReadsParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
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

    public UploadReadsParams withName(String name) {
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

    public UploadReadsParams withSingleGenome(String singleGenome) {
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

    public UploadReadsParams withInterleaved(String interleaved) {
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

    public UploadReadsParams withInsertSizeMean(String insertSizeMean) {
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

    public UploadReadsParams withInsertSizeStdDev(String insertSizeStdDev) {
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

    public UploadReadsParams withReadOrientationOutward(String readOrientationOutward) {
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
        return ((((((((((((((((((((((((((("UploadReadsParams"+" [importType=")+ importType)+", fastqFwdStagingFileName=")+ fastqFwdStagingFileName)+", fastqRevStagingFileName=")+ fastqRevStagingFileName)+", sraStagingFileName=")+ sraStagingFileName)+", sequencingTech=")+ sequencingTech)+", workspaceName=")+ workspaceName)+", name=")+ name)+", singleGenome=")+ singleGenome)+", interleaved=")+ interleaved)+", insertSizeMean=")+ insertSizeMean)+", insertSizeStdDev=")+ insertSizeStdDev)+", readOrientationOutward=")+ readOrientationOutward)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
