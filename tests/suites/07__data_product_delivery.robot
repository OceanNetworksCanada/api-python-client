# Data product delivery tests.
# Note that downloaded files for each test are output into a different folder; This avoids race conditions when running in parallel
*** Settings ***
Documentation    07. Data Product Delivery Test Suite
Library         OperatingSystem
Library         Collections
Resource        ../resources/general.robot
Library         ../libraries/delivery.py


*** Variables ***

&{F_DUMMY1}=    dataProductCode=TSSD    extension=csv    locationCode=BACAX    deviceCategoryCode=ADCP2MHZ
...             dateFrom=2016-07-27T00:00:00.000Z    dateTo=2016-07-27T00:00:30.000Z
...             dpo_dataGaps=0    dpo_qualityControl=1    dpo_resample=none
&{F_DUMMY2}=    dataProductCode=TSSP    extension=png    locationCode=CRIP.C1    deviceCategoryCode=CTD
...             dateFrom=2019-08-29T00:00:00.000Z    dateTo=2019-08-30T00:00:00.000Z
...             dpo_qualityControl=1    dpo_resample=none
&{F_FAKE}=      dataProductCode=FAKECODE    extension=XYZ    locationCode=AREA51    deviceCategoryCode=AK47
...             dateFrom=2019-03-20T00:00:00.000Z    dateTo=2019-03-20T00:30:00.000Z
...             dpo_qualityControl=1    dpo_resample=none


*** Test Cases ***

01. Order product links only
    Prepare output directory  output/07/01
    ${data}=    Order product ${F_DUMMY1} with resultsOnly ${True}, metadata ${False}, save to "output/07/01"
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 1 rows
    Elements in ${rows[0]} have the expected fields for orderDataProduct
    Element ${rows[0]} with index 1 was completed and not downloaded
    Downloaded 0 files to output/07/01

02. Order links with metadata
    Prepare output directory  output/07/02
    ${data}=    Order product ${F_DUMMY1} with resultsOnly ${True}, metadata ${True}, save to "output/07/02"
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 2 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and not downloaded
    Element ${rows}[1] with index meta was completed and not downloaded
    Downloaded 0 files to output/07/02

03. Order and download
    Prepare output directory  output/07/03
    ${data}=    Order product ${F_DUMMY1} with resultsOnly ${False}, metadata ${False}, save to "output/07/03"
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 1 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and downloaded
    Downloaded 1 files to output/07/03

04. Order and download multiple
    Prepare output directory  output/07/04
    ${data}=    Order product ${F_DUMMY2} with resultsOnly ${False}, metadata ${False}, save to "output/07/04"
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 2 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and downloaded
    Element ${rows}[1] with index 2 was completed and downloaded
    Downloaded 2 files to output/07/04

05. Order and download with metadata
    Prepare output directory  output/07/05
    ${data}=    Order product ${F_DUMMY1} with resultsOnly ${False}, metadata ${True}, save to "output/07/05"
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 2 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and downloaded
    Element ${rows}[1] with index meta was completed and downloaded
    Downloaded 2 files to output/07/05

06. Order and download multiple with metadata
    Prepare output directory  output/07/06
    ${data}=    Order product ${F_DUMMY2} with resultsOnly ${False}, metadata ${True}, save to "output/07/06"
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 3 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and downloaded
    Element ${rows}[1] with index 2 was completed and downloaded
    Element ${rows}[2] with index meta was completed and downloaded
    Downloaded 3 files to output/07/06

07. Wrong order request argument
    Run Keyword And Expect Error    *    Order Product    filters=&{F_FAKE}  retries=${0}  resultsOnly=${True}  metadata=${True}  outPath=output/07/07

08. Manual request, run and download
    Prepare output directory  output/07/08
    ${reqId}=      Manual request with filters ${F_DUMMY1}
    ${runId}=      Manual run with request id=${reqId}
    ${rows}=       Manual download with runId=${runId}, resultOnly=${False}, save to "output/07/08"
    List ${rows} has exactly 2 rows
    Element ${rows}[0] with index 1 was completed and downloaded
    Element ${rows}[1] with index meta was completed and downloaded
    Downloaded 2 files to output/07/08

09. Manual request, run and download results only
    [Tags]  run
    Prepare output directory  output/07/09
    ${reqId}=      Manual request with filters ${F_DUMMY1}
    ${runId}=      Manual run with request id=${reqId}
    ${rows}=       Manual download with runId=${runId}, resultOnly=${True}, save to "output/07/09"
    List ${rows} has exactly 2 rows
    Element ${rows}[0] with index 1 was completed and not downloaded
    Element ${rows}[1] with index meta was completed and not downloaded
    Downloaded 0 files to output/07/09

10. Manual run with wrong argument
    Run Keyword And Expect Error    *400*       Manual run with request id=${1234568790}

11. Manual download with wrong argument
    Run Keyword And Expect Error    *400*       Manual download with runId=${1234567890}, resultOnly=${False}, save to "output/07/11"


*** Keywords ***

# Wraps Order Product with embedded arguments
Order product ${fil} with resultsOnly ${resultsOnly}, metadata ${metadata}, save to "${outPath}"
    ${response}=   Order Product    ${fil}  ${0}  ${resultsOnly}  ${metadata}  ${outPath}
    [Return]       ${response}

Order Product
    [Arguments]    ${filters}={None}  ${retries}=${0}  ${resultsOnly}=${true}  ${metadata}=${False}  ${outPath}=output
    Prepare output directory  ${outPath}
    ${onc}=        Make ONC with path   ${outPath}
    ${response}=   Call Method    ${onc}    orderDataProduct    filters=&{filters}  maxRetries=${0}  downloadResultsOnly=${resultsOnly}  includeMetadataFile=${metadata}
    [Return]       ${response}

Manual request with filters ${filters}
    ${dataRequest}=    Manual Request Product    ${filters}
    Dictionary Should Contain Key    ${dataRequest}  dpRequestId
    ${reqId}=          Get From Dictionary    ${dataRequest}  dpRequestId
    [Return]           ${reqId}

Manual run with request id=${reqId}
    ${runRequest}=     Manual Run Product     ${reqId}
    ${runIds}=         Get From Dictionary    ${runRequest}  runIds
    [Return]           ${runIds}[0]

Manual download with runId=${runId}, resultOnly=${resultsOnly}, save to "${outPath}"
    Prepare output directory  ${outPath}
    ${rows}=           manualDownloadProduct    ${runId}  ${outPath}  ${resultsOnly}
    Should Not Be Empty  ${rows}
    [Return]           ${rows}

Element ${data} with index ${index} was completed and downloaded
    Should Be Equal      ${data}[status]        complete
    Should Be Equal      ${data}[downloaded]    ${True}
    Should Be Equal      ${data}[index]         ${index}
    Should Not Be Empty  ${data}[url]
    Should Not Be Empty  ${data}[file]

Element ${data} with index ${index} was completed and not downloaded
    Should Be Equal      ${data}[status]        complete
    Should Be Equal      ${data}[downloaded]    ${False}
    Should Be Equal      ${data}[index]         ${index}
    Should Not Be Empty  ${data}[url]
    Should Be Empty  ${data}[file]
