#!/bin/bash
# SMARTBOXX Client-Installation
# Führt Update-Check und Erstinstallation durch

set -e
REPO="https://github.com/deinuser/smartboxx"

echo "SMARTBOXX Installation"
echo "======================"
echo ""

# Prüfe ob bereits installiert
if [ -f ~/.local/bin/smartboxx.py ]; then
    echo "SMARTBOXX ist bereits installiert."
    echo "Updates werden automatisch über das Programm geprüft."
    exit 0
fi

# Verzeichnisse anlegen
mkdir -p ~/.local/bin
mkdir -p ~/SMARTBOXX-TOOLS
mkdir -p ~/mariadb-backups

# Dateien herunterladen
echo "Lade SMARTBOXX herunter..."
curl -sL "$REPO/releases/latest/download/smartboxx.py" -o ~/.local/bin/smartboxx.py
curl -sL "$REPO/releases/latest/download/sql-import" -o ~/SMARTBOXX-TOOLS/sql-import
chmod +x ~/.local/bin/smartboxx.py ~/SMARTBOXX-TOOLS/sql-import

# Autostart
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/smartboxx.desktop << EOF
[Desktop Entry]
Type=Application
Name=SMARTBOXX
Exec=python3 ~/.local/bin/smartboxx.py
Terminal=false
EOF

# sudoers für reboot/shutdown
echo "dakeeper ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/reboot" | sudo tee /etc/sudoers.d/010_smartboxx

echo ""
echo "Installation abgeschlossen!"
echo "Starte SMARTBOXX mit: python3 ~/.local/bin/smartboxx.py"
