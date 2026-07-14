# TBC-tplink

Kamera-Plugin für [TBC](https://github.com/404GamerNotFound/TBC-camera-manager) für
TP-Link-Tapo-Netzwerkkameras via ONVIF und RTSP.

## Fähigkeiten

- **Live**: RTSP-Stream, primär über die vom Gerät per ONVIF gemeldete Medien-URI.
- **Aufnahme**: Ereignis- und Daueraufzeichnung über TBCs generische Aufnahme-Pipeline.
- **Erkennung**: Bewegung, Person, Fahrzeug, Haustier, Weinen und Klingel/Besucher – siehe
  `detections.json`. Welche Schlüssel tatsächlich unterstützt werden, ermittelt TBC live
  über die ONVIF-Ereigniseigenschaften des Geräts.
- **Steuerung**: PTZ (Schwenken/Neigen/Zoom) über den herstellerneutralen ONVIF-PTZ-Service.

## Einrichtung

1. ONVIF in der Tapo-App aktivieren (Standardport `2020`).
2. Kamera in TBC mit Host, ONVIF-Port und den in der Tapo-App vergebenen
   Kamera-Zugangsdaten (nicht das TP-Link-Cloud-Konto) anlegen.
3. Liefert ONVIF keine brauchbare Stream-URI, verwendet dieses Plugin automatisch den
   Tapo-Standardpfad `rtsp://.../stream1` (Hauptstream) als Rückfallebene.

## Bekannte Einschränkungen

- Viele Tapo-Modelle setzen ONVIF `GetStreamUri` nur unzuverlässig um; in diesem Fall
  greift automatisch die RTSP-Rückfallebene.

