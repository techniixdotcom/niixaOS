# Draws the NiiX icon theme for the ISO build, into NIIX_ICON_DEST. The
# drawings and the tile come from niix-iconify, which keeps adding icons for
# new apps on installed systems. Prints how many icons it wrote.
import importlib.machinery
import importlib.util
import os
import sys

sys.dont_write_bytecode = True      # don't leave a cache next to niix-iconify

ICONIFY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "profile", "airootfs",
                       "usr", "local", "bin", "niix-iconify")
loader = importlib.machinery.SourceFileLoader("niix_iconify", ICONIFY)
iconify = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
loader.exec_module(iconify)
TEAL, PINK = iconify.TEAL, iconify.PINK
DEST = os.environ["NIIX_ICON_DEST"]

INDEX_THEME = """[Icon Theme]
Name=NiiX
Comment=NiiX Arch flat icon theme (Tabler-glyph squircles, teal + pink accents)
Inherits=Adwaita,hicolor
Directories=scalable/apps,scalable/places,scalable/mimetypes

[scalable/apps]
Context=Applications
Size=256
MinSize=8
MaxSize=512
Type=Scalable

[scalable/places]
Context=Places
Size=256
MinSize=8
MaxSize=512
Type=Scalable

[scalable/mimetypes]
Context=MimeTypes
Size=256
MinSize=8
MaxSize=512
Type=Scalable
"""

