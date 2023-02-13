import slsc_web.requests as requests


def test_initialize_request():
    message = requests.InitializeRequest(3, "SLSC-12201")

    result = r'{"id": "3", "jsonrpc": "2.0", "method": "initializeSession", "params": {"devices": ["SLSC-12201"]}}'
    assert message.serialize() == result


def test_close_request():
    message = requests.CloseRequest(4, "_session0")

    result = r'{"id": "4", "jsonrpc": "2.0", "method": "closeSession", "params": {"session_id": "_session0"}}'
    assert message.serialize() == result


def test_get_property_list():
    message = requests.GetDevicePropertyListRequest(8, "_session2", "TSE1")

    result = r'{"id": "8", "jsonrpc": "2.0", "method": "getDevicePropertyList", "params": {"session_id": "_session2", "device": "TSE1"}}'
    assert message.serialize() == result


def test_get_session_property_list():
    message = requests.GetSessionPropertyListRequest(11, "_session12")

    result = r'{"id": "11", "jsonrpc": "2.0", "method": "getSessionPropertyList", "params": {"session_id": "_session12"}}'
    assert message.serialize() == result


def test_get_property():
    message = requests.GetPropertyRequest(3, "_session7", "Dev.Modules", "TSE2")

    result = r'{"id": "3", "jsonrpc": "2.0", "method": "getProperty", "params": {"devices": ["TSE2"], "session_id": "_session7", "property": "Dev.Modules"}}'
    assert message.serialize() == result


def test_abort_session():
    message = requests.AbortRequest(4, "_session11")

    result = r'{"id": "4", "jsonrpc": "2.0", "method": "abortSession", "params": {"session_id": "_session11"}}'
    assert message.serialize() == result


def test_connect_to_device():
    message = requests.ConnectToDevicesRequest(9, "_session42", "TSE21")

    result = r'{"id": "9", "jsonrpc": "2.0", "method": "connectToDevices", "params": {"session_id": "_session42", "devices": ["TSE21"]}}'
    assert message.serialize() == result


def test_disconnect_from_device():
    message = requests.DisconnectFromDevicesRequest(19, "_session2", "TSE21,TSE_Mod1")

    result = r'{"id": "19", "jsonrpc": "2.0", "method": "disconnectFromDevices", "params": {"session_id": "_session2", "devices": ["TSE21", "TSE_Mod1"]}}'
    assert message.serialize() == result


def test_rename_device():
    message = requests.RenameDeviceRequest(7, "_session0", "Mod1", "RTD_Sim")

    result = r'{"id": "7", "jsonrpc": "2.0", "method": "renameDevice", "params": {"session_id": "_session0", "device": "Mod1", "new_device_name": "RTD_Sim"}}'
    assert message.serialize() == result


def test_reserve_devices():
    message = requests.ReserveDeviceRequest(
        5, "_session4", "TSE21,TSE_Mod1", requests.AccessType.ReadOnly, "nitest", 1.5
    )

    result = r'{"id": "5", "jsonrpc": "2.0", "method": "reserveDevices", "params": {"session_id": "_session4", "devices": ["TSE21", "TSE_Mod1"], "access": "ReadOnly", "reservation_group": "nitest", "reservation_timeout": 1.5}}'
    assert message.serialize() == result


def test_reset_devices():
    message = requests.ResetDevicesRequest(87, "_session99", "TSE_Mod1,TSE_Mod2")

    result = r'{"id": "87", "jsonrpc": "2.0", "method": "resetDevices", "params": {"session_id": "_session99", "devices": ["TSE_Mod1", "TSE_Mod2"]}}'
    assert message.serialize() == result


def test_unreserve_devices():
    message = requests.UnreserveDevicesRequest(7, "_session99", "TSE_Mod11,TSE_Mod22")

    result = r'{"id": "7", "jsonrpc": "2.0", "method": "unreserveDevices", "params": {"session_id": "_session99", "devices": ["TSE_Mod11", "TSE_Mod22"]}}'
    assert message.serialize() == result


def test_commit_properties():
    message = requests.CommitPropertiesRequest(31, "_session9", "SLSC-12201")

    result = r'{"id": "31", "jsonrpc": "2.0", "method": "commitProperties", "params": {"devices": ["SLSC-12201"], "session_id": "_session9"}}'
    assert message.serialize() == result


def test_get_property_information():
    message = requests.GetPropertyInformationRequest(3, "_session7", "Dev.Modules", "TSE2")

    result = r'{"id": "3", "jsonrpc": "2.0", "method": "getPropertyInformation", "params": {"devices": ["TSE2"], "session_id": "_session7", "property": "Dev.Modules"}}'
    assert message.serialize() == result
