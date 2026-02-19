"""
Documentation used:
    * https://doc.qt.io/qtforpython-6.5/PySide6/QtWidgets/
    * https://www.tutorialspoint.com/pyqt/index.htm

Wallpapers from:
    * r/wallpapers
    * https://github.com/D3Ext/aesthetic-wallpapers
    * https://microsoft.design/wallpapers/
"""
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os, subprocess, platform

# === Initialize important variables ===
osName = platform.system()
defWallpapers = os.listdir("./wallpapers")
idx = defWallpapers.index("fox.png")

# === Functions ===
def openFile(): # Allows user to select a file for the wallpaper
    fileDialog = QFileDialog(window)
    fileDialog.setWindowTitle("Select File")
    fileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    fileDialog.setViewMode(QFileDialog.ViewMode.Detail)
    fileDialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.webp)")

    if fileDialog.exec():
        file = fileDialog.selectedFiles()
        print("Selected Wallpaper:", file[0])
        changePaper(file[0])

def detectDE(file): # Detects desktop environments on Linux
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

def winPaper(file): # Windows custom wallpaper function
    import ctypes
    from PIL import Image

    # file = os.path.abspath(file)
    img = Image.open(file)
    if img.mode != 'RGB': img = img.convert("RGB")

    img.save("img.bmp", 'BMP')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("img.bmp"), 3)

    os.remove("img.bmp")

def changePaper(file): # Main wallpaper function
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

def change(dir: str): # Changes displayed wallpaper in the app
    global idx
    if dir == "back": idx -= 1
    if dir == "next": idx += 1
    wallpaper.setPixmap(QPixmap(f"wallpapers/{defWallpapers[idx]}").scaled(wallpaper.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

# === Initialize app and window ===
app = QApplication([])
window = QWidget()
window.setWindowTitle("Test2")
window.setGeometry(0, 0, 1024, 512)

# === Setup app layout ===
mainLay = QVBoxLayout()
secLay = QHBoxLayout()

# === Create Widgets ===
wallpaper = QLabel()
wallpaper.setFixedSize(1024, 512)
wallpaper.setPixmap(QPixmap(f"wallpapers/{defWallpapers[idx]}").scaled(wallpaper.size()))

backBtn = QPushButton("<- Previous")
backBtn.clicked.connect(lambda: change("back"))

selectBtn = QPushButton("Select")
selectBtn.clicked.connect(lambda: changePaper(f"wallpapers/{defWallpapers[idx]}"))

fileBtn = QPushButton("Open File")
fileBtn.clicked.connect(openFile)

nextBtn = QPushButton("Next ->")
nextBtn.clicked.connect(lambda: change("next"))

# === Add widgets to the screen ===
window.setLayout(mainLay)
mainLay.addWidget(wallpaper)
secLay.addWidget(backBtn)
secLay.addWidget(selectBtn)
secLay.addWidget(fileBtn)
secLay.addWidget(nextBtn)
mainLay.addLayout(secLay)

window.show()
app.exec()