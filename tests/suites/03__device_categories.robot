*** Settings ***
Documentation    DeviceCategories Test Suite
Suite Setup      Inital Setup
Resource         ../resources/general.robot


*** Variables ***
&{F_NO_RESULTS}=       locationCode=SAAN    propertyCode=co2concentration


*** Test Cases ***

Get all deviceCategories
    ${data}=        Run method getDeviceCategories without filters
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has at least 100 rows

# Single filters

Filter deviceCategoryCode
    ${data}=        Run method getDeviceCategories with filter deviceCategoryCode="ADCP1200KHZ"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has exactly 1 rows
    Field "deviceCategoryCode" in ${data}[0] holds the value "ADCP1200KHZ"

Filter deviceCategoryName
    ${data}=        Run method getDeviceCategories with filter deviceCategoryName="ADCP 1200 kHz"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has exactly 1 rows
    Field "deviceCategoryCode" in ${data}[0] holds the value "ADCP1200KHZ"

Filter description
    ${data}=        Run method getDeviceCategories with filter description="3D Camera"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has exactly 1 rows
    Field "deviceCategoryCode" in ${data}[0] holds the value "CAMERA_3D"

Filter locationCode
    ${data}=        Run method getDeviceCategories with filter locationCode="CQSBG"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has at least 1 rows

Filter propertyCode
    ${data}=        Run method getDeviceCategories with filter propertyCode="co2concentration"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has at least 1 rows

Wrong deviceCategoryCode
    Run Keyword And Expect Error    *400*    Run method getDeviceCategories with filter deviceCategoryCode="XYZ321"

No deviceCategories found
    ${data}=        Run method getDeviceCategories with filters ${F_NO_RESULTS}
    List ${data} is empty
