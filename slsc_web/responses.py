from typing import List


class GenericResponse:
    """
    Generic Response object for SLSC Web responses that don't return data
    """

    def __init__(self, data: dict):
        self.id = data.get("id")
        self.rpc_version = data.get("jsonrpc")
        self.error = data.get("error")

        if not self.has_error():
            self._read_results(data)

    @property
    def id(self) -> int:
        """
        Same as the value of the id member in the request.
        If the JSON format of the request body is invalid, id returns null
        """
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def rpc_version(self) -> str:
        """
        Version of the JSON-RPC protocol
        """
        return self._rpc_version

    @rpc_version.setter
    def rpc_version(self, version: str):
        self._rpc_version = version

    @property
    def error(self) -> dict:
        """
        Error that the web server returns
        """
        return self._error

    @error.setter
    def error(self, error: dict):
        self._error = error

    def has_error(self):
        if self.error is None:
            return False
        else:
            return True

    def _read_results(self, data: dict):
        """
        Adds results from data input to Reponse object data
        """
        pass

    def _get_result(self, data: dict, result: str):
        """
        Gets single result from response dictionary
        """
        return data.get("result").get(result)


class InitializeResponse(GenericResponse):
    """
    Response of initializeSession request
    """

    def __init__(self, data: dict):
        self.session_id = ""
        super().__init__(data)

    @property
    def session_id(self) -> str:
        """
        ID of the session
        """
        return self._session_id

    @session_id.setter
    def session_id(self, id: str):
        self._session_id = id

    def _read_results(self, data: dict):
        self.session_id = self._get_result(data, "session_id")


class GetPropertyListResponse(GenericResponse):
    """
    Response of getDevicePropertyList request
    """

    def __init__(self, data: dict):
        self.static_properties = []
        self.dynamic_properties = []
        super().__init__(data)

    @property
    def static_properties(self) -> List[str]:
        return self._static_properties

    @static_properties.setter
    def static_properties(self, properties: List[str]):
        self._static_properties = properties

    @property
    def dynamic_properties(self) -> List[str]:
        return self._dynamic_properties

    @dynamic_properties.setter
    def dynamic_properties(self, properties: List[str]):
        self._dynamic_properties = properties

    def _read_results(self, data: dict):
        self.static_properties = self._get_result(data, "static_properties")
        self.dynamic_properties = self._get_result(data, "dynamic_properties")
