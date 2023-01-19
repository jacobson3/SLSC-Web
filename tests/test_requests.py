import slsc_web.requests as requests


def test_initialize_request():
    message = requests.InitializeRequest(3, "SLSC-12201")
    
    result = r'{"id": "3", "jsonrpc": "2.0", "method": "initializeSession", "params": {"devices": ["SLSC-12201"]}}'
    assert message.serialize() == result

def test_close_request():
    message = requests.CloseRequest(4, "_session0")

    result = r'{"id": "4", "jsonrpc": "2.0", "method": "closeSession", "params": {"session_id": "_session0"}}'
    assert message.serialize() == result
