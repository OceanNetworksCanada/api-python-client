*** Settings ***
Documentation    Properties Test Suite
Suite Setup      Inital Setup
Resource         ../resources/general.robot


*** Variables ***
&{F_NO_RESULTS}=       locationCode=SAAN    deviceCategoryCode=POWER_SUPPLY


*** Test Cases ***

Get all properties
    ${data}=        Run method getProperties without filters
    Elements in ${data}[0] have the expected fields for getProperties
    List ${data} has at least 150 rows

# Single filters

Filter propertyCode
    ${data}=        Run method getProperties with filter propertyCode="absolutehumidity"
    Elements in ${data}[0] have the expected fields for getProperties
    List ${data} has exactly 1 rows
    Field "propertyCode" in ${data}[0] holds the value "absolutehumidity"

Filter propertyName
    ${data}=        Run method getProperties with filter propertyName="Bender Electrical Resistance"
    Elements in ${data}[0] have the expected fields for getProperties
    List ${data} has exactly 1 rows
    Field "propertyCode" in ${data}[0] holds the value "benderelectricalresistance"

Filter description
    ${data}=        Run method getProperties with filter description="Kurtosis Statistical Analysis"
    Elements in ${data}[0] have the expected fields for getProperties
    List ${data} has exactly 1 rows
    Field "propertyCode" in ${data}[0] holds the value "kurtosisstatisticalanalysis"

Filter locationCode
    ${data}=        Run method getProperties with filter locationCode="ROVMP"
    Elements in ${data}[0] have the expected fields for getProperties
    List ${data} has at least 1 rows

Filter deviceCategoryCode
    ${data}=        Run method getProperties with filter deviceCategoryCode="CTD"
    Elements in ${data}[0] have the expected fields for getProperties
    List ${data} has at least 10 rows

Filter deviceCode
    ${data}=        Run method getProperties with filter deviceCode="ALECACTW-CAR0014"
    Elements in ${data}[0] have the expected fields for getProperties
    List ${data} has at least 3 rows

# Other

Wrong propertyCode
    Run Keyword And Expect Error    *400*    Run method getProperties with filter propertyCode="XYZ321"


No properties found
    ${data}=        Run method getProperties with filters ${F_NO_RESULTS}
    List ${data} is empty