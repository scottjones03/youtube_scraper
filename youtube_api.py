# -----------------------------------------------------------------------------------------------------
# Youtube Minecraft Scraper - All Rights Reserved
# -----------------------------------------------------------------------------------------------------
# Copyright (C) Scott Jones - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Authors:
# - Scott Jones <scott.jones9336@gmail.com>
# -----------------------------------------------------------------------------------------------------
import datetime
from typing import List, Optional, Tuple
from black import Iterable
from pyyoutube import Api, Channel, Video, PlaylistItem, Comment
from youtubesearchpython import ChannelsSearch, VideosSearch, CustomSearch, VideoSortOrder, Comments

class YouTubeAPI:
    def __init__(self, api_key: str, language: str = "en", region: str = "US") -> None:
        self.api_key: str = api_key
        self.api: Api = Api(api_key=api_key)
        self.language: str = language
        self.region: str = region

    def _get_channel_info_by_id(self, channel_id: str) -> Optional[Channel]:
        channel_info_list: List[Channel] = self.api.get_channel_info(channel_id=channel_id, hl=f"{self.language}_{self.region}").items
        if len(channel_info_list) == 1:
            channel_info: Channel = channel_info_list[0]
            return channel_info
        else:
            return None

    def _get_channels_from_search(self, channel_search: ChannelsSearch, max_channels: int = 100) -> List[Channel]:
        channels: List[Channel] = []
        search_result = channel_search.result()
        if not isinstance(search_result, dict) or "result" not in search_result:
            return channels
        channels_ids_found: Iterable[str] = [channel["id"] for channel in search_result["result"]]
        for channel_id in channels_ids_found:
            if len(channels) == max_channels:
                break
            channel_info = self._get_channel_info_by_id(channel_id)
            if channel_info:
                channels.append(channel_info)
        return channels

    def _filter_subscribers(self, channels: List[Channel], subscriber_range: Tuple[int, int]) -> List[Channel]:
        filtered_channels: List[Channel] = []
        for channel in channels:
            subscribers = channel.statistics.subscriberCount
            if not subscribers:
                continue
            elif subscriber_range[0] < int(subscribers) and int(subscribers) < subscriber_range[1]:
                filtered_channels.append(channel)
        return filtered_channels

    def _filter_by_activity(self, channels: Iterable[Channel], min_activity: int = 1, time_delta: int = 14) -> List[Channel]:
        filtered_channels: List[Channel] = []
        for channel in channels:
            all_videos: List[Video] = self._get_uploads(channel_info=channel)
            recent_videos: List[Video] = [video for video in all_videos if self._isRecent(video, time_delta)]
            if len(recent_videos) >= min_activity:
                filtered_channels.append(channel)
        return filtered_channels         

    def sort_by_subscribers(self, channels: Iterable[Channel]) -> List[Channel]:
        filtered_channels: List[Channel] = [channel for channel in channels if channel.statistics.subscriberCount]
        return sorted(filtered_channels, key=lambda x: int(x.statistics.subscriberCount), reverse=True)
    
    def sort_by_recent_views(self, channels: Iterable[Channel], time_delta: int) -> List[Channel]:
        channels_with_views: List[dict] = []
        for channel in channels:
            all_videos: List[Video] = self._get_uploads(channel_info=channel)
            recent_videos: List[Video] = [video for video in all_videos if self._isRecent(video, time_delta)]
            recent_views: int = sum([int(video.statistics.viewCount) for video in recent_videos if video.statistics.viewCount])
            channels_with_views.append({"channel": channel, "views": recent_views})
        channels_with_views = sorted(channels_with_views, key=lambda d: d["views"], reverse=True)
        channels_sorted: List[Video] = [channel_views["channel"] for channel_views in channels_with_views]
        return channels_sorted   

    def get_small_channels(self, niche: str, num_channels: int = 100, time_delta: int = 14, subscriber_range: Tuple[int, int] = (1000, 200000)) -> List[Channel]:
        channel_search = ChannelsSearch(query=niche, language=self.language, region=self.region)
        channels: List[Channel] = []
        while len(channels) < num_channels*2:
            channels_found = self._get_channels_from_search(channel_search, num_channels)
            if not channels_found:
                return channels
            filtered_channels_by_subs = self._filter_subscribers(channels_found, subscriber_range)
            if not filtered_channels_by_subs:
                return channels
            channels = [*channels, *filtered_channels_by_subs]
            channel_search.next()
        active_channels = self._filter_by_activity(channels_found, time_delta=time_delta)
        return active_channels

    def _get_uploads(self, channel_info: Channel) -> List[Video]:
        uploads_id = channel_info.contentDetails.relatedPlaylists.uploads
        if not uploads_id:
            return []
        try:
            uploads_items_res = self.api.get_playlist_items(playlist_id=uploads_id, count=10, limit=6).items
        except:
            uploads_items_res = []
        videos = []
        for item in uploads_items_res:
            if not isinstance(item, PlaylistItem):
                continue
            video_id = item.contentDetails.videoId
            if not video_id:
                continue
            video_res: List[Video] = self.api.get_video_by_id(video_id=video_id).items
            if len(video_res) == 1:
                video = video_res[0]
                videos.append(video)
        return videos
    
    def _isRecent(self, video: Video, time_delta: int) -> bool:
        """
        Time Delta is in days.
        """
        unconv_video_time = video.snippet.publishedAt
        if not unconv_video_time:
            return False
        video_time = datetime.datetime.strptime(unconv_video_time, "%Y-%m-%dT%H:%M:%S%z")
        minimum_time = datetime.datetime.now(video_time.tzinfo) - datetime.timedelta(days=time_delta)
        return bool(video_time > minimum_time)

    def _isOldVideo(self, video: Video, time_delta: int) -> bool:
        """
        Time Delta is in years.
        """
        unconv_video_time = video.snippet.publishedAt
        if not unconv_video_time:
            return False
        video_time = datetime.datetime.strptime(unconv_video_time, "%Y-%m-%dT%H:%M:%S%z")
        maximum_time = datetime.datetime.now(video_time.tzinfo) - datetime.timedelta(days=int(time_delta*365))
        return bool(video_time < maximum_time)

    def _isPushed(self, video: Video) -> Tuple[bool, float]:
        views = video.statistics.viewCount
        channel_id = video.snippet.channelId
        if not views or not channel_id:
            return False, 0.0
        channel = self._get_channel_info_by_id(channel_id=channel_id)
        if not channel:
            return False, 0.0
        subscribers = channel.statistics.subscriberCount
        if subscribers:
            views=int(views)
            subscribers=int(subscribers)
            return bool((views / subscribers) > 1), float(views / subscribers)
        else:
            return False, 0.0

    def _get_video_info_by_id(self, video_id: str, language: Optional[str] = None, region: Optional[str] = None) -> Optional[Video]:
        if not language or not region:
            language = self.language
            region = self.region
        video_info_list: List[Video] = self.api.get_video_by_id(video_id=video_id, hl=f"{language}_{region}").items
        if len(video_info_list) == 1:
            video_info: Video = video_info_list[0]
            return video_info
        else:
            return None

    def _get_videos_from_search(self, video_search: CustomSearch, language: str, region: str, max_videos: int = 100) -> List[Video]:
        videos: List[Video] = []
        search_result = video_search.result()
        if not isinstance(search_result, dict) or "result" not in search_result:
            return videos
        video_ids_found: Iterable[str] = [video["id"] for video in search_result["result"]]
        for video_id in video_ids_found:
            if len(videos) == max_videos:
                break
            video_info = self._get_video_info_by_id(video_id=video_id, language=language, region=region)
            if video_info:
                videos.append(video_info)
        return videos

    def get_most_viewed_videos(self, niche: str, language: str, region: str, num_videos: int = 100, time_delta: int = 14) -> List[Video]:
        video_search = CustomSearch(query=niche, searchPreferences=VideoSortOrder.uploadDate)
        videos: List[Video] = []
        while len(videos) < num_videos**2:
            videos_found = self._get_videos_from_search(video_search, language, region, max_videos=num_videos)
            recent_videos = [video for video in videos_found if self._isRecent(video, time_delta)]
            if not recent_videos or not videos_found:
                break
            videos = [*videos, *recent_videos]
            video_search.next()
        if videos:
            most_viewed_videos = sorted(videos, key= lambda x: int(x.statistics.viewCount), reverse=True)[0: min(len(videos), num_videos)]
            return most_viewed_videos
        else:
            return videos

    def get_pushed_videos(self, niche: str, num_videos: int = 100, time_delta: int = 14) -> List[Video]:
        video_search = CustomSearch(query=niche, searchPreferences=VideoSortOrder.uploadDate)
        videos_with_score: List[dict] = []
        while len(videos_with_score) < num_videos:
            videos_found = self._get_videos_from_search(video_search, language=self.language, region=self.region, max_videos=num_videos)
            recent_videos = [video for video in videos_found if self._isRecent(video, time_delta)]
            if not recent_videos or not videos_found:
                break
            for video in recent_videos:
                isPushed, score = self._isPushed(video)
                if isPushed:
                    videos_with_score.append({"video": video, "score": score})
            video_search.next()
        if videos_with_score:
            sorted_by_score: List[dict] = sorted(videos_with_score, key= lambda x: x["score"], reverse=True)[0: min(len(videos_with_score), num_videos)]
            most_pushed_videos = [video_dict["video"] for video_dict in sorted_by_score]
            return most_pushed_videos
        else:
            return []

    def get_old_videos(self, niche: str, num_videos: int = 100, time_delta: int = 2) -> List[Video]:
        video_search = VideosSearch(query=niche)
        videos: List[Video] = []
        while len(videos) < num_videos:
            videos_found = self._get_videos_from_search(video_search, language=self.language, region=self.region, max_videos=num_videos)
            if not videos_found:
                break
            old_videos = [video for video in videos_found if self._isOldVideo(video, time_delta)]
            videos = [*videos, *old_videos]
            video_search.next()
        return videos

    def _get_comment_from_id(self, comment_id: str) -> Optional[Comment]:
        comment_info_list: List[Comment] = self.api.get_comment_by_id(comment_id=comment_id).items
        if len(comment_info_list) == 1:
            comment_info: Comment = comment_info_list[0]
            return comment_info
        else:
            return None

    def get_comments(self, video_id: str, query: Optional[str] = None, num_comments: int = 100) -> List[Comment]:
        comment_search = Comments(video_id)
        while comment_search.hasMoreComments:
            try:
                comment_search.getNextComments()
                comment_result = comment_search.comments
                if not isinstance(comment_result, dict) or "result" not in comment_result:
                    return []
                elif len(comment_result["result"]) > num_comments:
                    break
            except TypeError as err:
                print(err)
                break
        comment_ids = [comment["id"] for comment in comment_result["result"]]
        comments: List[Comment] = [self._get_comment_from_id(comment_id) for comment_id in comment_ids]
        comments_with_text = [comment for comment in comments if comment.snippet.textDisplay]
        if query:
            seperated_query = query.split(" ")
            comments_with_query = [comment for comment in comments_with_text if any([_query in comment.snippet.textDisplay for _query in seperated_query])]
            return comments_with_query
        else:
            return comments_with_text
        


            