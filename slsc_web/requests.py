from abc import ABC, abstractmethod
from enum import Enum
import json


class AccessType(Enum):
    ReadOnly = 1
    ReadWrite = 3


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

    def _initialize_parameters(
        self,
        devices: str = None,
        physical_channels: str = None,
        nvmem_areas: str = None,
    ) -> dict:
        if devices is not None:
            return {"devices": devices.split(",")}
        elif physical_channels is not None:
            return {"physical_channels": physical_channels.split(",")}
        else:  # TODO: need to think about case where they are all None
            return {"nvmem_areas": nvmem_areas.split(",")}


class InitializeRequest(Request):
    """
    Request for initializing an SLSC session
    """

    def __init__(
        self,
        id: int,
        devices: str = None,
        physical_channels: str = None,
        nvmem_areas: str = None,
    ):
        params = self._initialize_parameters(devices, physical_channels, nvmem_areas)
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


class GetDevicePropertyListRequest(Request):
    """
    Request for getDevicePropertyList
    Lists all properties for single device, channel, or nvmem_area
    """

    def __init__(self, id: int, session_id: str, device: str):

        params = {"session_id": session_id, "device": device}

        super().__init__(id, params)

    def _get_method(self) -> str:
        return "getDevicePropertyList"


class GetSessionPropertyListRequest(Request):
    """
    Request for getSessionPropertyList
    Lists all session properties
    """

    def __init__(self, id: int, session_id: str):
        params = {"session_id": session_id}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "getSessionPropertyList"


class GetPropertyRequest(Request):
    """
    Gets properties for device, physical channel, or nvmem area
    """

    def __init__(
        self,
        id: int,
        session_id: str,
        property: str,
        devices: str = None,
        physical_channels: str = None,
        nvmem_areas: str = None,
    ):
        params = self._initialize_parameters(devices, physical_channels, nvmem_areas)
        params["session_id"] = session_id
        params["property"] = property
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "getProperty"


class AbortRequest(Request):
    """
    Cancels a method that blocks network communications

    After aborting the session, the session handle remains valid, but the methods that access
    network connections return errors. To recover from an aborted session, close the session
    and initialize a new one.
    """

    def __init__(self, id: int, session_id: str):
        params = {"session_id": session_id}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "abortSession"


class ConnectToDevicesRequest(Request):
    """
    Connects to an SLSC Device
    """

    def __init__(self, id: int, session_id: str, devices: str):
        params = {"session_id": session_id, "devices": devices.split(",")}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "connectToDevices"


class DisconnectFromDevicesRequest(Request):
    """
    Disconnects from an SLSC Device
    """

    def __init__(self, id: int, session_id: str, devices: str):
        params = {"session_id": session_id, "devices": devices.split(",")}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "disconnectFromDevices"


class ResetDevicesRequest(Request):
    """
    Resets devices to default state
    """

    def __init__(self, id: int, session_id: str, devices: str):
        params = {"session_id": session_id, "devices": devices.split(",")}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "resetDevices"


class RenameDeviceRequest(Request):
    """
    Renames a device
    """

    def __init__(self, id: int, session_id: str, device: str, new_name: str):
        params = {"session_id": session_id, "device": device, "new_device_name": new_name}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "renameDevice"


class ReserveDeviceRequest(Request):
    """
    Reserves one or multiple devices to prevent other sessions from accessing the devices
    """

    def __init__(
        self,
        id: int,
        session_id: str,
        devices: str = None,
        access: AccessType = AccessType.ReadWrite,
        reservation_group: str = "",
        reservation_timeout: float = 0.0,
    ):
        params = {
            "session_id": session_id,
            "devices": devices.split(","),
            "access": access.name,
            "reservation_group": reservation_group,
            "reservation_timeout": reservation_timeout,
        }
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "reserveDevices"


class UnreserveDevicesRequest(Request):
    """
    Resets devices to default state
    """

    def __init__(self, id: int, session_id: str, devices: str):
        params = {"session_id": session_id, "devices": devices.split(",")}
        super().__init__(id, params)

    def _get_method(self) -> str:
        return "unreserveDevices"


if __name__ == "__main__":
    init = InitializeRequest(4, "SLSC-12201")
    print(init.serialize())
