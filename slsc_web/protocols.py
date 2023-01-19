import urllib3
import json
from slsc_web.requests import Request


class JSON_RPC:
    """
    Defines mechanism for sending JSON RPC requests
    """

    def __init__(self, url: str):
        self._http = urllib3.PoolManager()
        self._url = f"http://{url}/nislsc/call"

    def query(self, request: Request) -> dict:
        response = self._http.request("POST", self._url, body=request.serialize())

        return json.loads(response.data.decode())
