import os, platform, subprocess
import customtkinter as ctk
from CTkFileDialog import askopenfilename

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

def winPaper(file):
    import ctypes
    from PIL import Image

    file = os.path.abspath(file)
    img = Image.open(file)
    if img.mode != 'RGB': img = img.convert("RGB")

    img.save("img.bmp", 'BMP')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("img.bmp"), 3)

    os.remove("img.bmp")

def changePaper():
    # file = "/home/neuro/Downloads/FrierenWallpaper.jpeg"
    # file = "c:/Users/n2194/Downloads/FrierenWallpaper.jpg"
    file = askopenfilename(preview_img=True, autocomplete=True, filetypes=["png", 'jpeg', 'jpg', 'webp'])
    if osName == "Windows":
        print("Running on Windows")
        winPaper(file)
        return
    elif osName == "Linux":
        print("Running on Linux")
        cmd = detectDE(file)
    elif osName == "Darwin":
        print("Running on macOS")
        cmd = f"osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file {file}'"
    else:
        print(f"Running on an unidentified system: {osName}")

    subprocess.run(cmd.split())

app = ctk.CTk()
app.geometry("512x512")

btn = ctk.CTkButton(app, text="Select BG", command=changePaper)
btn.pack()

app.mainloop()