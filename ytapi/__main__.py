# -----------------------------------------------------------------------------------------------------
# Youtube Minecraft Scraper - All Rights Reserved
# -----------------------------------------------------------------------------------------------------
# Copyright (C) Scott Jones - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Authors:
# - Scott Jones <scott.jones9336@gmail.com>
# -----------------------------------------------------------------------------------------------------
from ytapi.gui import MainWindow
from ytapi.pyside.app import createApplication 
import sys

if __name__ == "__main__":
    app=createApplication(sys.argv, "YouTube MineCraft Scraper", "Scott Jones")
    dia = MainWindow(None)
    dia.exec_()