# TBC-tplink

Camera plugin for [TBC](https://github.com/404GamerNotFound/TBC-camera-manager) for TP-Link
Tapo network cameras through ONVIF and RTSP.

## Features

- **Live view**: RTSP stream, primarily from the media URI reported by the device via ONVIF.
- **Recording**: Event and continuous recording through TBC's generic recording pipeline.
- **Detection**: Motion, person, vehicle, pet, crying, and doorbell/visitor — see
  `detections.json`. TBC discovers the keys actually supported by a device from its ONVIF
  event properties at runtime.
- **Control**: PTZ (pan/tilt/zoom) through the vendor-neutral ONVIF PTZ service.

## Setup

1. Enable ONVIF in the Tapo app (default port `2020`).
2. Add the camera in TBC with its host, ONVIF port, and the camera credentials assigned in the
   Tapo app — not the TP-Link cloud account.
3. If ONVIF does not provide a usable stream URI, this plugin automatically uses the Tapo
   default path `rtsp://.../stream1` (main stream) as a fallback.

## Known limitations

- Many Tapo models implement ONVIF `GetStreamUri` unreliably; the RTSP fallback is used
  automatically in that case.

## Independence

This project is independent and is not affiliated with, endorsed by, or sponsored by TP-Link.
