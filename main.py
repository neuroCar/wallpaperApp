import os, platform, subprocess

osName = platform.system()

def detectDE(file):
    de = os.environ["XDG_CURRENT_DESKTOP"]
    
    match de:
        case "GNOME":
            theme = subprocess.run("gsettings get org.gnome.desktop.interface color-scheme".split(), capture_output=True, text=True)
            print(theme.stdout)
            if theme.stdout.strip() == '\'prefer-dark\'':
                cmd = f"gsettings set org.gnome.desktop.background picture-uri-dark file://{file}"
            else:
                cmd = f"gsettings set org.gnome.desktop.background picture-uri file://{file}"
        case "Hyprland" | "sway" | "niri":
            cmd = f"awww img {file}"

        case "i3":
            cmd = f"feh --bg-scale {file}"

        case "KDE":
            cmd = f"plasma-apply-wallpaperimage {file}"

    print(f"DE: {de}\nCommand: {cmd}")
    return cmd

def changePaper():
    file = "/home/neuro/Downloads/FrierenWallpaper.jpeg"
    if osName == "Windows":
        print("Running on Windows")
        # Windows-specific code
    elif osName == "Linux":
        print("Running on Linux")
        cmd = detectDE(file)
    elif osName == "Darwin":
        print("Running on macOS")
        cmd = f"osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file ${file}'"
    else:
        print(f"Running on an unidentified system: {osName}")

    subprocess.run(cmd.split())

changePaper()