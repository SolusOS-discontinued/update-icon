#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  update-icon.py - Simple update notification system
#  
#  Copyright 2013 Ikey Doherty <ikey@solusos.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import gi.repository

from gi.repository import Gtk, GObject, Notify
from gi.repository import PackageKitGlib as PackageKit
import gettext
import os

gettext.install("update-icon", "/usr/share/locale")


class UpdateIcon:

    def __init__(self):
        # in future we must support appindicators so that we're not X dependent
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_icon_name("system-software-install")
        self.icon.set_title(_("Software Update"))
        self.icon.connect("popup-menu", self.popup)
        self.icon.connect("activate", self.open_client)
        
        # our menu
        self.menu = Gtk.Menu()
        reload = Gtk.MenuItem(_("Reload"))
        reload.connect("activate", self.refresh)
        self.menu.append(reload)
        
        quit = Gtk.MenuItem(_("Quit"))
        quit.connect("activate", Gtk.main_quit)
        self.menu.append(quit)

        self.menu.show_all()

        # We'll reload our icon every 60 seconds
        GObject.timeout_add (60 * 1000, self.refresh)

        self.reported = False


        try:
            Notify.init('update-icon')
        except:
            # Should probably log this
            print "Notification daemon could not be reached"
            
        self.client = PackageKit.Client()
        self.refresh()

    def popup(self, source, button, time):
        self.menu.popup(None, None, Gtk.StatusIcon.position_menu, self.icon, button, time)

    def open_client(self, widg, user=None):
        self.icon.set_visible(False)
        GObject.idle_add(self._open_client)

    def _open_client(self):
        os.system("gpk-update-viewer")
        # Essentially blocked until we return from the process
        self._reload()
        
    def refresh(self, wid=None):
        ''' Refresh possible updates '''
        GObject.idle_add(self._reload)

        return True

    def _reload(self):
        result = self.client.get_updates(PackageKit.FilterEnum.NONE, None, self.progress, None)
        security = 0
        packages = result.get_package_array()
        updates = len(packages)
        for package in packages:
            name = package.get_name()
            print name
            version = package.get_version()
            if package.get_info() == PackageKit.InfoEnum.SECURITY:
                security += 1
        if security >= 1:
            self.icon.set_from_icon_name("software-update-urgent")
            self.icon.set_visible(True)

            # Show notification
            update_str = _("There is a new security update") if security == 1 else \
                         _("There are %d security updates available") % security
            self.icon.set_tooltip_text(update_str)
            if not self.reported:
                notif = Notify.Notification.new(_('Security update'), update_str, 'software-update-urgent')
                notif.show()
                self.reported = True
        else:
            if updates >= 1:
                self.icon.set_from_icon_name("software-update-available")
                self.icon.set_visible(True)

                # Show notification
                update_str = _("There is a new software update") if updates == 1 else \
                             _("There are %d software updates available") % updates
                self.icon.set_tooltip_text(update_str)
                if not self.reported:
                    notif = Notify.Notification.new(_('Software update'), update_str, 'software-update-available')
                    notif.show()
                    self.reported = True
            
            else:
                self.icon.set_tooltip_text(_("All software is up to date"))
                self.icon.set_visible(False)
                # Hide
                self.icon.hide()   

    def progress(self, progress, type, user_data=None):
        pass
        
if __name__ == "__main__":
    icon = UpdateIcon()
    Gtk.main()
