*** Settings ***
Documentation    Deployments Test Suite
Suite Setup      Inital Setup
Resource         ../resources/general.robot


*** Variables ***
&{F_NO_RESULTS}=       locationCode=SAAN    dateTo=1995-03-24T00:00:01.000Z


*** Test Cases ***

Get all deployments
    ${data}=        Run method getDeployments without filters
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 500 rows

# Single filters

Filter locationCode
    [Tags]          runthis
    ${data}=        Run method getDeployments with filter locationCode="CQSBG"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 2 rows

Filter deviceCategoryCode
    ${data}=        Run method getDeployments with filter deviceCategoryCode="CTD"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 50 rows

Filter deviceCode
    ${data}=        Run method getDeployments with filter deviceCode="NORTEKADCP9917"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 1 rows

Filter propertyCode
    ${data}=        Run method getDeployments with filter propertyCode="co2concentration"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 1 rows

ISO Date Range
    ${data}=        Run method getDeployments from "2014-02-24T00:00:01.000Z" to "2014-03-24T00:00:01.000Z"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 100 rows

Wrong locationCode
    Run Keyword And Expect Error    *400*    Run method getDeployments with filter locationCode="XYZ123"

No deployments found
    ${data}=        Run method getDeployments with filters ${F_NO_RESULTS}
    List ${data} is empty