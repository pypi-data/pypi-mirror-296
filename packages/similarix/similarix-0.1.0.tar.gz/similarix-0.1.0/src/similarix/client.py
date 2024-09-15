from typing import Dict, Any, Union, BinaryIO

import requests
from requests.exceptions import RequestException


class SimilarixAPIError(Exception):
    """Custom exception for Similarix API errors."""

    pass


class Similarix:
    def __init__(self, token: str, base_url: str = "https://similarix.com"):
        self.token: str = token
        self.base_url: str = base_url
        self.headers: Dict[str, str] = {"Authorization": f"Token {self.token}"}

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Dict[str, Any]:
        url = f"{self.base_url}/api{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            print(f"Request successful: {method} {endpoint}")
            return response.json()
        except RequestException as e:
            print(f"Error in request: {method} {endpoint}")
            print(f"Error details: {str(e)}")
            raise SimilarixAPIError(f"API request failed: {str(e)}") from e

    def text_search(self, query: str) -> Dict[str, Any]:
        return self._request("GET", "/search/", params={"query": query})

    def image_search(self, image_file: Union[str, BinaryIO]) -> Dict[str, Any]:
        files = {"file": image_file}
        return self._request("POST", "/search/", files=files)

    def list_collections(self) -> Dict[str, Any]:
        return self._request("GET", "/collections/")

    def get_collection(self, uuid: str) -> Dict[str, Any]:
        return self._request("GET", f"/collections/{uuid}/")

    def trigger_sync(self, uuid: str) -> Dict[str, Any]:
        return self._request("POST", f"/collections/{uuid}/sync/")

    def check_sync_status(self, uuid: str) -> Dict[str, Any]:
        return self._request("GET", f"/collections/{uuid}/sync-status/")

    def upload_to_managed_collection(
        self, uuid: str, file: Union[str, BinaryIO]
    ) -> Dict[str, Any]:
        files = {"file": file}
        return self._request("POST", f"/collections/{uuid}/upload/", files=files)
