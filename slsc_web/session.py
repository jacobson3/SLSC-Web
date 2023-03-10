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

    def abort(self) -> GenericResponse:
        """
        Cancels a method that blocks network communications

        After aborting the session, the session handle remains valid, but the methods that access
        network connections return errors. To recover from an aborted session, close the session
        and initialize a new one.
        """

        request = AbortRequest(self._get_uid(), self._session_id)
        response = self._query(request)

        return GenericResponse(response)

    def connect(self, devices: str = None) -> GenericResponse:
        """
        Connects to an SLSC device.

        By default, connect to session device(s)
        """

        if devices is None:
            devices = self._resources

        request = ConnectToDevicesRequest(self._get_uid(), self._session_id, devices)
        response = self._query(request)

        return GenericResponse(response)

    def disconnect(self, devices: str = None) -> GenericResponse:
        """
        Disconnects from an SLSC device.

        By default, disconnect from session device(s)
        """

        if devices is None:
            devices = self._resources

        request = DisconnectFromDevicesRequest(self._get_uid(), self._session_id, devices)
        response = self._query(request)

        return GenericResponse(response)

    def _get_uid(self) -> int:
        """
        Returns incrementing unique ID starting at 1
        """

        self._uid += 1
        return self._uid

    def get_session_properties(self) -> GetSessionPropertyListResponse:
        """
        Lists all session properties
        """

        request = GetSessionPropertyListRequest(self._get_uid(), self._session_id)
        response = self._query(request)

        return GetSessionPropertyListResponse(response)


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

    def get_property_information(
        self, property: str, resources: str = None
    ) -> GetPropertyInformationResponse:
        """
        Gets all information of a property

        Leaving resources empty will use the resources opened with this session
        """
        if resources is None:
            resources = self._resources

        request = GetPropertyInformationRequest(
            self._get_uid(), self._session_id, property, devices=resources
        )
        response = self._query(request)

        return GetPropertyInformationResponse(response)

    def rename_device(self, device: str, new_name: str) -> GenericResponse:
        """
        Renames device to new_name
        """

        request = RenameDeviceRequest(self._get_uid(), self._session_id, device, new_name)
        response = self._query(request)

        return GenericResponse(response)

    def reserve_devices(
        self,
        devices: str = None,
        access: AccessType = AccessType.ReadWrite,
        reservation_group: str = "",
        reservation_timeout: float = 0.0,
    ) -> GenericResponse:
        """
        Reserves one or multiple devices to prevent other sessions from accessing the devices.
        You must reserve a device before using it.
        """

        if devices is None:
            devices = self._resources

        request = ReserveDeviceRequest(
            self._get_uid, self._session_id, devices, access, reservation_group, reservation_timeout
        )
        response = self._query(request)

        return GenericResponse(response)

    def reset_devices(self, devices: str = None) -> GenericResponse:
        """
        Resets devices to default state.

        This method sends the specified modules a software reset signal, reinitializes module
        registers to their initial value, and rereads the module's non-volatile memory.
        If you specify a chassis, this method resets all modules in the chassis.

        By default the function will reset the session devices
        """

        if devices is None:
            devices = self._resources

        request = ResetDevicesRequest(self._get_uid(), self._session_id, devices)
        response = self._query(request)

        return GenericResponse(response)

    def unreserve_devices(self, devices: str = None) -> GenericResponse:
        """
        Unreserves one or multiple devices so that other sessions can reserve them.

        By default, function will unreserve session devices
        """

        if devices is None:
            devices = self._resources

        request = UnreserveDevicesRequest(self._get_uid(), self._session_id, devices)
        response = self._query(request)

        return GenericResponse(response)

    def commit_properties(self, devices: str = None) -> GenericResponse:
        """
        Commits properties with pending changes to SLSC hardware.

        You must commit dynamic properties for the changes to take effect.

        You do not have to commit static properties because changes take effect immediately after
        you set static properties.

        If you set a property multiple times before you commit the
        property, this method commits only the last value.
        """

        if devices is None:
            devices = self._resources

        request = CommitPropertiesRequest(self._get_uid(), self._session_id, devices)
        response = self._query(request)

        return GenericResponse(response)


if __name__ == "__main__":
    chassis_name = "SLSC-12001-TSE"

    with Device(chassis_name, devices=chassis_name) as dev:
        props = dev.get_property_list()
        print(props.dynamic_properties)
        print(props.static_properties)
