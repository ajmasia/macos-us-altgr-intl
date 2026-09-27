#!/usr/bin/env bash
#
# Uninstall the "US AltGr Intl No Dead Keys" keyboard layout.
#
# Usage: scripts/uninstall.sh
#
# Removes the bundle from ~/Library/Keyboard Layouts and /Library/Keyboard
# Layouts, whichever contain it. sudo is used only for the /Library copy.
# Input source settings are left untouched.

set -euo pipefail

NAME="US AltGr Intl No Dead Keys"
BUNDLE="$NAME.bundle"

usage() {
  cat <<EOF
Usage: $(basename "$0")

Remove the "$NAME" keyboard layout from ~/Library/Keyboard Layouts and
/Library/Keyboard Layouts.

  -h, --help  show this help
EOF
}

for arg in "$@"; do
  case "$arg" in
    -h | --help) usage; exit 0 ;;
    *) echo "Error: unknown option: $arg" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "Error: this layout can only be uninstalled on macOS." >&2
  exit 1
fi

user_copy="$HOME/Library/Keyboard Layouts/$BUNDLE"
system_copy="/Library/Keyboard Layouts/$BUNDLE"
removed=false

if [[ -e "$user_copy" ]]; then
  rm -rf "$user_copy"
  echo "Removed $user_copy"
  removed=true
fi

if [[ -e "$system_copy" ]]; then
  echo "A system-wide copy exists; administrator privileges are needed to remove it."
  sudo rm -rf "$system_copy"
  echo "Removed $system_copy"
  removed=true
fi

if ! $removed; then
  echo "\"$NAME\" is not installed; nothing to remove."
  exit 0
fi

killall TextInputMenuAgent 2>/dev/null || true

cat <<EOF

Next steps:
  1. If "$NAME" is still listed in System Settings > Keyboard >
     Input Sources, remove it there.
  2. Log out and log back in to clear the system cache.
EOF
