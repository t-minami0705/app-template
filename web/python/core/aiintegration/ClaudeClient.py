import requests
import copy

class ClaudeResponse:
    """
    Class for storing Claude API response information.

    This class provides a unified interface for handling
    API response results, including HTTP status code and
    response body.

    The response content is stored regardless of success
    or failure, allowing the caller to determine how to
    handle the result.

    :author: T.Minami
    :version: 1.0.0
    :since: 1.0.0
    """
    def __init__(
            self,
            status_code: int,
            body: dict | str
        ) -> None:
        """
        Initialize Claude API response.

        :param status_code:
            HTTP status code.

        :param body:
            Response body returned from Claude API.
            This value can be a JSON object or raw text.
        """
        self._status_code = status_code
        self._body = body

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def body(self) -> dict | str:
        return self._body

    @property
    def is_success(self) -> bool:
        return 200 <= self._status_code < 300
    

class ClaudeClient:
    """
    Client class for communicating with Claude API.

    This class provides functions for creating API requests,
    sending messages to Claude API, and receiving responses.

    The class manages API configuration parameters such as
    model name, token limit, temperature, and API key.

    :author: T.Minami
    :version: 1.0.0
    :since: 1.0.0
    """
    class Model:
        """
        Claude API model definitions.
        """
        SONNET_5 = "claude-sonnet-5"
        SONNET_4_6 = "claude-sonnet-4-6"
        SONNET_4_5 = "claude-sonnet-4-5-20250929"

        OPUS_4_8 = "claude-opus-4-8"
        OPUS_4_7 = "claude-opus-4-7"
        OPUS_4_6 = "claude-opus-4-6"
        OPUS_4_5 = "claude-opus4-5-20251101"

        FABLE_5 = "claude-fable-5"
        HAIKU_4_5 = "claude-haiku-4-5-20251001"
    
    class Role:
        """
        Claude API role definitions.
        """
        USER = "user"
        ASSISTANT = "assistant"
    
    class MaxTokens:
        """
        Claude API max tokens definitions.
        """
        DEFAULT = 4096
        LARGE = 8192

    class API:
        """
        Claude API definitions.
        """
        URL = "https://api.anthropic.com/v1/messages"
        VERSION = "2023-06-01"

    # ========================================================================================
    # Constructor / Destructor
    # ========================================================================================
    def __init__(
            self,
            model: str = Model.SONNET_5,
            max_tokens: int = MaxTokens.DEFAULT,
            temperature: float = 1.0
        ) -> None:

        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._api_key: str | None = None

        self._request = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": self.Role.USER,
                    "content": ""
                }
            ]
        }

    # ========================================================================================
    # Properties
    # ========================================================================================
    @property
    def model(self) -> str:
        return self._model

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    @property
    def temperature(self) -> float:
        return self._temperature
    
    @property
    def api_key(self) -> str | None:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._api_key = value

    # ========================================================================================
    # Public method
    # ========================================================================================
    def send_message(self, content: str) -> ClaudeResponse:
        """
        Send a message to Claude API.

        The method creates an API request using the configured
        model parameters and sends the specified message.

        The API response is returned as a ClaudeResponse object.
        HTTP errors and API errors are not evaluated here;
        the caller is responsible for handling the result.

        :param content:
            Message content sent to Claude API.

        :return:
            ClaudeResponse object containing HTTP status
            and response body.

        :raises RuntimeError:
            If API communication fails.

        :raises ValueError:
            If message content is empty.
        """
        # ==============================
        # Validation
        # ==============================
        if not self._api_key:
            raise RuntimeError(
                "API key has not been configured."
            )

        if not content:
            raise ValueError(
                "Content must not be empty."
            )

        # ==============================
        # Update Request
        # ==============================
        request = copy.deepcopy(self._request)
        request["messages"][0]["content"] = content

        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": self.API.VERSION,
            "content-type": "application/json"
        }

        # ==============================
        # Send Request
        # ==============================
        try:
            response = requests.post(
                self.API.URL,
                headers=headers,
                json=request,
                timeout=30
            )

        except requests.RequestException as e:
            raise RuntimeError(
                f"Claude API communication error: {e}"
            )

        # ==============================
        # Response Parsing
        # ==============================
        try:
            body = response.json()

        except ValueError:
            body = response.text

        # ==============================
        # Create Response Object
        # ==============================
        return ClaudeResponse(
            status_code=response.status_code,
            body=body
        )
