
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
 * <p>Original spec-file type: FileToMatrixParams</p>
 * <pre>
 * required params:
 * staging_file_subdir_path: subdirectory file path
 * e.g. 
 *   for file: /data/bulk/user_name/file_name
 *   staging_file_subdir_path is file_name
 *   for file: /data/bulk/user_name/subdir_1/subdir_2/file_name
 *   staging_file_subdir_path is subdir_1/subdir_2/file_name
 * matrix_name: output Expressin Matirx file name
 * workspace_name: workspace name/ID of the object
 * genome_ref: optional reference to a Genome object that will be
 *     used for mapping feature IDs to
 * fill_missing_values: optional flag for filling in missing 
 *       values in matrix (default value is false)
 * data_type: optional filed, value is one of 'untransformed',
 *       'log2_level', 'log10_level', 'log2_ratio', 'log10_ratio' or
 *       'unknown' (last one is default value)
 * data_scale: optional parameter (default value is '1.0')
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "staging_file_subdir_path",
    "workspace_name",
    "matrix_name",
    "genome_ref",
    "fill_missing_values",
    "data_type",
    "data_scale"
})
public class FileToMatrixParams {

    @JsonProperty("staging_file_subdir_path")
    private String stagingFileSubdirPath;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("matrix_name")
    private String matrixName;
    @JsonProperty("genome_ref")
    private String genomeRef;
    @JsonProperty("fill_missing_values")
    private Long fillMissingValues;
    @JsonProperty("data_type")
    private String dataType;
    @JsonProperty("data_scale")
    private String dataScale;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("staging_file_subdir_path")
    public String getStagingFileSubdirPath() {
        return stagingFileSubdirPath;
    }

    @JsonProperty("staging_file_subdir_path")
    public void setStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
    }

    public FileToMatrixParams withStagingFileSubdirPath(String stagingFileSubdirPath) {
        this.stagingFileSubdirPath = stagingFileSubdirPath;
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

    public FileToMatrixParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("matrix_name")
    public String getMatrixName() {
        return matrixName;
    }

    @JsonProperty("matrix_name")
    public void setMatrixName(String matrixName) {
        this.matrixName = matrixName;
    }

    public FileToMatrixParams withMatrixName(String matrixName) {
        this.matrixName = matrixName;
        return this;
    }

    @JsonProperty("genome_ref")
    public String getGenomeRef() {
        return genomeRef;
    }

    @JsonProperty("genome_ref")
    public void setGenomeRef(String genomeRef) {
        this.genomeRef = genomeRef;
    }

    public FileToMatrixParams withGenomeRef(String genomeRef) {
        this.genomeRef = genomeRef;
        return this;
    }

    @JsonProperty("fill_missing_values")
    public Long getFillMissingValues() {
        return fillMissingValues;
    }

    @JsonProperty("fill_missing_values")
    public void setFillMissingValues(Long fillMissingValues) {
        this.fillMissingValues = fillMissingValues;
    }

    public FileToMatrixParams withFillMissingValues(Long fillMissingValues) {
        this.fillMissingValues = fillMissingValues;
        return this;
    }

    @JsonProperty("data_type")
    public String getDataType() {
        return dataType;
    }

    @JsonProperty("data_type")
    public void setDataType(String dataType) {
        this.dataType = dataType;
    }

    public FileToMatrixParams withDataType(String dataType) {
        this.dataType = dataType;
        return this;
    }

    @JsonProperty("data_scale")
    public String getDataScale() {
        return dataScale;
    }

    @JsonProperty("data_scale")
    public void setDataScale(String dataScale) {
        this.dataScale = dataScale;
    }

    public FileToMatrixParams withDataScale(String dataScale) {
        this.dataScale = dataScale;
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
        return ((((((((((((((((("FileToMatrixParams"+" [stagingFileSubdirPath=")+ stagingFileSubdirPath)+", workspaceName=")+ workspaceName)+", matrixName=")+ matrixName)+", genomeRef=")+ genomeRef)+", fillMissingValues=")+ fillMissingValues)+", dataType=")+ dataType)+", dataScale=")+ dataScale)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
