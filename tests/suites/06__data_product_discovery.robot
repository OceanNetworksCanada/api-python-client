*** Settings ***
Documentation    06. Data Product Discovery Test Suite
Resource         ../resources/general.robot


*** Variables ***

&{F_NO_RESULTS}=       locationCode=SAAN    deviceCategoryCode=POWER_SUPPLY


*** Test Cases ***

01. Get all data products
    ${data}=        Run method getDataProducts without filters
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 100 rows

02. Filter dataProductCode
    ${data}=        Run method getDataProducts with filter dataProductCode="CPD"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has exactly 1 rows
    Field "dataProductCode" in ${data}[0] holds the value "CPD"

03. Filter extension
    ${data}=        Run method getDataProducts with filter extension="cor"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has exactly 2 rows
    Field "extension" in ${data}[0] holds the value "cor"

04. Filter locationCode
    ${data}=        Run method getDataProducts with filter locationCode="SAAN"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 1 rows

05. Filter deviceCategoryCode
    ${data}=        Run method getDataProducts with filter deviceCategoryCode="CTD"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 20 rows

06. Filter deviceCode
    ${data}=        Run method getDataProducts with filter deviceCode="BC_POD1_AD2M"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 5 rows

07. Filter propertyCode
    ${data}=        Run method getDataProducts with filter propertyCode="oxygen"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 10 rows

08. Wrong dataProductCode
    Run Keyword And Expect Error    *400*    Run method getDataProducts with filter dataProductCode="XYZ321"

09. No data products found
    Run Keyword And Expect Error    *404*    Run method getDataProducts with filters ${F_NO_RESULTS}
