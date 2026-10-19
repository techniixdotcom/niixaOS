#!/usr/bin/env bash
# Builds the NiiX Arch ISO. Runs inside a throwaway Arch Linux container -
# started by ../build.sh on any Linux machine, or directly by GitHub Actions.
# It changes the container's pacman setup, so it refuses to run elsewhere.
#
#   build/in-container.sh [--split]
#
#   --split   also put release files in out/release/: the ISO, or - when it is
#             bigger than GitHub's 2 GiB file limit - parts to join with cat
#
# Environment:
#   NIIX_VERSION   version shown in the ISO (default: git describe, else the date)
#   GITHUB_TOKEN   optional - raises the GitHub API limit for the GE-Proton lookup
#
# Output in out/: niixaos-YYYY.MM.DD-x86_64.iso and its .sha256 (+ release/ with --split)
set -Eeuo pipefail

REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
WORK=$REPO/work
STAGE=$WORK/profile
AIROOT=$STAGE/airootfs
LOCALREPO=$WORK/localrepo
OUT=$REPO/out
SPLIT=false
[[ "${1:-}" == --split ]] && SPLIT=true

WALLPAPER_URL="https://niixa.org/niix-background.png"
LOGO_URL="https://raw.githubusercontent.com/techniixdotcom/niixarch-install/main/niixarch-logo.png"
CACHYOS_KEY="882DCFE48E2051D48E2562ABF3B607488DB35A47"   # as published on wiki.cachyos.org
# shellcheck disable=SC2016  # $arch/$repo are pacman's
CACHYOS_SERVER='https://mirror.cachyos.org/repo/$arch/$repo'
# Shell extensions without an Arch package: the build for this GNOME comes
# from extensions.gnome.org. ding (desktop icons) is for the live session only.
EGO_EXTENSIONS=(tiling-assistant@leleat-on-github screen-rotate@shyzus.github.io ding@rastersoft.com)
PART_SIZE=1900M   # GitHub release assets must stay under 2 GiB

say()  { printf '\033[38;5;118m  ->\033[0m %s\n' "$*"; }
note() { printf '\033[38;5;215m  !\033[0m %s\n' "$*"; }
die()  {
    printf '\033[38;5;203mERROR:\033[0m %s\n' "$*" >&2
    [[ -n "$STEP_NAME" ]] && printf '\033[38;5;203mERROR:\033[0m the build failed in step [%d/%d] %s\n' "$STEP_N" "$STEP_TOTAL" "$STEP_NAME" >&2
    exit 1
}
trap 'die "line $LINENO of build/in-container.sh: $BASH_COMMAND"' ERR

# step TITLE FUNCTION : a numbered build step, timed. ../build.sh picks the
# "==> [n/N]" lines up to say which step a failure happened in.
STEP_N=0; STEP_TOTAL=11; STEP_NAME=""
step() {
    local title=$1 start=$SECONDS took
    shift
    STEP_N=$(( STEP_N + 1 )); STEP_NAME=$title
    printf '\n\033[1;38;5;205m==> [%d/%d] %s\033[0m\n' "$STEP_N" "$STEP_TOTAL" "$title"
    "$@"
    took=$(( SECONDS - start ))
    printf '\033[38;5;118m    done in %dm %02ds\033[0m\n' $(( took / 60 )) $(( took % 60 ))
}

retry() {
    local n
    for n in 1 2 3; do
        "$@" && return 0
        (( n < 3 )) && { note "attempt $n failed - retrying in 15s: $*"; sleep 15; }
    done
    return 1
}

[[ -f /run/.containerenv || -f /.dockerenv || "${NIIX_IN_CONTAINER:-}" == 1 ]] \
    || die "Run this inside the build container: sudo ./build.sh (or the GitHub workflow)."
[[ $EUID -eq 0 ]] || die "Run as root (inside the container)."

# -- The container ------------------------------------------------------------
fetch_key() {
    local server
    for server in hkps://keyserver.ubuntu.com hkps://keys.openpgp.org; do
        "$@" --keyserver "$server" --recv-keys "${KEY:?}" && return 0
    done
    return 1
}

