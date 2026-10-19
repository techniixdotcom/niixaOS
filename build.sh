#!/usr/bin/env bash
# Builds the NiiX Arch ISO on any x86_64 Linux machine:
#
#   sudo ./build.sh [--split]
#
# Everything happens in a throwaway Arch Linux container (podman, or docker),
# so this machine is not changed - except that podman is installed if neither
# is present. Needs ~40 GB free next to this file and an internet connection;
# takes 30-90 minutes.
#
#   out/niixaos-YYYY.MM.DD-x86_64.iso (+ .sha256)   the ISO
#   out/build-*.log                                 everything, with timestamps
#   out/build-*.errors.log                          only the lines that look like errors
#   out/build-latest.log                            -> the newest log
#   cache/                                          downloaded packages: the next
#                                                   build is much faster (safe to delete)
#
# Follow a running build from another terminal:  tail -f out/build-latest.log
set -Eeuo pipefail

IMAGE=docker.io/archlinux/archlinux:latest
LOCAL_IMAGE=niix-builder:latest    # made here when the registry can't be reached
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
MIN_FREE_GB=${NIIX_MIN_FREE_GB:-40}

[[ "$(uname -m)" == x86_64 ]] || { echo "ERROR: build on an x86_64 machine." >&2; exit 1; }
[[ $EUID -eq 0 ]] || exec sudo -E bash "$0" "$@"

mkdir -p "$HERE/out" "$HERE/cache"
STAMP=$(date +%Y%m%d-%H%M%S)
LOG=$HERE/out/build-$STAMP.log
ERRLOG=$HERE/out/build-$STAMP.errors.log
STEPFILE=$(mktemp)
: > "$LOG"; : > "$ERRLOG"
ln -sfn "$(basename "$LOG")" "$HERE/out/build-latest.log"
trap 'rm -f "$STEPFILE"' EXIT

if [[ -t 1 ]]; then
    C_ERR=$'\033[1;38;5;203m'; C_WARN=$'\033[38;5;215m'; C_STEP=$'\033[1;38;5;205m'
    C_OK=$'\033[38;5;118m'; C_DIM=$'\033[2m'; C_OFF=$'\033[0m'
else
    C_ERR=""; C_WARN=""; C_STEP=""; C_OK=""; C_DIM=""; C_OFF=""
fi

# Lines that look like a problem. Compiler flags and option names that only
# contain the word are left out.
ERR_RE='(^|[^a-z_-])(error|fatal|failed|failure|cannot|could not|unable to|no such host|timed out|timeout|permission denied|not found|corrupted|invalid)([^a-z_]|$)'
ANSI_RE=$'\033''\[[0-9;?]*[A-Za-z]'
NOISE_RE='(-werror|error\.(h|c|o)|errors=|0 errors|error_|_error|warning: )'

