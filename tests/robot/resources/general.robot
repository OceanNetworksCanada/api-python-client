*** Settings ***
Library             ../libraries/common.py
Library             Collections
Library             OperatingSystem
Variables           ../libraries/env_variable.py

*** Variables ***
${onc}    makeOnc  ${token}  output

*** Keywords ***
# Object generation
Make ONC with path
    [Arguments]         ${path}
    ${oncObj}=          makeOnc  ${token}  ${path}
    [Return]            ${oncObj}


# Create directory if it doesn't exist, delete its contents otherwise
Prepare output directory
    [Arguments]        ${testPath}
    ${path}=           Catenate    SEPARATOR=  ${EXECDIR}  ${/}  ${testPath}
    Create Directory   ${path} 
    Empty Directory    ${path}

Downloaded ${expected} files to ${outPath}
    ${count}=                      Count Files In Directory    ${EXECDIR}${/}${outPath}
    Should Be Equal As Integers    ${count}    ${expected}


# List conditions

List ${list} has at least ${txtMin} rows
    ${min}=             Convert To Integer    ${txtMin}
    ${length}=          Get length            ${list}
    Should Be True      ${length} >= ${min}

List ${list} has at most ${txtMax} rows
    ${max}=             Convert To Integer    ${txtMax}
    ${length}=          Get length            ${list}
    Should Be True      ${length} <= ${max}

List ${list} has exactly ${txtNum} rows
    ${n}=               Convert To Integer    ${txtNum}
    ${length}=          Get length            ${list}
    Should Be Equal     ${length}             ${n}

List ${data} is empty
    ${type} =           Evaluate    type($data).__name__
    Should Be Equal     ${type}     list
    Length Should Be    ${data}     ${0}

First row in ${list} has key "${name:[^"]+}"
    Dictionary Should Contain Key   ${list}[0]  ${name}

First row in ${list} has key "${name}" with value "${value}"
    Dictionary Should Contain Key   ${list}[0]          ${name}
    ${myValue}=                     Get From Dictionary  ${list}[0]  ${name}
    Should Be Equal                 ${myValue}    ${value}


# Field checks

Elements in ${data} have the expected fields for ${methodName}
    ${valid}=           Data Has Expected Fields    ${data}    ${methodName}
    Should Be True      ${valid}

Field "${fieldName}" in ${list} holds the value "${expected}"
    Should Be Equal     ${list}[${fieldName}]    ${expected}

Should be an error response
    [Arguments]                     ${data}
    Length Should Be                ${data}      ${1}
    Dictionary Should Contain Key   ${data}[0]   errors
    ${errors}=                      ${data}[0][errors]
    Dictionary Should Contain Key   ${errors}    errorCode
    Dictionary Should Contain Key   ${errors}    errorMessage


# Method execution

Run method ${methodName} without filters
    ${result}=          Run Method            ${methodName}    {}
    [return]            ${result}

Run method ${methodName} with filters ${filters}
    ${result}=          Run Method            ${methodName}    ${filters}
    [return]            ${result}

Run method ${methodName} with ${filters} and parameter ${param1}
    ${result}=          Run Method            ${methodName}    ${filters}    ${param1}
    [return]            ${result}

Run method ${methodName} with filter ${filterName}="${filterValue}"
    ${result}=          Run Method            ${methodName}    {"${filterName}": "${filterValue}"}
    [return]            ${result}

Method ${methodName} with filter ${filterName}="${filterValue}" returns a row with ${expectedName}="${expectedValue}"
    ${result}=          Run Method            ${methodName}    {"${filterName}": "${filterValue}"}
    ${resultValue}=     Get From Dictionary   ${result}[0]     ${expectedName}
    Should Be Equal     ${resultValue}        ${expectedValue}

Run method ${methodName} from "${dateFrom}" to "${dateTo}"
    ${result}=          Run Method            ${methodName}    {"dateFrom": "${dateFrom}", "dateTo": "${dateTo}"}
    [return]            ${result}
