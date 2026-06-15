#!/usr/bin/env python3
# Tue es, oder tue es nicht. Es gibt kein Versuchen.
# Coded by Holger Palloks - Support @ holger.palloks@gut-gruppe.de
import tkinter as tk
import urllib.request
import threading
import socket
import os
import subprocess
import shutil
import datetime
import re
# Coded by Holger Palloks - Support @ holger.palloks@gut-gruppe.de
# Tue es, oder tue es nicht. Es gibt kein Versuchen.

LOCAL_VER = "1.3"
IS_MASTER = os.path.exists(os.path.expanduser("~/.smartboxx_master"))
GITHUB_USER = "dakeeper"
GITHUB_REPO = "smartboxx"
UPDATE_CHECK_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
# TESTTESTTEST

class ShowIP:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#1a1a2e")
        self.root.config(cursor="none")
        self.last_activity = datetime.datetime.now()
        self.idle_timeout = 180
        self.ss_active = False
        self.ss_top = None
        self.ss_label = None
        self.ss_after_id = None
        self.root.bind_all("<Button>", self._on_touch)

        self.header = tk.Frame(self.root, bg="#1a1a2e")
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.uptime_label = tk.Label(
            self.header,
            text="",
            font=("Helvetica", 9),
            fg="#888",
            bg="#1a1a2e",
        )
        self.uptime_label.pack(side=tk.LEFT, padx=3)
        self.countdown_label = tk.Label(
            self.header,
            text="",
            font=("Helvetica", 9),
            fg="#888",
            bg="#1a1a2e",
        )
        self.boot_label = tk.Label(
            self.header,
            text="",
            font=("Helvetica", 9),
            fg="#888",
            bg="#1a1a2e",
        )
        self.boot_label.pack(side=tk.LEFT, padx=3)
        self.srcn_label = tk.Label(
            self.header,
            text="",
            font=("Helvetica", 9),
            fg="#888",
            bg="#1a1a2e",
        )
        self.srcn_label.pack(side=tk.LEFT, padx=3)
        self.countdown_label.pack(side=tk.LEFT, expand=True)
        self.date_label = tk.Label(
            self.header,
            text="",
            font=("Helvetica", 9),
            fg="#888",
            bg="#1a1a2e",
        )
        self.date_label.pack(side=tk.RIGHT, padx=3)

        self.frame = tk.Frame(self.root, bg="#1a1a2e")
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.title = tk.Label(
            self.frame,
            text="SMARTBOXX V1.3",
            font=("Helvetica", 18, "bold"),
            fg="#00cc66",
            bg="#1a1a2e",
        )
        self.title.pack(pady=(15, 0))

        self.label = tk.Label(
            self.frame,
            text="Fetching IP...",
            font=("Helvetica", 14, "bold"),
            fg="white",
            bg="#1a1a2e",
        )
        self.label.pack(pady=(10, 0))

        self.sub = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 14),
            fg="white",
            bg="#1a1a2e",
        )
        self.sub.pack()

        self.cpu = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 14),
            fg="white",
            bg="#1a1a2e",
        )
        self.cpu.pack()

        self.disk = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 14),
            fg="white",
            bg="#1a1a2e",
        )
        self.disk.pack()

        self.ram = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 14),
            fg="white",
            bg="#1a1a2e",
        )
        self.ram.pack()

        self.mdb = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 14),
            fg="white",
            bg="#1a1a2e",
        )
        self.mdb.pack()

        self.smb = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 14),
            fg="white",
            bg="#1a1a2e",
        )
        self.smb.pack()

        self.btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.btn_frame.pack(pady=5)

        btn_style = {"font": ("Helvetica", 15, "bold"), "width": 10, "bd": 0}
        self.btn_row1 = tk.Frame(self.btn_frame, bg="#1a1a2e")
        self.btn_row1.pack()
        self.btn_row2 = tk.Frame(self.btn_frame, bg="#1a1a2e")
        self.btn_row2.pack(pady=5)

        tk.Button(
            self.btn_row1, text="CLOSE", command=self.show_exit_dialog,
            bg="#e94560", fg="white", **btn_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.btn_row1, text="REBOOT", command=self.reboot,
            bg="#0f3460", fg="white", **btn_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.btn_row1, text="SERV", command=self.show_services,
            bg="#16213e", fg="white", **btn_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.btn_row2, text="DB", command=self.show_credentials,
            bg="#16213e", fg="white", **btn_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.btn_row2, text="NET", command=self.show_network_settings,
            bg="#16213e", fg="white", **btn_style
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.btn_row2, text="SMB", command=self.show_smb_info,
            bg="#16213e", fg="white", **btn_style
        ).pack(side=tk.LEFT, padx=5)

        self.cred_frame = tk.Frame(self.root, bg="#1a1a2e")
        tk.Label(
            self.cred_frame, text="MariaDB Credentials",
            font=("Helvetica", 14, "bold"), fg="white", bg="#1a1a2e"
        ).pack(pady=10)
        tk.Label(
            self.cred_frame, text="User: admin",
            font=("Helvetica", 14), fg="#00cc66", bg="#1a1a2e"
        ).pack()
        tk.Label(
            self.cred_frame, text="Pass: admin",
            font=("Helvetica", 14), fg="#00cc66", bg="#1a1a2e"
        ).pack()
        tk.Label(
            self.cred_frame, text="",
            font=("Helvetica", 14), fg="white", bg="#1a1a2e"
        ).pack()
        tk.Label(
            self.cred_frame, text="phpMyAdmin:",
            font=("Helvetica", 14, "bold"), fg="white", bg="#1a1a2e"
        ).pack()
        self.cred_url = tk.Label(
            self.cred_frame, text="",
            font=("Helvetica", 14), fg="#e94560", bg="#1a1a2e"
        )
        self.cred_url.pack()
        tk.Button(
            self.cred_frame, text="Back", command=self.hide_credentials,
            bg="#0f3460", fg="white", font=("Helvetica", 15, "bold"), width=10, bd=0
        ).pack(pady=20)

        self.net_frame = tk.Frame(self.root, bg="#1a1a2e")
        tk.Label(
            self.net_frame, text="Network Settings",
            font=("Helvetica", 14, "bold"), fg="white", bg="#1a1a2e"
        ).pack(pady=10)
        self.net_info = tk.Label(
            self.net_frame, text="",
            font=("Helvetica", 12), fg="#888", bg="#1a1a2e"
        )
        self.net_info.pack()
        self.btn_dhcp = tk.Button(
            self.net_frame, text="DHCP", command=self.set_dhcp,
            font=("Helvetica", 15, "bold"), width=10, bd=0
        )
        self.btn_dhcp.pack(pady=5)
        self.btn_static = tk.Button(
            self.net_frame, text="Static IP", command=self.show_static_input,
            font=("Helvetica", 15, "bold"), width=10, bd=0
        )
        self.btn_static.pack(pady=5)
        tk.Button(
            self.net_frame, text="Back", command=self.hide_network_settings,
            bg="#0f3460", fg="white", font=("Helvetica", 15, "bold"), width=10, bd=0
        ).pack(pady=20)

        self.smb_frame = tk.Frame(self.root, bg="#1a1a2e")
        tk.Label(
            self.smb_frame, text="SMB (Samba) Freigabe",
            font=("Helvetica", 13, "bold"), fg="white", bg="#1a1a2e"
        ).pack(pady=4)
        tk.Label(
            self.smb_frame, text="Netzwerkzugriff:",
            font=("Helvetica", 12, "bold"), fg="#888", bg="#1a1a2e"
        ).pack()
        self.smb_path_label = tk.Label(
            self.smb_frame, text="",
            font=("Helvetica", 12), fg="#00cc66", bg="#1a1a2e"
        )
        self.smb_path_label.pack(pady=2)
        tk.Label(
            self.smb_frame, text="",
            font=("Helvetica", 8), fg="white", bg="#1a1a2e"
        ).pack()
        tk.Label(
            self.smb_frame, text="Lokaler Pfad:",
            font=("Helvetica", 12, "bold"), fg="#888", bg="#1a1a2e"
        ).pack()
        self.smb_local_label = tk.Label(
            self.smb_frame, text="",
            font=("Helvetica", 12), fg="#00cc66", bg="#1a1a2e"
        )
        self.smb_local_label.pack(pady=2)
        tk.Label(
            self.smb_frame, text="Konfiguration:",
            font=("Helvetica", 12, "bold"), fg="#888", bg="#1a1a2e"
        ).pack()
        tk.Label(
            self.smb_frame, text="/etc/samba/smb.conf",
            font=("Helvetica", 12), fg="#e94560", bg="#1a1a2e"
        ).pack(pady=2)
        tk.Label(
            self.smb_frame,
            text="Gästezugang (kein Passwort)",
            font=("Helvetica", 11), fg="#aaa", bg="#1a1a2e"
        ).pack(pady=4)
        tk.Button(
            self.smb_frame, text="Back", command=self.hide_smb_info,
            bg="#0f3460", fg="white", font=("Helvetica", 15, "bold"), width=10, bd=0
        ).pack(pady=8)

        self._flash_id = None
        self._refresh_count = 10
        self._tick_running = False
        self.boot_count = self.load_boot_count()
        self.refresh()
        self.tick()
        if self.boot_count > 0 and self.boot_count % 25 == 0:
            self.root.after(2000, self.show_boot_reminder)
        if not IS_MASTER:
            self.root.after(1000, self.check_update)
