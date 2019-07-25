# Archivefiles test suite
# Downloaded files each go to their own test folder to avoid race conditions
# Requires a "token" provided as an execution argument (ie --variable token:ABC123)

*** Settings ***
Documentation    Archive Files Test Suite
Resource         ../resources/general.robot


*** Variables ***

${onc0}              Make ONC with path  output/09
&{F_LOCATION1}       locationCode=RISS    deviceCategoryCode=VIDEOCAM    dateFrom=2016-12-01T00:00:00.000Z    dateTo=2016-12-01T01:00:00.000Z
&{F_LOCATION3}       locationCode=RISS    deviceCategoryCode=VIDEOCAM    dateFrom=2016-12-01T00:00:00.000Z    dateTo=2016-12-01T01:00:00.000Z    rowLimit=5
&{F_LOCATIONFULL}    locationCode=RISS    deviceCategoryCode=VIDEOCAM    dateFrom=2016-12-01T00:00:00.000Z    dateTo=2016-12-01T01:00:00.000Z    extension=mp4
&{F_LOC_RETURN1}     locationCode=RISS    deviceCategoryCode=VIDEOCAM    dateFrom=2016-12-01T00:00:00.000Z    dateTo=2016-12-01T01:00:00.000Z    rowLimit=5    returnOptions=archiveLocation
&{F_LOC_RETURN2}     locationCode=RISS    deviceCategoryCode=VIDEOCAM    dateFrom=2016-12-01T00:00:00.000Z    dateTo=2016-12-03T00:00:00.000Z    rowLimit=50    returnOptions=all    extension=mp4
&{F_DEVICE1}         dateFrom=2010-01-01T00:00:00.000Z    dateTo=2010-01-01T00:02:00.000Z
&{F_DEVICE1EXT}      deviceCode=NAXYS_HYD_007    dateFrom=2010-01-01T00:00:00.000Z    dateTo=2010-01-01T00:02:00.000Z    extension=mp3
&{F_GETDIRECT_DEV}   dateFrom=2010-01-01T00:00:00.000Z  dateTo=2010-01-01T00:00:30.000Z  deviceCode=NAXYS_HYD_007  returnOptions=all
&{F_GETDIRECT_LOC}   dateFrom=2016-12-01T00:00:00.000Z  dateTo=2016-12-01T01:00:00.000Z  locationCode=RISS  deviceCategoryCode=VIDEOCAM  extension=mp4


*** Test Cases ***

1. Get list by location, 1 page
    ${result}=    Run method getListByLocation with filters &{F_LOCATION1}
    List ${result}[files] has exactly 15 rows

2. Get list by location, 3 pages
    ${result}=    Run method getListByLocation with &{F_LOCATION1} and parameter ${True}
    List ${result}[files] has exactly 15 rows

3. Get list by location, 1 page, filter by extension
    ${result}=    Run method getListByLocation with filters &{F_LOCATIONFULL}
    List ${result}[files] has exactly 1 rows

4. Get list by location, wrong filters
    
    Run Keyword And Expect Error  *400*     Run method getListByLocation with filters &{F_DEVICE1}

5. Get list by device, 1 page, filter by extension
    ${result}=    Run method getListByDevice with filters &{F_DEVICE1EXT}
    List ${result}[files] has exactly 4 rows

6. Get a file
    Prepare output directory  output/09/06
    Get file with name "NAXYS_HYD_007_20091231T235919.476Z-spect-small.png" and save to "output/09/06"
    File was downloaded     output/09/06/NAXYS_HYD_007_20091231T235919.476Z-spect-small.png

7. Get direct files from device, include returnOptions
    Prepare output directory  output/09/07
    ${result}=    GetDirectFiles with filters &{F_GETDIRECT_DEV} and save to "output/09/07"
    Downloaded 12 files to output/09/07
    List ${result}[downloadResults] has exactly 12 rows

8. Get direct files from location, try to overwrite
    Prepare output directory  output/09/08
    ${result}=    GetDirectFiles with filters &{F_GETDIRECT_LOC} and save to "output/09/08"
    List ${result}[downloadResults] has exactly 1 rows
    First row in ${result}[downloadResults] has key "status" with value "completed"
    Downloaded 1 files to output/09/08
    ${result}=    GetDirectFiles with filters &{F_GETDIRECT_LOC} and save to "output/09/08"
    List ${result}[downloadResults] has exactly 1 rows
    First row in ${result}[downloadResults] has key "status" with value "skipped"
    Downloaded 1 files to output/09/08

9. Wrong getFile filename
    Run Keyword And Expect Error  *400*     Get file with name "FAKEFILE.XYZ" and save to "output/09/09"

10. Wrong getDirectFile parameters
    [Tags]    run
    ${onc}=                 Make ONC with path      output/09/10
    Run Keyword And Expect Error  *combination*     Call Method    ${onc}    getDirectFiles    filters=${F_LOCATION1}

11. Get list by device, wrong filters
    Run Keyword And Expect Error  *400*     Run method getListByDevice with filters &{F_LOCATION1}

12. Get list by location, 3 pages, return archiveLocations
    ${result}=    Run method getListByLocation with &{F_LOC_RETURN1} and parameter ${True}
    List ${result}[files] has exactly 15 rows
    First row in ${result}[files] has key archiveLocation

13. Get list by device, 3 pages, filter extension, return all metadata per sample
    ${result}=    Run method getListByLocation with &{F_LOC_RETURN2} and parameter ${True}
    List ${result}[files] has exactly 2 rows
    First row in ${result}[files] has key uncompressedFileSize

14. Save a file to current directory (empty outpath)
    Get file with name "NAXYS_HYD_007_20091231T235919.476Z-spect-small.png" and save to ""
    File was downloaded     NAXYS_HYD_007_20091231T235919.476Z-spect-small.png
    # clean up
    Remove File             NAXYS_HYD_007_20091231T235919.476Z-spect-small.png

*** Keywords ***

File was downloaded
    [Arguments]             ${file}
    File Should Exist       ${EXECDIR}${/}${file}

Get file with name "${file}" and save to "${path}"
    ${onc}=                 Make ONC with path        ${path}
    Call Method             ${onc}         getFile    filename=${file}

GetDirectFiles with filters ${filters} and save to "${path}"
    Log   ${filters}
    ${onc}=                 Make ONC with path      ${path}
    ${result}=              Call Method    ${onc}    getDirectFiles    filters=${filters}
    [return]                ${result}