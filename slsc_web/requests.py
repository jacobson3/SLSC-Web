from abc import ABC, abstractmethod
import json


class Request(ABC):
    """
    Generic Request object for creating JSON RPC requests
    """

    def __init__(self, id: int, params: dict):
        self._request_dict = {
            "id": str(id),
            "jsonrpc": "2.0",
            "method": self._get_method(),
            "params": params,
        }

    @abstractmethod
    def _get_method(self) -> str:
        """
        Name of the method to invoke
        """
        return ""

    def serialize(self) -> str:
        return json.dumps(self._request_dict)


class InitializeRequest(Request):
    """
    Request for initializing an SLSC session
    """

    def __init__(self, id: int, resources: str):
        params = {"devices": resources.split(",")}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "initializeSession"


class CloseRequest(Request):
    """
    Request for closing an SLSC session
    """

    def __init__(self, id: int, session_id: str):
        params = {"session_id": session_id}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "closeSession"


class GetPropertyListRequest(Request):
    """
    Request for getDevicePropertyList
    Lists all device properties
    """

    def __init__(self, id: int, session_id: str, device: str):
        params = {"session_id": session_id, "device": device}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "getDevicePropertyList"


if __name__ == "__main__":
    init = InitializeRequest(4, "SLSC-12201")
    print(init.serialize())