prepare_container() {
    # The ISO is built from CachyOS's x86-64-v3 packages and the build runs
    # some of them (initramfs, DKMS) - this CPU has to run v3 code.
    /lib64/ld-linux-x86-64.so.2 --help | grep -q 'x86-64-v3 (supported, searched)' \
        || die "This CPU can't run x86-64-v3 code - build on a computer with AVX2."
    pacman-key --init
    pacman-key --populate archlinux
    KEY=$CACHYOS_KEY retry fetch_key pacman-key || die "Could not download CachyOS's signing key."
    pacman-key --lsign-key "$CACHYOS_KEY"
    [[ -f /etc/pacman.d/cachyos-mirrorlist ]] || printf 'Server = %s\n' "$CACHYOS_SERVER" > /etc/pacman.d/cachyos-mirrorlist
    grep -q '^\[cachyos\]' /etc/pacman.conf \
        || sed -i '/^\[core\]/i [cachyos]\nInclude = /etc/pacman.d/cachyos-mirrorlist\n' /etc/pacman.conf
    grep -q '^\[multilib\]' /etc/pacman.conf || printf '\n[multilib]\nInclude = /etc/pacman.d/mirrorlist\n' >> /etc/pacman.conf
    sed -i 's/^#\?ParallelDownloads.*/ParallelDownloads = 10/' /etc/pacman.conf
    retry pacman -Syu --noconfirm --needed --overwrite /etc/pacman.d/cachyos-mirrorlist \
        archiso git base-devel sudo curl python libarchive glib2 gtk-update-icon-cache reflector \
        cachyos-keyring cachyos-mirrorlist cachyos-v3-mirrorlist cachyos-v4-mirrorlist
    pacman-key --populate cachyos
    reflector --protocol https --age 12 --latest 25 --fastest 10 --save /etc/pacman.d/mirrorlist \
        || note "reflector failed - using the default mirrors"
    rm -rf "$WORK"
    mkdir -p "$WORK" "$LOCALREPO" "$OUT"
}

# -- Packages -----------------------------------------------------------------
# list FILE : the entries of a package list, comments and blanks dropped.
list() { sed 's/#.*//; s/[[:space:]]//g; /^$/d' "$1"; }

AUR_BASES=(); AUR_PKGS=()
read_aur_list() {
    local line
    local -a names
    while IFS= read -r line; do
        AUR_BASES+=("${line%%=*}")
        if [[ "$line" == *=* ]]; then
            IFS=, read -ra names <<< "${line#*=}"
            AUR_PKGS+=("${names[@]}")
        else
            AUR_PKGS+=("$line")
        fi
    done < <(list "$REPO/packages/aur.txt")
}

