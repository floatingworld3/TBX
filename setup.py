import PyInstaller.__main__
import sys
import os


def write_file(path, data=""):
    with open(path, "w") as f:
        f.write(data)
        f.close()


if __name__ == "__main__":
    tmp_path = "./build/tmp"
    build_path = "./build/dist"
    exe_name = "TxtToFbx"
    separator = ";" if "win" in sys.platform else ":"
    PyInstaller.__main__.run([
        "main.py",
        "--onedir",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--distpath={}".format(build_path),
        "--workpath={}".format(tmp_path),
        "--name={}".format(exe_name),
        "--hidden-import=PIL._tkinter_finder",
        "--icon=./assets/tbx_logo.ico",
        "--add-data=./assets/tbx_logo.ico{}./assets".format(separator),
        "--add-data=./assets/tbx_logo.png{}./assets/".format(separator),
        "--add-data=./assets/arrow.gif{}./assets/".format(separator)
    ])

    desktop_data = "[Desktop Entry]\n" \
                   "Exec={}\n" \
                   "Type=Application\n" \
                   "Name=TBX\n" \
                   "Icon=tbx_logo\n" \
                   "Terminal=false\n" \
                   "Categories=Utility;".format(exe_name)
    app_run_data = '#!/bin/sh\n' \
                   'SELF=$(readlink -f "$0")\n' \
                   'HERE=${SELF%/*}\n' \
                   '#export PATH="${HERE}/TxtToFbx/${PATH:+:$PATH}"\n' \
                   'cd "${HERE}/TxtToFbx/"\n' \
                   'EXEC=$(grep -e "^Exec=.*" "${HERE}"/*.desktop | head -n 1 | cut -d "=" -f 2 | cut -d " " -f 1)\n' \
                   'exec "./${EXEC}" "$@"'
    if "linux" in sys.platform:
        write_file(build_path + "/test.desktop", data=desktop_data)
        write_file(build_path + "/AppRun", data=app_run_data)
        os.system("chmod +x {}'/AppRun'".format(build_path))
        os.system("cp ./assets/tbx_logo.png {}".format(build_path))
        os.system("./appimagetool-x86_64.AppImage {} {}/TBX-x86_64.AppImage".format(build_path, build_path))


