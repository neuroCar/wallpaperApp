from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os, subprocess, platform

osName = platform.system()

def openFile():
    fileDialog = QFileDialog(window)
    fileDialog.setWindowTitle("Select File")
    fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    fileDialog.setViewMode(QFileDialog.ViewMode.Detail)
    fileDialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.webp)")

    if fileDialog.exec():
        file = fileDialog.selectedFiles()
        print("Selected Wallpaper:", file[0])
        return file[0]

def detectDE(file):
    de = os.environ["XDG_CURRENT_DESKTOP"]
    
    match de:
        case "GNOME":
            theme = subprocess.run("gsettings get org.gnome.desktop.interface color-scheme".split(), capture_output=True, text=True)
            print(theme.stdout)
            if theme.stdout.strip() == '\'prefer-dark\'':
                cmd = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", f'file://{file}']
            else:
                cmd = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f'file://{file}']
        case "Hyprland" | "sway" | "niri":
            cmd = ["awww", "img" f"{file}"]

        case "i3":
            cmd = ["feh", "--bg-scale", f"{file}"]

        case "KDE":
            cmd = ["plasma-apply-wallpaperimage", f"{file}"]

    print(f"DE: {de}\nCommand: {cmd}")
    return cmd

def winPaper(file):
    import ctypes
    from PIL import Image

    # file = os.path.abspath(file)
    img = Image.open(file)
    if img.mode != 'RGB': img = img.convert("RGB")

    img.save("img.bmp", 'BMP')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("img.bmp"), 3)

    os.remove("img.bmp")

def changePaper():
    # file = "/home/neuro/Downloads/FrierenWallpaper.jpeg"
    # file = "c:/Users/n2194/Downloads/FrierenWallpaper.jpg"
    file = openFile()
    file = os.path.abspath(file)
    if osName == "Windows":
        print("Running on Windows")
        winPaper(file)
        return
    elif osName == "Linux":
        print("Running on Linux")
        cmd = detectDE(file)
    # elif osName == "Darwin":
    #     print("Running on macOS")
    #     cmd = ["osascript", "-e", "'tell application \"Finder\" to set desktop picture to POSIX file'", f"'{file}'"
    else:
        print(f"System is not supported: {osName}\n\nIf you know how to add your system, feel free to contribute.")

    subprocess.run(cmd)

app = QApplication([])
window = QMainWindow()
window.setWindowTitle("Test2")
window.setGeometry(0, 0, 1024, 512)

btn = QPushButton("Open File", window)
btn.clicked.connect(changePaper)

window.show()
app.exec()