build_aur_packages() {
    local pkg key built=0
    id builder &>/dev/null || useradd -m builder
    echo 'builder ALL=(ALL) NOPASSWD: /usr/bin/pacman' > /etc/sudoers.d/builder
    chown builder "$LOCALREPO"
    for pkg in "${AUR_BASES[@]}"; do
        if pacman -Si "$pkg" &>/dev/null; then
            say "$pkg: in the repositories - using that signed build"
            continue
        fi
        say "Building $pkg from the AUR..."
        rm -rf "/home/builder/$pkg"
        retry sudo -u builder git clone --depth 1 "https://aur.archlinux.org/$pkg.git" "/home/builder/$pkg"
        # The keys its sources are signed with (validpgpkeys), so makepkg
        # checks the signatures instead of skipping them.
        for key in $(awk '$1 == "validpgpkeys" { print $3 }' "/home/builder/$pkg/.SRCINFO"); do
            [[ "$key" =~ ^[0-9A-Fa-f]{40}$ ]] || die "Unexpected signing key '$key' in $pkg"
            sudo -u builder gpg --batch --list-keys "$key" &>/dev/null \
                || KEY=$key retry fetch_key sudo -u builder gpg --batch || die "No signing key $key for $pkg"
        done
        retry sudo -u builder env -C "/home/builder/$pkg" makepkg --verifysource --noconfirm
        sudo -u builder env -C "/home/builder/$pkg" PKGDEST="$LOCALREPO" makepkg -s --noconfirm --needed
        built=$(( built + 1 ))
    done
    (( built == 0 )) || repo-add "$LOCALREPO/niix-local.db.tar.gz" "$LOCALREPO"/*.pkg.tar.*
}

write_package_list() {
    local pkg entry
    local -a groups=() skip=() required=() optional=() members=() missing=() pkgs=()
    local -A have=()
    while IFS= read -r entry; do
        case "$entry" in
            '!'*) skip+=("${entry:1}") ;;
            '@'*) groups+=("${entry:1}") ;;
            '?'*) optional+=("${entry:1}") ;;
            *)    required+=("$entry") ;;
        esac
    done < <(list "$REPO/packages/repo.txt")
    mapfile -t -O "${#required[@]}" required < <(list "$REPO/packages/live-only.txt")
    while IFS= read -r pkg; do have[$pkg]=1; done < <(pacman -Slq)

    mapfile -t members < <(pacman -Sgq "${groups[@]}" | grep -vxF -f <(printf '%s\n' "${skip[@]}"))
    (( ${#members[@]} > 10 )) || die "Could not read the package groups: ${groups[*]}"
    for pkg in "${required[@]}"; do
        if [[ -n "${have[$pkg]:-}" ]]; then pkgs+=("$pkg"); else missing+=("$pkg"); fi
    done
    (( ${#missing[@]} == 0 )) || die "Not in the repositories (renamed or removed?): ${missing[*]}"
    for pkg in "${optional[@]}"; do
        if [[ -n "${have[$pkg]:-}" ]]; then pkgs+=("$pkg"); else note "optional, not in the repos now: $pkg"; fi
    done
    printf '%s\n' "${pkgs[@]}" "${members[@]}" "${AUR_PKGS[@]}" | sort -u > "$STAGE/packages.x86_64"
    say "$(wc -l < "$STAGE/packages.x86_64") packages on the ISO"
}

# -- The profile --------------------------------------------------------------
stage_profile() {
    cp -a "$REPO/profile" "$STAGE"
    cp "$AIROOT/usr/local/share/niix/pacman.conf" "$STAGE/pacman.conf"
    if [[ -f "$LOCALREPO/niix-local.db.tar.gz" ]]; then
        printf '\n[niix-local]\nSigLevel = Optional TrustAll\nServer = file://%s\n' "$LOCALREPO" >> "$STAGE/pacman.conf"
    fi
    local version=${NIIX_VERSION:-}
    [[ -n "$version" ]] || version=$(git -C "$REPO" describe --tags --always --dirty 2>/dev/null || date +%Y.%m.%d)
    echo "$version" > "$AIROOT/usr/local/share/niix/version"
    install -m 644 "$REPO/packages/flatpak.txt" "$AIROOT/usr/local/share/niix/flatpak-apps"
    say "Version $version"
}

# asset NAME URL DEST : from assets/ in the repository, else downloaded.
asset() {
    mkdir -p "$(dirname "$3")"
    if [[ -f "$REPO/assets/$1" ]]; then cp "$REPO/assets/$1" "$3"; else retry curl -fsSL "$2" -o "$3"; fi
}

add_branding() {
    asset niixarch-logo.png "$LOGO_URL" "$AIROOT/usr/share/pixmaps/niixarch-logo.png"
    asset niix-background.png "$WALLPAPER_URL" "$AIROOT/usr/share/backgrounds/niix/niix-background.png"
    NIIX_ICON_DEST="$AIROOT/usr/share/icons/NiiX" python3 "$REPO/build/gen-icon-theme.py" >/dev/null
    [[ -f "$AIROOT/usr/share/icons/NiiX/index.theme" ]] || die "The icon theme was not generated."
}

# ext_from_git UUID DEST : the extension from its source repository when
# extensions.gnome.org has no build for this GNOME yet.
ext_from_git() {
    local repo tag="" tmp
    case "$1" in
        screen-rotate@shyzus.github.io)    repo=https://github.com/shyzus/gnome-shell-extension-screen-autorotate.git ;;
        tiling-assistant@leleat-on-github) repo=https://github.com/Leleat/Tiling-Assistant.git; tag=v55 ;;
        *) return 1 ;;
    esac
    tmp=$(mktemp -d)
    git clone --depth 1 ${tag:+--branch "$tag"} "$repo" "$tmp/src" &>/dev/null \
        && [[ -f "$tmp/src/$1/metadata.json" ]] && cp -r "$tmp/src/$1" "$2/"
    local rc=$?
    rm -rf "$tmp"
    return "$rc"
}

ENABLED_EXTENSIONS="'appindicatorsupport@rgcjonas.gmail.com', 'system-monitor@gnome-shell-extensions.gcampax.github.com', 'dash-to-panel@jderose9.github.com', 'arcmenu@arcmenu.com', 'ddterm@amezin.github.com', 'niix-osk@niixa.org'"
add_extensions() {
    local ver uuid meta url dest=$AIROOT/usr/share/gnome-shell/extensions
    ver=$(pacman -Si gnome-shell | sed -n 's/^Version *: *\([0-9]*:\)\{0,1\}\([0-9]*\).*/\2/p' | head -1)
    [[ "$ver" =~ ^[0-9]+$ ]] || die "Could not read the GNOME Shell version."
    say "GNOME Shell $ver extensions..."
    mkdir -p "$dest"
    for uuid in "${EGO_EXTENSIONS[@]}"; do
        meta=$(curl -fsS --retry 3 "https://extensions.gnome.org/extension-info/?uuid=$uuid&shell_version=$ver" || true)
        url=$(python3 -c 'import json, sys
try: print(json.load(sys.stdin).get("download_url") or "")
except ValueError: print("")' <<< "$meta")
        if [[ -n "$url" ]] && retry curl -fsSL "https://extensions.gnome.org$url" -o "$WORK/ext.zip"; then
            mkdir -p "$dest/$uuid"
            bsdtar -xf "$WORK/ext.zip" -C "$dest/$uuid"
        elif ! ext_from_git "$uuid" "$dest"; then
            note "$uuid: no build for GNOME $ver - left out"
            continue
        fi
        [[ -d "$dest/$uuid/schemas" ]] && glib-compile-schemas "$dest/$uuid/schemas"
        echo "    $uuid"
        ENABLED_EXTENSIONS+=", '$uuid'"
    done
}

# The live session's desktop: the installer icon, no screen lock, no suspend.
write_live_dconf() {
    cat > "$AIROOT/etc/dconf/db/local.d/90-niix-live" <<EOF
[org/gnome/shell]
enabled-extensions=[$ENABLED_EXTENSIONS]
favorite-apps=['org.niixa.Installer.desktop', 'org.gnome.Nautilus.desktop', 'helium.desktop', 'steam.desktop', 'org.gnome.Terminal.desktop']

[org/gnome/desktop/screensaver]
lock-enabled=false

[org/gnome/settings-daemon/plugins/power]
sleep-inactive-battery-type='nothing'
sleep-inactive-ac-type='nothing'

[org/gnome/shell/extensions/ding]
show-home=false
show-trash=false
show-volumes=false
EOF
}

# GE-Proton, sha512-checked, where Steam finds tools for every user. The
# checksum comes from the same release, so it proves the download is intact
# (GE-Proton publishes no signatures).
add_ge_proton() {
    local api=https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest
    local -a hdr=(-H "Accept: application/vnd.github+json")
    local json urls tar_url sum_url name dest=$AIROOT/usr/share/steam/compatibilitytools.d
    [[ -n "${GITHUB_TOKEN:-}" ]] && hdr+=(-H "Authorization: Bearer $GITHUB_TOKEN")
    json=$(retry curl -fsSL "${hdr[@]}" "$api") || die "GitHub API unreachable (set GITHUB_TOKEN if rate-limited)."
    urls=$(grep -oE '"browser_download_url": *"[^"]*"' <<< "$json" | cut -d'"' -f4)
    tar_url=$(grep -E 'x86_64\.tar\.gz$' <<< "$urls" | head -1 || true)
    [[ -n "$tar_url" ]] || tar_url=$(grep -E '\.tar\.gz$' <<< "$urls" | grep -viE 'aarch64|arm64' | head -1)
    name=$(basename "$tar_url" .tar.gz)
    sum_url=$(grep -E "/$name\.sha512sum$" <<< "$urls" | head -1)
    [[ -n "$tar_url" && -n "$sum_url" ]] || die "No GE-Proton x86_64 download found in the latest release."
    mkdir -p "$WORK/ge" "$dest"
    retry curl -fsSL -o "$WORK/ge/$name.tar.gz" "$tar_url"
    retry curl -fsSL -o "$WORK/ge/$name.sha512sum" "$sum_url"
    (cd "$WORK/ge" && sha512sum -c "$name.sha512sum") || die "GE-Proton checksum mismatch."
    tar -xzf "$WORK/ge/$name.tar.gz" -C "$dest"
    echo "    $name"
}

# git and some systems lose modes and owners: set them from the paths.
write_permissions() {
    local path
    {
        echo 'file_permissions=('
        echo '  ["/etc/sudoers.d"]="0:0:750"'
        echo '  ["/etc/sudoers.d/10-wheel"]="0:0:440"'
        echo '  ["/etc/sudoers.d/niix-live"]="0:0:440"'
        while IFS= read -r path; do
            printf '  ["/%s"]="0:0:755"\n' "$path"
        done < <(cd "$AIROOT" && {
            find usr/local/bin usr/local/lib/niix usr/local/lib/niix-build etc/NetworkManager/dispatcher.d -type f
            find . -path ./usr/share/steam -prune -o -type f -perm -u+x -printf '%P\n'
            echo usr/local/lib/niix-branding
        } | sed 's|^\./||' | sort -u)
        echo ')'
    } >> "$STAGE/profiledef.sh"
}

# -- The image ----------------------------------------------------------------
build_iso() {
    say "This is the long part - mkarchiso installs ~1500 packages, then compresses the image."
    # A cached package from another repo with the same file name fails its
    # signature check; pacman deletes it and the retry continues the build.
    retry mkarchiso -v -w "$WORK/archiso" -o "$OUT" "$STAGE"
    [[ -f "$WORK/archiso/x86_64/airootfs/var/lib/niix/image-customized" ]] \
        || die "The image was not finished (customize-image failed) - see 'Finishing the NiiX image' above."

    local iso
    iso=$(find "$OUT" -maxdepth 1 -name 'niixaos-*.iso' -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)
    [[ -f "$iso" ]] || die "mkarchiso finished but no ISO is in out/"
    (cd "$OUT" && sha256sum "$(basename "$iso")" > "$(basename "$iso").sha256")
    say "ISO: $iso ($(du -h "$iso" | cut -f1))"
    # out/release: what a GitHub release can carry (files under 2 GiB).
    if $SPLIT; then
        rm -rf "$OUT/release"; mkdir -p "$OUT/release"
        cp "$iso.sha256" "$OUT/release/"
        if (( $(stat -c %s "$iso") > 2000000000 )); then
            split -b "$PART_SIZE" -d -a 2 "$iso" "$OUT/release/$(basename "$iso").part-"
            say "Split into $(find "$OUT/release" -name '*.part-*' | wc -l) parts in out/release/"
        else
            ln "$iso" "$OUT/release/" 2>/dev/null || cp "$iso" "$OUT/release/"
        fi
    fi
    rm -rf "$WORK"
}

read_aur_list
step "Preparing the build container"   prepare_container
step "Building AUR packages"            build_aur_packages
step "Staging the ISO profile"          stage_profile
step "Resolving the package list"       write_package_list
step "Logo, wallpaper and icon theme"   add_branding
step "GNOME Shell extensions"           add_extensions
step "Live session settings"            write_live_dconf
step "GE-Proton"                        add_ge_proton
step "File permissions"                 write_permissions
step "Building the ISO image"           build_iso
step "Done"                             true
