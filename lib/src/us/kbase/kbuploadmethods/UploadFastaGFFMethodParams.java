
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
 * <p>Original spec-file type: UploadFastaGFFMethodParams</p>
 * <pre>
 * genome_name: output genome object name
 * workspace_name: workspace name/ID of the object
 * For staging area:
 * fasta_file: fasta file containing assembled contigs/chromosomes
 * gff_file: gff file containing predicted gene models and corresponding features
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "fasta_file",
    "gff_file",
    "genome_name",
    "workspace_name"
})
public class UploadFastaGFFMethodParams {

    @JsonProperty("fasta_file")
    private String fastaFile;
    @JsonProperty("gff_file")
    private String gffFile;
    @JsonProperty("genome_name")
    private String genomeName;
    @JsonProperty("workspace_name")
    private String workspaceName;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("fasta_file")
    public String getFastaFile() {
        return fastaFile;
    }

    @JsonProperty("fasta_file")
    public void setFastaFile(String fastaFile) {
        this.fastaFile = fastaFile;
    }

    public UploadFastaGFFMethodParams withFastaFile(String fastaFile) {
        this.fastaFile = fastaFile;
        return this;
    }

    @JsonProperty("gff_file")
    public String getGffFile() {
        return gffFile;
    }

    @JsonProperty("gff_file")
    public void setGffFile(String gffFile) {
        this.gffFile = gffFile;
    }

    public UploadFastaGFFMethodParams withGffFile(String gffFile) {
        this.gffFile = gffFile;
        return this;
    }

    @JsonProperty("genome_name")
    public String getGenomeName() {
        return genomeName;
    }

    @JsonProperty("genome_name")
    public void setGenomeName(String genomeName) {
        this.genomeName = genomeName;
    }

    public UploadFastaGFFMethodParams withGenomeName(String genomeName) {
        this.genomeName = genomeName;
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

    public UploadFastaGFFMethodParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
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
        return ((((((((((("UploadFastaGFFMethodParams"+" [fastaFile=")+ fastaFile)+", gffFile=")+ gffFile)+", genomeName=")+ genomeName)+", workspaceName=")+ workspaceName)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
