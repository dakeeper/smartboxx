#!/bin/bash
# SMARTBOXX Client-Installation
# Führt Update-Check und Erstinstallation durch

set -e
REPO="https://github.com/dakeeper/smartboxx"
USER_HOME="$HOME"

echo "SMARTBOXX Installation"
echo "======================"
echo ""

# Prüfe ob bereits installiert
if [ -f "$USER_HOME/.local/bin/smartboxx.py" ]; then
    echo "SMARTBOXX ist bereits installiert."
    echo "Updates werden automatisch über das Programm geprüft."
    exit 0
fi

# Verzeichnisse anlegen
mkdir -p "$USER_HOME/.local/bin"
mkdir -p "$USER_HOME/SMARTBOXX-TOOLS"
mkdir -p "$USER_HOME/mariadb-backups"

# Dateien herunterladen
echo "Lade SMARTBOXX herunter..."
curl -sL "$REPO/releases/latest/download/smartboxx.py" \
  -o "$USER_HOME/.local/bin/smartboxx.py"
curl -sL "$REPO/releases/latest/download/sql-import" \
  -o "$USER_HOME/SMARTBOXX-TOOLS/sql-import"
chmod +x "$USER_HOME/.local/bin/smartboxx.py"
chmod +x "$USER_HOME/SMARTBOXX-TOOLS/sql-import"

# Abhängigkeiten installieren
echo "Installiere Abhängigkeiten..."
sudo apt update
sudo apt install -y python3-tk python3-pip mariadb-client pv 2>/dev/null

# Autostart
echo "Richte Autostart ein..."
mkdir -p "$USER_HOME/.config/autostart"
cat > "$USER_HOME/.config/autostart/smartboxx.desktop" << EOF
[Desktop Entry]
Type=Application
Name=SMARTBOXX
Exec=python3 $USER_HOME/.local/bin/smartboxx.py
Terminal=false
EOF

# Desktop-Verknüpfung
cat > "$USER_HOME/Desktop/SMARTBOXX.desktop" << EOF
[Desktop Entry]
Type=Application
Name=SMARTBOXX
Exec=python3 $USER_HOME/.local/bin/smartboxx.py
Terminal=false
EOF
chmod +x "$USER_HOME/Desktop/SMARTBOXX.desktop"

# sudoers für reboot/shutdown
echo "Setze sudo-Rechte (shutdown/reboot)..."
echo "$USER ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/reboot" \
  | sudo tee /etc/sudoers.d/010_smartboxx > /dev/null

# sudoers für Bildschirmrotation (ROTATE-Button)
echo "Setze sudo-Rechte (rotate)..."
echo "$USER ALL=(ALL) NOPASSWD: /bin/cat, /bin/cp, /bin/bash, /bin/sync, /bin/sed" \
  | sudo tee /etc/sudoers.d/010_rotate > /dev/null

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║  Installation abgeschlossen!          ║"
echo "║                                       ║"
echo "║  Starte SMARTBOXX mit:                ║"
echo "║    python3 ~/.local/bin/smartboxx.py  ║"
echo "║                                       ║"
echo "║  Oder: Pi neustarten →                ║"
echo "║    sudo reboot                        ║"
echo "╚═══════════════════════════════════════╝"
echo ""
