SMARTBOXX V1.40 - Display-Programm
===================================

  GitHub:       https://github.com/dakeeper/smartboxx

  Clients prüfen automatisch auf Updates.
  Bei neuer Version erscheint [Update vX.X] im Header (klickbar).

Installation
-------------
  Schnellstart (ein Befehl):
    curl -sL https://raw.githubusercontent.com/dakeeper/smartboxx/main/install.sh | bash

  Manuell:
    1. sudo apt install -y python3-tk mariadb-client pv
    2. ~/SMARTBOXX-TOOLS/sql-import
    3. mkdir -p ~/.config/autostart
    4. Autostart-Datei erstellen (siehe GitHub README)
    5. sudo reboot

Das Programm zeigt System-Informationen auf dem 3.5"-Touchscreen an.
Es startet automatisch beim Hochfahren.

Hauptbildschirm
---------------
Oben (Kopfzeile):
  • Uptime         - wie lange der Pi schon läuft (z.B. 2d 14h 32m)
  • Boots: X       - Boot-Zähler (alle 25: Backup-Erinnerung)
  • Refresh: Xs    - Countdown bis zur nächsten Aktualisierung
  • SRCN:MM:SS     - Countdown bis Screensaver (10 Min. Inaktivität)
  • SRCN:AKTIV     - Screensaver läuft (Touch beendet ihn)
  • Datum + Uhrzeit

Mitte (System-Daten):
  • Ext-IP         - öffentliche IP-Adresse (Internet)
  • Loc-IP         - lokale IP-Adresse im Netzwerk
  • CPU-Temp       - Prozessor-Temperatur mit Farbe:
       Grün  (< 55°C)  - Alles gut
       Gelb  (55-63°C) - Warnung
       Rot   (64-70°C) - Heiß
       Rot + !        (> 70°C) - Zu heiß
       Rot + !!! blinkend (≥ 80°C) - Kritisch!
  • SD-Free        - freier Speicherplatz auf der SD-Karte
  • RAM            - Arbeitsspeicher-Nutzung
  • MariaDB        - Datenbank-Status (Running/Not Running)
  • Samba           - SMB-Freigabe-Status (Running/Not Running)

Die Daten aktualisieren sich automatisch alle 10 Sekunden.

Buttons (unten)
---------------
  CLOSE  - Programm beenden
  REBOOT - Pi neu starten
  SERV   - Dienste-Status anzeigen (MariaDB, Apache, SSH, Samba)
  DB     - Datenbank-Zugangsdaten (MariaDB, phpMyAdmin)
  NET    - Netzwerk-Einstellungen
  SMB    - Samba-Freigabe Info (Netzwerkpfad, Konfiguration)

  Tipp: 3x im Hauptbereich tippen → Shutdown-Dialog (JA/NEIN)

NET - Netzwerk-Einstellungen
-----------------------------
  DHCP     - automatische IP (wenn vorher statisch: erscheint eine
             Sicherheitsfrage "Wechseln zu DHCP?")
  Static IP- manuelle IP-Eingabe mit Bildschirm-Tastatur
  Back     - zurück zum Hauptbildschirm

Static IP eingeben:
  Die aktuellen Werte sind in Grau vorgefüllt.
  Einfach ins Feld tippen - es wird leer und du kannst die neue IP
  eintragen.
  Mit den IP/GW/DNS-Buttons springst du zwischen den Feldern.
  Nach Speichern: Wenn sich die IP ändert, fragt das Programm ob
  neu gestartet werden soll.

SERV - Dienste
-------------
  Zeigt OS-Version, Kernel-Version und welche Dienste laufen (grün)
  oder gestoppt sind (rot):
  • MariaDB, Apache, SSH, Samba
  Hinter dem Status steht die Versionsnummer (z.B. 11.8.6, 2.4.67)

  Neben jedem Dienst gibt es 3 Buttons:
  - START  → Dienst starten
  - STOP   → Dienst stoppen
  - REST   → Dienst neustarten
  - Vor der Aktion erscheint eine Sicherheitsfrage (Ja/Nein)
  - Nach erfolgreicher Änderung erscheint ein Info-Fenster

DB - Datenbank-Zugangsdaten
----------------------------
  MariaDB:
    Benutzer: admin
    Passwort: admin
    (auch root / root)

  phpMyAdmin:
    http://IP-Adresse/phpmyadmin
    (IP-Adresse steht auf dem Hauptbildschirm unter Loc-IP)

SMARTBOXX SQL-TOOL (sql-import)
-------------------------------
  Terminal-Befehl:  ~/SMARTBOXX-TOOLS/sql-import

  Zweistufiges Menü (ESC = eine Ebene zurück):

  ─── Hauptmenü ───
    • Backup erstellen
      → DB Komplettbackup (alle)  (mariadb-dump)
      → Einzelne DB exportieren
      → Einzelne Tabelle exportieren
    • Wiederherstellen
      → DB Backup wiederherstellen  (komplettes Backup)
      → Einzelne DB wiederherstellen
      → Einzelne Tabelle wiederherstellen
    • DB / Tabelle verwalten
      → Datenbank löschen
      → Tabelle löschen
      → DB duplizieren
      → Tabelle duplizieren
    • Tools
      → SQL-Datei importieren  (Datei-Browser mit Pfeiltasten)
      → Import verifizieren  (Zeilenvergleich Datei ↔ DB)
      → Alle Backups anzeigen  (Liste mit ↑↓ blättern)

  Zugangsdaten: root / root
  Backup-Ordner: ~/mariadb-backups/ (wird im Menü angezeigt)
  Fortschrittsanzeige: pv mit echten Balken + Prozent

  Das Skript liegt in ~/SMARTBOXX-TOOLS/sql-import

