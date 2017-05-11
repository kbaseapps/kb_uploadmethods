
package us.kbase.kbuploadmethods;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: WebSRAToReadsResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obj_refs",
    "report_name",
    "report_ref"
})
public class WebSRAToReadsResult {

    @JsonProperty("obj_refs")
    private List<String> objRefs;
    @JsonProperty("report_name")
    private java.lang.String reportName;
    @JsonProperty("report_ref")
    private java.lang.String reportRef;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("obj_refs")
    public List<String> getObjRefs() {
        return objRefs;
    }

    @JsonProperty("obj_refs")
    public void setObjRefs(List<String> objRefs) {
        this.objRefs = objRefs;
    }

    public WebSRAToReadsResult withObjRefs(List<String> objRefs) {
        this.objRefs = objRefs;
        return this;
    }

    @JsonProperty("report_name")
    public java.lang.String getReportName() {
        return reportName;
    }

    @JsonProperty("report_name")
    public void setReportName(java.lang.String reportName) {
        this.reportName = reportName;
    }

    public WebSRAToReadsResult withReportName(java.lang.String reportName) {
        this.reportName = reportName;
        return this;
    }

    @JsonProperty("report_ref")
    public java.lang.String getReportRef() {
        return reportRef;
    }

    @JsonProperty("report_ref")
    public void setReportRef(java.lang.String reportRef) {
        this.reportRef = reportRef;
    }

    public WebSRAToReadsResult withReportRef(java.lang.String reportRef) {
        this.reportRef = reportRef;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((("WebSRAToReadsResult"+" [objRefs=")+ objRefs)+", reportName=")+ reportName)+", reportRef=")+ reportRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
