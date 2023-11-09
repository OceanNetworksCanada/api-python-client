*** Settings ***
Documentation    03. DeviceCategories Test Suite
Resource         ../resources/general.robot


*** Variables ***

&{F_NO_RESULTS}=       locationCode=SAAN    propertyCode=co2concentration


*** Test Cases ***

01. Get all deviceCategories
    ${data}=        Run method getDeviceCategories without filters
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has at least 100 rows

02. Filter deviceCategoryCode
    ${data}=        Run method getDeviceCategories with filter deviceCategoryCode="ADCP1200KHZ"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has exactly 1 rows
    Field "deviceCategoryCode" in ${data}[0] holds the value "ADCP1200KHZ"

03. Filter deviceCategoryName
    ${data}=        Run method getDeviceCategories with filter deviceCategoryName="Current Profiler 1200"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has exactly 1 rows
    Field "deviceCategoryCode" in ${data}[0] holds the value "ADCP1200KHZ"

04. Filter description
    ${data}=        Run method getDeviceCategories with filter description="3D Camera"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has exactly 1 rows
    Field "deviceCategoryCode" in ${data}[0] holds the value "CAMERA_3D"

05. Filter locationCode
    ${data}=        Run method getDeviceCategories with filter locationCode="CQSBG"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has at least 1 rows

06. Filter propertyCode
    ${data}=        Run method getDeviceCategories with filter propertyCode="co2concentration"
    Elements in ${data}[0] have the expected fields for getDeviceCategories
    List ${data} has at least 1 rows

07. Wrong deviceCategoryCode
    Run Keyword And Expect Error    *400*    Run method getDeviceCategories with filter deviceCategoryCode="XYZ321"

08. No deviceCategories found
    Run Keyword And Expect Error    *404*    Run method getDeviceCategories with filters ${F_NO_RESULTS}
