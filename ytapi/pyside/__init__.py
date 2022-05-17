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
from PySide6 import QtWidgets
from typing import Type, Protocol
from ytapi.pyside.pyside_dynamic import loadUi as _loadUi
import defusedxml.ElementTree as ET

class UiClassProtocol(Protocol):
    _uiFilepath: Path

def makeUiClass(uiFilepath: Path) -> Type[QtWidgets.QWidget]: 
    assert (
        uiFilepath.suffix == ".ui"
    ), "PySide6 class construction error: file is not a ui file."
    assert (
        uiFilepath.is_file()
    ), "PySide6 class construction error: file does not exist."

    def setupUi(self: UiClassProtocol, baseinstance: QtWidgets.QWidget) -> None:
        _loadUi(self._uiFilepath, baseinstance)

    attributes = dict(_uiFilepath=uiFilepath, setupUi=setupUi)
    # Look up class name from UI file
    ui = ET.parse(str(uiFilepath))
    widget = ui.find("widget")
    assert widget is not None, "makeUiClass: ui.find('widget') is None"
    baseclassName = f"{widget.attrib['class']}"
    baseclass: Type[QtWidgets.QWidget] = getattr(QtWidgets, baseclassName)
    derivedClassName = f"{baseclassName}Ui"
    return type(derivedClassName, (baseclass,), attributes)