# Icon file (under scalable/), drawing, colour.
ICONS = [
    ("apps/accessories-calculator.svg", "calculator", TEAL),
    ("apps/accessories-text-editor.svg", "file-text", TEAL),
    ("apps/applets-screenshooter.svg", "camera", TEAL),
    ("apps/application-default-icon.svg", "app-window", TEAL),
    ("apps/application-x-addon.svg", "app-window", TEAL),
    ("apps/application-x-executable.svg", "app-window", TEAL),
    ("apps/applications-other.svg", "app-window", TEAL),
    ("apps/baobab.svg", "disk-usage", TEAL),
    ("apps/brasero.svg", "disc", TEAL),
    ("apps/com.heroicgameslauncher.hgl.svg", "heroic", PINK),
    ("apps/com.leinardi.gwe.svg", "gpu-fan", TEAL),
    ("apps/com.stremio.Stremio.svg", "movie", PINK),
    ("apps/corectrl.svg", "gpu-tune", TEAL),
    ("apps/drive-harddisk.svg", "server-2", TEAL),
    ("apps/eog.svg", "photo", PINK),
    ("apps/evince.svg", "book", TEAL),
    ("apps/exec.svg", "app-window", TEAL),
    ("apps/folder.svg", "folder", TEAL),
    ("apps/gedit.svg", "file-text", TEAL),
    ("apps/gnome-calculator.svg", "calculator", TEAL),
    ("apps/gnome-calendar.svg", "calendar", TEAL),
    ("apps/gnome-control-center.svg", "settings", TEAL),
    ("apps/gnome-disks.svg", "server-2", TEAL),
    ("apps/gnome-other.svg", "app-window", TEAL),
    ("apps/gnome-power-statistics.svg", "battery", TEAL),
    ("apps/gnome-software.svg", "apps", TEAL),
    ("apps/gnome-system-monitor.svg", "activity", TEAL),
    ("apps/gnome-terminal.svg", "terminal-2", TEAL),
    ("apps/gnome-tweaks.svg", "tweaks", TEAL),
    ("apps/gwe.svg", "gpu-fan", TEAL),
    ("apps/helium-browser.svg", "world", PINK),
    ("apps/helium.svg", "world", PINK),
    ("apps/heroic.svg", "heroic", PINK),
    ("apps/image-viewer.svg", "photo", PINK),
    ("apps/inode-directory.svg", "folder", TEAL),
    ("apps/internet-web-browser.svg", "world", PINK),
    ("apps/lutris.svg", "lutris", PINK),
    ("apps/multimedia-audio-player.svg", "music", PINK),
    ("apps/multimedia-photo-viewer.svg", "photo", PINK),
    ("apps/multimedia-video-player.svg", "movie", PINK),
    ("apps/nautilus.svg", "folder", TEAL),
    ("apps/net.davidotek.pupgui2.svg", "proton-up", PINK),
    ("apps/net.lutris.Lutris.svg", "lutris", PINK),
    ("apps/nvidia-settings.svg", "nvidia", TEAL),
    ("apps/org.corectrl.CoreCtrl.svg", "gpu-tune", TEAL),
    ("apps/org.corectrl.corectrl.svg", "gpu-tune", TEAL),
    ("apps/org.gnome.Boxes.svg", "box", TEAL),
    ("apps/org.gnome.Calculator.svg", "calculator", TEAL),
    ("apps/org.gnome.Calendar.Devel.svg", "calendar", TEAL),
    ("apps/org.gnome.Calendar.svg", "calendar", TEAL),
    ("apps/org.gnome.Characters.svg", "characters", TEAL),
    ("apps/org.gnome.Clocks.svg", "clock", TEAL),
    ("apps/org.gnome.Connections.svg", "remote-desktop", TEAL),
    ("apps/org.gnome.Console.Devel.svg", "terminal-2", TEAL),
    ("apps/org.gnome.Console.svg", "terminal-2", TEAL),
    ("apps/org.gnome.Contacts.svg", "contacts", TEAL),
    ("apps/org.gnome.Decibels.svg", "music", PINK),
    ("apps/org.gnome.DiskUsageAnalyzer.svg", "disk-usage", TEAL),
    ("apps/org.gnome.DiskUtility.svg", "server-2", TEAL),
    ("apps/org.gnome.Disks.svg", "server-2", TEAL),
    ("apps/org.gnome.Documents.svg", "book", TEAL),
    ("apps/org.gnome.Epiphany.svg", "world", PINK),
    ("apps/org.gnome.Evince.svg", "book", TEAL),
    ("apps/org.gnome.Extensions.Devel.svg", "extensions-dev", TEAL),
    ("apps/org.gnome.Extensions.svg", "extensions-dev", TEAL),
    ("apps/org.gnome.Files.svg", "folder", TEAL),
    ("apps/org.gnome.FontViewer.svg", "fonts", TEAL),
    ("apps/org.gnome.Image-Viewer.svg", "photo", PINK),
    ("apps/org.gnome.Logs.svg", "logs", TEAL),
    ("apps/org.gnome.Loupe.svg", "photo", PINK),
    ("apps/org.gnome.Maps.svg", "map-2", TEAL),
    ("apps/org.gnome.MultiWriter.svg", "disc", TEAL),
    ("apps/org.gnome.Music.svg", "music", PINK),
    ("apps/org.gnome.Nautilus.svg", "folder", TEAL),
    ("apps/org.gnome.Papers.svg", "book", TEAL),
    ("apps/org.gnome.PowerStats.svg", "battery", TEAL),
    ("apps/org.gnome.Screenshot.svg", "camera", TEAL),
    ("apps/org.gnome.Settings.svg", "settings", TEAL),
    ("apps/org.gnome.SimpleScan.svg", "scanner", TEAL),
    ("apps/org.gnome.Snapshot.svg", "camera", TEAL),
    ("apps/org.gnome.Software.svg", "apps", TEAL),
    ("apps/org.gnome.SystemMonitor.Devel.svg", "activity", TEAL),
    ("apps/org.gnome.SystemMonitor.svg", "activity", TEAL),
    ("apps/org.gnome.Terminal.svg", "terminal-2", TEAL),
    ("apps/org.gnome.TextEditor.svg", "file-text", TEAL),
    ("apps/org.gnome.Totem.svg", "movie", PINK),
    ("apps/org.gnome.Tweaks.svg", "tweaks", TEAL),
    ("apps/org.gnome.Usage.svg", "usage", TEAL),
    ("apps/org.gnome.Videos.svg", "movie", PINK),
    ("apps/org.gnome.Weather.svg", "cloud", TEAL),
    ("apps/org.gnome.Web.svg", "world", PINK),
    ("apps/org.gnome.baobab.svg", "disk-usage", TEAL),
    ("apps/org.gnome.clocks.svg", "clock", TEAL),
    ("apps/org.gnome.eog.svg", "photo", PINK),
    ("apps/org.gnome.font-viewer.svg", "fonts", TEAL),
    ("apps/org.gnome.gedit.svg", "file-text", TEAL),
    ("apps/org.gnome.seahorse.Application.svg", "key", TEAL),
    ("apps/org.gnome.tweaks.svg", "tweaks", TEAL),
    ("apps/preferences-desktop-font.svg", "fonts", TEAL),
    ("apps/preferences-desktop.svg", "settings", TEAL),
    ("apps/preferences-other.svg", "tweaks", TEAL),
    ("apps/preferences-system.svg", "settings", TEAL),
    ("apps/protonup-qt.svg", "proton-up", PINK),
    ("apps/rhythmbox.svg", "music", PINK),
    ("apps/seahorse.svg", "key", TEAL),
    ("apps/simple-scan.svg", "scanner", TEAL),
    ("apps/software-properties-gtk.svg", "apps", TEAL),
    ("apps/software-properties.svg", "apps", TEAL),
    ("apps/steam-native.svg", "device-gamepad-2", PINK),
    ("apps/steam.svg", "device-gamepad-2", PINK),
    ("apps/stremio.svg", "movie", PINK),
    ("apps/system-file-manager.svg", "folder", TEAL),
    ("apps/system-software-install.svg", "apps", TEAL),
    ("apps/terminal.svg", "terminal-2", TEAL),
    ("apps/text-editor.svg", "file-text", TEAL),
    ("apps/text-x-generic.svg", "file-text", TEAL),
    ("apps/totem.svg", "movie", PINK),
    ("apps/utilities-system-monitor.svg", "activity", TEAL),
    ("apps/utilities-terminal.svg", "terminal-2", TEAL),
    ("apps/web-browser.svg", "world", PINK),
    ("mimetypes/application-octet-stream.svg", "app-window", TEAL),
    ("mimetypes/application-x-executable.svg", "app-window", TEAL),
    ("mimetypes/inode-directory.svg", "folder", TEAL),
    ("mimetypes/text-plain.svg", "file-text", TEAL),
    ("mimetypes/text-x-generic.svg", "file-text", TEAL),
    ("places/default-folder.svg", "folder", TEAL),
    ("places/emptytrash.svg", "trash-empty", TEAL),
    ("places/folder-desktop.svg", "desktop", TEAL),
    ("places/folder-documents.svg", "file-text", TEAL),
    ("places/folder-download.svg", "download", TEAL),
    ("places/folder-downloads.svg", "download", TEAL),
    ("places/folder-home.svg", "home", TEAL),
    ("places/folder-music.svg", "music", TEAL),
    ("places/folder-network.svg", "server-2", TEAL),
    ("places/folder-open.svg", "folder", TEAL),
    ("places/folder-pictures.svg", "photo", TEAL),
    ("places/folder-public.svg", "contacts", TEAL),
    ("places/folder-publicshare.svg", "contacts", TEAL),
    ("places/folder-remote.svg", "server-2", TEAL),
    ("places/folder-templates.svg", "templates", TEAL),
    ("places/folder-videos.svg", "movie", TEAL),
    ("places/folder.svg", "folder", TEAL),
    ("places/inode-directory.svg", "folder", TEAL),
    ("places/network-server.svg", "server-2", TEAL),
    ("places/network-workgroup.svg", "server-2", TEAL),
    ("places/trashcan_empty.svg", "trash-empty", TEAL),
    ("places/user-desktop.svg", "desktop", TEAL),
    ("places/user-home.svg", "home", TEAL),
    ("places/user-trash-full.svg", "trash-empty", TEAL),
    ("places/user-trash.svg", "trash-empty", TEAL),
]


os.makedirs(DEST, mode=0o755, exist_ok=True)
with open(os.path.join(DEST, "index.theme"), "w", encoding="utf-8") as f:
    f.write(INDEX_THEME)
for rel, glyph, colour in ICONS:
    path = os.path.join(DEST, "scalable", rel)
    os.makedirs(os.path.dirname(path), mode=0o755, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(iconify.tile(glyph, colour, auto=False))
for root, _dirs, files in os.walk(DEST):
    os.chmod(root, 0o755)
    for name in files:
        os.chmod(os.path.join(root, name), 0o644)
print(len(ICONS))
