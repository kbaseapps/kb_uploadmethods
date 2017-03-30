
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
 * Required:
 * genome_name: output genome object name
 * workspace_name: workspace name/ID of the object
 * For staging area:
 * fasta_file: fasta file containing assembled contigs/chromosomes
 * gff_file: gff file containing predicted gene models and corresponding features
 * Optional params:
 * scientific_name: proper name for species, key for taxonomy lookup. Default to 'unknown_taxon'
 * source: Source Of The GenBank File. Default to 'User'
 * taxon_wsname - where the reference taxons are. Default to 'ReferenceTaxons'
 * taxon_reference - if defined, will try to link the Genome to the specified taxonomy object
 * release: Release Or Version Of The Source Data
 * genetic_code: Genetic Code For The Organism
 * type: 'Reference', 'User upload', 'Representative'
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "fasta_file",
    "gff_file",
    "genome_name",
    "workspace_name",
    "scientific_name",
    "source",
    "taxon_wsname",
    "taxon_reference",
    "release",
    "genetic_code",
    "type"
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
    @JsonProperty("scientific_name")
    private String scientificName;
    @JsonProperty("source")
    private String source;
    @JsonProperty("taxon_wsname")
    private String taxonWsname;
    @JsonProperty("taxon_reference")
    private String taxonReference;
    @JsonProperty("release")
    private String release;
    @JsonProperty("genetic_code")
    private Long geneticCode;
    @JsonProperty("type")
    private String type;
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

    @JsonProperty("scientific_name")
    public String getScientificName() {
        return scientificName;
    }

    @JsonProperty("scientific_name")
    public void setScientificName(String scientificName) {
        this.scientificName = scientificName;
    }

    public UploadFastaGFFMethodParams withScientificName(String scientificName) {
        this.scientificName = scientificName;
        return this;
    }

    @JsonProperty("source")
    public String getSource() {
        return source;
    }

    @JsonProperty("source")
    public void setSource(String source) {
        this.source = source;
    }

    public UploadFastaGFFMethodParams withSource(String source) {
        this.source = source;
        return this;
    }

    @JsonProperty("taxon_wsname")
    public String getTaxonWsname() {
        return taxonWsname;
    }

    @JsonProperty("taxon_wsname")
    public void setTaxonWsname(String taxonWsname) {
        this.taxonWsname = taxonWsname;
    }

    public UploadFastaGFFMethodParams withTaxonWsname(String taxonWsname) {
        this.taxonWsname = taxonWsname;
        return this;
    }

    @JsonProperty("taxon_reference")
    public String getTaxonReference() {
        return taxonReference;
    }

    @JsonProperty("taxon_reference")
    public void setTaxonReference(String taxonReference) {
        this.taxonReference = taxonReference;
    }

    public UploadFastaGFFMethodParams withTaxonReference(String taxonReference) {
        this.taxonReference = taxonReference;
        return this;
    }

    @JsonProperty("release")
    public String getRelease() {
        return release;
    }

    @JsonProperty("release")
    public void setRelease(String release) {
        this.release = release;
    }

    public UploadFastaGFFMethodParams withRelease(String release) {
        this.release = release;
        return this;
    }

    @JsonProperty("genetic_code")
    public Long getGeneticCode() {
        return geneticCode;
    }

    @JsonProperty("genetic_code")
    public void setGeneticCode(Long geneticCode) {
        this.geneticCode = geneticCode;
    }

    public UploadFastaGFFMethodParams withGeneticCode(Long geneticCode) {
        this.geneticCode = geneticCode;
        return this;
    }

    @JsonProperty("type")
    public String getType() {
        return type;
    }

    @JsonProperty("type")
    public void setType(String type) {
        this.type = type;
    }

    public UploadFastaGFFMethodParams withType(String type) {
        this.type = type;
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
        return ((((((((((((((((((((((((("UploadFastaGFFMethodParams"+" [fastaFile=")+ fastaFile)+", gffFile=")+ gffFile)+", genomeName=")+ genomeName)+", workspaceName=")+ workspaceName)+", scientificName=")+ scientificName)+", source=")+ source)+", taxonWsname=")+ taxonWsname)+", taxonReference=")+ taxonReference)+", release=")+ release)+", geneticCode=")+ geneticCode)+", type=")+ type)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
