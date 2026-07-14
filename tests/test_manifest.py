import json
from pathlib import Path

from tplink.module import TpLinkCameraModule
from tbc_camera_api import CameraCapability

_PLUGIN_DIR = Path(__file__).resolve().parent.parent


def _manifest() -> dict:
    return json.loads((_PLUGIN_DIR / "manifest.json").read_text(encoding="utf-8"))


def test_manifest_capabilities_match_module_class():
    manifest = _manifest()
    manifest_capabilities = {CameraCapability(value) for value in manifest["capabilities"]}
    assert manifest_capabilities == TpLinkCameraModule.capabilities


def test_manifest_key_and_ports_match_module_defaults():
    manifest = _manifest()
    module = TpLinkCameraModule()
    assert manifest["key"] == module.key
    assert manifest["ports"]["onvif"] == module.default_onvif_port
    assert manifest["ports"]["http"] == module.default_http_port
    assert manifest["ports"]["rtsp"] == module.default_rtsp_port


def test_module_exposes_required_capability_methods():
    module = TpLinkCameraModule()
    assert hasattr(module, "probe")
    if CameraCapability.DETECTIONS in module.capabilities:
        assert module.detection_definitions()
    if CameraCapability.CONTROL in module.capabilities:
        assert hasattr(module, "get_control_state")
        assert hasattr(module, "send_control")
