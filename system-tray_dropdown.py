#!/usr/bin/env python3
import gi
import subprocess
import os
import json

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

DISPLAYS = CONFIG.get("displays", {})
monitors = list(DISPLAYS.keys())

def display_label(monitor):
    return DISPLAYS.get(monitor, monitor)

def run_layout(profile):
    layouts = CONFIG["layouts"]

    if profile not in layouts:
        print(f"Invalid profile: {profile}")
        return

    layout_cmds = layouts[profile]
    cmd = ["xrandr"]

    for idx, flags in enumerate(layout_cmds):
        monitor = monitors[idx]
        resolved_flags = []
        for flag in flags:
            if flag.startswith("{") and flag.endswith("}"):
                try:
                    ref_index = int(flag.strip("{}"))
                    resolved_flags.append(monitors[ref_index])
                except (ValueError, IndexError):
                    resolved_flags.append(flag)
            else:
                resolved_flags.append(flag)
        cmd.extend(["--output", monitor] + resolved_flags)

    subprocess.run(cmd)

    # Only restart x11vnc if currently running
    result = subprocess.run(["pgrep", "x11vnc"], stdout=subprocess.PIPE)
    if result.stdout:
        subprocess.run(["pkill", "x11vnc"])
        subprocess.Popen(
            ["nohup", "x11vnc", "-usepw", "-forever", "-display", ":0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def make_label(profile):
    layout = CONFIG["layouts"][profile]

    active_monitors = []
    for idx, flags in enumerate(layout):
        if "--off" not in flags:
            monitor_name = monitors[idx]
            active_monitors.append(display_label(monitor_name))

    if not active_monitors:
        return f"Layout {profile} (No active monitors)"

    names = ", ".join(active_monitors)
    return f"Layout {profile} ({names})"

def menu():
    menu = Gtk.Menu()
    for key in sorted(CONFIG["layouts"].keys(), key=int):
        label = make_label(key)
        item = Gtk.MenuItem(label=label)
        item.connect('activate', lambda _, c=key: run_layout(c))
        menu.append(item)
    menu.show_all()
    return menu

def main():
    indicator = AppIndicator3.Indicator.new(
        "screen-switcher",
        "video-display",
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu())
    Gtk.main()

if __name__ == "__main__":
    main()
