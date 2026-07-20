using module "../../../src/core/aiintefration/NemotronClient.psm1"

param(
    [Parameter(Mandatory=$true)]
    [string]$Package,
    [string]$ProjectRoot,
    [int]$StartStep = 1
)


# =========================================================
# 共通関数
# =========================================================
function Invoke-TestStep {
    param(
        [int]$Step,
        [string]$Name,
        [scriptblock]$Action
    )

    if ($Step -lt $StartStep) {
        Write-Host "[SKIP] Step $Step : $Name"
        return
    }


    Write-Host ""
    Write-Host "================================="
    Write-Host "Step $Step : $Name"
    Write-Host "================================="


    try {
        & $Action
        Write-Host "[OK] Step $Step"
    }
    catch {
        Write-Host "[NG] Step $Step"
        Write-Host $_.Exception.Message
    }
}

<#
.SYNOPSIS
    Main Process for Running Test Code.
.DESCRIPTION
    Load target psm1 module and prepare test execution environment.
.NOTES
#>
# =========================================================
# Test Steps
# =========================================================
<# Validation Check Tests Based on Actual Execution #>
Invoke-TestStep `
    -Step 1 `
    -Name "SendMessage without API Key" `
    -Action {
        $client = [NemotronClient]::new()
        try {
            $client.SendMessage("test message")
            throw "Exception was not thrown"
        }
        catch [System.InvalidOperationException] {
            Write-Host "Expected exception:"
            Write-Host $_.Exception.Message
        }
        catch {
            throw "Unexpected exception type: $($_.Exception.GetType().FullName)"
        }
    }

<# Argument Validation Test #>
Invoke-TestStep `
    -Step 2 `
    -Name "SendMessage with empty content" `
    -Action {

        $client = [NemotronClient]::new()
        $client.SetApiKey("dummy")

        try {
            $client.SendMessage("")

            throw "Exception was not thrown"
        }
        catch [System.ArgumentException] {

            Write-Host "Expected exception:"
            Write-Host $_.Exception.Message
        }
        catch {
            throw "Unexpected exception type: $($_.Exception.GetType().FullName)"
        }
    }

<# Response status code test #>
Invoke-TestStep `
    -Step 3 `
    -Name "Check Response Status" `
    -Action {

        $testCases = @(
            @{ StatusCode = 199; Expected = $false }
            @{ StatusCode = 200; Expected = $true  }
            @{ StatusCode = 201; Expected = $true  }
            @{ StatusCode = 299; Expected = $true  }
            @{ StatusCode = 300; Expected = $false }
            @{ StatusCode = 400; Expected = $false }
        )

        foreach ($testCase in $testCases) {

            $response = [NemotronResponse]::new(
                $testCase.StatusCode,
                $null
            )

            $result = $response.IsSuccess()

            if ($result -ne $testCase.Expected) {
                throw `
                    "Unexpected result. StatusCode=$($testCase.StatusCode), " +
                    "Expected=$($testCase.Expected), Actual=$result"
            }

            Write-Host `
                "StatusCode=$($testCase.StatusCode) : $result"
        }
    }

Invoke-TestStep `
    -Step 4 `
    -Name "HTTP Error returns NemotronResponse" `
    -Action {

        $client = [NemotronClient]::new()
        $client.SetApiKey("invalid-key")

        $response = $client.SendMessage("test")

        if ($null -eq $response) {
            throw "Response is null."
        }

        if ($response.StatusCode -ne 401) {
            throw "Unexpected StatusCode: $($response.StatusCode)"
        }

        if ($null -eq $response.Body) {
            throw "Response body is null."
        }

        Write-Host "StatusCode : $($response.StatusCode)"
        Write-Host "Body       : $($response.Body)"
    }

    Invoke-TestStep `
    -Step 5 `
    -Name "Communication Error returns NemotronResponse" `
    -Action {

        $client = [NemotronClient]::new()
        $client.SetApiKey("test-key")

        [NemotronClient]::API_URL = "https://invalid-host.example.com/v1/chat/completions"

        $response = $client.SendMessage("test")

        if ($null -eq $response) {
            throw "Response is null."
        }

        if ($response.StatusCode -ne -1) {
            throw "Unexpected StatusCode: $($response.StatusCode)"
        }

        if ($null -eq $response.Body) {
            throw "Response body is null."
        }

        if ($null -eq $response.Body.ErrorType) {
            throw "ErrorType is missing."
        }

        if ($null -eq $response.Body.Message) {
            throw "Message is missing."
        }

        Write-Host "StatusCode : $($response.StatusCode)"
        Write-Host "ErrorType  : $($response.Body.ErrorType)"
        Write-Host "Message    : $($response.Body.Message)"
    }