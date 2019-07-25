*** Settings ***
Library         OperatingSystem
Library         String
Documentation   Scalar Data Test Suite
Suite Setup     Inital Setup
Resource        ../resources/general.robot

*** Variables ***

&{F_TEMPERATURE1}      locationCode=JDATF    deviceCategoryCode=ADCP600KHZ    propertyCode=seawatertemperature
...                    dateFrom=2019-04-24T00:00:00.000Z    dateTo=2019-04-24T00:00:15.000Z
&{F_TEMPERATURE3}      locationCode=JDATF    deviceCategoryCode=ADCP600KHZ    propertyCode=seawatertemperature
...                    dateFrom=2019-04-24T00:00:00.000Z    dateTo=2019-04-24T00:00:15.000Z    rowLimit=5
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

# Scalar data

1. Get scalar data with 1 page
    [Tags]  run
    ${response}=      Run method getDirectScalar with filters ${F_TEMPERATURE1}  
    ${sensorData}=    Get From Dictionary  ${response}  sensorData
    First row in ${sensorData} has key data
    First row in ${sensorData} has key "sensorCode" with value "temperature"
    No next page in ${response}

2. Get scalar data with 3 pages
    ${response}=        Run method getDirectScalar with ${F_TEMPERATURE3} and parameter ${True}
    ${sensorData}=      Get From Dictionary  ${response}  sensorData
    First row in ${sensorData} has key data
    First row in ${sensorData} has key "sensorCode" with value "temperature"
    List ${sensorData}[0][data][values] has exactly 15 rows
    No next page in ${response}
    #Save Json To File   ${data}     out_realtime_2.json

3. Scalar data not found for these filters
    ${data}=          Run method getDirectScalar with filters ${F_NODATA}
    Should Be Equal   ${sensorData}[data]  ${None}

4. Scalar data with wrong filters
    Run Keyword And Expect Error    *400*       Run method getDirectScalar with filters ${F_WRONG_FILTERS}

# Raw data

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
    [Tags]    run
    ${response}=        Run method getDirectRawByLocation with filters ${F_NODATA}
    List ${response}[data][readings] has exactly 0 rows
    
9. Raw data with wrong filters
    Run Keyword And Expect Error    *400*     Run method getDirectRawByLocation with filters ${F_WRONG_FILTERS}


*** Keywords ***

No next page in ${response}
    Should Be Equal       ${response}[next]     ${None}

