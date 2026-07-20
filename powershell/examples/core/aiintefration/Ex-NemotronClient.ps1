using module "../../../src/core/aiintefration/NemotronClient.psm1"

# ========================================================================================
# NemotronClient - Execution Sample
#
# Usage:
#   Run-Test.bat NemotronClient
#   or
#   pwsh.exe -NoProfile -ExecutionPolicy Bypass -File "examples\core\aiintegration\NemotronClient.ps1"
#
# Run command:
# Run-Test.bat 経由
#    Run-Test.bat NemotronClient
#
#    # PowerShell 直接実行
#    pwsh.exe -NoProfile -ExecutionPolicy Bypass -File "examples\core\aiintegration\NemotronClient.ps1"
# ========================================================================================
param(
    [string]$Package,
    [string]$ProjectRoot,
    [int]   $StartStep   = 1
)

# ========================================================================================
# Sample
# ========================================================================================
Write-Host "========================================"
Write-Host " NemotronClient - Sample"
Write-Host "========================================"
Write-Host ""

# --- API Key ---
$apiKey = Read-Host "NVIDIA API Key"
if ([string]::IsNullOrEmpty($apiKey)) {
    Write-Error "API Key is required."
    exit 1
}

# --- Message ---
$message = Read-Host "Send message"
if ([string]::IsNullOrWhiteSpace($message)) {
    Write-Error "Message is required."
    exit 1
}

# --- Execute ---
Write-Host ""
Write-Host "Sending message..." -ForegroundColor Cyan

try {
    $client = [NemotronClient]::new()
    $client.SetApiKey($apiKey)

    $response = $client.SendMessage($message)

    Write-Host ""
    Write-Host "----------------------------------------"
    Write-Host "Status  : $($response.StatusCode)"
    Write-Host "Success : $($response.IsSuccess())"
    Write-Host "----------------------------------------"
    Write-Host "Answer  :"
    Write-Host ""

    if ($response.IsSuccess()) {
        if ($response.Body -is [PSCustomObject]) {
            Write-Host $response.Body.choices[0].message.content -ForegroundColor Green
        } else {
            Write-Host $response.Body -ForegroundColor Green
        }
    } else {
        Write-Host "Error response:" -ForegroundColor Red
        Write-Host ($response.Body | ConvertTo-Json -Depth 5) -ForegroundColor Red
    }

} catch {
    Write-Error "Unexpected error: $($_.Exception.Message)"
    exit 1
}

Write-Host ""
Write-Host "========================================"
Write-Host " Done."
Write-Host "========================================"
