# -----------------------------------------------------------------------------------------------------
# Youtube Minecraft Scraper - All Rights Reserved
# -----------------------------------------------------------------------------------------------------
# Copyright (C) Scott Jones - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Authors:
# - Scott Jones <scott.jones9336@gmail.com>
# -----------------------------------------------------------------------------------------------------
from pathlib import Path
from typing import List, Optional
from PySide6 import QtCore, QtWidgets


LAST_DIRECTORY_SETTINGS_KEY = "last_directory"
isPySide = True

class ExplorerApp:
    # Class for selecting file/s and save locations

    def __init__(self, parent: QtCore.QObject = None) -> None:
        self._parent = parent
        self._settings = QtCore.QSettings()

    def _lastDirectory(self) -> str:
        lastDir = self._settings.value(LAST_DIRECTORY_SETTINGS_KEY)
        if isinstance(lastDir, str):
            try:
                # Path.is_dir calls Path.stat which will throw OSError
                # if directory is blocked or corrupted
                if Path(lastDir).is_dir():
                    return lastDir
            except OSError:
                pass
        return str(Path("~").expanduser())

    def _updateLastDirectoryFromSelectedFile(self, path: Path) -> None:
        self._settings.setValue(
            LAST_DIRECTORY_SETTINGS_KEY, str(path.absolute().parent)
        )

    def openFilePathDialog(
        self,
        nameFilter: str = "Json Files (*.json);;All Files (*)",
        title: str = "Open",
    ) -> Optional[Path]:
        if isPySide:
            selectedFile, _ = QtWidgets.QFileDialog.getOpenFileName(
                self._parent,
                caption=title,
                dir=self._lastDirectory(),
                filter=nameFilter,
            )
        else:
            selectedFile, _ = QtWidgets.QFileDialog.getOpenFileName( # type: ignore[call-arg]  
                self._parent,
                caption=title,
                directory=self._lastDirectory(),
                filter=nameFilter,
            )
        if selectedFile != "":
            path = Path(selectedFile)
            self._updateLastDirectoryFromSelectedFile(path)
            return path
        return None

    def openFilePathsDialog(
        self,
        nameFilter: str = "Json Files (*.json);;All Files (*)",
        title: str = "Open",
    ) -> Optional[List[Path]]:
        if isPySide:
            selectedFiles, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self._parent,
                caption=title,
                dir=self._lastDirectory(),
                filter=nameFilter,
            )
        else:
            selectedFiles, _ = QtWidgets.QFileDialog.getOpenFileNames( # type: ignore[call-arg]  
                self._parent,
                caption=title,
                directory=self._lastDirectory(),
                filter=nameFilter,
            )
        if len(selectedFiles) > 0:
            paths = [Path(f) for f in selectedFiles]
            self._updateLastDirectoryFromSelectedFile(paths[0])
            return paths
        return None

    def _addSuffixIfRequired(self, path: Path, suffix: str) -> Path:
        if path.suffix == "":
            return path.with_suffix("." + suffix)
        return path

    def saveFilePathDialog(
        self,
        nameFilter: str = "Json Files (*.json);;All Files (*)",
        defaultSuffix: str = "json",
        title: str = "Save",
        startLocation: Optional[Path] = None,
        defaultFilename: Optional[str] = None,
    ) -> Optional[Path]:
        startDir = self._lastDirectory()
        if startLocation is not None and startLocation.is_dir():
            startDir = str(startLocation)
        if defaultFilename is not None:
            startDir = str(Path(startDir) / defaultFilename)
        if isPySide:
            selectedFile, _ = QtWidgets.QFileDialog.getSaveFileName(
                self._parent,
                caption=title,
                dir=startDir,
                filter=nameFilter,
            )
        else:
            selectedFile, _ = QtWidgets.QFileDialog.getSaveFileName(  # type: ignore[call-arg]
                self._parent,
                caption=title,
                directory=startDir,
                filter=nameFilter,
            )
        if selectedFile != "":
            path = self._addSuffixIfRequired(Path(selectedFile), defaultSuffix)
            self._updateLastDirectoryFromSelectedFile(path)
            return path
        return None

    def openDirectoryPathDialog(
        self,
        title: str = "Open Directory",
        startLocation: Optional[Path] = None,
    ) -> Optional[Path]:
        startDir = self._lastDirectory()
        if startLocation is not None and startLocation.is_dir():
            startDir = str(startLocation)
        if isPySide:
            selectedDir = QtWidgets.QFileDialog.getExistingDirectory(
                self._parent, caption=title, dir=startDir
            )
        else:
            selectedDir = QtWidgets.QFileDialog.getExistingDirectory(  # type: ignore[call-arg] 
                self._parent, caption=title, directory=startDir
            )
        if selectedDir != "":
            path = Path(selectedDir)
            self._updateLastDirectoryFromSelectedFile(path)
            return path
        return None

    def saveDirectoryPathDialog(
        self,
        title: str = "Save Directory",
        defaultFolderName: Optional[Path] = None,
    ) -> Optional[Path]:
        startDir = self._lastDirectory()
        if defaultFolderName is not None:
            startDir = str(defaultFolderName)
        if isPySide:
            selectedDir, _ = QtWidgets.QFileDialog.getSaveFileName(
                self._parent,
                caption=title,
                dir=startDir,
                options=QtWidgets.QFileDialog.ShowDirsOnly,
            )
        else:
            selectedDir, _ = QtWidgets.QFileDialog.getSaveFileName(  # type: ignore[call-arg]
                self._parent,
                caption=title,
                directory=startDir,
                options=QtWidgets.QFileDialog.ShowDirsOnly,
            )
        if selectedDir != "":
            path = Path(selectedDir)
            self._updateLastDirectoryFromSelectedFile(path)
            return path
        return None
