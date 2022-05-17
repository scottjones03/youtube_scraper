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
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QPushButton, QTableWidget, QLineEdit, QSpinBox, QTableWidgetItem
from ytapi.pyside import makeUiClass, typed_signal
from ytapi.youtube_api import YouTubeAPI
from ytapi.save_to_csv import StoredYoutubeData
from pyyoutube import Api, Channel, Video, PlaylistItem, Comment
# Define classes from ui templates
UI_DIR = Path(__file__).resolve().parent
MainWindowUi = makeUiClass(UI_DIR / "gui.ui")

class MainWindow(MainWindowUi): # type: ignore

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

    def getYouTubeAPI(self) -> YouTubeAPI:
        api_key = self.lineEdit_APIKEY.text()
        return YouTubeAPI(api_key)

    @typed_signal.TypedSlot
    def onAPIKeyChanged(self) -> None:
        self.pushButton_searchChannel.setEnabled(True)
        self.pushButton_searchComments.setEnabled(True)
        self.pushButton_searchVideos.setEnabled(True)

    @typed_signal.TypedSlot
    def onVideoSearchTypeChanged(self) -> None:
        if self.comboBox_searchTypeVideo.currentText() == "Most Viewed":
            self.label_7.setText("Days:")
        elif self.comboBox_searchTypeVideo.currentText() == "Recycled":
            self.label_7.setText("Years:")
        elif self.comboBox_searchTypeVideo.currentText() == "Most Pushed":
            self.label_7.setText("Days:")

    @typed_signal.TypedSlot
    def onSearchVideos(self) -> None:
        self._setEnabled(False)
        niche = self.lineEdit_nicheVideo.text()
        num_videos = self.spinBox_numVideos.value()
        time_delta = self.spinBox_timeDeltaVideos.value()
        language, region = self.lineEdit_languageRegion.text().split("/")
        self._setEnabled(True)
        api=self.getYouTubeAPI()
        if self.comboBox_searchTypeVideo.currentText() == "Most Viewed":
            self.currentVideos=api.get_most_viewed_videos(niche=niche, language=language, region=region, num_videos=num_videos, time_delta=time_delta)
        elif self.comboBox_searchTypeVideo.currentText() == "Recycled":
            self.currentVideos=api.get_old_videos(niche=niche, num_videos=num_videos, time_delta=time_delta)
        elif self.comboBox_searchTypeVideo.currentText() == "Most Pushed":
            self.currentVideos=api.get_pushed_videos(niche=niche, num_videos=num_videos, time_delta=time_delta)
        video_dict = StoredYoutubeData().get_videos_dict(self.currentVideos)
        self.tableWidget_videos.clear()
        for colIdx, (columnName, columnData) in enumerate(video_dict.items()):
            self.tableWidget_videos.insertColumn(self.tableWidget_videos.columnCount())
            for rowIdx, itemData in enumerate(columnData):
                if colIdx==0:
                    self.tableWidget_videos.insertRow(self.tableWidget_videos.rowCount())
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, self._addCommas(itemData) if itemData.isnumeric() else itemData)
                self.tableWidget_videos.setItem(rowIdx, colIdx, item)
        labels: Sequence[str] = [label for label in video_dict.keys()]
        self.tableWidget_videos.setHorizontalHeaderLabels(labels)
        self.pushButton_exportVideos.setEnabled(True)
            

    @typed_signal.TypedSlot
    def onSearchChannel(self) -> None:
        self._setEnabled(False)
        niche = self.lineEdit_nicheChannel.text()
        num_channels = self.spinBox_numChannels.value()
        min_subs, max_subs = self.spinBox_minSubs.value(), self.spinBox_maxSubs.value()
        time_delta = self.spinBox_timeDeltaChannel.value()
        self._setEnabled(True)
        api=self.getYouTubeAPI()
        self.currentChannels=api.get_small_channels(niche=niche, num_channels=num_channels, time_delta=time_delta, subscriber_range=(min_subs, max_subs))
        if self.comboBox_sortTypeChannel.currentText() == "Sort by Subs":
            self.currentChannels=api.sort_by_subscribers(self.currentChannels)
        elif self.comboBox_sortTypeChannel.currentText() == "Sort by Views":
            self.currentChannels=api.sort_by_recent_views(self.currentChannels, time_delta)
        channel_dict = StoredYoutubeData().get_channels_dict(self.currentChannels)
        self.tableWidget_channel.clear()
        for colIdx, (columnName, columnData) in enumerate(channel_dict.items()):
            self.tableWidget_channel.insertColumn(self.tableWidget_channel.columnCount())
            for rowIdx, itemData in enumerate(columnData):
                if colIdx == 0:
                    self.tableWidget_channel.insertRow(self.tableWidget_channel.rowCount())
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, self._addCommas(itemData) if itemData.isnumeric() else itemData)
                self.tableWidget_channel.setItem(rowIdx, colIdx, item)
        labels: Sequence[str] = [label for label in channel_dict.keys()]
        self.tableWidget_channel.setHorizontalHeaderLabels(labels)
        self.pushButton_exportChannel.setEnabled(True)

    
    @typed_signal.TypedSlot
    def onSearchComments(self) -> None:
        self._setEnabled(False)
        video_id = self.lineEdit_videoID.text()
        keywords = self.lineEdit_keywords.text()
        num_comments = self.spinBox_comments.value()
        self._setEnabled(True)
        api=self.getYouTubeAPI()
        self.currentComments=api.get_comments(video_id, keywords, num_comments)
        comments_dict = StoredYoutubeData().get_comments_dict(self.currentComments)
        self.tableWidget_comments.clear()
        for colIdx, (columnName, columnData) in enumerate(comments_dict.items()):
            self.tableWidget_comments.insertColumn(self.tableWidget_comments.columnCount())
            for rowIdx, itemData in enumerate(columnData):
                if colIdx == 0:
                    self.tableWidget_comments.insertRow(self.tableWidget_comments.rowCount())
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, self._addCommas(itemData) if itemData.isnumeric() else itemData)
                self.tableWidget_comments.setItem(rowIdx, colIdx, item)
        labels: Sequence[str] = [label for label in comments_dict.keys()]
        self.tableWidget_comments.setHorizontalHeaderLabels(labels)
        self.pushButton_exportComments.setEnabled(True)

    @typed_signal.TypedSlot
    def onExportVideos(self) -> None:
        StoredYoutubeData().save_videos_to_file(self.currentVideos)
    
    @typed_signal.TypedSlot
    def onExportChannel(self) -> None:
        StoredYoutubeData().save_channels_to_file(self.currentChannels)

    @typed_signal.TypedSlot
    def onExportComments(self) -> None:
        StoredYoutubeData().save_comments_to_file(self.currentComments)


    
