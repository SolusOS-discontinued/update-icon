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

from gi.repository import Gtk
import gettext

gettext.install("update-icon", "/usr/share/locale")


class UpdateIcon:

    def __init__(self):
        # in future we must support appindicators so that we're not X dependent
        self.icon = Gtk.StatusIcon()
        self.icon.set_from_icon_name("system-software-install")
        self.icon.set_title(_("Software Update"))
        self.icon.connect("popup-menu", self.popup)

        # our menu
        self.menu = Gtk.Menu()
        quit = Gtk.MenuItem(_("Quit"))
        quit.connect("activate", Gtk.main_quit)
        self.menu.append(quit)

        self.menu.show_all()

    def popup(self, source, button, time):
        self.menu.popup(None, None, Gtk.StatusIcon.position_menu, self.icon, button, time)
        

if __name__ == "__main__":
    icon = UpdateIcon()
    Gtk.main()