Samba (Netzwerk-Freigabe)
-------------------------
  Der Ordner ~/SAMBA ist ohne Passwort im Netzwerk freigegeben.
  Die Geräte sollten automatisch im Netzwerk erscheinen (WS-Discovery).
  Falls nicht, direkt eingeben:
    Windows: \\\\NETBIOS-NAME\\home
    Linux:   smb://NETBIOS-NAME/home

  Dieser Pi: \\\\SMARTBOXX-Pi4M\\home  →  /home/dakeeper/SAMBA

Screensaver
-----------
  Nach 3 Minuten Inaktivität (kein Touch) startet der Screensaver.
  Der Screensaver zeigt im Wechsel an:
    - SMARTBOXX + Datum/Uhrzeit (15s)
    - Black (15s)
    - SMARTBOXX + System uptime (15s)
    - Black (15s)
    - SMARTBOXX + CPU Temp (15s)
    - Black (15s)
  Ein Tipp auf den Touchscreen beendet den Screensaver sofort.
  Im Hauptbildschirm zeigt SRCN:MM:SS den Countdown bis zum
  Screensaver an (z.B. SRCN:09:59).

Bildschirmrotation (ROTATE)
----------------------------
  Der ROTATE-Button im Exit-Dialog (CLOSE-Menü) dreht den Bildschirm
  um 180°. Die Einstellung bleibt nach Neustart erhalten.

  Voraussetzungen:
    1. LCD-show installiert (MHS35-Overlay + Kalibrierungs-Dateien)
    2. NOPASSWD für rotate-Kommandos (automatisch via install.sh):
         /bin/cat, /bin/cp, /bin/bash, /bin/sync, /bin/sed

  Ablauf:
    • ROTATE im Exit-Dialog klicken
    • Config wird umgeschaltet (90° ↔ 270°)
    • Touch-Kalibrierung wird getauscht
    • Neustart-Dialog → JA = sofort rebooten / NEIN = später

  Ohne diese Voraussetzungen hängt das Programm (kein TTY für sudo).

MariaDB Optimierung
-------------------
  Config: /etc/mysql/mariadb.conf.d/50-server.cnf
  Aktuelle Werte (Pi4 mit 4GB RAM):
    innodb_buffer_pool_size = 2G   (50% des RAM)
    innodb_log_file_size    = 128M
    max_connections         = 50
    query_cache_size        = 0

  Nach Änderungen: sudo systemctl restart mariadb

Changelog
---------
  1.40 (15.06.2026)
    - [NEU] ROTATE-Button im Exit-Dialog (180°-Bildschirmrotation)
    - [NEU] Touch-Kalibrierung inkludiert (Umschalten per NOPASSWD)
    - [FIX] sudo-Passwort-Cache: NOPASSWD für cat/cp/bash/sync/sed
    - [FIX] Zuverlässige Rotation via Python-IO (kein grep/sed mehr)

  1.32 (15.06.2026)
    - [NEU] Modernes Menü-Design (Doppellinien-Rahmen, Nummern-Kurztasten 1-9)
    - [NEU] DB-Erstellungsabfrage bei Tabellen-Restore (fehlende DB wird angelegt)
    - [FIX] DB-Marker-Suche liest nur erste 1MB (von 16ms statt 5,5s)
    - [FIX] Header-Box korrekt ausgerichtet (44 Zeichen)
    - [FIX] Fortschrittsanzeige bei Extraktion aus großen Backups

  1.31 (15.06.2026)
    - [NEU] 2-stufiges Menü im SQL-Tool (Backup/Wiederherstellen/Verwalten/Tools)
    - [FIX] Verify-Zeilen zählt multi-line INSERTs korrekt
    - [FIX] Table-Restore bei Dumps ohne DB-Marker (in_db=1 Fallback)
    - [FIX] stderr unterdrückt (2>/dev/null), EST_SIZE ×2 für pv

  1.30 (15.06.2026)
    - [NEU] MariaDB-Konfiguration optimiert (innodb_buffer_pool_size=2G u.a.)
    - [NEU] Screensaver 6-Phasen-Zyklus mit Single-Tick-Loop
    - [FIX] GDBus PolicyKit-Fehler (lxpolkit auf /bin/true umgeleitet)

  1.0 (Initialversion)
    - System-Monitor mit IP, CPU, RAM, HD, Diensten
    - SQL-Import/Backup/Restore-Tool
    - Screensaver, Netzwerk-Einstellungen

  1.2 (12.06.2026)
    - [NEU] Automatische Update-Prüfung über GitHub
    - [NEU] Installationsanleitung (README + install.sh)
    - [NEU] Master-Erkennung via ~/.smartboxx_marker
    - [NEU] öffentliche IP-Anzeige, Version 1.2

  1.1 (12.06.2026)
    - [NEU] Menüpunkt "Alle Backups anzeigen" mit ↑↓-Blättern
    - [FIX] Fortschrittsbalken: pv zeigt jetzt echten Balken + Prozent
            (Backup mit geschätzter Größe aus information_schema)
    - [FIX] Strg+C bricht Backup ab → direkt zurück ins Menü
            (keine "Alte Backups löschen"-Abfrage mehr)
    - [FIX] Import/Wiederherstellung: pv mit Dateigröße = sauberer Balken
