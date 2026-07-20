# ========================================================================================
# NemotronResponse クラス
# ========================================================================================
class NemotronResponse {
    [int]$StatusCode
    [object]$Body

    NemotronResponse([int]$statusCode, [object]$body) {
        $this.StatusCode = $statusCode
        $this.Body = $body
    }

    [bool] IsSuccess() {
        return ($this.StatusCode -ge 200 -and $this.StatusCode -lt 300)
    }
}

# ========================================================================================
# NemotronClient クラス
# ========================================================================================
class NemotronClient {

    # --- 定数 ---
    static [string]$API_URL         = "https://integrate.api.nvidia.com/v1/chat/completions"
    static [string]$DEFAULT_MODEL   = "nvidia/nemotron-3-nano-30b-a3b"
    static [int]   $DEFAULT_TOKENS  = 16384
    static [float] $DEFAULT_TEMP    = 1.0

    # --- フィールド ---
    hidden [string]$_model
    hidden [int]   $_maxTokens
    hidden [float] $_temperature
    hidden [string]$_apiKey

    # --- コンストラクタ ---
    NemotronClient() {
        $this._model       = [NemotronClient]::DEFAULT_MODEL
        $this._maxTokens   = [NemotronClient]::DEFAULT_TOKENS
        $this._temperature = [NemotronClient]::DEFAULT_TEMP
        $this._apiKey      = ""
    }

    NemotronClient([string]$model, [int]$maxTokens, [float]$temperature) {
        $this._model       = $model
        $this._maxTokens   = $maxTokens
        $this._temperature = $temperature
        $this._apiKey      = ""
    }

    # --- API Key セッター ---
    [void] SetApiKey([string]$key) {
        $this._apiKey = $key
    }

    # ========================================================================================
    # SendMessage メソッド
    # ========================================================================================
    [NemotronResponse] SendMessage([string]$content) {

        # --- バリデーション ---
        if ([string]::IsNullOrEmpty($this._apiKey)) {
            throw [System.InvalidOperationException]"No API key has been configured."
        }
        if ([string]::IsNullOrWhiteSpace($content)) {
            throw [System.ArgumentException]"メッセージ内容が空です。"
        }

        # --- リクエストボディ構築 ---
        $requestBody = @{
            model       = $this._model
            messages    = @(
                @{
                    role    = "user"
                    content = $content
                }
            )
            temperature     = $this._temperature
            top_p           = 1
            max_tokens      = $this._maxTokens
            reasoning_budget = $this._maxTokens
            seed            = 42
            stream          = $false   # ストリームOFF（レスポンス全体を受け取る）
        } | ConvertTo-Json -Depth 10

        # --- ヘッダー構築 ---
        $headers = @{
            "Authorization" = "Bearer $($this._apiKey)"
            "Accept"        = "application/json"
            "Content-Type"  = "application/json"
        }

        # --- API呼び出し ---
        try {
            $url = [NemotronClient]::API_URL
            $response = Invoke-WebRequest `
                -Uri     $url `
                -Method  POST `
                -Headers $headers `
                -Body    $requestBody `
                -TimeoutSec 120

            # --- レスポンスパース ---
            try {
                $body = $response.Content | ConvertFrom-Json
            }
            catch {
                $body = $response.Content
            }

            return [NemotronResponse]::new($response.StatusCode, $body)

        }
        catch {

            # HTTPレスポンスあり
            # 例: 401, 403, 500
            if ($null -ne $_.Exception.Response) {
                $httpResponse = $_.Exception.Response
                $statusCode = [int]$httpResponse.StatusCode
                $errorBody = $_.ErrorDetails.Message

                try {
                    $body = $errorBody | ConvertFrom-Json
                }
                catch {
                    $body = $errorBody
                }

                return [NemotronResponse]::new($statusCode, $body)
            }

            # HTTPレスポンスなし
            # 例: DNS失敗、タイムアウト、接続失敗
            $errorBody = @{
                ErrorType = $_.Exception.GetType().FullName
                Message   = $_.Exception.Message
            }

            return [NemotronResponse]::new(-1, $errorBody)
        }
    }
}
