from abc import ABC, abstractmethod
from slsc_web.requests import *
from slsc_web.responses import *
from slsc_web.protocols import JSON_RPC


class SLSC_Session(ABC):
    """
    Parent class to all SLSC devices, physical channels, or NVMEM areas.
    """

    def __init__(self, chassis: str, resources: str):
        self._rpc = JSON_RPC(chassis)
        self._uid = 0
        self._session_id = ""
        self._resources = resources

        response = self.initialize(resources)
        if response.has_error():
            print(response.error)
        else:
            self._session_id = response.session_id

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        self._rpc.close()

    @abstractmethod
    def initialize(self, resources: str) -> InitializeResponse:
        pass

    @staticmethod
    def _close_session(chassis: str, session_id: str) -> GenericResponse:
        """
        Static method used to close session by given session_id
        """
        rpc = JSON_RPC(chassis)

        request = CloseRequest(1, session_id)
        response = rpc.query(request)

        return GenericResponse(response)

    def _query(self, request: Request) -> dict:
        return self._rpc.query(request)

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

    @abstractmethod
    def get_property_list(self, resource: str = None) -> GetPropertyListResponse:
        """
        Lists properties of given resource.
        No input resource will return properties of first resource in session.
        """
        pass

    def get_session_properties(self) -> GetSessionPropertyListResponse:
        """
        Lists all session properties
        """
        request = GetSessionPropertyListRequest(self._get_uid(), self._session_id)
        response = self._query(request)

        return GetSessionPropertyListResponse(response)

    @abstractmethod
    def get_property(self, property: str, resources: str = None) -> GetPropertyResponse:
        """
        Returns value and type of given property
        No input resource will return properties of resources used to open session
        """
        pass


class Device(SLSC_Session):
    """
    Reference to SLSC devices.
    Used to query and command SLSC chassis/modules
    """

    def __init__(self, chassis: str, devices: str):
        super().__init__(chassis, devices)

    def initialize(self, resources: str) -> InitializeResponse:
        """
        Initialize SLSC connection, returning session ID
        """
        request = InitializeRequest(self._get_uid(), devices=resources)
        response = self._query(request)

        return InitializeResponse(response)

    def get_property_list(self, resource: str = None) -> GetPropertyListResponse:
        """
        Lists properties of given device.
        No input resource will return properties of first resource in session.
        """
        if resource is None:  # set resource to first resource
            resource = self._resources.split(",")[0]

        request = GetDevicePropertyListRequest(self._get_uid(), self._session_id, resource)
        response = self._query(request)

        return GetPropertyListResponse(response)

    def get_property(self, property: str, resources: str = None) -> GetPropertyResponse:
        if resources is None:
            resources = self._resources

        request = GetPropertyRequest(self._get_uid(), self._session_id, property, devices=resources)
        response = self._query(request)

        return GetPropertyResponse(response)


if __name__ == "__main__":
    chassis_name = "SLSC-12001-TSE"

    with Device(chassis_name, devices=chassis_name) as dev:
        modules = dev.get_property("Dev.Modules")

        print(modules.data_type)
        print(modules.value)

    # close_response = Device._close_session(device, "_session15")
    # print(close_response.error)
