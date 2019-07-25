*** Settings ***
Documentation    Data Product Discovery Test Suite
Suite Setup      Inital Setup
Resource         ../resources/general.robot


*** Variables ***
&{F_NO_RESULTS}=       locationCode=SAAN    deviceCategoryCode=POWER_SUPPLY


*** Test Cases ***

Get all data products
    ${data}=        Run method getDataProducts without filters
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 100 rows

# Single filters

Filter dataProductCode
    ${data}=        Run method getDataProducts with filter dataProductCode="CPD"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has exactly 1 rows
    Field "dataProductCode" in ${data}[0] holds the value "CPD"

Filter extension
    ${data}=        Run method getDataProducts with filter extension="cor"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has exactly 1 rows
    Field "dataProductCode" in ${data}[0] holds the value "CPD"

Filter locationCode
    ${data}=        Run method getDataProducts with filter locationCode="SAAN"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 1 rows

Filter deviceCategoryCode
    ${data}=        Run method getDataProducts with filter deviceCategoryCode="CTD"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 20 rows

Filter deviceCode
    ${data}=        Run method getDataProducts with filter deviceCode="BC_POD1_AD2M"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 5 rows

Filter propertyCode
    ${data}=        Run method getDataProducts with filter propertyCode="oxygen"
    Elements in ${data}[0] have the expected fields for getDataProducts
    List ${data} has at least 10 rows

# Other

Wrong dataProductCode
    Run Keyword And Expect Error    *400*    Run method getDataProducts with filter dataProductCode="XYZ321"

No data products found
    ${data}=        Run method getDataProducts with filters ${F_NO_RESULTS}
    List ${data} is empty
