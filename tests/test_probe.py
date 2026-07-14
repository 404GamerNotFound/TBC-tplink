import asyncio

import tplink.service as service_module
from tbc_camera_api import onvif as _onvif
from tplink.service import probe_camera

OnvifProbe = _onvif.OnvifProbe


def test_probe_camera_prefers_onvif_stream_uri(monkeypatch):
    def fake_probe_onvif(**kwargs):
        return OnvifProbe(success=True, message="ok", stream_uris=["rtsp://192.0.2.10:554/onvif-profile"])

    monkeypatch.setattr(service_module, "probe_onvif", fake_probe_onvif)
    camera = {"host": "192.0.2.10", "username": "admin", "password": "secret", "rtsp_port": 554}
    snapshot = asyncio.run(probe_camera(camera))
    assert snapshot.stream_uri == "rtsp://admin:secret@192.0.2.10:554/onvif-profile"


def test_probe_camera_falls_back_to_tapo_default_path(monkeypatch):
    def fake_probe_onvif(**kwargs):
        return OnvifProbe(success=False, message="ONVIF nicht erreichbar", stream_uris=[])

    monkeypatch.setattr(service_module, "probe_onvif", fake_probe_onvif)
    camera = {"host": "192.0.2.10", "username": "admin", "password": "secret", "rtsp_port": 554}
    snapshot = asyncio.run(probe_camera(camera))
    assert snapshot.stream_uri == "rtsp://admin:secret@192.0.2.10:554/stream1"
    assert snapshot.status == "warn"
