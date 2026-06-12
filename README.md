# SMARTBOXX

[GitHub](https://github.com/dakeeper/smartboxx)

System-Monitor & Verwaltung für Raspberry Pi mit 3.5" Touchscreen.

## Versionen

| Version | Datum | Änderungen |
|---------|-------|-----------|
| 1.1 | 12.06.2026 | Alle Backups anzeigen, Fortschrittsbalken, Strg+C Fix |
| 1.0 | - | Initialversion |

## Master-Gerät

Das Gerät mit Hostname `SMARTBOXX-Pi4M` ist der Master.
Nur hier werden Änderungen entwickelt und per Git pushed.

## Client-Installation

```bash
curl -sL https://raw.githubusercontent.com/dakeeper/smartboxx/main/install.sh | bash
```

Clients prüfen automatisch jede Stunde auf neue Releases.
Bei einem Update erscheint `[Update vX.X]` im Header – klickbar zum Download.