# Coded by Holger Palloks - Support @ holger.palloks@gut-gruppe.de

    def show_credentials(self):
        self.frame.pack_forget()
        self.btn_frame.pack_forget()
        self.cred_url.config(text=f"http://{self.get_local_ip()}/phpmyadmin")
        self.cred_frame.pack(expand=True)

    def hide_credentials(self):
        self.cred_frame.pack_forget()
        self.frame.pack(expand=True)
        self.btn_frame.pack(pady=5)

    def show_smb_info(self):
        self.frame.pack_forget()
        self.btn_frame.pack_forget()
        nb = self.get_samba_netbios_name()
        ip = self.get_local_ip()
        user = os.environ.get("USER", "")
        home = os.path.expanduser("~")
        self.smb_path_label.config(text=f"\\\\{nb}\\home\n({ip}\\home)")
        self.smb_local_label.config(text=f"{home}/SAMBA")
        self.smb_frame.pack(expand=True)

    def get_samba_netbios_name(self):
        try:
            with open("/etc/samba/smb.conf") as f:
                for line in f:
                    m = re.search(r"netbios name\s*=\s*(\S+)", line, re.I)
                    if m:
                        return m.group(1)
        except Exception:
            pass
        return socket.gethostname()

    def hide_smb_info(self):
        self.smb_frame.pack_forget()
        self.frame.pack(expand=True)
        self.btn_frame.pack(pady=5)

    def is_service_active(self, name):
        try:
            out = subprocess.check_output(
                ["systemctl", "is-active", name], timeout=5
            ).decode().strip()
            return out == "active"
        except Exception:
            return False

    def get_service_version(self, name):
        try:
            pkgs = {
                "mariadb": "mariadb-server",
                "apache2": "apache2",
                "vsftpd": "vsftpd",
                "ssh": "openssh-server",
                "smbd": "samba",
            }
            pkg = pkgs.get(name)
            if not pkg:
                return ""
            out = subprocess.check_output(
                ["dpkg-query", "-W", "-f=${Version}", pkg],
                timeout=3).decode().strip()
            if out:
                return out.split(":")[-1].split("-")[0].split("~")[0].split("+")[0]
        except Exception:
            pass
        return ""

    def get_os_version(self):
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=", 1)[1].strip().strip('"')
        except Exception:
            pass
        return ""

    def get_kernel(self):
        try:
            return subprocess.check_output(["uname", "-r"], timeout=3).decode().strip()
        except Exception:
            return ""

    def get_last_unattended_upgrade(self):
        try:
            log = "/var/log/unattended-upgrades/unattended-upgrades.log"
            with open(log) as f:
                for line in f:
                    pass
                last = line.split(",")[0].strip()
                return last
        except Exception:
            return "?"

    def toggle_service(self, action, svc_name):
        top = tk.Toplevel(self.root)
        top.attributes("-fullscreen", True)
        top.configure(bg="#1a1a2e")
        top.config(cursor="none")
        verb = {"start": "start", "stop": "stop", "restart": "restart"}.get(action, action)
        tk.Label(top, text=f"{verb.title()} {svc_name}?",
                 font=("Helvetica", 13, "bold"), fg="white",
                 bg="#1a1a2e").pack(pady=40)
        btn_frame = tk.Frame(top, bg="#1a1a2e")
        btn_frame.pack(pady=30)

        def confirm():
            top.destroy()
            try:
                subprocess.run(["sudo", "systemctl", action, svc_name],
                               timeout=10, check=True)
                self.show_info(f"{svc_name} {verb}ed")
            except Exception:
                self.show_info(f"Failed to {action} {svc_name}")

            self.svc_frame.pack_forget()
            self.show_services()

        tk.Button(btn_frame, text="Yes", command=confirm,
                  bg="#00cc66", fg="white",
                  font=("Helvetica", 14, "bold"), width=8, bd=0
                  ).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="No", command=top.destroy,
                  bg="#e94560", fg="white",
                  font=("Helvetica", 14, "bold"), width=8, bd=0
                  ).pack(side=tk.LEFT, padx=15)

    def show_info(self, msg):
        top = tk.Toplevel(self.root)
        top.attributes("-fullscreen", True)
        top.configure(bg="#1a1a2e")
        top.config(cursor="none")
        tk.Label(top, text=msg,
                 font=("Helvetica", 14, "bold"), fg="#00cc66",
                 bg="#1a1a2e").pack(pady=50)
        tk.Button(top, text="OK", command=top.destroy,
                  bg="#0f3460", fg="white",
                  font=("Helvetica", 14, "bold"), width=8, bd=0
                  ).pack(pady=30)

    def show_services(self):
        # Lernen wir müssen, loszulassen, was wir fürchten zu verlieren.
        self.frame.pack_forget()
        self.btn_frame.pack_forget()
        if hasattr(self, "svc_frame") and self.svc_frame:
            self.svc_frame.destroy()
        self.svc_frame = tk.Frame(self.root, bg="#1a1a2e")
        tk.Label(self.svc_frame, text="Services",
                 font=("Helvetica", 12, "bold"), fg="white",
                 bg="#1a1a2e").pack(pady=5)

        os_ver = self.get_os_version()
        kernel = self.get_kernel()
        tk.Label(self.svc_frame, text=os_ver,
                 font=("Helvetica", 9), fg="#888",
                 bg="#1a1a2e").pack()
        tk.Label(self.svc_frame, text=f"Kernel: {kernel}",
                 font=("Helvetica", 9), fg="#888",
                 bg="#1a1a2e").pack(pady=(0, 2))
        last_upgrade = self.get_last_unattended_upgrade()
        tk.Label(self.svc_frame, text=f"Letztes unattended-upgrade: {last_upgrade}",
                 font=("Helvetica", 9), fg="#888",
                 bg="#1a1a2e").pack(pady=(0, 5))

        services = [("MariaDB", "mariadb"),
                    ("Apache", "apache2"),
                    ("SSH", "ssh"),
                    ("Samba", "smbd"),
                    ("Falcon", "falcon-sensor")]
        for label, svc in services:
            row = tk.Frame(self.svc_frame, bg="#1a1a2e")
            row.pack(fill=tk.X, padx=5, pady=2)

            active = self.is_service_active(svc)
            ver = self.get_service_version(svc)
            status = "Running" if active else "Stopped"
            color = "#00cc66" if active else "#e94560"
            display = f"{label}: {status}"
            if ver:
                display += f" ({ver})"
            tk.Label(row, text=display,
                     font=("Helvetica", 10), fg=color,
                     bg="#1a1a2e").pack(side=tk.LEFT)

            if svc == "falcon-sensor":
                continue

            start_cmd = lambda s=svc: self.toggle_service("start", s)
            stop_cmd = lambda s=svc: self.toggle_service("stop", s)
            rest_cmd = lambda s=svc: self.toggle_service("restart", s)

            btn_s = {"font": ("Helvetica", 9, "bold"), "width": 5, "bd": 0,
                     "bg": "#0f3460", "fg": "white", "activebackground": "#16213e"}
            tk.Button(row, text="START", command=start_cmd, **btn_s
                      ).pack(side=tk.RIGHT, padx=1)
            tk.Button(row, text="STOP", command=stop_cmd, **btn_s
                      ).pack(side=tk.RIGHT, padx=1)
            tk.Button(row, text="REST", command=rest_cmd, **btn_s
                      ).pack(side=tk.RIGHT, padx=1)

        tk.Button(self.svc_frame, text="Back", command=self.hide_services,
                  bg="#0f3460", fg="white",
                  font=("Helvetica", 13, "bold"), width=8, bd=0
                  ).pack(pady=10)
        self.svc_frame.pack(expand=True)

    def hide_services(self):
        # Aus der Furcht entspringt der Zorn, aus dem Zorn die Gewalt und aus der Gewalt der Schmerz
        self.svc_frame.pack_forget()
        self.frame.pack(expand=True)
        self.btn_frame.pack(pady=5)

    def stop_flash(self):
        if self._flash_id:
            self.root.after_cancel(self._flash_id)
        self.smb_frame = tk.Frame(self.root, bg="#1a1a2e")
        tk.Label(
            self.smb_frame, text="SMB (Samba) Freigabe",
            font=("Helvetica", 14, "bold"), fg="white", bg="#1a1a2e"
        ).pack(pady=10)
        tk.Label(
            self.smb_frame, text="Netzwerkzugriff:",
            font=("Helvetica", 14, "bold"), fg="#888", bg="#1a1a2e"
        ).pack()
        self.smb_path_label = tk.Label(
            self.smb_frame, text="",
            font=("Helvetica", 14), fg="#00cc66", bg="#1a1a2e"
        )
        self.smb_path_label.pack(pady=5)
        tk.Label(
            self.smb_frame, text="",
            font=("Helvetica", 14), fg="white", bg="#1a1a2e"
        ).pack()
        tk.Label(
            self.smb_frame, text="Lokale Konfiguration:",
            font=("Helvetica", 14, "bold"), fg="#888", bg="#1a1a2e"
        ).pack()
        tk.Label(
            self.smb_frame, text="/etc/samba/smb.conf",
            font=("Helvetica", 14), fg="#e94560", bg="#1a1a2e"
        ).pack(pady=5)
        tk.Label(
            self.smb_frame,
            text="Benutzername: dakeeper (Pi4) / bonev (Pi5)\nPasswort: (keines - Gästezugang)",
            font=("Helvetica", 12), fg="#aaa", bg="#1a1a2e", justify=tk.CENTER,
        ).pack(pady=10)
        tk.Button(
            self.smb_frame, text="Back", command=self.hide_smb_info,
            bg="#0f3460", fg="white", font=("Helvetica", 15, "bold"), width=10, bd=0
        ).pack(pady=20)

        self._flash_id = None

    def flash_cpu(self):
        self.stop_flash()
        self._flash_on = False
        self._do_flash()

    def _do_flash(self):
        self._flash_on = not self._flash_on
        if self._flash_on:
            self.cpu.config(fg="#1a1a2e")
        else:
            self.cpu.config(fg="#e94560")
        self._flash_id = self.root.after(500, self._do_flash)

    def refresh(self):
        # Lernen wir müssen, loszulassen, was wir fürchten zu verlieren.
        threading.Thread(target=self.fetch_ip, daemon=True).start()
        self.root.after(10000, self.refresh)

    def tick(self):
        # Lernen wir müssen, loszulassen, was wir fürchten zu verlieren.
        threading.Thread(target=self._tick_loop, daemon=True).start()

    def _tick_loop(self):
