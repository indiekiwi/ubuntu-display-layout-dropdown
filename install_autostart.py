#!/bin/bash

APP_NAME="System Tray Desktop Layout Switcher"
APP_DESC="Switch monitor layouts from a System Tray dropdown on Ubuntu"
AUTOSTART_DIR="$HOME/.config/autostart"
SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/system-tray_dropdown.py"
FILE_NAME="${APP_NAME,,}"
FILE_NAME="${FILE_NAME// /_}.desktop"
AUTOSTART_FILE="$AUTOSTART_DIR/$FILE_NAME"

echo "Choose an option:"
echo "1) Install"
echo "2) Uninstall"
read -rp "Enter choice [1 or 2]: " choice

case $choice in
  1)
    mkdir -p "$AUTOSTART_DIR"
    cat > "$AUTOSTART_FILE" <<EOF
[Desktop Entry]
Type=Application
Exec=$SCRIPT_PATH
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=$APP_NAME
Comment=$APP_DESC
EOF
    echo "Installed autostart entry at $AUTOSTART_FILE"
    ;;
  2)
    if [ -f "$AUTOSTART_FILE" ]; then
      rm "$AUTOSTART_FILE"
      echo "Uninstalled autostart entry at $AUTOSTART_FILE"
    else
      echo "No autostart entry found to uninstall."
    fi
    ;;
  *)
    echo "Invalid choice. Exiting."
    ;;
esac
