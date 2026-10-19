# Draws the NiiX icon theme: every icon is the same dark rounded tile with one
# line drawing (Tabler Icons, MIT) in teal or pink. Run by the ISO build with
# NIIX_ICON_DEST set to the theme folder; prints how many icons it wrote.
import os

DEST = os.environ["NIIX_ICON_DEST"]
TEAL = "#5eead4"
PINK = "#f0a6c0"

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

# Every icon is the same dark rounded tile with one line drawing on it.
HEAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">\n'
    '  <rect x="14" y="14" width="228" height="228" rx="58" fill="#121821" stroke="#1f2a33" stroke-width="2"/>\n'
    '  <g transform="translate(64,64) scale(5.3333)" fill="none" stroke="'
)
MID = '" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
TAIL = '</g>\n</svg>\n'

# The line drawings (Tabler Icons glyphs, MIT licence), one SVG path per line.
GLYPHS = {
    "activity": [
        '<path d="M3 12h4l3 8l4 -16l3 8h4" />',
    ],
    "app-window": [
        '<path d="M3 7a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-10" />',
        '<path d="M6 8h.01" />',
        '<path d="M9 8h.01" />',
    ],
    "apps": [
        '<path d="M4 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />',
        '<path d="M4 15a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />',
        '<path d="M14 15a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />',
        '<path d="M14 7l6 0" />',
        '<path d="M17 4l0 6" />',
    ],
    "battery": [
        '<path d="M6 7h11a2 2 0 0 1 2 2v.5a.5 .5 0 0 0 .5 .5a.5 .5 0 0 1 .5 .5v3a.5 .5 0 0 1 -.5 .5a.5 .5 0 0 0 -.5 .5v.5a2 2 0 0 1 -2 2h-11a2 2 0 0 1 -2 -2v-6a2 2 0 0 1 2 -2" />',
    ],
    "book": [
        '<path d="M3 19a9 9 0 0 1 9 0a9 9 0 0 1 9 0" />',
        '<path d="M3 6a9 9 0 0 1 9 0a9 9 0 0 1 9 0" />',
        '<path d="M3 6l0 13" />',
        '<path d="M12 6l0 13" />',
        '<path d="M21 6l0 13" />',
    ],
    "box": [
        '<path d="M12 3l8 4.5l0 9l-8 4.5l-8 -4.5l0 -9l8 -4.5" />',
        '<path d="M12 12l8 -4.5" />',
        '<path d="M12 12l0 9" />',
        '<path d="M12 12l-8 -4.5" />',
    ],
    "calculator": [
        '<path d="M4 5a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2l0 -14" />',
        '<path d="M8 8a1 1 0 0 1 1 -1h6a1 1 0 0 1 1 1v1a1 1 0 0 1 -1 1h-6a1 1 0 0 1 -1 -1l0 -1" />',
        '<path d="M8 14l0 .01" />',
        '<path d="M12 14l0 .01" />',
        '<path d="M16 14l0 .01" />',
        '<path d="M8 17l0 .01" />',
        '<path d="M12 17l0 .01" />',
        '<path d="M16 17l0 .01" />',
    ],
    "calendar": [
        '<path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12" />',
        '<path d="M16 3v4" />',
        '<path d="M8 3v4" />',
        '<path d="M4 11h16" />',
        '<path d="M11 15h1" />',
        '<path d="M12 15v3" />',
    ],
    "camera": [
        '<path d="M5 7h1a2 2 0 0 0 2 -2a1 1 0 0 1 1 -1h6a1 1 0 0 1 1 1a2 2 0 0 0 2 2h1a2 2 0 0 1 2 2v9a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-9a2 2 0 0 1 2 -2" />',
        '<path d="M9 13a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" />',
    ],
    "characters": [
        '<path d="M14 15.5a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0 -7 0" />',
        '<path d="M3 19v-10.5a3.5 3.5 0 0 1 7 0v10.5" />',
        '<path d="M3 13h7" />',
        '<path d="M21 12v7" />',
    ],
    "clock": [
        '<path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" />',
        '<path d="M12 7v5l3 3" />',
    ],
    "cloud": [
        '<path d="M6.657 18c-2.572 0 -4.657 -2.007 -4.657 -4.483c0 -2.475 2.085 -4.482 4.657 -4.482c.393 -1.762 1.794 -3.2 3.675 -3.773c1.88 -.572 3.956 -.193 5.444 1c1.488 1.19 2.162 3.007 1.77 4.769h.99c1.913 0 3.464 1.56 3.464 3.486c0 1.927 -1.551 3.487 -3.465 3.487h-11.878" />',
    ],
    "contacts": [
        '<path d="M5 7a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" />',
        '<path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" />',
        '<path d="M16 3.13a4 4 0 0 1 0 7.75" />',
        '<path d="M21 21v-2a4 4 0 0 0 -3 -3.85" />',
    ],
    "desktop": [
        '<path d="M3 5a1 1 0 0 1 1 -1h16a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-16a1 1 0 0 1 -1 -1v-10" />',
        '<path d="M7 20h10" />',
        '<path d="M9 16v4" />',
        '<path d="M15 16v4" />',
    ],
    "device-gamepad-2": [
        '<path d="M12 5h3.5a5 5 0 0 1 0 10h-5.5l-4.015 4.227a2.3 2.3 0 0 1 -3.923 -2.035l1.634 -8.173a5 5 0 0 1 4.904 -4.019h3.4" />',
        '<path d="M14 15l4.07 4.284a2.3 2.3 0 0 0 3.925 -2.023l-1.6 -8.232" />',
        '<path d="M8 9v2" />',
        '<path d="M7 10h2" />',
        '<path d="M14 10h2" />',
    ],
    "disc": [
        '<path d="M3 12a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />',
        '<path d="M11 12a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" />',
        '<path d="M7 12a5 5 0 0 1 5 -5" />',
        '<path d="M12 17a5 5 0 0 0 5 -5" />',
    ],
    "disk-usage": [
        '<path d="M10 3.2a9 9 0 1 0 10.8 10.8a1 1 0 0 0 -1 -1h-6.8a2 2 0 0 1 -2 -2v-7a.9 .9 0 0 0 -1 -.8" />',
        '<path d="M15 3.5a9 9 0 0 1 5.5 5.5h-4.5a1 1 0 0 1 -1 -1v-4.5" />',
    ],
    "download": [
        '<path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />',
        '<path d="M7 11l5 5l5 -5" />',
        '<path d="M12 4l0 12" />',
    ],
    "extensions-dev": [
        '<path d="M4 7h3a1 1 0 0 0 1 -1v-1a2 2 0 0 1 4 0v1a1 1 0 0 0 1 1h3a1 1 0 0 1 1 1v3a1 1 0 0 0 1 1h1a2 2 0 0 1 0 4h-1a1 1 0 0 0 -1 1v3a1 1 0 0 1 -1 1h-3a1 1 0 0 1 -1 -1v-1a2 2 0 0 0 -4 0v1a1 1 0 0 1 -1 1h-3a1 1 0 0 1 -1 -1v-3a1 1 0 0 1 1 -1h1a2 2 0 0 0 0 -4h-1a1 1 0 0 1 -1 -1v-3a1 1 0 0 1 1 -1" />',
    ],
    "file-text": [
        '<path d="M14 3v4a1 1 0 0 0 1 1h4" />',
        '<path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2" />',
        '<path d="M9 9l1 0" />',
        '<path d="M9 13l6 0" />',
        '<path d="M9 17l6 0" />',
    ],
    "folder": [
        '<path d="M5 4h4l3 3h7a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-11a2 2 0 0 1 2 -2" />',
    ],
    "fonts": [
        '<path d="M4 20l3 0" />',
        '<path d="M14 20l7 0" />',
        '<path d="M6.9 15l6.9 0" />',
        '<path d="M10.2 6.3l5.8 13.7" />',
        '<path d="M5 20l6 -16l2 0l7 16" />',
    ],
    "gpu-fan": [
        '<path d="M3 5a1 1 0 0 1 1 -1h16a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-16a1 1 0 0 1 -1 -1l0 -10" />',
        '<path d="M7 20h10" />',
        '<path d="M9 16v4" />',
        '<path d="M15 16v4" />',
        '<path d="M9 12v-4" />',
        '<path d="M12 12v-1" />',
        '<path d="M15 12v-2" />',
        '<path d="M12 12v-1" />',
    ],
    "gpu-tune": [
        '<path d="M5 6a1 1 0 0 1 1 -1h12a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-12a1 1 0 0 1 -1 -1l0 -12" />',
        '<path d="M9 9h6v6h-6l0 -6" />',
        '<path d="M3 10h2" />',
        '<path d="M3 14h2" />',
        '<path d="M10 3v2" />',
        '<path d="M14 3v2" />',
        '<path d="M21 10h-2" />',
        '<path d="M21 14h-2" />',
        '<path d="M14 21v-2" />',
        '<path d="M10 21v-2" />',
    ],
    "heroic": [
        '<path d="M9 12l-3 -3h-2a1 1 0 0 0 -1 1v4a1 1 0 0 0 1 1h2l3 -3" />',
        '<path d="M15 12l3 -3h2a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-2l-3 -3" />',
        '<path d="M12 15l-3 3v2a1 1 0 0 0 1 1h4a1 1 0 0 0 1 -1v-2l-3 -3" />',
        '<path d="M12 9l-3 -3v-2a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v2l-3 3" />',
    ],
    "home": [
        '<path d="M5 12l-2 0l9 -9l9 9l-2 0" />',
        '<path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7" />',
        '<path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6" />',
    ],
    "key": [
        '<path d="M16.555 3.843l3.602 3.602a2.877 2.877 0 0 1 0 4.069l-2.643 2.643a2.877 2.877 0 0 1 -4.069 0l-.301 -.301l-6.558 6.558a2 2 0 0 1 -1.239 .578l-.175 .008h-1.172a1 1 0 0 1 -.993 -.883l-.007 -.117v-1.172a2 2 0 0 1 .467 -1.284l.119 -.13l.414 -.414h2v-2h2v-2l2.144 -2.144l-.301 -.301a2.877 2.877 0 0 1 0 -4.069l2.643 -2.643a2.877 2.877 0 0 1 4.069 0" />',
        '<path d="M15 9h.01" />',
    ],
    "logs": [
        '<path d="M13 5h8" />',
        '<path d="M13 9h5" />',
        '<path d="M13 15h8" />',
        '<path d="M13 19h5" />',
        '<path d="M3 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />',
        '<path d="M3 15a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" />',
    ],
    "lutris": [
        '<path d="M2 8a2 2 0 0 1 2 -2h16a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-16a2 2 0 0 1 -2 -2l0 -8" />',
        '<path d="M6 12h4m-2 -2v4" />',
        '<path d="M15 11l0 .01" />',
        '<path d="M18 13l0 .01" />',
    ],
    "map-2": [
        '<path d="M12 18.5l-3 -1.5l-6 3v-13l6 -3l6 3l6 -3v7.5" />',
        '<path d="M9 4v13" />',
        '<path d="M15 7v5.5" />',
        '<path d="M21.121 20.121a3 3 0 1 0 -4.242 0c.418 .419 1.125 1.045 2.121 1.879c1.051 -.89 1.759 -1.516 2.121 -1.879" />',
        '<path d="M19 18v.01" />',
    ],
    "movie": [
        '<path d="M4 6a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2l0 -12" />',
        '<path d="M8 4l0 16" />',
        '<path d="M16 4l0 16" />',
        '<path d="M4 8l4 0" />',
        '<path d="M4 16l4 0" />',
        '<path d="M4 12l16 0" />',
        '<path d="M16 8l4 0" />',
        '<path d="M16 16l4 0" />',
    ],
    "music": [
        '<path d="M3 17a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" />',
        '<path d="M13 17a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" />',
        '<path d="M9 17v-13h10v13" />',
        '<path d="M9 8h10" />',
    ],
    "nvidia": [
        '<path d="M13.256 20.473c-.855 .907 -2.583 .643 -2.931 -.79a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.07 .26 1.488 1.29 1.254 2.15" />',
        '<path d="M19 16l-2 3h4l-2 3" />',
        '<path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" />',
    ],
    "photo": [
        '<path d="M15 8h.01" />',
        '<path d="M3 6a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v12a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3v-12" />',
        '<path d="M3 16l5 -5c.928 -.893 2.072 -.893 3 0l5 5" />',
        '<path d="M14 14l1 -1c.928 -.893 2.072 -.893 3 0l3 3" />',
    ],
    "proton-up": [
        '<path d="M9 12h-3.586a1 1 0 0 1 -.707 -1.707l6.586 -6.586a1 1 0 0 1 1.414 0l6.586 6.586a1 1 0 0 1 -.707 1.707h-3.586v3h-6v-3" />',
        '<path d="M9 21h6" />',
        '<path d="M9 18h6" />',
    ],
    "remote-desktop": [
        '<path d="M7 12l5 5l-1.5 1.5a3.536 3.536 0 1 1 -5 -5l1.5 -1.5" />',
        '<path d="M17 12l-5 -5l1.5 -1.5a3.536 3.536 0 1 1 5 5l-1.5 1.5" />',
        '<path d="M3 21l2.5 -2.5" />',
        '<path d="M18.5 5.5l2.5 -2.5" />',
        '<path d="M10 11l-2 2" />',
        '<path d="M13 14l-2 2" />',
    ],
    "scanner": [
        '<path d="M5 12h14" />',
        '<path d="M3 7v-2a2 2 0 0 1 2 -2h2" />',
        '<path d="M3 17v2a2 2 0 0 0 2 2h2" />',
        '<path d="M17 3h2a2 2 0 0 1 2 2v2" />',
        '<path d="M17 21h2a2 2 0 0 0 2 -2v-2" />',
    ],
    "server-2": [
        '<path d="M3 7a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3v-2" />',
        '<path d="M3 15a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3l0 -2" />',
        '<path d="M7 8l0 .01" />',
        '<path d="M7 16l0 .01" />',
        '<path d="M11 8h6" />',
        '<path d="M11 16h6" />',
    ],
    "settings": [
        '<path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065" />',
        '<path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0" />',
    ],
    "templates": [
        '<path d="M4 5a1 1 0 0 1 1 -1h14a1 1 0 0 1 1 1v2a1 1 0 0 1 -1 1h-14a1 1 0 0 1 -1 -1l0 -2" />',
        '<path d="M4 13a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -6" />',
        '<path d="M14 12l6 0" />',
        '<path d="M14 16l6 0" />',
        '<path d="M14 20l6 0" />',
    ],
    "terminal-2": [
        '<path d="M8 9l3 3l-3 3" />',
        '<path d="M13 15l3 0" />',
        '<path d="M3 6a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2l0 -12" />',
    ],
    "trash-empty": [
        '<path d="M4 7l16 0" />',
        '<path d="M10 11l0 6" />',
        '<path d="M14 11l0 6" />',
        '<path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />',
        '<path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />',
    ],
    "tweaks": [
        '<path d="M4 10a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />',
        '<path d="M6 4v4" />',
        '<path d="M6 12v8" />',
        '<path d="M10 16a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />',
        '<path d="M12 4v10" />',
        '<path d="M12 18v2" />',
        '<path d="M16 7a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />',
        '<path d="M18 4v1" />',
        '<path d="M18 9v11" />',
    ],
    "usage": [
        '<path d="M4 19l16 0" />',
        '<path d="M4 15l4 -6l4 2l4 -5l4 4" />',
    ],
    "world": [
        '<path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" />',
        '<path d="M3.6 9h16.8" />',
        '<path d="M3.6 15h16.8" />',
        '<path d="M11.5 3a17 17 0 0 0 0 18" />',
        '<path d="M12.5 3a17 17 0 0 1 0 18" />',
    ],
}

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


def svg(glyph, colour):
    paths = GLYPHS[glyph]
    return HEAD + colour + MID + "\n    " + "\n  ".join(paths) + "\n  " + TAIL


os.makedirs(DEST, mode=0o755, exist_ok=True)
with open(os.path.join(DEST, "index.theme"), "w", encoding="utf-8") as f:
    f.write(INDEX_THEME)
for rel, glyph, colour in ICONS:
    path = os.path.join(DEST, "scalable", rel)
    os.makedirs(os.path.dirname(path), mode=0o755, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg(glyph, colour))
for root, _dirs, files in os.walk(DEST):
    os.chmod(root, 0o755)
    for name in files:
        os.chmod(os.path.join(root, name), 0o644)
print(len(ICONS))
