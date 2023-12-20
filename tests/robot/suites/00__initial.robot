# Generic tests outside the other test suites

*** Settings ***
Documentation    00. Initialization Test Suite
Resource         ../resources/general.robot

*** Variables ***
&{F_LOCATIONCODE}           locationCode=CQSBG

*** Test Cases ***
01. ONC pip package is installed
    ${isInstalled}=         isOncInstalled
    Should Be True      ${isInstalled}

02. Invalid token return unauthorized error
    ${onc}=                 makeOnc    FAKE_TOKEN  output
    Run Keyword And Expect Error    *401*    Call Method     ${onc}  getLocations  ${F_LOCATIONCODE}

03. Save arbitrary JSON to file (getLocations)
    Prepare output directory  output/00/03
    ${onc3}=                Make ONC with path         output/00/03
    ${result}=              Call Method     ${onc3}  getLocations  ${F_LOCATIONCODE}
    Call Method             ${onc3}         print    ${result}     03.json
    File Should Exist       output/00/03/03.json