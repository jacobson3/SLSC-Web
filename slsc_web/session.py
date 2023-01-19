from slsc_web.requests import *
from slsc_web.responses import *
from slsc_web.protocols import JSON_RPC


class Session:
    """
    Reference to SLSC devices, physical channels, or NVMEM areas.
    Used to query and command SLSC Chassis
    """

    def __init__(self, chassis: str, resources: str):
        self._rpc = JSON_RPC(chassis)
        self._uid = 0
        self._session_id = ""

        response = self.initialize(resources)
        if response.is_error():
            print(response.error)
        else:
            self._session_id = response.session_id

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _query(self, request: Request) -> dict:
        return self._rpc.query(request)

    def initialize(self, resources: str) -> InitializeResponse:
        """
        Initialize SLSC connection, returning session ID
        """
        request = InitializeRequest(self._get_uid(), resources)
        response = self._query(request)

        return InitializeResponse(response)

    def close(self) -> GenericResponse:
        """
        Closes any open SLSC references
        """
        request = CloseRequest(self._get_uid(), self._session_id)
        response = self._query(request)

        return GenericResponse(response)

    def _get_uid(self) -> int:
        """
        Returns incrementing unique ID starting at 1
        """
        self._uid += 1
        return self._uid

    def get_property_list(self, device: str) -> GetPropertyListResponse:
        """
        Lists all devicee properties
        """
        request = GetPropertyListRequest(self._get_uid(), self._session_id, device)
        response = self._query(request)

        return GetPropertyListResponse(response)


if __name__ == "__main__":
    device = "SLSC-12001-TSE"
    with Session("SLSC-12001-TSE", device) as sess:
        properties = sess.get_property_list(device)

        print(f"Dynamic Properties:\n{properties.dynamic_properties}")
        print(f"Dynamic Properties:\n{properties.static_properties}")
