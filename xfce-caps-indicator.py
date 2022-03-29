#!/usr/bin/env python3

import gi
import re
import os
import sys
import base64
import subprocess
from threading import Thread

gi.require_version("Gio", "2.0")
gi.require_version("AyatanaAppIndicator3", "0.1")

from gi.repository import Gio, AyatanaAppIndicator3 as AppIndicator3, Gtk
from pynput.keyboard import Key, KeyCode, Listener


BASE_DIR = os.path.dirname(__file__)
APPINDICATOR_ID = "xfce-caps-indicator"
# Icon encoded in Base64
ICON_BASDEC = b"""
AAABAAEAICACAAEAAQAwAQAAFgAAACgAAAAgAAAAQAAAAAEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD
///8AAAAAAP///////////////////////AAA//wAAP/8AAD//AAA//////////8Pw+APD8PgDw+D4A8Hh+
APgAfgD4AH4A+AD+APww/gD8IMAADAHAAA4B4AAeA/AAPwP4AH8D/AD/B/4B/4f/A////4f////P///////
//////////////////////////////////////8AAD//AAA//wAAP/8AAD//////////w/D4A8Pw+APD4Pg
DweH4A+AB+APgAfgD4AP4A/DD+APwgwAAMAcAADgHgAB4D8AA/A/gAfwP8AP8H/gH/h/8D////h////8///
///////////////////8=
"""

class ApplicationInterface:
    def show_about_application_window(self, event):

        win = Gtk.Window(title="About", default_height=130, default_width=400)
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        hbox.set_homogeneous(False)

        name_label = Gtk.Label()
        name_label.set_markup("<big>{}</big>".format(APPINDICATOR_ID))
        name_label.set_justify(Gtk.Justification.CENTER)

        version_label = Gtk.Label()
        version_label.set_text("ver. 0.1")
        version_label.set_justify(Gtk.Justification.CENTER)

        desc_label = Gtk.Label()
        desc_label.set_text(
            "A simple Python plugin for XFCE,\n"
            "wich indicate the current state of CapsLock key."
        )
        desc_label.set_justify(Gtk.Justification.CENTER)

        footer_label = Gtk.Label()
        footer_label.set_markup(
            'Project site:\n<a href="https://github.com/mrachuta">' "http://github.com/mrachuta</a>"
        )
        footer_label.set_justify(Gtk.Justification.CENTER)

        hbox.pack_start(name_label, True, True, 0)
        hbox.pack_start(version_label, True, True, 0)
        hbox.pack_start(desc_label, True, True, 0)
        hbox.pack_start(footer_label, True, True, 0)

        win.add(hbox)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()

    def generate_menu(self):

        menu = Gtk.Menu()
        about_app = Gtk.MenuItem(label="About")
        exit_app = Gtk.MenuItem(label="Exit")

        about_app.connect("activate", self.show_about_application_window)
        exit_app.connect("activate", sys.exit)

        menu.append(about_app)
        menu.append(exit_app)
        menu.show_all()

        return menu

    def show_tray_icon(self):

        icon_path = os.path.join(BASE_DIR, "app-icon.ico")

        if not os.path.isfile(icon_path):
            with open(icon_path, "wb") as f:
                f.write(base64.decodebytes(ICON_BASDEC))

        indicator = AppIndicator3.Indicator.new(
            APPINDICATOR_ID,
            os.path.abspath(icon_path),
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES,
        )
        indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.generate_menu())
        Gtk.main()


class NotificationPopup:
    def __init__(self):

        self.notification_app = Gio.Application.new(
            "xfce.caps.indicator", Gio.ApplicationFlags.FLAGS_NONE
        )
        self.notification_app.register()

        self.notification = Gio.Notification.new("{}".format(APPINDICATOR_ID))

        self.notification_icon = Gio.ThemedIcon.new("input-keyboard")
        self.notification.set_icon(self.notification_icon)

    def show_popup(self, capsl_state):
        # If capslock was turned on, after click turn it off
        # and display message about current status
        if capsl_state:
            popup_message = "CapsLock ON"
        else:
            popup_message = "CapsLock OFF"

        self.notification.set_body(popup_message)
        self.notification_app.send_notification(None, self.notification)


class CapsLockListener:
    def __init__(self):

        xset_output = subprocess.check_output("xset q | grep LED", shell=True)
        re_text = xset_output.decode("UTF-8")
        regex = r"mask:\s*(\d+)"
        matches = re.search(regex, re_text, re.MULTILINE)

        if matches.group(1) == "00000001":
            self.key_status = True
        else:
            self.key_status = False

        self.new_notification = NotificationPopup()

    def on_press(self, key):

        if key == Key.caps_lock:

            if self.key_status:
                self.key_status = False
                self.new_notification.show_popup(False)
            else:
                self.key_status = True
                self.new_notification.show_popup(True)
                

    def run_listener(self):

        with Listener(on_press=self.on_press) as listener:
            listener.join()


if __name__ == "__main__":

    app_interface = ApplicationInterface()

    Thread(target=app_interface.show_tray_icon, daemon=True).start()

    capsl_listener = CapsLockListener()
    capsl_listener.run_listener()
