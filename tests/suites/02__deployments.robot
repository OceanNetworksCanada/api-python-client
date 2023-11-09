*** Settings ***

Documentation    02. Deployments Test Suite
Resource         ../resources/general.robot


*** Variables ***

&{F_NO_RESULTS}=       locationCode=SAAN    dateTo=1995-03-24T00:00:01.000Z


*** Test Cases ***

01. Get all deployments
    ${data}=        Run method getDeployments without filters
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 500 rows

02. Filter locationCode
    [Tags]          runthis
    ${data}=        Run method getDeployments with filter locationCode="CQSBG"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 2 rows

03. Filter deviceCategoryCode
    ${data}=        Run method getDeployments with filter deviceCategoryCode="CTD"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 50 rows

04. Filter deviceCode
    ${data}=        Run method getDeployments with filter deviceCode="NORTEKADCP9917"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 1 rows

05. Filter propertyCode
    ${data}=        Run method getDeployments with filter propertyCode="co2concentration"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 1 rows

06. ISO Date Range
    ${data}=        Run method getDeployments from "2014-02-24T00:00:01.000Z" to "2014-03-24T00:00:01.000Z"
    Elements in ${data}[0] have the expected fields for getDeployments
    List ${data} has at least 100 rows

07. Wrong locationCode
    Run Keyword And Expect Error    *400*    Run method getDeployments with filter locationCode="XYZ123"

08. No deployments found
    Run Keyword And Expect Error    *404*    Run method getDeployments with filters ${F_NO_RESULTS}