# Coded by Holger Palloks - Support @ holger.palloks@gut-gruppe.de
        while True:
            try:
                uptime = self.get_uptime()
                bc = self.boot_count
                now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                rc = self._refresh_count
                self._refresh_count -= 1
                if self._refresh_count <= 0:
                    self._refresh_count = 10
                if not self.ss_active:
                    la = self.last_activity
                    elapsed = (datetime.datetime.now() - la).total_seconds()
                    if elapsed >= self.idle_timeout:
                        srcn = "SRCN:AKTIV"
                    else:
                        remain = int(self.idle_timeout - elapsed)
                        srcn = f"SRCN:{remain // 60:02d}:{remain % 60:02d}"
                else:
                    srcn = "SRCN:AKTIV"
                self.root.after(0, lambda: self._update_header(uptime, bc, now, rc, srcn))
            except Exception:
                pass
            if not self.ss_active:
                try:
                    la = self.last_activity
                    elapsed = (datetime.datetime.now() - la).total_seconds()
                    if elapsed >= self.idle_timeout:
                        self.root.after(0, self.start_screensaver)
                except Exception:
                    pass
            import time
            time.sleep(1)

    def _update_header(self, uptime, boot_count, date_str, refresh_count, srcn):
        try:
            self.uptime_label.config(text=f"Uptime: {uptime}")
            self.boot_label.config(text=f"Boots: {boot_count}")
            self.date_label.config(text=date_str)
            self.countdown_label.config(text=f"Refresh: {refresh_count}s")
            self.srcn_label.config(text=srcn)
        except Exception:
            pass

    def _on_touch(self, event=None):
        # Tue es, oder tue es nicht. Es gibt kein Versuchen.
        self.last_activity = datetime.datetime.now()
        if self.ss_active:
            self.stop_screensaver()

    def show_exit_dialog(self):
        # Tue es, oder tue es nicht. Es gibt kein Versuchen.
        top = tk.Toplevel(self.root, bg="#1a1a2e")
        top.attributes("-fullscreen", True)
        top.attributes("-topmost", True)
        tk.Label(
            top,
            text="Programm beenden?",
            font=("Helvetica", 18, "bold"),
            fg="white", bg="#1a1a2e",
        ).pack(expand=True)
        btn_frame = tk.Frame(top, bg="#1a1a2e")
        btn_frame.pack(pady=30)
        tk.Button(
            btn_frame, text="SHUTDOWN",
            command=lambda: self._do_exit_shutdown(top),
            bg="#e94560", fg="white",
            font=("Helvetica", 15, "bold"), width=10, bd=0
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            btn_frame, text="CLOSE",
            command=lambda: self._do_exit_close(top),
            bg="#0f3460", fg="white",
            font=("Helvetica", 15, "bold"), width=10, bd=0
        ).pack(side=tk.LEFT, padx=10)

    def _do_exit_shutdown(self, top):
        # Tue es, oder tue es nicht. Es gibt kein Versuchen.
        top.destroy()
        subprocess.run(["sudo", "shutdown", "-h", "now"], check=False)
        self.root.destroy()

    def _do_exit_close(self, top):
        top.destroy()
        self.root.destroy()

    def start_screensaver(self):
        if self.ss_active:
            return
        self.ss_active = True
        self.ss_top = tk.Toplevel(self.root)
        self.ss_top.attributes("-fullscreen", True)
        self.ss_top.attributes("-topmost", True)
        self.ss_top.configure(bg="black")
        self.ss_top.config(cursor="none")
        self.ss_top.bind("<Button>", lambda e: self.stop_screensaver())
        self.ss_brand = tk.Label(
            self.ss_top, text="",
            font=("Helvetica", 40, "bold"),
            fg="#00cc66", bg="black",
        )
        self.ss_brand.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.ss_info = tk.Label(
            self.ss_top, text="",
            font=("Helvetica", 28, "bold"),
            fg="#00cc66", bg="black",
        )
        self.ss_info.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.ss_phase = 0
        self.ss_timer = 0
        self._ss_tick()

    def stop_screensaver(self):
        if self.ss_after_id:
            self.root.after_cancel(self.ss_after_id)
            self.ss_after_id = None
        self.ss_active = False
        self.last_activity = datetime.datetime.now()
        if self.ss_top:
            self.ss_top.destroy()
            self.ss_top = None
            self.ss_brand = None
            self.ss_info = None

    def _ss_tick(self):
        if not self.ss_active:
            return
        try:
            if self.ss_phase == 0:
                now = datetime.datetime.now().strftime("%d.%m.%Y  %H:%M")
                self.ss_brand.config(text="SMARTBOXX")
                self.ss_info.config(text=now)
                self.ss_timer += 1
                if self.ss_timer >= 15:
                    self.ss_phase = 1
                    self.ss_timer = 0
                    self.ss_brand.config(text="")
                    self.ss_info.config(text="")
            elif self.ss_phase == 1:
                self.ss_timer += 1
                if self.ss_timer >= 15:
                    self.ss_phase = 2
                    self.ss_timer = 0
                    try:
                        with open("/proc/uptime") as f:
                            s = float(f.read().split()[0])
                        h = int(s // 3600)
                        m = int((s % 3600) // 60)
                        u = f"{h:02d}:{m:02d}"
                    except Exception:
                        u = ""
                    self.ss_brand.config(text="SMARTBOXX")
                    self.ss_info.config(text=f"System uptime {u}")
            elif self.ss_phase == 2:
                self.ss_timer += 1
                if self.ss_timer >= 15:
                    self.ss_phase = 3
                    self.ss_timer = 0
                    self.ss_brand.config(text="")
                    self.ss_info.config(text="")
            elif self.ss_phase == 3:
                self.ss_timer += 1
                if self.ss_timer >= 15:
                    self.ss_phase = 4
                    self.ss_timer = 0
                    t = self.get_cpu_temp()
                    self.ss_brand.config(text="SMARTBOXX")
                    self.ss_info.config(text=f"CPU Temp {t}")
            elif self.ss_phase == 4:
                self.ss_timer += 1
                if self.ss_timer >= 15:
                    self.ss_phase = 5
                    self.ss_timer = 0
                    self.ss_brand.config(text="")
                    self.ss_info.config(text="")
            elif self.ss_phase == 5:
                self.ss_timer += 1
                if self.ss_timer >= 15:
                    self.ss_phase = 0
                    self.ss_timer = 0
        except Exception:
            pass
        self.ss_after_id = self.root.after(1000, self._ss_tick)

    def fetch_ip(self):
        # Aus der Furcht entspringt der Zorn, aus dem Zorn die Gewalt und aus der Gewalt der Schmerz
        try:
            ip = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
        except Exception:
            ip = "No connection"
        local = self.get_local_ip()
        cpu_temp = self.get_cpu_temp()
        disk_free = self.get_free_disk()
        ram_info = self.get_ram_usage()
        mdb_status = self.get_mariadb_status()
        mdb_size = self.get_mariadb_size() if mdb_status else ""
        self.root.after(0, lambda: self.label.config(text=f"Ext-IP: {ip}"))
        self.root.after(0, lambda: self.sub.config(text=f"Loc-IP: {local}"))
        if cpu_temp != "N/A":
            temp_val = float(cpu_temp.replace("°C", ""))
            if temp_val >= 80:
                color, text, font, flashing = "#e94560", f"CPU-Temp: {cpu_temp}!!!", ("Helvetica", 14, "bold"), True
            elif temp_val > 70:
                color, text, font, flashing = "#e94560", f"CPU-Temp: {cpu_temp}!", ("Helvetica", 14, "bold"), False
            elif temp_val > 63:
                color, text, font, flashing = "#e94560", f"CPU-Temp: {cpu_temp}", ("Helvetica", 14), False
            elif temp_val >= 55:
                color, text, font, flashing = "#ffcc00", f"CPU-Temp: {cpu_temp}", ("Helvetica", 14), False
            else:
                color, text, font, flashing = "#00cc66", f"CPU-Temp: {cpu_temp}", ("Helvetica", 14), False
        else:
            color, text, font, flashing = "white", f"CPU-Temp: {cpu_temp}", ("Helvetica", 14), False
        self.root.after(0, lambda: self.cpu.config(text=text, fg=color, font=font))
        self.root.after(0, lambda: self.disk.config(text=f"SD-Free: {disk_free}"))
        self.root.after(0, lambda: self.ram.config(text=f"RAM: {ram_info}"))
        if flashing:
            self.root.after(0, self.flash_cpu)
        elif self._flash_id:
            self.root.after(0, self.stop_flash)

        if mdb_status:
            mdb_text, mdb_color, mdb_font = f"MariaDB: Running ({mdb_size})", "#00cc66", ("Helvetica", 14)
        else:
            mdb_text, mdb_color, mdb_font = "MariaDB: Not Running", "#e94560", ("Helvetica", 14, "bold")
        self.root.after(0, lambda: self.mdb.config(text=mdb_text, fg=mdb_color, font=mdb_font))

        smb_status = self.get_smb_status()
        if smb_status:
            smb_text, smb_color, smb_font = "Samba: Running", "#00cc66", ("Helvetica", 14)
        else:
            smb_text, smb_color, smb_font = "Samba: Not Running", "#e94560", ("Helvetica", 14, "bold")
        self.root.after(0, lambda: self.smb.config(text=smb_text, fg=smb_color, font=smb_font))

    def get_uptime(self):
        try:
            with open("/proc/uptime") as f:
                seconds = float(f.read().split()[0])
            days, rem = divmod(seconds, 86400)
            hours, rem = divmod(rem, 3600)
            minutes = rem // 60
            parts = []
            if days > 0:
                parts.append(f"{int(days)}d")
            parts.append(f"{int(hours)}h")
            parts.append(f"{int(minutes)}m")
            return " ".join(parts)
        except Exception:
            return ""

    def load_boot_count(self):
        path = os.path.expanduser("~/.boot_count")
        try:
            with open(path) as f:
                val = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            val = 0
        val += 1
        try:
            with open(path, "w") as f:
                f.write(str(val))
        except Exception:
            pass
        return val

    def show_boot_reminder(self):
        # Aus der Furcht entspringt der Zorn, aus dem Zorn die Gewalt und aus der Gewalt der Schmerz
        top = tk.Toplevel(self.root, bg="#e94560")
        top.attributes("-fullscreen", True)
        top.attributes("-topmost", True)
        tk.Label(
            top,
            text=f"{self.boot_count} Boots done.\nBitte SD-Card backup machen!",
            font=("Helvetica", 18, "bold"),
            fg="white", bg="#e94560", justify=tk.CENTER,
        ).pack(expand=True)
        tk.Button(
            top, text="OK", command=top.destroy,
            bg="#0f3460", fg="white", font=("Helvetica", 15, "bold"), width=10, bd=0
        ).pack(pady=30)

    def get_gateway(self):
        try:
            out = subprocess.check_output(
                ["nmcli", "-t", "-f", "ipv4.gateway", "con", "show", "netplan-eth0"],
                timeout=5).decode().strip()
            if ":" in out:
                return out.split(":")[-1]
        except Exception:
            pass
        return ""

    def get_dns(self):
        try:
            out = subprocess.check_output(
                ["nmcli", "-t", "-f", "ipv4.dns", "con", "show", "netplan-eth0"],
                timeout=5).decode().strip()
            if ":" in out:
                dns = out.split(":", 1)[-1].strip()
                return dns
        except Exception:
            pass
        return ""

    def get_local_ip(self):
        # Aus der Furcht entspringt der Zorn, aus dem Zorn die Gewalt und aus der Gewalt der Schmerz
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "unknown"

    def get_cpu_temp(self):
        zones = ["/sys/class/thermal/thermal_zone0/temp",
                   "/sys/class/thermal/thermal_zone1/temp"]
        for path in zones:
            if os.path.isfile(path):
                try:
                    raw = open(path).read().strip()
                    temp = round(int(raw) / 1000, 1)
                    return f"{temp}°C"
                except Exception:
                    pass
        try:
            out = subprocess.check_output(["sensors", "-u"], timeout=3).decode()
            for line in out.splitlines():
                if "temp1_input" in line:
                    temp = float(line.split()[-1])
                    return f"{temp:.1f}°C"
        except Exception:
            pass
        return "N/A"

    def get_free_disk(self):
        try:
            usage = shutil.disk_usage("/")
            free_gb = usage.free / (1024 ** 3)
            return f"{free_gb:.1f} GB"
        except Exception:
            return "N/A"

    def get_ram_usage(self):
        try:
            with open("/proc/meminfo") as f:
                mem = f.read()
            total = int([l for l in mem.splitlines() if "MemTotal" in l][0].split()[1])
            avail = int([l for l in mem.splitlines() if "MemAvailable" in l][0].split()[1])
            used = total - avail
            return f"{used / 1024 ** 2:.2f} GB of {total / 1024 ** 2:.1f} GB used"
        except Exception:
            return "N/A"

    def get_mariadb_status(self):
        try:
            out = subprocess.check_output(
                ["systemctl", "is-active", "mariadb"], timeout=5
            ).decode().strip()
            return out == "active"
        except Exception:
            return False

    def get_mariadb_size(self):
        try:
            out = subprocess.check_output(
                ["mysql", "-u", "root", "-proot",
                 "-e", "SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) FROM information_schema.tables"],
                timeout=5
            ).decode().strip()
            size = out.splitlines()[-1].strip()
            return f"{size} MB"
        except Exception:
            return "? MB"

    def get_smb_status(self):
        try:
            out = subprocess.check_output(
                ["systemctl", "is-active", "smbd"], timeout=5
            ).decode().strip()
            return out == "active"
        except Exception:
            return False

    def show_network_settings(self):
        self.frame.pack_forget()
        self.btn_frame.pack_forget()
        method, ip = self.get_network_method()
        local = self.get_local_ip()
        self.net_info.config(text=f"Current: {method} - IP: {local}")
        dhcp_bg = "#00cc66" if method == "DHCP" else "#0f3460"
        static_bg = "#00cc66" if method == "Static" else "#0f3460"
        self.btn_dhcp.config(bg=dhcp_bg)
        self.btn_static.config(bg=static_bg)
        self.net_frame.pack(expand=True)

    def hide_network_settings(self):
        self.net_frame.pack_forget()
        self.frame.pack(expand=True)
        self.btn_frame.pack(pady=5)

    def get_network_method(self):
        try:
            out = subprocess.check_output(
                ["nmcli", "-t", "-f", "ipv4.method,ipv4.addresses",
                 "con", "show", "netplan-eth0"], timeout=5
            ).decode().strip()
            method = "DHCP" if "auto" in out else "Static"
            addr = ""
            for line in out.splitlines():
                if "ipv4.addresses" in line:
                    addr = line.split(":", 1)[-1].strip()
            return method, addr
        except Exception:
            return "Unknown", ""

    def set_dhcp(self):
        top = tk.Toplevel(self.root)
        top.attributes("-fullscreen", True)
        top.configure(bg="#1a1a2e")
        top.config(cursor="none")
        tk.Label(top, text="Switch to DHCP?",
                 font=("Helvetica", 14, "bold"), fg="white",
                 bg="#1a1a2e").pack(pady=40)
        tk.Label(top, text="All static settings will be lost.",
                 font=("Helvetica", 11), fg="#e94560",
                 bg="#1a1a2e").pack(pady=10)

        btn_frame = tk.Frame(top, bg="#1a1a2e")
        btn_frame.pack(pady=30)

        def do_dhcp():
            top.destroy()
            try:
                subprocess.run(["nmcli", "con", "mod", "netplan-eth0",
                               "ipv4.method", "auto",
                               "ipv4.addresses", "",
                               "ipv4.gateway", "",
                               "ipv4.dns", ""], timeout=10)
                subprocess.run(["nmcli", "con", "down", "netplan-eth0"], timeout=10)
                subprocess.run(["nmcli", "con", "up", "netplan-eth0"], timeout=10)
            except Exception:
                pass
            self.hide_network_settings()

        tk.Button(btn_frame, text="Yes", command=do_dhcp,
                  bg="#00cc66", fg="white",
                  font=("Helvetica", 14, "bold"), width=8, bd=0
                  ).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="Cancel", command=lambda: (top.destroy(), self.hide_network_settings()),
                  bg="#e94560", fg="white",
                  font=("Helvetica", 14, "bold"), width=8, bd=0
                  ).pack(side=tk.LEFT, padx=15)

    def show_static_input(self):
        top = tk.Toplevel(self.root)
        top.attributes("-fullscreen", True)
        top.configure(bg="#1a1a2e")
        top.config(cursor="none")
        top.protocol("WM_DELETE_WINDOW", top.destroy)

        main = tk.Frame(top, bg="#1a1a2e")
        main.pack(expand=True, fill=tk.BOTH)

        tk.Label(main, text="Static IP Configuration",
                 font=("Helvetica", 10, "bold"), fg="white",
                 bg="#1a1a2e").pack(pady=2)

        cur_ip = self.get_local_ip()
        if cur_ip == "unknown":
            cur_ip = "---"
        cur_gw = self.get_gateway() or "---"
        cur_dns = self.get_dns() or "---"
        fields = [("IP (z.B. 192.168.0.100/24)", cur_ip),
                  ("Gateway", cur_gw),
                  ("DNS", cur_dns)]
        entries = []
        for label, default in fields:
            tk.Label(main, text=label, font=("Helvetica", 9),
                     fg="#888", bg="#1a1a2e").pack()
            e = tk.Entry(main, font=("Helvetica", 9), width=20,
                         bg="#16213e", fg="#888", insertbackground="white")
            e.insert(0, default)
            e.bind("<FocusIn>", lambda ev, ent=e: (ent.delete(0, tk.END), ent.config(fg="white")) if ent.cget("fg") == "#888" else None)
            e.pack(fill=tk.X, padx=10)
            entries.append(e)

        btn_frame = tk.Frame(main, bg="#1a1a2e")
        btn_frame.pack(pady=2)

        def save():
            ip_addr = entries[0].get().strip()
            gateway = entries[1].get().strip()
            dns = entries[2].get().strip()
            top.destroy()
            self.save_static(ip_addr, gateway, dns)

        tk.Button(btn_frame, text="Save", command=save,
                  bg="#00cc66", fg="white",
                  font=("Helvetica", 11, "bold"), width=7, bd=0
                  ).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=top.destroy,
                  bg="#e94560", fg="white",
                  font=("Helvetica", 11, "bold"), width=7, bd=0
                  ).pack(side=tk.LEFT, padx=5)

        self._build_keyboard(main, entries)

    def save_static(self, ip_addr, gateway, dns):
        old_ip = self.get_local_ip()
        try:
            subprocess.run(["nmcli", "con", "mod", "netplan-eth0",
                           "ipv4.method", "manual",
                           "ipv4.addresses", ip_addr,
                           "ipv4.gateway", gateway,
                           "ipv4.dns", dns], timeout=10)
            subprocess.run(["nmcli", "con", "down", "netplan-eth0"], timeout=10)
            subprocess.run(["nmcli", "con", "up", "netplan-eth0"], timeout=10)
            new_ip = self.get_local_ip()
            if new_ip != old_ip and new_ip != "unknown":
                self.confirm_reboot()
        except Exception:
            pass
        self.hide_network_settings()

    def _build_keyboard(self, parent, entries):
        kb = tk.Frame(parent, bg="#1a1a2e")
        kb.pack(fill=tk.X, side=tk.BOTTOM, padx=2)

        keys = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            [".", "0", "/"],
            ["<-", "CLEAR"],
            ["IP", "GW", "DNS"],
        ]

        current = [0]
        for i, e in enumerate(entries):
            e.bind("<FocusIn>", lambda ev, idx=i: current.__setitem__(0, idx), "+")

        def insert(ch):
            try:
                entries[current[0]].insert(tk.INSERT, ch)
            except Exception:
                pass

        def backspace():
            try:
                e = entries[current[0]]
                idx = e.index(tk.INSERT)
                if idx > 0:
                    e.delete(idx - 1, idx)
            except Exception:
                pass

        def clear():
            try:
                entries[current[0]].delete(0, tk.END)
            except Exception:
                pass

        def set_focus(i):
            current[0] = i
            entries[i].focus_set()

        for row in keys:
            rframe = tk.Frame(kb, bg="#1a1a2e")
            rframe.pack(fill=tk.X)
            for k in row:
                if k == "<-":
                    cmd, bg = backspace, "#0f3460"
                elif k == "CLEAR":
                    cmd, bg = clear, "#e94560"
                elif k in ("IP", "GW", "DNS"):
                    cmd, bg = lambda i=keys[-1].index(k): set_focus(i), "#533483"
                else:
                    cmd, bg = lambda ch=k: insert(ch), "#16213e"
                tk.Button(rframe, text=k, command=cmd,
                          font=("Helvetica", 9, "bold"),
                          bd=0, bg=bg, fg="white",
                          activebackground="#0f3460"
                          ).pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=2, padx=1, pady=1)

    def confirm_reboot(self):
        top = tk.Toplevel(self.root)
        top.attributes("-fullscreen", True)
        top.configure(bg="#1a1a2e")
        top.config(cursor="none")
        tk.Label(top, text="IP address changed!",
                 font=("Helvetica", 16, "bold"), fg="white",
                 bg="#1a1a2e").pack(pady=30)
        tk.Label(top, text="Reboot now?",
                 font=("Helvetica", 14), fg="white",
                 bg="#1a1a2e").pack(pady=10)

        btn_frame = tk.Frame(top, bg="#1a1a2e")
        btn_frame.pack(pady=20)

        def do_reboot():
            top.destroy()
            self.root.destroy()
            subprocess.run(["sudo", "reboot"], check=False)

        def discard():
            top.destroy()
            try:
                subprocess.run(["nmcli", "con", "mod", "netplan-eth0",
                               "ipv4.method", "auto",
                               "ipv4.addresses", "",
                               "ipv4.gateway", "",
                               "ipv4.dns", ""], timeout=10)
                subprocess.run(["nmcli", "con", "down", "netplan-eth0"], timeout=10)
                subprocess.run(["nmcli", "con", "up", "netplan-eth0"], timeout=10)
            except Exception:
                pass
            self.hide_network_settings()

        tk.Button(btn_frame, text="Yes", command=do_reboot,
                  bg="#e94560", fg="white",
                  font=("Helvetica", 15, "bold"), width=10, bd=0
                  ).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="No", command=discard,
                  bg="#0f3460", fg="white",
                  font=("Helvetica", 15, "bold"), width=10, bd=0
                  ).pack(side=tk.LEFT, padx=10)

    def check_update(self):
        if IS_MASTER:
            return
        try:
            req = urllib.request.Request(UPDATE_CHECK_URL, headers={"User-Agent": "SMARTBOXX"})
            resp = urllib.request.urlopen(req, timeout=10)
            import json
            data = json.loads(resp.read())
            latest = data["tag_name"].lstrip("v")
            if latest > LOCAL_VER:
                self.show_update_dialog(latest, data["zipball_url"])
        except:
            pass
        self.root.after(432000000, self.check_update)

    def show_update_dialog(self, version, url):
        top = tk.Toplevel(self.root, bg="#e94560")
        top.attributes("-fullscreen", True)
        top.attributes("-topmost", True)
        tk.Label(
            top,
            text=f"Update v{version} verfügbar!",
            font=("Helvetica", 20, "bold"),
            fg="white", bg="#e94560",
        ).pack(expand=True)
        tk.Label(
            top,
            text="Jetzt herunterladen und installieren?",
            font=("Helvetica", 14),
            fg="white", bg="#e94560",
        ).pack()
        btn_frame = tk.Frame(top, bg="#e94560")
        btn_frame.pack(pady=30)
        tk.Button(
            btn_frame, text="UPDATE",
            command=lambda: self.do_update(top, version, url),
            bg="#00cc66", fg="white",
            font=("Helvetica", 18, "bold"), width=10, bd=0
        ).pack(side=tk.LEFT, padx=15)
        tk.Button(
            btn_frame, text="NEIN",
            command=top.destroy,
            bg="#0f3460", fg="white",
            font=("Helvetica", 18, "bold"), width=10, bd=0
        ).pack(side=tk.LEFT, padx=15)

    def do_update(self, top, version, url):
        top.destroy()
        dlg = tk.Toplevel(self.root, bg="#1a1a2e")
        dlg.attributes("-fullscreen", True)
        dlg.attributes("-topmost", True)
        tk.Label(
            dlg,
            text=f"Downloade v{version}...",
            font=("Helvetica", 18, "bold"),
            fg="#ffc107", bg="#1a1a2e",
        ).pack(expand=True)
        dlg.update()
        import zipfile, io, tempfile, glob
        tmp = None
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SMARTBOXX"})
            resp = urllib.request.urlopen(req, timeout=60)
            z = zipfile.ZipFile(io.BytesIO(resp.read()))
            tmp = tempfile.mkdtemp()
            z.extractall(tmp)
            extracted = glob.glob(os.path.join(tmp, "*/smartboxx.py"))
            extracted_sql = glob.glob(os.path.join(tmp, "*/sql-import"))
            if extracted:
                shutil.copy2(extracted[0], os.path.expanduser("~/.local/bin/smartboxx.py"))
                os.chmod(os.path.expanduser("~/.local/bin/smartboxx.py"), 0o755)
            if extracted_sql:
                shutil.copy2(extracted_sql[0], os.path.expanduser("~/SMARTBOXX-TOOLS/sql-import"))
                os.chmod(os.path.expanduser("~/SMARTBOXX-TOOLS/sql-import"), 0o755)
            if extracted:
                tk.Label(
                    dlg, text="Neustart...",
                    font=("Helvetica", 18, "bold"),
                    fg="#00cc66", bg="#1a1a2e",
                ).pack(expand=True)
                dlg.update()
                self.root.after(2000, lambda: subprocess.run(["sudo", "reboot"], check=False))
            else:
                tk.Label(
                    dlg, text="Fehler: Datei nicht gefunden",
                    font=("Helvetica", 18, "bold"),
                    fg="#e94560", bg="#1a1a2e",
                ).pack(expand=True)
        except:
            tk.Label(
                dlg, text="Fehler beim Download",
                font=("Helvetica", 18, "bold"),
                fg="#e94560", bg="#1a1a2e",
            ).pack(expand=True)
        finally:
            if tmp:
                shutil.rmtree(tmp, ignore_errors=True)

    def reboot(self):
        # Lernen wir müssen, loszulassen, was wir fürchten zu verlieren.
        self.root.destroy()
        subprocess.run(["sudo", "reboot"], check=False)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ShowIP().run()

# Coded by Holger Palloks - Support @ holger.palloks@gut-gruppe.de
# SHA256: 53a40e9f004a2d12e66b96585330db1d003e28940bea5797b079386a8907842d
