#!/usr/bin/env bash
#
# Install the "US AltGr Intl No Dead Keys" keyboard layout.
#
# Usage: scripts/install.sh [--system]
#
# Installs into ~/Library/Keyboard Layouts, or into /Library/Keyboard Layouts
# with --system (requires sudo). Input source settings are left untouched.

set -euo pipefail

NAME="US AltGr Intl No Dead Keys"
BUNDLE="$NAME.bundle"
MIN_MACOS=26

usage() {
  cat <<EOF
Usage: $(basename "$0") [--system]

Install the "$NAME" keyboard layout.

  --system    install for all users in /Library/Keyboard Layouts (uses sudo)
  -h, --help  show this help
EOF
}

system=false
for arg in "$@"; do
  case "$arg" in
    --system) system=true ;;
    -h | --help) usage; exit 0 ;;
    *) echo "Error: unknown option: $arg" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "Error: this layout can only be installed on macOS." >&2
  exit 1
fi

version="$(sw_vers -productVersion)"
if (( ${version%%.*} < MIN_MACOS )); then
  echo "Warning: macOS $version is not supported. This layout is designed for macOS $MIN_MACOS and later; installing anyway." >&2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_bundle="$repo_root/$BUNDLE"
if [[ ! -d "$source_bundle" ]]; then
  echo "Error: $source_bundle not found." >&2
  exit 1
fi

if $system; then
  target_dir="/Library/Keyboard Layouts"
else
  target_dir="$HOME/Library/Keyboard Layouts"
fi

# Run a file operation in the target directory, with sudo for --system.
run() {
  if $system; then sudo "$@"; else "$@"; fi
}

target="$target_dir/$BUNDLE"
staging="$target_dir/.$BUNDLE.installing"
previous="$target_dir/.$BUNDLE.previous"

cleanup() {
  run rm -rf "$staging" "$previous"
}
trap cleanup EXIT

# Copy to a staging name first, then swap it into place, so a failed copy
# never leaves a half-installed bundle.
run mkdir -p "$target_dir"
run rm -rf "$staging" "$previous"
run cp -R "$source_bundle" "$staging"
if [[ -e "$target" ]]; then
  run mv "$target" "$previous"
fi
run mv "$staging" "$target"

# Drop cached icons.
run touch "$target"
killall TextInputMenuAgent 2>/dev/null || true

cat <<EOF

Installed "$NAME" in $target_dir.

Next steps:
  1. Log out and log back in. macOS only registers new layouts at login.
  2. Open System Settings > Keyboard > Input Sources > Edit, click "+",
     choose English and add "$NAME".
EOF
