# System Tray Desktop Layout Switcher

This Python script provides a system tray dropdown on Ubuntu to switch monitor layouts using `xrandr` and resets `x11vnc` if it's running.

---

## Prerequisites

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 x11-xserver-utils x11vnc
```
## Setup

### config.json
Get display names `xrandr --query | grep " connected"`

### Installation
Run `./system-tray_dropdown.py` directly or run `./install_autostart.py` to install it to `~/.config/autostart/`
