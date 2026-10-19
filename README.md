<p align="center">
  <img src="niixarch-logo.png" alt="niixaOS" width="120">
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

---

Arch is powerful but slow to set up. niixaOS does the setup for you. Boot the USB stick, click **Install niixaOS**, answer a few questions, and you get a clean GNOME desktop with your drivers and games ready to go.

## What you get

- **One click install** – next to Windows (dual boot) or on a whole drive. Nothing changes until you confirm.
- **Fast** – the CachyOS kernel and packages built for modern CPUs, with ZRAM swap.
- **Gaming ready** – Steam, Lutris and Heroic with Proton-CachyOS, GE-Proton, Gamescope, GameMode and MangoHud. Game controllers work on the desktop too.
- **Drivers handled** – NVIDIA, AMD and Intel are detected automatically, hybrid laptops included. The most powerful GPU is always used.
- **Adapts to your hardware** – desktop, laptop, handheld or virtual machine, monitor refresh rate and VRR, X3D and hybrid CPUs.
- **Encrypted** – full disk encryption with LUKS2. You unlock it once when the PC starts.
- **Undo bad updates** – Btrfs snapshots before and after every update, selectable from the boot menu.
- **A familiar desktop** – GNOME with a taskbar and start menu, and no clutter on the desktop.
- **Extras** – Windows drives readable straight away, USB sticks mount automatically, optional Wi-Fi hotspot.

## Requirements

| | |
|---|---|
| PC | 64-bit, **UEFI** (legacy BIOS is not supported) |
| CPU | **AVX2** (x86-64-v3): Intel Core 4th gen (2013) / AMD Ryzen or newer |
| Secure Boot | **Off** – the Limine bootloader doesn't support it |
| Disk | Free space next to Windows, or a drive you are willing to wipe (64 GB+ recommended) |
| USB stick | 8 GB or more |
| Internet | During the install, for updates newer than the ISO, the NVIDIA driver, GE-Proton and Flatpak apps |

## Install

1. **Download** the ISO from [niixa.org](https://niixa.org/#download) and check it:
   ```sh
   sha256sum -c latest.sha256
   ```
2. **Write it to a USB stick** with [balenaEtcher](https://etcher.balena.io), [Ventoy](https://www.ventoy.net) or `dd`:
   ```sh
   sudo dd if=niixaos-YYYY.MM.DD-x86_64.iso of=/dev/sdX bs=4M status=progress oflag=sync
   ```
3. **Boot from it.** Turn Secure Boot off in the BIOS, then pick the USB stick in the boot menu (usually `F12`, `F11` or `Esc`).
4. **Click install.** The live desktop opens. Try it out, then double-click **Install niixaOS** and answer the questions: keyboard, time zone, disk passphrase, user name, and dual or single boot.

After the restart, unlock the disk with your passphrase. The first start downloads the newest updates and drivers, then you're ready to go.

> **Back up your files first**, especially when installing next to Windows. For dual boot, shrink Windows in Disk Management to make free space.

## Handy commands

Open a terminal with `Ctrl` + `Alt` + `T`.

| Command | What it does |
|---|---|
| `niix-update` | Update everything: system, AUR, Flatpak apps. Shows Arch news first. |
| `niix-update --firmware` | Also install firmware updates (BIOS, SSD, docks). |
| `niix-gpu status` | Show the GPUs found and which one is used. |
| `niix-ntfs list` | Show the Windows (NTFS) drives and how they are mounted. |
| `niix-hotspot start` | Turn on the Wi-Fi hotspot. |
| `niix-hotspot auto off` | Stop the hotspot coming back after a restart. |

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

Everything (the installer, the graphical installer and the ISO builder) is in the one `install` file. On any x86_64 Linux PC with about 40 GB free and a CPU with AVX2:

```sh
sudo bash install --build-iso
```

The build runs inside a throwaway Arch Linux container (podman or docker; podman is installed if neither is there) and takes 30–90 minutes. When it's done:

```
out/niixaos-YYYY.MM.DD-x86_64.iso          the ISO
out/niixaos-YYYY.MM.DD-x86_64.iso.sha256   its checksum
out/build-YYYYMMDD-HHMMSS.log              the full build log
cache/                                     downloaded packages (makes the next build faster)
```

## Verify the installer

`install.sha256` holds the checksum of the `install` file in this repository:

```sh
sha256sum -c install.sha256
```

The ISO also records the installer's checksum when it is built, and the installer checks itself against it before it touches any disk.

## Privacy

niixaOS has no telemetry and sends nothing to niixa.org. The installer only downloads from Arch, CachyOS, Flathub, the AUR, GNOME Extensions and GitHub. Like most Linux desktops, it checks whether you're online using GNOME's and Google's standard connectivity check pages (`nmcheck.gnome.org`, `gstatic.com`).

## Help and bugs

Open an [issue](https://github.com/techniixdotcom/niixarch-install/issues) or use the contact form on [niixa.org](https://niixa.org/#contact). Including your CPU, GPU and whether it's a laptop or desktop helps a lot.

## License

[GPL-3.0](LICENSE)
