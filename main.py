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
from PySide6.QtCore import Qt, QTimer
import os, subprocess, platform
import random as rand

# === Initialize important variables ===
osName = platform.system()
defWallpapers = os.listdir("./wallpapers/")
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
            cmd = ["awww", "img", f"{file}"]

        case "i3":
            cmd = ["feh", "--bg-scale", f"{file}"]

        case "KDE":
            cmd = ["plasma-apply-wallpaperimage", f"{file}"]

    print(f"DE: {de}\nCommand: {cmd}")
    return cmd

def winPaper(file): # Windows custom wallpaper function
    import ctypes, shutil
    from PIL import Image

    APPDATA = os.getenv("APPDATA")
    dest = os.path.join(APPDATA, 'wallpaper')
    os.makedirs(dest, exist_ok=True)

    # file = os.path.abspath(file)
    img = Image.open(file)
    if img.mode != 'RGB': img = img.convert("RGB")
    img.save("img.bmp", 'BMP')
    if (os.path.isfile(dest + '/img.bmp')):
        os.remove(f'{dest}/img.bmp')
    shutil.move('img.bmp', dest)

    
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(dest + "/img.bmp"), 3)

def changePaper(file): # Main wallpaper function
    file = os.path.abspath(file)
    if osName == "Windows":
        # print("Running on Windows")
        winPaper(file)
        return
    elif osName == "Linux":
        # print("Running on Linux")
        cmd = detectDE(file)
    # elif osName == "Darwin":
    #     print("Running on macOS")
    #     cmd = ["osascript", "-e", "'tell application \"Finder\" to set desktop picture to POSIX file'", f"'{file}'"
    else:
        print(f"System is not supported: {osName}\n\nIf you know how to add your system, feel free to contribute.")

    subprocess.run(cmd)

def change(dir: str): # Changes displayed wallpaper in the app
    global idx
    if dir == "back":
        if idx == 0: idx = len(defWallpapers)
        idx -= 1
    if dir == "next":
        if idx == len(defWallpapers): idx = 0 
        idx += 1
    if dir == "rand": idx = rand.randint(0, len(defWallpapers)-1)
    wallpaper.setPixmap(QPixmap(f"wallpapers/{defWallpapers[idx]}").scaled(wallpaper.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

def slideshow():
    if slideshowToggle.isChecked():
        change("rand") if randToggle.isChecked() else change("next")
        changePaper(f"wallpapers/{defWallpapers[idx]}")
    else:
        timer.stop()

# === Initialize app and window ===
app = QApplication([])
window = QWidget()
window.setWindowTitle("Test2")
window.setGeometry(0, 0, 512, 256)

# === Setup app layout ===
mainLay = QVBoxLayout()
secLay = QHBoxLayout()
thirdLay = QHBoxLayout()

# === Create Widgets ===
timer = QTimer()
timer.timeout.connect(slideshow)

wallpaper = QLabel()
wallpaper.setFixedSize(512, 256)
wallpaper.setPixmap(QPixmap(f"wallpapers/{defWallpapers[idx]}").scaled(wallpaper.size()))

backBtn = QPushButton("<- Previous")
backBtn.clicked.connect(lambda: change("back"))
backBtn.setFixedWidth(100)

randBtn = QPushButton("Random 🎲")
randBtn.clicked.connect(lambda: change("rand"))
randBtn.setFixedWidth(100)

selectBtn = QPushButton("Select")
selectBtn.clicked.connect(lambda: changePaper(f"wallpapers/{defWallpapers[idx]}"))
selectBtn.setFixedWidth(100)

fileBtn = QPushButton("Open File")
fileBtn.clicked.connect(openFile)
fileBtn.setFixedWidth(100)

nextBtn = QPushButton("Next ->")
nextBtn.clicked.connect(lambda: change("next"))
nextBtn.setFixedWidth(100)

slideshowToggle = QCheckBox("Enable Slideshow")
slideshowToggle.setChecked(False)
slideshowToggle.toggled.connect(lambda: timer.start(60000))
slideshowToggle.setFixedWidth(110)

randToggle = QCheckBox("Enable Random For Slideshow")
randToggle.setChecked(True)
randToggle.setFixedWidth(105)

timeSpinbox = QSpinBox()
timeSpinbox.setRange(1, 240)
timeSpinbox.setValue(1)
timeSpinbox.setSuffix(" Minutes")
timeSpinbox.valueChanged.connect(lambda val: timer.setInterval(val * 60000))
timeSpinbox.setFixedWidth(100)

spinLabel = QLabel("Time between changes in slideshow")
spinLabel.setFixedWidth(125)

# === Add widgets to the screen ===
window.setLayout(mainLay)
mainLay.addWidget(wallpaper)

secLay.addWidget(backBtn)
secLay.addWidget(randBtn)
secLay.addWidget(selectBtn)
secLay.addWidget(fileBtn)
secLay.addWidget(nextBtn)

thirdLay.addWidget(slideshowToggle)
thirdLay.addWidget(randToggle)
thirdLay.addWidget(timeSpinbox)
thirdLay.addWidget(spinLabel)

mainLay.addLayout(secLay)
mainLay.addLayout(thirdLay)

window.show()
app.exec()
