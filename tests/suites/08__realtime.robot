*** Settings ***
Library         OperatingSystem
Library         String
Documentation   Scalar Data Test Suite
Suite Setup     Inital Setup
Resource        ../resources/general.robot


*** Variables ***

# 1 page of temperature, by location
&{F_SCALAR1}           locationCode=JDATF    deviceCategoryCode=ADCP600KHZ    propertyCode=seawatertemperature
...                    dateFrom=2019-04-24T00:00:00.000Z    dateTo=2019-04-24T00:00:15.000Z
# 3 pages of temperature, by location
&{F_SCALAR2}           locationCode=JDATF    deviceCategoryCode=ADCP600KHZ    propertyCode=seawatertemperature
...                    dateFrom=2019-04-24T00:00:00.000Z    dateTo=2019-04-24T00:00:15.000Z    rowLimit=5
# 3 pages of temperature
&{F_SCALAR3}           deviceCode=BARIX001    dateFrom=2017-06-08T00:00:00.000Z    dateTo=PT7M    rowLimit=5

&{F_RAW1}              locationCode=JDATF    deviceCategoryCode=ADCP600KHZ
...                    dateFrom=2019-04-24T00:00:00.000Z    dateTo=2019-04-24T00:00:10.000Z
&{F_RAW3}              locationCode=JDATF    deviceCategoryCode=PHSENSOR
...                    dateFrom=2019-04-24T00:00:00.000Z    dateTo=2019-04-24T00:01:30.000Z    rowLimit=5
&{F_RAWDEV1}           deviceCode=BARIX001    dateFrom=2017-06-08T00:00:00.000Z    dateTo=PT5S
&{F_WRONG_FILTERS}     locationCode=ONION    deviceCategoryCode=POTATO    propertyCode=BANANA
...                    dateFrom=2019-04-24T00:00:00.000Z    dateTo=2019-04-24T00:00:10.000Z
&{F_NODATA}            locationCode=JDATF    deviceCategoryCode=ADCP600KHZ
...                    dateFrom=2018-03-24T00:00:00.000Z    dateTo=2018-03-24T00:00:10.000Z


*** Test Cases ***

1. Get scalar data by location with 1 page
    ${response}=      Run method getDirectByLocation with filters ${F_SCALAR1}
    ${sensorData}=    Get From Dictionary  ${response}  sensorData
    First row in ${sensorData} has key "data"
    First row in ${sensorData} has key "sensorCode" with value "temperature"
    No next page in ${response}

2. Get scalar data by location with 3 pages
    ${response}=        Run method getDirectByLocation with ${F_SCALAR2} and parameter ${True}
    ${sensorData}=      Get From Dictionary  ${response}  sensorData
    First row in ${sensorData} has key "data"
    First row in ${sensorData} has key "sensorCode" with value "temperature"
    List ${sensorData}[0][data][values] has exactly 15 rows
    No next page in ${response}
    #Save Json To File   ${data}     out_realtime_2.json

3. Scalar data by location not found for these filters
    ${response}=       Run method getDirectByLocation with filters ${F_NODATA}
    Should Be Equal    ${response}[sensorData]  ${None}

4. Scalar data by location with wrong filters
    Run Keyword And Expect Error    *400*       Run method getDirectByLocation with filters ${F_WRONG_FILTERS}

5. Get raw data by location with 1 page
    ${response}=          Run method getDirectRawByLocation with filters ${F_RAW1}
    List ${response}[data][readings] has exactly 10 rows
    No next page in ${response}

6. Get raw data by location with 3 pages
    ${response}=        Run method getDirectRawByLocation with ${F_RAW3} and parameter ${True}
    List ${response}[data][readings] has exactly 9 rows
    No next page in ${response}
    #Save Json To File   ${data}     out_realtime_6.json

7. Raw data by device with 1 page
    ${response}=          Run method getDirectRawByDevice with filters ${F_RAWDEV1}
    List ${response}[data][readings] has exactly 47 rows
    No next page in ${response}

8. Raw data not found for these filters
    ${response}=        Run method getDirectRawByLocation with filters ${F_NODATA}
    List ${response}[data][readings] has exactly 0 rows

9. Raw data with wrong filters
    Run Keyword And Expect Error    *400*     Run method getDirectRawByLocation with filters ${F_WRONG_FILTERS}

10. Get scalar data by device with 6 pages
    [Tags]  run
    ${response}=        Run method getDirectByDevice with ${F_SCALAR3} and parameter ${True}
    ${sensorData}=      Get From Dictionary  ${response}  sensorData
    First row in ${sensorData} has key "data"
    First row in ${sensorData} has key "sensorCode" with value "analog_input501"
    List ${sensorData}[0][data][values] has exactly 14 rows
    No next page in ${response}
    Save Json To File   ${response}     output/08/10/out_realtime_10.json


*** Keywords ***

No next page in ${response}
    Should Be Equal       ${response}[next]     ${None}

