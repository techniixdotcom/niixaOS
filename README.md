<p align="center">
  <img src="niixarch-logo.png" alt="niixaOS" width="240">
</p>

<h1 align="center">niixaOS</h1>

<p align="center">
  <b>Arch Linux, ready to play.</b><br>
  A fast, encrypted Arch desktop that sets itself up.
</p>

<p align="center">
  <a href="https://niixa.org">Website</a> ·
  <a href="https://niixa.org/#download">Download</a> ·
  <a href="https://github.com/techniixdotcom/niixarch-install/issues">Report a bug</a>
</p>


<p align="center">
  <img src="niixarch-logo.png" alt="niixaOS" width="500">
</p>



Arch is powerful but slow to set up. niixaOS does the setup for you. Boot the USB stick, click **Install NiiX**, answer a few questions, and you get a clean GNOME desktop with your drivers and games ready to go.

## What you get

- **One click install** – next to Windows (dual boot) or on a whole drive. Nothing changes until you confirm.
- **Fast** – the CachyOS kernel and packages built for modern CPUs, with ZRAM swap.
- **Gaming ready** – Steam, Lutris and Heroic with Proton-CachyOS, GE-Proton, Gamescope, GameMode and MangoHud. Game controllers work on the desktop too.
- **Drivers handled** – NVIDIA, AMD and Intel are detected automatically, hybrid laptops included. The most powerful GPU is always used.
- **Adapts to your hardware** – desktop, laptop, handheld or virtual machine, monitor refresh rate and VRR, X3D and hybrid CPUs.
- **Encrypted** – full disk encryption with LUKS2. You unlock it once when the PC starts.
- **Undo bad updates** – Btrfs snapshots before and after every update, plus a "clean state" entry in the boot menu that starts the system as it was installed.
- **A familiar desktop** – GNOME with a taskbar and start menu, and no clutter on the desktop.
- **Extras** – Windows drives readable straight away, USB sticks mount automatically, optional Wi-Fi hotspot, VR headsets (WiVRn and SteamVR).

## Requirements

| | |
|---|---|
| PC | 64-bit, **UEFI** (legacy BIOS is not supported) |
| CPU | **AVX2** (x86-64-v3): Intel Core 4th gen (2013) / AMD Ryzen or newer |
| Secure Boot | **Off** – the Limine bootloader doesn't support it |
| Disk | Free space next to Windows, or a drive you are willing to wipe (40 GB minimum, 64 GB+ recommended) |
| USB stick | 8 GB or more |
| Internet | During the install, for updates newer than the ISO, the NVIDIA driver and the Flatpak apps |

## Install

