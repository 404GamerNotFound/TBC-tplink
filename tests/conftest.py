"""Stub tbc_camera_api so this plugin's tests run standalone (no TBC-camera-manager checkout needed).

module.py/service.py/catalog.py/control.py import CameraCapability/CameraModule/
CameraSnapshot plus the onvif/onvif_control/streams/detections helper
submodules from tbc_camera_api at module scope - inside the real TBC process
that facade is installed by camera_modules/packages.py before a plugin is
ever imported, but a plugin's own standalone test run never goes through
that loader, so this fake stands in for it. The pure URI/dataclass helpers
below are copied from app/tbc/camera_modules/{streams,onvif,detections}.py
so tests that exercise real stream-URI-building logic (not just imports)
still get correct results; probe_onvif/onvif_control/probe_rtsp_stream are
always monkeypatched by tests that need them, so those stay stubs.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import types
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit


def _install_fake_tbc_camera_api() -> None:
    if "tbc_camera_api" in sys.modules:
        return

    class _FakeCameraCapability(str, Enum):
        LIVE = "live"
        RECORDING = "recording"
        DETECTIONS = "detections"
        CHANNELS = "channels"
        ARCHIVE = "archive"
        CONTROL = "control"
        FIRMWARE = "firmware"

    class _FakeCameraModule:
        key = ""
        label = ""
        description = ""
        default_onvif_port = 8000
        default_http_port = 80
        default_rtsp_port = 554
        supports_manual_stream_uri = False
        requires_manual_stream_uri = False
        requires_credentials = True
        capabilities: frozenset = frozenset()
        identifier_label = None

        def supports(self, capability):
            return capability in self.capabilities

        def detection_definitions(self):
            return ()

        async def probe(self, camera):
            raise NotImplementedError

    @dataclass
    class _FakeCameraSnapshot:
        status: str
        message: str
        manufacturer: str | None = None
        model: str | None = None
        firmware: str | None = None
        serial: str | None = None
        stream_uri: str | None = None
        detections: list = field(default_factory=list)
        channels: list = field(default_factory=list)
        metrics: dict = field(default_factory=dict)

    @dataclass(frozen=True)
    class _FakeDetectionDefinition:
        key: str
        label: str
        category: str

    detections_module = types.ModuleType("tbc_camera_api.detections")
    detections_module.DetectionDefinition = _FakeDetectionDefinition

    @dataclass
    class _FakeOnvifProbe:
        success: bool
        message: str
        manufacturer: str | None = None
        model: str | None = None
        firmware: str | None = None
        serial: str | None = None
        stream_uris: list = field(default_factory=list)
        stream_profiles: list = field(default_factory=list)
        event_detection_keys: set = field(default_factory=set)
        raw_events: str | None = None

    def _fake_probe_onvif(*, host, port, username, password, timeout_seconds=8):
        raise NotImplementedError

    onvif_module = types.ModuleType("tbc_camera_api.onvif")
    onvif_module.OnvifProbe = _FakeOnvifProbe
    onvif_module.probe_onvif = _fake_probe_onvif

    def _rtsp_uri_with_credentials(uri, username, password):
        parsed = urlsplit(str(uri))
        if parsed.scheme.lower() != "rtsp" or not parsed.hostname:
            return str(uri)
        host = parsed.hostname
        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        port = f":{parsed.port}" if parsed.port else ""
        userinfo = f"{quote(str(username), safe='')}:{quote(str(password), safe='')}@"
        return urlunsplit(("rtsp", f"{userinfo}{host}{port}", parsed.path, parsed.query, parsed.fragment))

    def _build_rtsp_uri(*, host, port, path, username, password):
        normalized_host = str(host).strip()
        if ":" in normalized_host and not normalized_host.startswith("["):
            normalized_host = f"[{normalized_host}]"
        normalized_path = f"/{str(path).lstrip('/')}"
        userinfo = f"{quote(str(username), safe='')}:{quote(str(password), safe='')}@"
        return f"rtsp://{userinfo}{normalized_host}:{int(port)}{normalized_path}"

    def _probe_rtsp_stream(stream_uri, timeout_seconds=8):
        raise NotImplementedError

    def _validate_manual_stream_uri(value):
        uri = str(value or "").strip()
        if not uri or any(character in uri for character in ("\r", "\n", "\x00")):
            raise ValueError("A valid RTSP/RTSPS URL is required")
        parsed = urlsplit(uri)
        if parsed.scheme.lower() not in {"rtsp", "rtsps"} or not parsed.hostname:
            raise ValueError("The stream URL must start with rtsp:// or rtsps:// and contain a host")
        try:
            _ = parsed.port
        except ValueError as exc:
            raise ValueError("The RTSP/RTSPS URL contains an invalid port") from exc
        return uri

    streams_module = types.ModuleType("tbc_camera_api.streams")
    streams_module.rtsp_uri_with_credentials = _rtsp_uri_with_credentials
    streams_module.build_rtsp_uri = _build_rtsp_uri
    streams_module.probe_rtsp_stream = _probe_rtsp_stream
    streams_module.validate_manual_stream_uri = _validate_manual_stream_uri

    async def _get_ptz_control_state(camera, *, default_port=80):
        raise NotImplementedError

    async def _send_ptz_control(camera, *, action, default_port=80, **params):
        raise NotImplementedError

    onvif_control_module = types.ModuleType("tbc_camera_api.onvif_control")
    onvif_control_module.get_ptz_control_state = _get_ptz_control_state
    onvif_control_module.send_ptz_control = _send_ptz_control

    api = types.ModuleType("tbc_camera_api")
    api.CameraCapability = _FakeCameraCapability
    api.CameraModule = _FakeCameraModule
    api.CameraSnapshot = _FakeCameraSnapshot
    api.detections = detections_module
    api.onvif = onvif_module
    api.streams = streams_module
    api.onvif_control = onvif_control_module
    sys.modules["tbc_camera_api"] = api
    sys.modules["tbc_camera_api.detections"] = detections_module
    sys.modules["tbc_camera_api.onvif"] = onvif_module
    sys.modules["tbc_camera_api.streams"] = streams_module
    sys.modules["tbc_camera_api.onvif_control"] = onvif_control_module


_install_fake_tbc_camera_api()

_PLUGIN_DIR = Path(__file__).resolve().parent.parent
_MANIFEST = json.loads((_PLUGIN_DIR / "manifest.json").read_text(encoding="utf-8"))
_PACKAGE_NAME = _MANIFEST["key"]

# The plugin directory has no valid Python package name of its own (repo names
# like "TBC-tplink" contain a hyphen), so TBC's real loader
# (app/tbc/camera_modules/packages.py:load_plugin_module) never imports it by
# path either - it registers a synthetic module name via
# importlib.util.spec_from_file_location and lets the plugin's relative
# imports (`from .catalog import ...`) resolve against that. Tests need the
# same trick to import service.py/catalog.py/control.py outside of TBC itself.
if _PACKAGE_NAME not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        _PACKAGE_NAME,
        _PLUGIN_DIR / "__init__.py",
        submodule_search_locations=[str(_PLUGIN_DIR)],
    )
    _module = importlib.util.module_from_spec(_spec)
    sys.modules[_PACKAGE_NAME] = _module
    _spec.loader.exec_module(_module)
