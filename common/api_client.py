import urllib.parse
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Union

import requests


class RequestMethod(Enum):
    DELETE = "DELETE"
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"


class APIClient(ABC):
    default_timeout = 5
    api_key_param = None

    @classmethod
    @abstractmethod
    def _get_base_url(cls, *args, **kwargs) -> str:
        pass

    @classmethod
    @abstractmethod
    def _get_api_key(cls, *args, **kwargs) -> str:
        pass

    @classmethod
    def _make_request(
        cls,
        method: RequestMethod,
        path: str,
        headers: Dict = None,
        params: Dict = None,
        json: Dict = None,
        timeout: int = None,
    ) -> Union[Dict, bytes]:
        if not timeout:
            timeout = cls.default_timeout

        if not headers:
            headers = {}

        if cls.api_key_param:
            params[cls.api_key_param] = cls._get_api_key()

        session = requests.Session()
        response = session.request(
            method=method.value,
            url=urllib.parse.urljoin(cls._get_base_url(), path),
            headers=headers,
            json=json,
            params=params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()