# logfilter : every line of the build goes through here as it happens -
# timestamped into the log, coloured on screen, and error-looking lines also
# into the errors log, with the step they happened in.
logfilter() {
    local line plain lower step
    exec 3>>"$LOG" 4>>"$ERRLOG"
    while IFS= read -r line || [[ -n "$line" ]]; do
        line=${line//$'\r'/}
        plain=$line
        while [[ "$plain" =~ $ANSI_RE ]]; do plain=${plain/"${BASH_REMATCH[0]}"/}; done
        printf '[%(%H:%M:%S)T] %s\n' -1 "$plain" >&3
        lower=${plain,,}
        if [[ "$plain" =~ ^==\>\ \[[0-9]+/[0-9]+\] ]]; then
            printf '%s\n' "$plain" > "$STEPFILE"
            printf '%s%s%s\n' "$C_STEP" "$plain" "$C_OFF"
        elif [[ "$lower" =~ $ERR_RE && ! "$lower" =~ $NOISE_RE ]]; then
            step=$(cat "$STEPFILE" 2>/dev/null)
            printf '[%(%H:%M:%S)T] %s | %s\n' -1 "${step:-==> setup}" "$plain" >&4
            printf '%s%s%s\n' "$C_ERR" "$plain" "$C_OFF"
        elif [[ "$lower" == warning:* || "$lower" == *" ! "* || "$lower" == "  !"* ]]; then
            printf '%s%s%s\n' "$C_WARN" "$plain" "$C_OFF"
        else
            printf '%s\n' "$line"
        fi
    done
}

# run CMD... : the command, its output through logfilter; returns its status.
run() {
    "$@" 2>&1 | logfilter
    return "${PIPESTATUS[0]}"
}

say()  { printf '==> %s\n' "$*" | logfilter; }
hstep() { printf '==> [host] %s\n' "$*" > "$STEPFILE"; printf '\n%s==> %s%s\n' "$C_STEP" "$*" "$C_OFF"; printf '[%(%H:%M:%S)T] ==> [host] %s\n' -1 "$*" >> "$LOG"; }

# failed MESSAGE : where it went wrong, the error lines, where the logs are.
failed() {
    local step n
    step=$(cat "$STEPFILE" 2>/dev/null)
    n=$(wc -l < "$ERRLOG")
    {
        printf '\n%s==================== BUILD FAILED ====================%s\n' "$C_ERR" "$C_OFF"
        printf '%sWhat:%s %s\n' "$C_ERR" "$C_OFF" "$1"
        [[ -n "$step" ]] && printf '%sStep:%s %s\n' "$C_ERR" "$C_OFF" "${step#==> }"
        if (( n )); then
            printf '\nThe last of %d lines that look like errors:\n' "$n"
            tail -n 15 "$ERRLOG" | sed "s/^/  /"
        fi
        printf '\n%sFull log:%s    %s\n' "$C_DIM" "$C_OFF" "$LOG"
        printf '%sErrors only:%s %s\n' "$C_DIM" "$C_OFF" "$ERRLOG"
        printf 'Search the full log with:  grep -n -i -B5 "error" %s\n' "${LOG#"$PWD"/}"
    } | tee -a "$LOG" >&2
    [[ -n "${SUDO_UID:-}" ]] && chown -R "$SUDO_UID:${SUDO_GID:-$SUDO_UID}" "$HERE/out"
    exit 1
}
trap 'failed "build.sh stopped at line $LINENO: $BASH_COMMAND"' ERR
trap 'echo; failed "interrupted (Ctrl+C)"' INT

# -- This machine ---------------------------------------------------------------
hstep "Checking this machine"
{
    echo "build.sh started $(date)"
    echo "host: $(. /etc/os-release 2>/dev/null; echo "${PRETTY_NAME:-unknown}"), kernel $(uname -r)"
    echo "cpu: $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs)"
    echo "free space: $(df -h --output=avail "$HERE" | tail -1 | xargs), args: ${*:-none}"
} | logfilter

free_gb=$(( $(df -Pk "$HERE" | awk 'NR == 2 {print $4}') / 1048576 ))
(( free_gb >= MIN_FREE_GB )) || failed "only ${free_gb} GB free here - the build needs about ${MIN_FREE_GB} GB"
getent hosts geo.mirror.pkgbuild.com >/dev/null || failed "no internet (or no DNS) - cannot look up the Arch mirrors"

if command -v podman >/dev/null; then engine=podman
elif command -v docker >/dev/null; then engine=docker
else
    say "Installing podman..."
    if   command -v pacman  >/dev/null; then run pacman -Sy --noconfirm --needed podman
    elif command -v apt-get >/dev/null; then run apt-get update && run apt-get install -y podman
    elif command -v dnf     >/dev/null; then run dnf install -y podman
    elif command -v zypper  >/dev/null; then run zypper --non-interactive install podman
    else failed "no podman or docker, and no known package manager to install podman"; fi
    engine=podman
fi
say "Container engine: $engine ($("$engine" --version 2>/dev/null | head -1))"

# -- The build image ---------------------------------------------------------------
# Arch's official image from Docker Hub. If the registry can't be reached
# (blocked, rate-limited, DNS trouble), one is made here instead - from this
# machine's pacman (pacstrap) or Arch's bootstrap tarball from the mirrors.
image_present() { "$engine" image inspect "$1" >/dev/null 2>&1; }

pull_image() {
    local n
    for n in 1 2 3; do
        run "$engine" pull "$IMAGE" && return 0
        (( n < 3 )) && { say "  ! pull attempt $n failed - retrying in 10s"; sleep 10; }
    done
    return 1
}

make_local_image() {
    local root tmp list name
    tmp=$(mktemp -d -p "$HERE/cache" bootstrap.XXXXXX)
    root=$tmp/root
    if command -v pacstrap >/dev/null; then
        say "Making the build image with pacstrap (this machine's mirrors and keys)..."
        mkdir -p "$root"
        run pacstrap -c -K "$root" base || { rm -rf "$tmp"; return 1; }
    else
        say "Making the build image from Arch's bootstrap tarball..."
        list=$(curl -fsSL --retry 3 https://geo.mirror.pkgbuild.com/iso/latest/sha256sums.txt) || { rm -rf "$tmp"; return 1; }
        name=archlinux-bootstrap-x86_64.tar.zst
        run curl -fL --retry 3 -o "$tmp/$name" "https://geo.mirror.pkgbuild.com/iso/latest/$name" || { rm -rf "$tmp"; return 1; }
        (cd "$tmp" && grep " $name\$" <<< "$list" | sha256sum -c -) 2>&1 | logfilter
        (( PIPESTATUS[0] == 0 )) || { rm -rf "$tmp"; say "  ! bootstrap checksum mismatch"; return 1; }
        run tar --zstd -xpf "$tmp/$name" -C "$tmp" || { rm -rf "$tmp"; return 1; }
        mv "$tmp/root.x86_64" "$root"
    fi
    # Mirrors for the container (the build ranks them again).
    printf 'Server = https://geo.mirror.pkgbuild.com/$repo/os/$arch\n' > "$root/etc/pacman.d/mirrorlist"
    tar -C "$root" -c . | "$engine" import - "$LOCAL_IMAGE" 2>&1 | logfilter
    local rc=${PIPESTATUS[1]}
    rm -rf "$tmp"
    return "$rc"
}

hstep "Getting the Arch Linux build image"
if pull_image; then
    BUILD_IMAGE=$IMAGE
elif image_present "$IMAGE"; then
    say "  ! Docker Hub unreachable - using the Arch image already on this machine (the build updates it)"
    BUILD_IMAGE=$IMAGE
elif image_present "$LOCAL_IMAGE"; then
    say "  ! Docker Hub unreachable - using the build image made here earlier (the build updates it)"
    BUILD_IMAGE=$LOCAL_IMAGE
else
    say "  ! Docker Hub unreachable - making the build image locally instead"
    make_local_image || failed "could not get an Arch Linux build image: Docker Hub is unreachable and making one locally failed"
    BUILD_IMAGE=$LOCAL_IMAGE
fi
say "Build image: $BUILD_IMAGE"

# -- The build ----------------------------------------------------------------------
hstep "Building in the container - follow it from another terminal: tail -f out/build-latest.log"
# --privileged     mkarchiso mounts /proc etc. inside the image it builds
# --network host   the host's network and DNS as they are (container DNS is
#                  broken on many setups: local resolvers, VPNs)
# --pids-limit -1  pacstrap leaves a gpg helper per signature check behind;
#                  with podman's default limit the last packages fail to verify
# nofile           with the huge default some engines set, fakeroot crawls
start=$SECONDS
if ! run "$engine" run --rm --privileged --network host --pids-limit -1 --ulimit nofile=1024:524288 \
        -e NIIX_IN_CONTAINER=1 -e NIIX_VERSION -e GITHUB_TOKEN \
        -v "$HERE:/build:Z" -v "$HERE/cache:/var/cache/pacman/pkg:Z" -w /build \
        "$BUILD_IMAGE" bash /build/build/in-container.sh "$@"; then
    failed "the build inside the container stopped"
fi
took=$(( SECONDS - start ))

[[ -n "${SUDO_UID:-}" ]] && chown -R "$SUDO_UID:${SUDO_GID:-$SUDO_UID}" "$HERE/out"
printf '\n%s==> Done in %dm %02ds%s\n' "$C_OK" $(( took / 60 )) $(( took % 60 )) "$C_OFF"
for iso in "$HERE"/out/*.iso; do [[ -f "$iso" ]] && printf '    %s\n' "$iso"; done
n=$(wc -l < "$ERRLOG")
(( n == 0 )) || printf '%s    %d lines looked like errors but did not stop the build - see %s%s\n' "$C_DIM" "$n" "$ERRLOG" "$C_OFF"
