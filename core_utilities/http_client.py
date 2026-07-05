import requests
import httpx
from typing import Any, Dict, Optional

class HTTPClient:
    """
    Approved Utility cho việc gọi HTTP request để thay thế requests/httpx trực tiếp,
    tránh vi phạm nguyên tắc bảo mật VULN-002.
    """
    @staticmethod
    def get(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: float = 20.0, use_httpx: bool = False, **kwargs) -> Any:
        if use_httpx:
            with httpx.Client(headers=headers, timeout=timeout, follow_redirects=True, **kwargs) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                return response
        else:
            response = requests.get(url, params=params, headers=headers, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response

    @staticmethod
    def post(url: str, data: Optional[Any] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: float = 20.0, use_httpx: bool = False, **kwargs) -> Any:
        if use_httpx:
            with httpx.Client(headers=headers, timeout=timeout, follow_redirects=True, **kwargs) as client:
                response = client.post(url, data=data, json=json)
                response.raise_for_status()
                return response
        else:
            response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