1. **Download** the ISO from [niixa.org](https://niixa.org/#download) or the [Releases page](https://github.com/techniixdotcom/niixarch-install/releases/latest), and check it:
   ```sh
   sha256sum -c niixaos-YYYY.MM.DD-x86_64.iso.sha256
   ```
   GitHub only allows files up to 2 GiB, so a release there may come in parts. Download every `.part-NN` file and join them first:
   ```sh
   cat niixaos-*.iso.part-* > niixaos-YYYY.MM.DD-x86_64.iso
   ```
   On Windows: `copy /b file.part-00 + file.part-01 + file.part-02 niixaos.iso` (every part, in order).
2. **Write it to a USB stick** with [balenaEtcher](https://etcher.balena.io), [Ventoy](https://www.ventoy.net) or `dd`:
   ```sh
   sudo dd if=niixaos-YYYY.MM.DD-x86_64.iso of=/dev/sdX bs=4M status=progress oflag=sync
   ```
3. **Boot from it.** Turn Secure Boot off in the BIOS, then pick the USB stick in the boot menu (usually `F12`, `F11` or `Esc`). Not sure the stick is good? Choose **check the USB stick first** in the niixaOS boot menu.
4. **Click install.** The live desktop opens. Try it out, then double-click **Install NiiX** and answer the questions: keyboard, time zone, disk passphrase, user name, and dual or single boot.

After the restart, unlock the disk with your passphrase. Everything was set up during the install, so the desktop opens ready to go.

> **Back up your files first**, especially when installing next to Windows. For dual boot, shrink Windows in Disk Management to make free space.

## Handy commands

Open a terminal with `Ctrl` + `Alt` + `T` (or `F12` for the drop-down terminal).

| Command | What it does |
|---|---|
| `niix-update` | Update everything: system, AUR, Flatpak apps. Shows Arch news first. |
| `niix-update --firmware` | Also install firmware updates (BIOS, SSD, docks). |
| `niix-gpu status` | Show the GPUs found and which one is used. |
| `niix-display status` | Show your monitors, their refresh rate and VRR. |
| `niix-ntfs list` | Show the Windows (NTFS) drives and how they are mounted. |
| `niix-hotspot start` | Turn on the Wi-Fi hotspot. |
| `niix-hotspot auto off` | Stop the hotspot coming back after a restart. |
| `sudo niixarch-refresh-clean` | Make the "clean state" boot entry start the system as it is now. |

System updates also run on their own every 12 hours, never during a game.

## Under the hood

| | |
|---|---|
| Base | Arch Linux + CachyOS repositories |
| Kernel | `linux-cachyos` |
| Bootloader | Limine (UEFI) |
| Encryption | LUKS2, full disk |
| Filesystem | Btrfs with zstd: `@`, `@home`, `@snapshots`, `@var_log` |
| Snapshots | Snapper + snap-pac |
| Swap | ZRAM (zstd, sized from RAM) |
| Desktop | GNOME on Wayland, dash-to-panel, ArcMenu, NiiX icons |
| Language | English (en_GB); keyboard and time zone chosen during install |

## Build the ISO yourself

On any x86_64 Linux PC with about 40 GB free and a CPU with AVX2:

```sh
git clone https://github.com/techniixdotcom/niixarch-install
cd niixarch-install
sudo ./build.sh
```

The build runs inside a throwaway Arch Linux container (podman or docker; podman is installed if neither is there) and takes 30–90 minutes. When it's done:

```
out/niixaos-YYYY.MM.DD-x86_64.iso          the ISO
out/niixaos-YYYY.MM.DD-x86_64.iso.sha256   its checksum
out/build-YYYYMMDD-HHMMSS.log              the full build log
cache/                                     downloaded packages (makes the next build faster)
```

GitHub builds it too: every push checks the scripts and builds the ISO, and pushing a tag (`git tag v2026.10.19 && git push origin v2026.10.19`) publishes it as a release.

### What's where

The ISO is the finished system. The installer copies it to the encrypted disk and adds only what depends on your PC: partitions, user, keyboard, time zone, GPU driver and the boot menu.

| To change | Edit |
|---|---|
| Packages | `packages/repo.txt`, `aur.txt`, `flatpak.txt` |
| A setting or tool | its file under `profile/airootfs/`, at the same path as on the system |
| Settings in files a package owns (pacman.conf, firewall, Bluetooth) | `profile/airootfs/usr/local/lib/niix-build/customize-image` |
| What the installer asks | `profile/airootfs/usr/local/bin/niix-installer` |
| What the install does | `profile/airootfs/usr/local/lib/niix/niix-install` |
| Logo and wallpaper | `assets/niixarch-logo.png`, `assets/niix-background.png` |

## Verify the ISO

Every ISO comes with a `.sha256` file:

```sh
sha256sum -c niixaos-YYYY.MM.DD-x86_64.iso.sha256
```

The boot menu entry **check the USB stick first** checks the system image on the stick itself before it starts, so a badly written stick is caught before anything is installed.

## Privacy

niixaOS has no telemetry and sends nothing to niixa.org. The installer only downloads from Arch, CachyOS and Flathub. Like most Linux desktops, it checks whether you're online using GNOME's and Google's standard connectivity check pages (`nmcheck.gnome.org`, `gstatic.com`).

## Help and bugs

Open an [issue](https://github.com/techniixdotcom/niixarch-install/issues) or use the contact form on [niixa.org](https://niixa.org/#contact). Including your CPU, GPU and whether it's a laptop or desktop helps a lot.

## License

[GPL-3.0](LICENSE)
