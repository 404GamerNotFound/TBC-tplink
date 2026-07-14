from tplink.service import tapo_rtsp_uri


def test_rtsp_uri_defaults_to_stream1():
    camera = {"host": "192.0.2.10", "username": "admin", "password": "secret", "rtsp_port": 554}
    uri = tapo_rtsp_uri(camera, stream="stream1")
    assert uri == "rtsp://admin:secret@192.0.2.10:554/stream1"


def test_rtsp_uri_stream2():
    camera = {"host": "192.0.2.10", "username": "admin", "password": "secret", "rtsp_port": 554}
    uri = tapo_rtsp_uri(camera, stream="stream2")
    assert uri.endswith("/stream2")


def test_rtsp_uri_escapes_credentials():
    camera = {"host": "192.0.2.10", "username": "ad min", "password": "p@ss/word", "rtsp_port": 554}
    uri = tapo_rtsp_uri(camera, stream="stream1")
    assert "ad%20min" in uri
    assert "p%40ss%2Fword" in uri


def test_rtsp_uri_brackets_ipv6_host():
    camera = {"host": "2001:db8::1", "username": "admin", "password": "secret", "rtsp_port": 554}
    uri = tapo_rtsp_uri(camera, stream="stream1")
    assert "@[2001:db8::1]:554/" in uri
