Simple update icon
------------------

update-icon merely relies on packagekit to discover potential updates.
If updates are available, we will only notify once using a Desktop Notification.
The icon itself reloads every 3 minutes, and will change its tooltip to reflect
the available package count.

If no updates are available, the icon will be invisible. The icon also changes to
reflect whether there are security updates available.

Updating itself is done via the PackageKit backend, and we simply launch gpk-update-viewer
when a user left clicks the icon.

update-icon should be automatically started on desktop launch, and will continue to run in
the background polling for updates. This does not in itself refresh the cache, this is done
by PackageKit.

Installation
------------
software-update-icon.py should be installed as /usr/bin/software-update-icon
software-update-icon.desktop should be installed to /etc/xdg/autostart/ so that it is automatically
running in the background for each user.

Note that this software requires gnome-packagekit + packagekit-glib to be installed (with the relevant
backend), Python2.7, Python-GObject, GTK3 (With gir and typelib).
It is recommended to use a suitable notification system, such as notification-daemon from Xfce or
notify-osd.

SolusOS Notes
-------------
Assuming this software is installed per the first installation paragraph, it will operate correctly with
no additional dependencies. notify-osd will replace notification-daemon as the notify system of choice
in SolusOS 2. Note the PiSi backend is also maintained by myself and will integrate well with this icon.


Authors
-------

 - Ikey Doherty <ikey@solusos.com>

