*** Settings ***
Documentation    04. Devices Test Suite
Resource         ../resources/general.robot


*** Variables ***

&{F_NO_RESULTS}=       locationCode=SAAN    dateTo=1995-03-24T00:00:01.000Z


*** Test Cases ***

01. Get all devices
    ${data}=        Run method getDevices without filters
    Elements in ${data}[0] have the expected fields for getDevices
    List ${data} has at least 300 rows

02. Filter deviceCode
    ${data}=        Run method getDevices with filter deviceCode="NORTEKADCP9917"
    Elements in ${data}[0] have the expected fields for getDevices
    List ${data} has exactly 1 rows
    Field "deviceCode" in ${data}[0] holds the value "NORTEKADCP9917"

03. Filter deviceName
    ${data}=        Run method getDevices with filter deviceName="Nortek Aquadopp HR-Profiler 2 MHz 2700"
    Elements in ${data}[0] have the expected fields for getDevices
    List ${data} has exactly 1 rows
    Field "deviceCode" in ${data}[0] holds the value "BC_POD1_AD2M"

04. Filter locationCode
    ${data}=        Run method getDevices with filter locationCode="CQSBG"
    Elements in ${data}[0] have the expected fields for getDevices
    List ${data} has at least 1 rows

05. Filter deviceCategoryCode
    ${data}=        Run method getDevices with filter deviceCategoryCode="CTD"
    Elements in ${data}[0] have the expected fields for getDevices
    List ${data} has at least 100 rows

06. Filter propertyCode
    ${data}=        Run method getDevices with filter propertyCode="co2concentration"
    Elements in ${data}[0] have the expected fields for getDevices
    List ${data} has at least 2 rows

07. Filter dataProductCode
    ${data}=        Run method getDevices with filter dataProductCode="MP4V"
    Elements in ${data}[0] have the expected fields for getDevices
    List ${data} has at least 20 rows

08. ISO Date Range
    ${data}=        Run method getDevices from "2014-02-24T00:00:01.000Z" to "2014-03-24T00:00:01.000Z"
    Elements in ${data}[0] have the expected fields for getDevices
    List ${data} has at least 100 rows

10. No devices found
    Run Keyword And Expect Error    *404*    Run method getDevices with filters ${F_NO_RESULTS}
