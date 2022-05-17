# -----------------------------------------------------------------------------------------------------
# Youtube Minecraft Scraper - All Rights Reserved
# -----------------------------------------------------------------------------------------------------
# Copyright (C) Scott Jones - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Authors:
# - Scott Jones <scott.jones9336@gmail.com>
# -----------------------------------------------------------------------------------------------------
from ytapi.backend import Backend
from ytapi.gui import MainWindow
from ytapi.pyside.app import createApplication 
import sys
from PySide6 import QtCore

if __name__ == "__main__":
    app=createApplication(sys.argv, "YouTube MineCraft Scraper", "Scott Jones")
    
    frontend = MainWindow(None)
    backendVids = Backend(None)
    backendChannels = Backend(None)
    backendComs = Backend(None)

    backendVidsThread=QtCore.QThread(None)
    backendVids.moveToThread(backendVidsThread)
    backendVidsThread.start()
    backendChannelsThread=QtCore.QThread(None)
    backendChannels.moveToThread(backendChannelsThread)
    backendChannelsThread.start()
    backendComsThread=QtCore.QThread(None)
    backendComs.moveToThread(backendComsThread)
    backendComsThread.start()
    frontendThread=QtCore.QThread(None)
    frontend.moveToThread(frontendThread)
    frontendThread.start()

    frontend.searchVideosRequested.connect(backendVids.onSearchVideosRequested)
    backendVids.searchVideosResults.connect(frontend.onSearchVideosResults)
    backendVids.searchVideosComplete.connect(frontend.onSearchVideosComplete)

    frontend.searchChannelRequested.connect(backendVids.onSearchChannelRequested)
    backendVids.searchChannelResults.connect(frontend.onSearchChannelResults)
    backendVids.searchChannelComplete.connect(frontend.onSearchChannelComplete)

    frontend.searchCommentsRequested.connect(backendVids.onSearchCommentsRequested)
    backendVids.searchCommentsResults.connect(frontend.onSearchCommentsResults)
    backendVids.searchCommentsComplete.connect(frontend.onSearchCommentsComplete)

    frontend.exec_()