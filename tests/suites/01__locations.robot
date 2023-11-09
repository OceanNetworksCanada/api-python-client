*** Settings ***
Documentation    01. Locations Test Suite
Resource         ../resources/general.robot


*** Variables ***
&{F_INCL_HILDREN}=     locationCode=SAAN    includeChildren=true
&{F_NO_RESULTS}=       locationCode=SAAN    dateTo=1995-03-24T00:00:01.000Z


*** Test Cases ***

01. Get all locations
    ${data}=        Run method getLocations without filters
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has at least 500 rows

02. Get locations hierarchy
    ${data}=        Run method getLocationHierarchy with filter locationCode="SAAN"
    Elements in ${data}[0] have the expected fields for getLocationHierarchy
    List ${data}[0][children] has at least 2 rows

# Single filters

03. Filter locationCode
    ${data}=        Run method getLocations with filter locationCode="CQSBG"
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has exactly 1 rows
    Field "locationCode" in ${data}[0] holds the value "CQSBG"

04. Filter locationName
    ${data}=        Run method getLocations with filter locationName="Bubbly Gulch"
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has exactly 1 rows
    Field "locationCode" in ${data}[0] holds the value "CQSBG"

05. Filter deviceCategoryCode
    ${data}=        Run method getLocations with filter deviceCategoryCode="CTD"
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has at least 50 rows

06. Filter deviceCode
    ${data}=        Run method getLocations with filter deviceCode="NORTEKADCP9917"
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has at least 1 rows

07. Filter propertyCode
    ${data}=        Run method getLocations with filter propertyCode="co2concentration"
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has at least 1 rows

08. Filter dataProductCode
    ${data}=        Run method getLocations with filter dataProductCode="MP4V"
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has at least 20 rows

09. Filter includeChildren
    ${data}=        Run method getLocations with filters ${F_INCL_HILDREN}
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has at least 30 rows

# Other

10. ISO Date Range
    ${data}=        Run method getLocations from "2014-02-24T00:00:01.000Z" to "2014-03-24T00:00:01.000Z"
    Elements in ${data}[0] have the expected fields for getLocations
    List ${data} has at least 100 rows

11. Wrong locationCode
    Run Keyword And Expect Error    *400*    Run method getLocations with filter locationCode="XYZ123"

12. No locations found
    Run Keyword And Expect Error    *404*    Run method getLocations with filters ${F_NO_RESULTS}