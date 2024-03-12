import shutil
import os

BASE = os.path.join("..", "..")
NEW_BASE = "build"
ACTIVATE_VENV = os.path.join(BASE, "venv", "Scripts", "activate")
EXE_DIR = "executable"
ICON_PATH = os.path.join("img", "shogi_eye.ico")
EXE_NAME = "ShogiVision"

if os.path.exists(NEW_BASE):
    shutil.rmtree(NEW_BASE)

os.makedirs(NEW_BASE, exist_ok=True)
os.makedirs(EXE_DIR, exist_ok=True)

EXCLUDE_COPY = ["temp", "tools", "README.md", "requirements_deploy.txt", ".idea", ".git",
                "requirements_linux.txt", "requirements_windows.txt", "create_models.py", ".gitignore", "venv"]
REMOVE_DUNDER = [
    os.path.join("GUI", "components"),
    os.path.join("GUI", "workers"),
    os.path.join("GUI", "views"),
]


for file_name in os.listdir(BASE):
    old_path = os.path.join(BASE, file_name)
    new_path = os.path.join(NEW_BASE, file_name)
    if file_name in EXCLUDE_COPY:
        continue
    if os.path.isdir(old_path):
        shutil.copytree(old_path, new_path)
    else:
        shutil.copy(old_path, new_path)

# removing double underscores in modules because somehow they break exe from nuitka
for dir_path in REMOVE_DUNDER:
    new_dir_path = os.path.join(NEW_BASE, dir_path)
    for file_name in os.listdir(new_dir_path):
        file_path = os.path.join(new_dir_path, file_name)
        if not os.path.isfile(file_path):
            continue
        with open(file_path, "r") as f:
            code = f.read()
        code = code.replace("__init__", "😎")
        code = code.replace("__", "")
        code = code.replace("😎", "__init__")
        with open(file_path, "w") as f:
            f.write(code)


shutil.copy("main.py", os.path.join(NEW_BASE, "main.py"))

nuitka_cmd = f"cd {NEW_BASE} && nuitka --standalone main.py --show-progress --enable-plugin=pyqt5 --disable-console --windows-icon-from-ico={ICON_PATH} --output-filename={EXE_NAME}.exe --output-dir={EXE_DIR} --include-data-files=models/model.onnx=models/model.onnx --include-data-files=config.ini=config.ini --include-data-dir=img=img"

os.system(f"start cmd /k \"{ACTIVATE_VENV} && {nuitka_cmd}\"")

