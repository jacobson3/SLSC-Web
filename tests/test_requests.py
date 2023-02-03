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
