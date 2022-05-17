# pylint: disable=all
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1192, 763)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 0))
        self.horizontalLayoutWidget_3 = QWidget(Dialog)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(13, 11, 1369, 741))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 200, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.lineEdit_APIKEY = QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_APIKEY.setObjectName(u"lineEdit_APIKEY")

        self.verticalLayout.addWidget(self.lineEdit_APIKEY)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.label_4 = QLabel(self.horizontalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(50, 0))
        self.label_4.setFrameShape(QFrame.Panel)
        self.label_4.setFrameShadow(QFrame.Raised)
        self.label_4.setLineWidth(3)
        self.label_4.setMidLineWidth(26)
        self.label_4.setMargin(7)

        self.horizontalLayout_6.addWidget(self.label_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 0)
        self.comboBox_searchTypeVideo = QComboBox(self.horizontalLayoutWidget_3)
        self.comboBox_searchTypeVideo.addItem("")
        self.comboBox_searchTypeVideo.addItem("")
        self.comboBox_searchTypeVideo.addItem("")
        self.comboBox_searchTypeVideo.setObjectName(u"comboBox_searchTypeVideo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_searchTypeVideo.sizePolicy().hasHeightForWidth())
        self.comboBox_searchTypeVideo.setSizePolicy(sizePolicy1)
        self.comboBox_searchTypeVideo.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_7.addWidget(self.comboBox_searchTypeVideo)

        self.label_5 = QLabel(self.horizontalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(50, 0))
        self.label_5.setMaximumSize(QSize(16777215, 5290))

        self.horizontalLayout_7.addWidget(self.label_5)

        self.lineEdit_nicheVideo = QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_nicheVideo.setObjectName(u"lineEdit_nicheVideo")

        self.horizontalLayout_7.addWidget(self.lineEdit_nicheVideo)

        self.label_6 = QLabel(self.horizontalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_7.addWidget(self.label_6)

        self.spinBox_numVideos = QSpinBox(self.horizontalLayoutWidget_3)
        self.spinBox_numVideos.setObjectName(u"spinBox_numVideos")
        self.spinBox_numVideos.setMinimum(1)
        self.spinBox_numVideos.setMaximum(1000)

        self.horizontalLayout_7.addWidget(self.spinBox_numVideos)

        self.label_7 = QLabel(self.horizontalLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.spinBox_timeDeltaVideos = QSpinBox(self.horizontalLayoutWidget_3)
        self.spinBox_timeDeltaVideos.setObjectName(u"spinBox_timeDeltaVideos")
        self.spinBox_timeDeltaVideos.setMinimum(1)
        self.spinBox_timeDeltaVideos.setMaximum(1000)

        self.horizontalLayout_7.addWidget(self.spinBox_timeDeltaVideos)

        self.label_13 = QLabel(self.horizontalLayoutWidget_3)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_7.addWidget(self.label_13)

        self.lineEdit_languageRegion = QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_languageRegion.setObjectName(u"lineEdit_languageRegion")

        self.horizontalLayout_7.addWidget(self.lineEdit_languageRegion)

        self.pushButton_searchVideos = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_searchVideos.setObjectName(u"pushButton_searchVideos")
        self.pushButton_searchVideos.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.pushButton_searchVideos)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.tableWidget_videos = QTableWidget(self.horizontalLayoutWidget_3)
        self.tableWidget_videos.setObjectName(u"tableWidget_videos")

        self.verticalLayout_3.addWidget(self.tableWidget_videos)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.pushButton_exportVideos = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_exportVideos.setObjectName(u"pushButton_exportVideos")
        self.pushButton_exportVideos.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.pushButton_exportVideos)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.label_8 = QLabel(self.horizontalLayoutWidget_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(50, 0))
        self.label_8.setFrameShape(QFrame.Panel)
        self.label_8.setFrameShadow(QFrame.Raised)
        self.label_8.setLineWidth(3)
        self.label_8.setMidLineWidth(26)
        self.label_8.setMargin(7)

        self.horizontalLayout_9.addWidget(self.label_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(5)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(-1, -1, -1, 0)
        self.comboBox_sortTypeChannel = QComboBox(self.horizontalLayoutWidget_3)
        self.comboBox_sortTypeChannel.addItem("")
        self.comboBox_sortTypeChannel.addItem("")
        self.comboBox_sortTypeChannel.setObjectName(u"comboBox_sortTypeChannel")
        sizePolicy1.setHeightForWidth(self.comboBox_sortTypeChannel.sizePolicy().hasHeightForWidth())
        self.comboBox_sortTypeChannel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_10.addWidget(self.comboBox_sortTypeChannel)

        self.label_9 = QLabel(self.horizontalLayoutWidget_3)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QSize(50, 0))
        self.label_9.setMaximumSize(QSize(16777215, 5290))

        self.horizontalLayout_10.addWidget(self.label_9)

        self.lineEdit_nicheChannel = QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_nicheChannel.setObjectName(u"lineEdit_nicheChannel")

        self.horizontalLayout_10.addWidget(self.lineEdit_nicheChannel)

        self.label_14 = QLabel(self.horizontalLayoutWidget_3)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_10.addWidget(self.label_14)

        self.spinBox_numChannels = QSpinBox(self.horizontalLayoutWidget_3)
        self.spinBox_numChannels.setObjectName(u"spinBox_numChannels")
        self.spinBox_numChannels.setMinimum(1)
        self.spinBox_numChannels.setMaximum(1000)

        self.horizontalLayout_10.addWidget(self.spinBox_numChannels)

        self.label_12 = QLabel(self.horizontalLayoutWidget_3)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_10.addWidget(self.label_12)

        self.spinBox_minSubs = QSpinBox(self.horizontalLayoutWidget_3)
        self.spinBox_minSubs.setObjectName(u"spinBox_minSubs")
        self.spinBox_minSubs.setMinimum(1)
        self.spinBox_minSubs.setMaximum(1000000000)

        self.horizontalLayout_10.addWidget(self.spinBox_minSubs)

        self.label_10 = QLabel(self.horizontalLayoutWidget_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_10.addWidget(self.label_10)

        self.spinBox_maxSubs = QSpinBox(self.horizontalLayoutWidget_3)
        self.spinBox_maxSubs.setObjectName(u"spinBox_maxSubs")
        self.spinBox_maxSubs.setMinimum(1)
        self.spinBox_maxSubs.setMaximum(1000000000)

        self.horizontalLayout_10.addWidget(self.spinBox_maxSubs)

        self.label_11 = QLabel(self.horizontalLayoutWidget_3)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_10.addWidget(self.label_11)

        self.spinBox_timeDeltaChannel = QSpinBox(self.horizontalLayoutWidget_3)
        self.spinBox_timeDeltaChannel.setObjectName(u"spinBox_timeDeltaChannel")
        self.spinBox_timeDeltaChannel.setMinimum(1)
        self.spinBox_timeDeltaChannel.setMaximum(1000)

        self.horizontalLayout_10.addWidget(self.spinBox_timeDeltaChannel)

        self.pushButton_searchChannel = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_searchChannel.setObjectName(u"pushButton_searchChannel")
        self.pushButton_searchChannel.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.pushButton_searchChannel)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.tableWidget_channel = QTableWidget(self.horizontalLayoutWidget_3)
        self.tableWidget_channel.setObjectName(u"tableWidget_channel")

        self.verticalLayout_4.addWidget(self.tableWidget_channel)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_3)

        self.pushButton_exportChannel = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_exportChannel.setObjectName(u"pushButton_exportChannel")
        self.pushButton_exportChannel.setEnabled(False)

        self.horizontalLayout_11.addWidget(self.pushButton_exportChannel)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)


        self.verticalLayout.addLayout(self.verticalLayout_4)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout_3.addItem(self.verticalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.label_3 = QLabel(self.horizontalLayoutWidget_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(50, 0))
        self.label_3.setFrameShape(QFrame.Panel)
        self.label_3.setFrameShadow(QFrame.Raised)
        self.label_3.setLineWidth(3)
        self.label_3.setMidLineWidth(26)
        self.label_3.setMargin(7)

        self.horizontalLayout.addWidget(self.label_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.label = QLabel(self.horizontalLayoutWidget_3)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(50, 0))
        self.label.setMaximumSize(QSize(16777215, 5290))

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit_videoID = QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_videoID.setObjectName(u"lineEdit_videoID")
        sizePolicy1.setHeightForWidth(self.lineEdit_videoID.sizePolicy().hasHeightForWidth())
        self.lineEdit_videoID.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.lineEdit_videoID)

        self.label_2 = QLabel(self.horizontalLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_keywords = QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_keywords.setObjectName(u"lineEdit_keywords")
        sizePolicy1.setHeightForWidth(self.lineEdit_keywords.sizePolicy().hasHeightForWidth())
        self.lineEdit_keywords.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.lineEdit_keywords)

        self.spinBox_comments = QSpinBox(self.horizontalLayoutWidget_3)
        self.spinBox_comments.setObjectName(u"spinBox_comments")
        self.spinBox_comments.setMaximum(1000)

        self.horizontalLayout_2.addWidget(self.spinBox_comments)

        self.pushButton_searchComments = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_searchComments.setObjectName(u"pushButton_searchComments")
        self.pushButton_searchComments.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.pushButton_searchComments)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.tableWidget_comments = QTableWidget(self.horizontalLayoutWidget_3)
        self.tableWidget_comments.setObjectName(u"tableWidget_comments")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget_comments.sizePolicy().hasHeightForWidth())
        self.tableWidget_comments.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.tableWidget_comments)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.pushButton_exportComments = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_exportComments.setObjectName(u"pushButton_exportComments")
        self.pushButton_exportComments.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_exportComments.sizePolicy().hasHeightForWidth())
        self.pushButton_exportComments.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.pushButton_exportComments)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Youtube Scraper", None))
        self.lineEdit_APIKEY.setText(QCoreApplication.translate("Dialog", u"***INPUT API KEY HERE***", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Video search tool:</p><p align=\"center\"><span style=\" font-size:7pt;\">Most viewed videos posted in the last N days, highest views/subs ratio videos posted in the last N days, and recycled videos older than N years being pushed.</span></p></body></html>", None))
        self.comboBox_searchTypeVideo.setItemText(0, QCoreApplication.translate("Dialog", u"Most Viewed", None))
        self.comboBox_searchTypeVideo.setItemText(1, QCoreApplication.translate("Dialog", u"Most Pushed", None))
        self.comboBox_searchTypeVideo.setItemText(2, QCoreApplication.translate("Dialog", u"Recycled", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"Niche:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Videos:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Days:", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Language/Region", None))
        self.lineEdit_languageRegion.setText(QCoreApplication.translate("Dialog", u"en/US", None))
        self.pushButton_searchVideos.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_exportVideos.setText(QCoreApplication.translate("Dialog", u"Export", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Channel search tool:</p><p align=\"center\"><span style=\" font-size:7pt;\">Channels that have posted in the last N days and sorted by subscribers or sorted byviews in the last N days.</span></p></body></html>", None))
        self.comboBox_sortTypeChannel.setItemText(0, QCoreApplication.translate("Dialog", u"Sort by Subs", None))
        self.comboBox_sortTypeChannel.setItemText(1, QCoreApplication.translate("Dialog", u"Sort by Views", None))

        self.label_9.setText(QCoreApplication.translate("Dialog", u"Niche:", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Channels:", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Min subs:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Max subs", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Days:", None))
        self.pushButton_searchChannel.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_exportChannel.setText(QCoreApplication.translate("Dialog", u"Export", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Comments search tool:</p><p align=\"center\"><span style=\" font-size:7pt;\">Input video ID and keywords should be split with a space.</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Video ID:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Keywords:", None))
        self.pushButton_searchComments.setText(QCoreApplication.translate("Dialog", u"Search", None))
        self.pushButton_exportComments.setText(QCoreApplication.translate("Dialog", u"Export", None))
    # retranslateUi

