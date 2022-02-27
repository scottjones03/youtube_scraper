# -----------------------------------------------------------------------------------------------------
# Youtube Minecraft Scraper - All Rights Reserved
# -----------------------------------------------------------------------------------------------------
# Copyright (C) Scott Jones - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Authors:
# - Scott Jones <scott.jones9336@gmail.com>
# -----------------------------------------------------------------------------------------------------
import ctypes
import os
from typing import List
import qdarkstyle
from PySide2 import QtWidgets, QtCore

def createApplication(
    argv: List[str],
    nameApp: str,
    namePublisher: str,
) -> QtWidgets.QApplication:

    # Enable HiDPI scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    # Initialise application
    app = QtWidgets.QApplication(argv)

    # Set the window icon and other metadata
    app.setApplicationName(nameApp)
    app.setOrganizationName(namePublisher)
    styleSheet = qdarkstyle.load_stylesheet_pyside2()
    app.setStyleSheet(styleSheet)

    # Following two lines are needed for setting the taskbar icon (https://stackoverflow.com/questions/14900510/changing-the-application-and-taskbar-icon-python-tkinter)
    # The appid string determines the id of the app. So if this is the same as AMP, then they will be considered the same app by windows and styleOriginal only one icon will appear for both AMP and DMP if they are both open. Needs to be unique
    myappid = f"{nameApp.lower()}.{namePublisher.lower()}.gui"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # with open(f"style{PyQt.__name__}.txt", "w") as f:
    #    f.write(styleSheet)

    print(f"Main application PID: {os.getpid()}")

    return app