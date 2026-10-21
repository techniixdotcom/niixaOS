#!/usr/bin/env bash
# shellcheck disable=SC2034
# archiso profile of the NiiX Arch live ISO (see build/in-container.sh).
# file_permissions is appended by the build: git keeps no owners, and only
# keeps exec bits on some systems, so they are set from the paths.

iso_name="niixaos"
iso_label="NIIXAOS_$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y%m)"
iso_publisher="NiiX <https://niixa.org>"
iso_application="NiiX Arch live system and installer"
iso_version="$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y.%m.%d)"
install_dir="niix"
buildmodes=('iso')
bootmodes=('uefi.systemd-boot')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'zstd' '-Xcompression-level' '19' '-b' '1M')
