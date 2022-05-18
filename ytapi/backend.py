# -----------------------------------------------------------------------------------------------------
# Youtube Minecraft Scraper - All Rights Reserved
# -----------------------------------------------------------------------------------------------------
# Copyright (C) Scott Jones - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Authors:
# - Scott Jones <scott.jones9336@gmail.com>
# -----------------------------------------------------------------------------------------------------
from typing import List, Optional

from PySide6 import QtCore
from pyyoutube import Channel, Comment, Video

from ytapi.pyside import typed_signal
from ytapi.youtube_api import YouTubeAPI


class Backend(QtCore.QObject):
    @typed_signal.TypedSignal
    def searchVideosResults(self, videos: List[Video], channels: List[Channel]):
        ...
    
    @typed_signal.TypedSignal
    def searchVideosComplete(self):
        ...
    
    @typed_signal.TypedSignal
    def searchChannelResults(self, channels: List[Channel]):
        ...
    
    @typed_signal.TypedSignal
    def searchChannelComplete(self):
        ...

    @typed_signal.TypedSignal
    def searchCommentsResults(self, comments: List[Comment]):
        ...
    
    @typed_signal.TypedSignal
    def searchCommentsComplete(self):
        ...

    def __init__(self, parent: Optional[QtCore.QObject]) -> None:
        super().__init__(parent=parent)

    def getYouTubeAPI(self, key: str) -> YouTubeAPI:
        return YouTubeAPI(key)

    @typed_signal.TypedSlot
    def onSearchVideosRequested(self, key: str, searchType: str, niche: str, num_videos: int, time_delta: int, language: str, region: str):
        api=self.getYouTubeAPI(key)
        if searchType == "Most Viewed":
            videos_gen=api.yield_most_viewed_videos(niche=niche, language=language, region=region, num_videos=num_videos, time_delta=time_delta)
        elif searchType == "Recycled":
            videos_gen=api.yield_old_videos(niche=niche, language=language, region=region, num_videos=num_videos, time_delta=time_delta)
        elif searchType == "Most Pushed":
            videos_gen=api.yield_pushed_videos(niche=niche, language=language, region=region, num_videos=num_videos, time_delta=time_delta)
        elif searchType == "Less than 4":
            videos_gen=api.yield_small_videos(niche=niche, language=language, region=region, num_videos=num_videos, time_delta=time_delta)
        for videos in videos_gen:
            channels=[api.get_channel_info_by_id(video.snippet.channelId) for video in videos]
            self.searchVideosResults.emit(videos, channels)
            if len(videos)>=num_videos:
                break
        self.searchVideosComplete.emit()


    @typed_signal.TypedSlot
    def onSearchChannelRequested(self, key: str, searchType: str, niche: str, num_channels: int, time_delta: int, min_subs: int, max_subs: int):
        api=self.getYouTubeAPI(key)
        channels_gen=api.yield_small_channels(niche=niche, num_channels=num_channels, time_delta=time_delta, subscriber_range=(min_subs, max_subs))
        for channels in channels_gen:
            if searchType == "Sort by Subs":
                self.searchChannelResults.emit(api.sort_by_subscribers(channels))
            elif searchType == "Sort by Views":
                self.searchChannelResults.emit(api.sort_by_recent_views(channels, time_delta))
            if len(channels)>=num_channels:
                break
        self.searchVideosComplete.emit()
        

    @typed_signal.TypedSlot
    def onSearchCommentsRequested(self, key: str, video_id: str, keywords: str, num_comments: int):
        api=self.getYouTubeAPI(key)
        comments_gen=api.yield_comments(video_id, keywords, num_comments)
        for comments in comments_gen:
            self.searchCommentsResults.emit(comments)
            if len(comments)>=num_comments:
                break
        self.searchVideosComplete.emit()