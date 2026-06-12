# SMARTBOXX

[GitHub](https://github.com/dakeeper/smartboxx)

System-Monitor & Verwaltung für Raspberry Pi mit 3.5" Touchscreen.

## Voraussetzungen

- Raspberry Pi (getestet auf Pi4 / Pi5)
- 3.5" HDMI TFT Display (z.B. Waveshare)
- Raspberry Pi OS (Bookworm oder neuer)
- Python 3 + Tkinter
- Internetzugang (für Update-Check)

## Installation – Schnellstart

Ein Befehl – lädt alles herunter und richtet Autostart ein:

```bash
curl -sL https://raw.githubusercontent.com/dakeeper/smartboxx/main/install.sh | bash
```

Nach Ausführung: **Pi neustarten** – SMARTBOXX startet automatisch.

## Manuelle Installation (Schritt für Schritt)

### 1. Display konfigurieren

```
# /boot/firmware/config.txt
dtoverlay=mhs35:rotate=90
```

### 2. SMARTBOXX installieren

```bash
# Verzeichnisse anlegen
mkdir -p ~/.local/bin ~/SMARTBOXX-TOOLS ~/mariadb-backups

# Dateien herunterladen (von GitHub Release)
curl -sL https://github.com/dakeeper/smartboxx/releases/latest/download/smartboxx.py \
  -o ~/.local/bin/smartboxx.py
curl -sL https://github.com/dakeeper/smartboxx/releases/latest/download/sql-import \
  -o ~/SMARTBOXX-TOOLS/sql-import
chmod +x ~/.local/bin/smartboxx.py ~/SMARTBOXX-TOOLS/sql-import
```

### 3. Abhängigkeiten installieren

```bash
sudo apt update
sudo apt install -y python3-tk python3-pip mariadb-client pv
```

### 4. Autostart einrichten

```bash
mkdir -p ~/.config/autostart

cat > ~/.config/autostart/smartboxx.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=SMARTBOXX
Exec=python3 /home/pi/.local/bin/smartboxx.py
Terminal=false
EOF
```

### 5. Sudo-Rechte (für Neustart / Herunterfahren)

```bash
echo "$USER ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/reboot" \
  | sudo tee /etc/sudoers.d/010_smartboxx
```

### 6. Benutzername anpassen

Ersetze in `~/.config/autostart/smartboxx.desktop` ggf. `/home/pi/` durch dein Home-Verzeichnis.

### 7. Neustarten

```bash
sudo reboot
```

## Updates

Clients prüfen automatisch beim Start und dann jede Stunde, ob ein neues Release auf GitHub verfügbar ist.

- **Kein Update:** Keine Anzeige – alles aktuell.
- **Update verfügbar:** Im Header erscheint grüner Link `[Update vX.X]` – einmal tippen, Programm lädt herunter und startet neu.

Manuelles Update:

```bash
curl -sL https://raw.githubusercontent.com/dakeeper/smartboxx/main/install.sh | bash
```

## Versionen

| Version | Datum | Änderungen |
|---------|-------|-----------|
| 1.2 | 12.06.2026 | Update-Prüfung, Installation, Master-Marker |
| 1.1 | 12.06.2026 | Alle Backups anzeigen, Fortschrittsbalken, Strg+C Fix |
| 1.0 | - | Initialversion |
