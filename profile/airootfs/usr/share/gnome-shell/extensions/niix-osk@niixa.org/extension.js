// niix-osk - lets niix-padnav open GNOME's on-screen keyboard on demand.
//
// GNOME only shows its keyboard when a text field gets focus, and only with
// the accessibility setting on. This adds a way to just open it:
//   gdbus call --session --dest org.gnome.Shell --object-path /org/niixa/Osk \
//       --method org.niixa.Osk.Toggle
// Opening turns the setting on; closing turns it off again, so the keyboard
// doesn't pop up by itself afterwards.
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

const IFACE = `
<node>
  <interface name="org.niixa.Osk">
    <method name="Toggle"/>
    <method name="Show"/>
    <method name="Hide"/>
  </interface>
</node>`;

const SCHEMA = 'org.gnome.desktop.a11y.applications';
const KEY = 'screen-keyboard-enabled';

export default class NiixOskExtension extends Extension {
    enable() {
        this._settings = new Gio.Settings({schema_id: SCHEMA});
        this._openId = 0;
        this._dbus = Gio.DBusExportedObject.wrapJSObject(IFACE, this);
        this._dbus.export(Gio.DBus.session, '/org/niixa/Osk');
    }

    disable() {
        this._cancelOpen();
        this._dbus?.unexport();
        this._dbus = null;
        this._settings = null;
    }

    Toggle() {
        if (Main.keyboard.visible)
            this.Hide();
        else
            this.Show();
    }

    Show() {
        this._cancelOpen();
        if (!this._settings.get_boolean(KEY))
            this._settings.set_boolean(KEY, true);
        // The keyboard is created once the setting change arrives; open it
        // as soon as it exists, waiting at most a second.
        let tries = 0;
        this._openId = GLib.timeout_add(GLib.PRIORITY_DEFAULT, 50, () => {
            tries++;
            if (!Main.keyboard.keyboardActor && tries < 20)
                return GLib.SOURCE_CONTINUE;
            this._openId = 0;
            Main.keyboard.open(Main.layoutManager.focusIndex);
            return GLib.SOURCE_REMOVE;
        });
    }

    Hide() {
        this._cancelOpen();
        Main.keyboard.close();
        if (this._settings.get_boolean(KEY))
            this._settings.set_boolean(KEY, false);
    }

    _cancelOpen() {
        if (this._openId) {
            GLib.source_remove(this._openId);
            this._openId = 0;
        }
    }
}
