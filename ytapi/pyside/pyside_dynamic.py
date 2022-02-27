#!/usr/bin/env python3
# found this here:
# https://github.com/lunaryorn/snippets/blob/master/qt4/designer/pyside_dynamic.py

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
    How to load a user interface dynamically with PySide.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@gmail.com>
"""

from pathlib import Path
from typing import Dict, Optional, Type, TYPE_CHECKING

from PySide2 import QtCore, QtUiTools, QtWidgets


class UiLoader(QtUiTools.QUiLoader):
    """
    Subclass :class:`~PySide.QtUiTools.QUiLoader` to create the user interface
    in a base instance.

    Unlike :class:`~PySide.QtUiTools.QUiLoader` itself this class does not
    create a new instance of the top-level widget, but creates the user
    interface in an existing instance of the top-level class.

    This mimics the behaviour of :func:`PyQt4.uic.loadUi`.
    """

    def __init__(
        self,
        baseinstance: Optional[QtWidgets.QWidget],
        customWidgets: Optional[Dict[str, Type[QtWidgets.QWidget]]] = None,
    ):
        """
        Create a loader for the given ``baseinstance``.

        The user interface is created in ``baseinstance``, which must be an
        instance of the top-level class in the user interface to load, or a
        subclass thereof.

        ``customWidgets`` is a dictionary mapping from class name to class object
        for widgets that you've promoted in the Qt Designer interface. Usually,
        this should be done by calling registerCustomWidget on the QUiLoader, but
        with PySide 1.1.2 on Ubuntu 12.04 x86_64 this causes a segfault.

        ``parent`` is the parent object of this loader.
        """

        QtUiTools.QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance
        if customWidgets is None:
            self.customWidgets: Dict[str, Type[QtWidgets.QWidget]] = {}
        else:
            self.customWidgets = customWidgets

    def createWidget(
        self,
        class_name: str,
        parent: Optional[QtWidgets.QWidget] = None,
        name: str = "",
    ) -> QtWidgets.QWidget:
        """
        Function that is called for each widget defined in ui file,
        overridden here to populate baseinstance instead.
        """

        if parent is None and self.baseinstance:
            # supposed to create the top-level widget, return the base instance
            # instead
            return self.baseinstance

        else:
            if class_name in self.availableWidgets() or class_name == "Line":
                # create a new widget for child widgets
                widget = QtUiTools.QUiLoader.createWidget(
                    self, class_name, parent, name
                )

            else:
                # if not in the list of availableWidgets, must be a custom widget
                # this will raise KeyError if the user has not supplied the
                # relevant class_name in the dictionary, or TypeError, if
                # customWidgets is None
                try:
                    widget = self.customWidgets[class_name](parent)

                except KeyError as e:
                    raise Exception(
                        "No custom widget "
                        + class_name
                        + " found in customWidgets param of UiLoader __init__."
                    )

            if self.baseinstance:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.baseinstance, name, widget)

                # this outputs the various widget names, e.g.
                # sampleGraphicsView, dockWidget, samplesTableView etc.
                # print(name)

            return widget


def _get_custom_widgets(ui_file: Path) -> Dict[str, Type[QtWidgets.QWidget]]:
    """
    This function is used to parse a ui file and look for the <customwidgets>
    section, then automatically load all the custom widget classes.
    """

    import sys
    import importlib

    if TYPE_CHECKING:
        from xml.etree.ElementTree import (  # nosec: Only used for type annotations
            Element,
        )

    import defusedxml.ElementTree as ET

    ui = ET.parse(str(ui_file))

    # Get the customwidgets section
    custom_widgets = ui.find("customwidgets")

    if custom_widgets is None:
        return {}

    custom_widget_classes = {}

    for custom_widget in custom_widgets:

        cw_class_element: Optional["Element"] = custom_widget.find("class")
        cw_header_element: Optional["Element"] = custom_widget.find("header")
        assert cw_class_element is not None, "Got None for class name element"
        assert cw_header_element is not None, "Got None for module name element"

        cw_class = cw_class_element.text
        cw_header = cw_header_element.text
        assert cw_class is not None, "Got None for class name"
        assert cw_header is not None, "Got None for module name"

        module = importlib.import_module(cw_header)

        custom_widget_classes[cw_class] = getattr(module, cw_class)

    return custom_widget_classes


def loadUi(
    uifile: Path,
    baseinstance: Optional[QtWidgets.QWidget] = None,
    workingDirectory: Optional[QtCore.QDir] = None,
) -> QtWidgets.QWidget:
    """
    Dynamically load a user interface from the given ``uifile``.

    ``uifile`` is a string containing a file name of the UI file to load.

    If ``baseinstance`` is ``None``, the a new instance of the top-level widget
    will be created.  Otherwise, the user interface is created within the given
    ``baseinstance``.  In this case ``baseinstance`` must be an instance of the
    top-level widget class in the UI file to load, or a subclass thereof.  In
    other words, if you've created a ``QMainWindow`` interface in the designer,
    ``baseinstance`` must be a ``QMainWindow`` or a subclass thereof, too.  You
    cannot load a ``QMainWindow`` UI file with a plain
    :class:`~PySide.QtGui.QWidget` as ``baseinstance``.

    ``customWidgets`` is a dictionary mapping from class name to class object
    for widgets that you've promoted in the Qt Designer interface. Usually,
    this should be done by calling registerCustomWidget on the QUiLoader, but
    with PySide 1.1.2 on Ubuntu 12.04 x86_64 this causes a segfault.

    :method:`~PySide.QtCore.QMetaObject.connectSlotsByName()` is called on the
    created user interface, so you can implemented your slots according to its
    conventions in your widget class.

    Return ``baseinstance``, if ``baseinstance`` is not ``None``.  Otherwise
    return the newly created instance of the user interface.
    """
    customWidgets = _get_custom_widgets(uifile)
    loader = UiLoader(baseinstance, customWidgets)

    if workingDirectory is not None:
        loader.setWorkingDirectory(workingDirectory)

    widget = loader.load(str(uifile))

    QtCore.QMetaObject.connectSlotsByName(widget)
    return widget