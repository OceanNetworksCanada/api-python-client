# Data product delivery tests.
# Note that downloaded files for each test are output into a different folder; This avoids race conditions when running in parallel

*** Settings ***

Suite Setup     Inital Setup
Resource        ../resources/general.robot
Library         OperatingSystem
Library         Collections
Library         ../libraries/delivery.py


*** Test Cases ***

01. Order product links only
    Prepare output directory  output/07/01
    ${data}=    Request product dummy1 with    retries=${100}  resultsOnly=${True}  metadata=${False}  outPath=output/07/01
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 1 rows
    Elements in ${rows[0]} have the expected fields for orderDataProduct
    Element ${rows[0]} with index 1 was completed and not downloaded
    Downloaded 0 files to output/07/01

02. Order links with metadata
    Prepare output directory  output/07/02
    ${data}=    Request product dummy1 with    retries=${100}  resultsOnly=${True}  metadata=${True}  outPath=output/07/02
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 2 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and not downloaded
    Element ${rows}[1] with index meta was completed and not downloaded
    Downloaded 0 files to output/07/02

03. Order and download
    Prepare output directory  output/07/03
    ${data}=    Request product dummy1 with    retries=${100}  resultsOnly=${False}  metadata=${False}  outPath=output/07/03
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 1 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and downloaded
    Downloaded 1 files to output/07/03

04. Order and download multiple
    Prepare output directory  output/07/04
    ${data}=    Request product dummy2 with    retries=${100}  resultsOnly=${False}  metadata=${False}  outPath=output/07/04
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 2 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and downloaded
    Element ${rows}[1] with index 2 was completed and downloaded
    Downloaded 2 files to output/07/04

05. Order and download with metadata
    Prepare output directory  output/07/05
    ${data}=    Request product dummy1 with    retries=${100}  resultsOnly=${False}  metadata=${True}  outPath=output/07/05
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 2 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and downloaded
    Element ${rows}[1] with index meta was completed and downloaded
    Downloaded 2 files to output/07/05

06. Order and download multiple with metadata
    Prepare output directory  output/07/06
    ${data}=    Request product dummy2 with    retries=${100}  resultsOnly=${False}  metadata=${True}  outPath=output/07/06
    ${rows}=    Set Variable    ${data['downloadResults']}
    List ${rows} has exactly 3 rows
    Elements in ${rows}[0] have the expected fields for orderDataProduct
    Element ${rows}[0] with index 1 was completed and downloaded
    Element ${rows}[1] with index 2 was completed and downloaded
    Element ${rows}[2] with index meta was completed and downloaded
    Downloaded 3 files to output/07/06

07. Wrong order request argument
    Run Keyword And Expect Error    *400*       Order Product  product=FAKECODE  extension=911  location=DISNEY  deviceCategory=ONION
    ...                                         from=2016-07-27T00:00:00.000Z  to=2016-07-27T01:00:00.000Z

08. Manual request, run and download
    Prepare output directory  output/07/08
    ${reqId}=      Manual request dummy1
    ${runId}=      Manual run dummy1         ${reqId}
    ${rows}=       Manual download dummy1    ${runId}    output/07/08
    List ${rows} has exactly 2 rows
    Element ${rows}[0] with index 1 was completed and downloaded
    Element ${rows}[1] with index meta was completed and downloaded
    Downloaded 2 files to output/07/08

09. Manual request, run and download results only 
    Prepare output directory  output/07/09
    ${reqId}=      Manual request dummy1
    ${runId}=      Manual run dummy1         ${reqId}
    ${rows}=       Manual download dummy1    ${runId}    output/07/09    ${True}
    List ${rows} has exactly 2 rows
    Element ${rows}[0] with index 1 was completed and not downloaded
    Element ${rows}[1] with index meta was completed and not downloaded
    Downloaded 0 files to output/07/09

10. Manual order run with wrong argument
    Run Keyword And Expect Error    *400*       Manual run dummy1   ${1234568790}

11. Manual order download with wrong argument
    Run Keyword And Expect Error    *400*       Manual download dummy1   ${1234568790}    output/07/11



*** Keywords ***

Request product dummy1 with
    [Arguments]    ${retries}=${100}  ${resultsOnly}=${False}  ${metadata}=${False}  ${outPath}=out
    ${response}=   Order Product        product=TSSD  extension=csv
    ...                                 location=BACAX  deviceCategory=ADCP2MHZ
    ...                                 from=2016-07-27T00:00:00.000Z  to=2016-07-27T00:00:30.000Z
    ...                                 retries=${retries}  resultsOnly=${resultsOnly}  metadata=${metadata}  outPath=${outPath}
    [Return]       ${response}

Request product dummy2 with
    [Arguments]    ${retries}=${100}  ${resultsOnly}=${False}  ${metadata}=${False}  ${outPath}=out
    ${response}=   Order Product        product=TSSP  extension=png
    ...                                 location=CRIP.C1  deviceCategory=CTD
    ...                                 from=2019-03-20T00:00:00.000Z  to=2019-03-20T00:30:00.000Z
    ...                                 retries=${retries}  resultsOnly=${resultsOnly}  metadata=${metadata}  outPath=${outPath}
    [Return]       ${response}

Order Product
    [Arguments]    ${product}=TSSD  ${extension}=txt  ${location}=BACAX  ${deviceCategory}=ADCP2MHZ
    ...            ${from}=2016-07-27T00:00:00.000Z  ${to}=2016-07-27T01:00:00.000Z
    ...            ${retries}=${100}  ${resultsOnly}=${true}  ${metadata}=${False}  ${outPath}=output
    Prepare output directory  ${outPath}
    ${response}=   Order Data Product      ${product}  ${extension}  ${location}  ${deviceCategory}  ${from}  ${to}  ${retries}  ${resultsOnly}  ${metadata}  ${outPath}
    [Return]       ${response}

Manual request dummy1
    ${dataRequest}=    manualRequestProduct    TSSD  csv  BACAX  ADCP2MHZ  2016-07-27T00:00:00.000Z  2016-07-27T00:01:00.000Z
    Dictionary Should Contain Key    ${dataRequest}  dpRequestId
    ${reqId}=          Get From Dictionary    ${dataRequest}  dpRequestId
    [Return]           ${reqId}

Manual run dummy1
    [Arguments]        ${reqId}
    ${runRequest}=     manualRunProduct       ${reqId}
    ${runIds}=         Get From Dictionary    ${runRequest}  runIds
    [Return]           ${runIds}[0]

Manual download dummy1
    [Arguments]        ${runId}  ${outPath}  ${resultsOnly}=${False}
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
