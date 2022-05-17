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
from typing import Optional, Sequence, List
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QPushButton, QTableWidget, QLineEdit, QSpinBox, QTableWidgetItem
from ytapi.pyside import makeUiClass, typed_signal
from ytapi.save_to_csv import StoredYoutubeData
from pyyoutube import Channel, Video, Comment
# Define classes from ui templates
UI_DIR = Path(__file__).resolve().parent
MainWindowUi = makeUiClass(UI_DIR / "gui.ui")

class MainWindow(MainWindowUi): # type: ignore
    @typed_signal.TypedSignal
    def searchVideosRequested(self, key: str, searchType: str, niche: str, num_videos: int, time_delta: int, language: str, region: str):
        ...
    
    @typed_signal.TypedSignal
    def searchChannelRequested(self, key: str, searchType: str, niche: str, num_channels: int, time_delta: int, min_subs: int, max_subs: int):
        ...

    @typed_signal.TypedSignal
    def searchCommentsRequested(self, key: str, video_id: str, keywords: str, num_comments: int):
        ...

    lineEdit_APIKEY: "QLineEdit"
    comboBox_searchTypeVideo: "QComboBox"
    lineEdit_nicheVideo: "QLineEdit"
    spinBox_numVideos: "QSpinBox"
    spinBox_timeDeltaVideos: "QSpinBox"
    lineEdit_languageRegion: "QLineEdit"
    pushButton_searchVideos: "QPushButton"
    tableWidget_videos: "QTableWidget"                                        
    pushButton_exportVideos: "QPushButton"
    comboBox_sortTypeChannel: "QComboBox"
    lineEdit_nicheChannel: "QLineEdit"
    spinBox_numChannels: "QSpinBox"
    spinBox_minSubs: "QSpinBox"
    spinBox_maxSubs: "QSpinBox"
    spinBox_timeDeltaChannel: "QSpinBox"
    pushButton_searchChannel: "QPushButton"
    tableWidget_channel: "QTableWidget"
    pushButton_exportChannel: "QPushButton"
    lineEdit_videoID: "QLineEdit"
    lineEdit_keywords: "QLineEdit"
    pushButton_searchComments: "QPushButton"
    tableWidget_comments: "QTableWidget"
    pushButton_exportComments: "QPushButton"
    spinBox_comments: "QSpinBox"

    def __init__(self, parent: Optional[QtCore.QObject]) -> None:
        super().__init__(parent=parent)
        self.setupUi(self)
        self._connectSignals()
        self._setEnabled(True)

        settings=QtCore.QSettings()
        self.apiKey: str=settings.value("apiKey", "")
        if len(self.apiKey)>0:
            self.pushButton_searchChannel.setEnabled(True)
            self.pushButton_searchComments.setEnabled(True)
            self.pushButton_searchVideos.setEnabled(True)
            self.lineEdit_APIKEY.setText(self.apiKey)
        else:
            self.lineEdit_APIKEY.setFocus()

        self.currentVideos: List[Video] = []
        self.currentChannels: List[Channel] = []
        self.currentComments: List[Comment] = []

    def _connectSignals(self) -> None:
        self.pushButton_searchVideos.clicked.connect(self.onSearchVideos)
        self.pushButton_searchChannel.clicked.connect(self.onSearchChannel)
        self.pushButton_searchComments.clicked.connect(self.onSearchComments)
        self.pushButton_exportVideos.clicked.connect(self.onExportVideos)
        self.pushButton_exportChannel.clicked.connect(self.onExportChannel)
        self.pushButton_exportComments.clicked.connect(self.onExportComments)
        self.comboBox_searchTypeVideo.currentTextChanged.connect(self.onVideoSearchTypeChanged)
        self.lineEdit_APIKEY.textChanged.connect(self.onAPIKeyChanged)



    def _setEnabled(self, enabled: bool) -> None:
        self.setEnabled(enabled)
        
    def _addCommas(self, value: str) -> str:
        splitValue = ""
        for i, char in enumerate(value):
            splitValue+=char
            if (len(value)-(i+1)) % 3 == 0 and i != len(value)-1:
                splitValue+=","
        return splitValue

    @typed_signal.TypedSlot
    def onAPIKeyChanged(self) -> None:
        self.pushButton_searchChannel.setEnabled(True)
        self.pushButton_searchComments.setEnabled(True)
        self.pushButton_searchVideos.setEnabled(True)
        self.apiKey=self.lineEdit_APIKEY.text()
        settings=QtCore.QSettings()
        settings.setValue("apiKey", self.apiKey)

    @typed_signal.TypedSlot
    def onVideoSearchTypeChanged(self) -> None:
        if self.comboBox_searchTypeVideo.currentText() == "Most Viewed":
            self.label_7.setText("Days:")
        elif self.comboBox_searchTypeVideo.currentText() == "Recycled":
            self.label_7.setText("Years:")
        elif self.comboBox_searchTypeVideo.currentText() == "Most Pushed":
            self.label_7.setText("Days:")
        elif self.comboBox_searchTypeVideo.currentText() == "Less than 4":
            self.label_7.setText("Days:")

    @typed_signal.TypedSlot
    def onSearchVideos(self) -> None:
        self.pushButton_searchVideos.setEnabled(False)
        self.pushButton_searchVideos.setText("loading...")
        niche = self.lineEdit_nicheVideo.text()
        num_videos = self.spinBox_numVideos.value()
        time_delta = self.spinBox_timeDeltaVideos.value()
        language, region = self.lineEdit_languageRegion.text().split("/")
        searchType = self.comboBox_searchTypeVideo.currentText()
        self.searchVideosRequested.emit(self.apiKey, searchType, niche, num_videos, time_delta, language, region)


    @typed_signal.TypedSlot
    def onSearchVideosResults(self, videos: List[Video], channels: List[Channel]) -> None:
        self.currentVideos=videos
        video_dict = StoredYoutubeData().get_videos_dict(self.currentVideos, channels)
        self.tableWidget_videos.clear()
        for colIdx, (columnName, columnData) in enumerate(video_dict.items()):
            self.tableWidget_videos.insertColumn(self.tableWidget_videos.columnCount())
            for rowIdx, itemData in enumerate(columnData):
                if colIdx==0:
                    self.tableWidget_videos.insertRow(self.tableWidget_videos.rowCount())
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, self._addCommas(str(itemData)) if str(itemData).isnumeric() else itemData)
                self.tableWidget_videos.setItem(rowIdx, colIdx, item)
        labels: Sequence[str] = [label for label in video_dict.keys()]
        self.tableWidget_videos.setHorizontalHeaderLabels(labels)
        self.pushButton_exportVideos.setEnabled(True)

    @typed_signal.TypedSlot
    def onSearchVideosComplete(self) -> None:
        self.pushButton_searchVideos.setText("search")
        self.pushButton_searchVideos.setEnabled(True)
            

    @typed_signal.TypedSlot
    def onSearchChannel(self) -> None:
        self.pushButton_searchChannel.setText("loading...")
        self.pushButton_searchChannel.setEnabled(False)
        niche = self.lineEdit_nicheChannel.text()
        num_channels = self.spinBox_numChannels.value()
        min_subs, max_subs = self.spinBox_minSubs.value(), self.spinBox_maxSubs.value()
        time_delta = self.spinBox_timeDeltaChannel.value()
        searchType = self.comboBox_sortTypeChannel.currentText() 
        self.searchChannelRequested.emit(self.apiKey, searchType, niche, num_channels, time_delta, min_subs, max_subs)

    @typed_signal.TypedSlot
    def onSearchChannelResults(self, channels: List[Channel]) -> None:
        self.currentChannels=channels
        channel_dict = StoredYoutubeData().get_channels_dict(self.currentChannels)
        self.tableWidget_channel.clear()
        for colIdx, (columnName, columnData) in enumerate(channel_dict.items()):
            self.tableWidget_channel.insertColumn(self.tableWidget_channel.columnCount())
            for rowIdx, itemData in enumerate(columnData):
                if colIdx == 0:
                    self.tableWidget_channel.insertRow(self.tableWidget_channel.rowCount())
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, self._addCommas(str(itemData)) if str(itemData).isnumeric() else itemData)
                self.tableWidget_channel.setItem(rowIdx, colIdx, item)
        labels: Sequence[str] = [label for label in channel_dict.keys()]
        self.tableWidget_channel.setHorizontalHeaderLabels(labels)
        self.pushButton_exportChannel.setEnabled(True)

    @typed_signal.TypedSlot
    def onSearchChannelComplete(self) -> None:
        self.pushButton_searchChannel.setText("search")
        self.pushButton_searchChannel.setEnabled(True)

    
    @typed_signal.TypedSlot
    def onSearchComments(self) -> None:
        self.pushButton_searchComments.setText("loading...")
        self.pushButton_searchComments.setEnabled(False)
        video_id = self.lineEdit_videoID.text()
        keywords = self.lineEdit_keywords.text()
        num_comments = self.spinBox_comments.value()
        self.searchCommentsRequested.emit(self.apiKey, video_id, keywords, num_comments)

    @typed_signal.TypedSlot
    def onSearchCommentsResults(self, comments: List[Comment]) -> None:
        self.currentComments=comments
        comments_dict = StoredYoutubeData().get_comments_dict(self.currentComments)
        self.tableWidget_comments.clear()
        for colIdx, (columnName, columnData) in enumerate(comments_dict.items()):
            self.tableWidget_comments.insertColumn(self.tableWidget_comments.columnCount())
            for rowIdx, itemData in enumerate(columnData):
                if colIdx == 0:
                    self.tableWidget_comments.insertRow(self.tableWidget_comments.rowCount())
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, self._addCommas(str(itemData)) if str(itemData).isnumeric() else itemData)
                self.tableWidget_comments.setItem(rowIdx, colIdx, item)
        labels: Sequence[str] = [label for label in comments_dict.keys()]
        self.tableWidget_comments.setHorizontalHeaderLabels(labels)
        self.pushButton_exportComments.setEnabled(True)
    
    @typed_signal.TypedSlot
    def onSearchCommentsComplete(self) -> None:
        self.pushButton_searchComments.setText("search")
        self.pushButton_searchComments.setEnabled(True)

    @typed_signal.TypedSlot
    def onExportVideos(self) -> None:
        StoredYoutubeData().save_videos_to_file(self.currentVideos)
    
    @typed_signal.TypedSlot
    def onExportChannel(self) -> None:
        StoredYoutubeData().save_channels_to_file(self.currentChannels)

    @typed_signal.TypedSlot
    def onExportComments(self) -> None:
        StoredYoutubeData().save_comments_to_file(self.currentComments)


    
