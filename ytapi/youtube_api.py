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

    def get_channel_info_by_id(self, channel_id: str) -> Optional[Channel]:
        channel_info_list: List[Channel] = self.api.get_channel_info(channel_id=channel_id, hl=f"{self.language}_{self.region}").items
        if len(channel_info_list) == 1:
            channel_info: Channel = channel_info_list[0]
            return channel_info
        else:
            return None

    def _get_channels_from_search(self, channel_search: ChannelsSearch, max_channels: int = 100) -> List[Channel]:
        channels: List[Channel] = []
        try:
            search_result = channel_search.result()
        except:
            return []
        if not isinstance(search_result, dict) or "result" not in search_result:
            return channels
        channels_ids_found: Iterable[str] = [channel["id"] for channel in search_result["result"]]
        for channel_id in channels_ids_found:
            if len(channels) == max_channels:
                break
            channel_info = self.get_channel_info_by_id(channel_id)
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

    def yield_small_channels(self, niche: str, num_channels: int = 100, time_delta: int = 14, subscriber_range: Tuple[int, int] = (1000, 200000)) -> Iterable[List[Channel]]:
        channel_search = ChannelsSearch(query=niche, language=self.language, region=self.region)
        channels: List[Channel] = []
        while len(channels) <= num_channels:
            channels_found = self._get_channels_from_search(channel_search, num_channels)
            if not channels_found:
                break
            filtered_channels = self._filter_by_activity(self._filter_subscribers(channels_found, subscriber_range), time_delta=time_delta)
            for channel in filtered_channels:
                channels.append(channel)
            try:
                channel_search.next()
            except:
                break
            yield channels
        yield channels

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
        elif "T" not in unconv_video_time:
            return False

        video_time = datetime.datetime.strptime(unconv_video_time.split("T")[0], r"%Y-%m-%d")
        minimum_time = datetime.datetime.now(video_time.tzinfo) - datetime.timedelta(days=time_delta)
        return bool(video_time.date()>minimum_time.date())

    @staticmethod
    def getDuration(duration: str) -> float:
        d=duration.replace("P", "").replace("T", "")
        dhoursInMins=0
        dMins=0
        dSecondsInMins=0.0
        for key in ("Y","D","H","M", "S"):
            if key in d and (key=="Y" or key=="D"):
                d=d.split(key)[1]
            elif key in d and (key=="H"):
                dhoursInMins=60*int(d.split(key)[0])
                d=d.split(key)[1]
            elif key in d and (key=="M"):
                dMins=int(d.split(key)[0])
                d=d.split(key)[1]
            elif key in d and (key=="S"):
                dSecondsInMins=int(d.split(key)[0])/60
        return round(float(dMins+dhoursInMins+dSecondsInMins), 2)

    
    def _isShort(self, video: Video, time: int = 4) -> bool:
        """
        Time Delta is in days.
        """
        dur=self.getDuration(video.contentDetails.duration)
        if dur==0:
            return False
        return bool(dur < time)

    def _isOldVideo(self, video: Video, time_delta: int) -> bool:
        """
        Time Delta is in years.
        """
        unconv_video_time = video.snippet.publishedAt
        if not unconv_video_time:
            return False
        elif "T" not in unconv_video_time:
            return False
        video_time = datetime.datetime.strptime(unconv_video_time.split("T")[0], "%Y-%m-%d")
        maximum_time = datetime.datetime.now(video_time.tzinfo) - datetime.timedelta(days=int(time_delta*365))
        return bool(video_time.date() < maximum_time.date())

    def _isPushed(self, video: Video) -> Tuple[bool, float]:
        views = video.statistics.viewCount
        channel_id = video.snippet.channelId
        if not views or not channel_id:
            return False, 0.0
        channel = self.get_channel_info_by_id(channel_id=channel_id)
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

    def _get_videos_from_search(self, video_search: CustomSearch, language: str, region: str) -> List[Video]:
        videos: List[Video] = []
        try:
            search_result = video_search.result()
        except:
            return []
        if not isinstance(search_result, dict) or "result" not in search_result:
            return videos
        video_ids_found: Iterable[str] = [video["id"] for video in search_result["result"]]
        for video_id in video_ids_found:
            video_info = self._get_video_info_by_id(video_id=video_id, language=language, region=region)
            if video_info:
                videos.append(video_info)
        return videos

    def _set_language_region(self, language: str, region: str) -> None:
        self.language=language
        self.region=region

    def yield_most_viewed_videos(self, niche: str, num_videos: int, language: str, region: str, time_delta: int = 14) -> Iterable[List[Video]]:
        self._set_language_region(language, region)
        video_search = CustomSearch(query=niche, searchPreferences=VideoSortOrder.uploadDate, language=language, region=region)
        videos: List[Video] = []
        notRecent=False
        while len(videos) < num_videos**20:
            videos_found = self._get_videos_from_search(video_search, language, region)
            for video in videos_found:
                if not self._isRecent(video, time_delta):
                    videos_found.remove(video)
                    notRecent=True
            if not videos_found or notRecent:
                break
            for video in videos_found:
                videos.append(video)
            try:
                video_search.next()
            except:
                break
            yield sorted(videos, key= lambda x: int(x.statistics.viewCount), reverse=True)[0: min(len(videos), num_videos)]
        if videos:
            most_viewed_videos = sorted(videos, key= lambda x: int(x.statistics.viewCount), reverse=True)[0: min(len(videos), num_videos)]
            yield most_viewed_videos

    def yield_small_videos(self, niche: str, language: str, region: str, num_videos: int = 100, time_delta: int = 14) -> Iterable[List[Video]]:
        self._set_language_region(language, region)
        video_search = CustomSearch(query=niche, searchPreferences=VideoSortOrder.uploadDate, language=language, region=region)
        videos: List[Video] = []
        notRecent=False
        while len(videos) < num_videos**20:
            videos_found = self._get_videos_from_search(video_search, language, region)
            for video in videos_found:
                if not self._isRecent(video, time_delta):
                    videos_found.remove(video)
                    notRecent=True
            if not videos_found or notRecent:
                break
            for video in videos_found:
                if self._isShort(video):
                    videos.append(video)
            try:
                video_search.next()
            except:
                break
            yield sorted(videos, key= lambda x: int(x.statistics.viewCount), reverse=True)[0: min(len(videos), num_videos)]
        if videos:
            small_videos_by_views = sorted(videos, key= lambda x: int(x.statistics.viewCount), reverse=True)[0: min(len(videos), num_videos)]
            yield small_videos_by_views

    def yield_pushed_videos(self, niche: str, language: str, region: str, num_videos: int = 100, time_delta: int = 14) -> Iterable[List[Video]]:
        self._set_language_region(language, region)
        video_search = CustomSearch(query=niche, searchPreferences=VideoSortOrder.uploadDate, language=language, region=region)
        videos_with_score: List[dict] = []
        notRecent=False
        while len(videos_with_score) < num_videos:
            videos_found = self._get_videos_from_search(video_search, language=self.language, region=self.region)
            for video in videos_found:
                if not self._isRecent(video, time_delta):
                    videos_found.remove(video)
                    notRecent=True
            if not videos_found or notRecent:
                break
            for video in videos_found:
                isPushed, score = self._isPushed(video)
                if isPushed:
                    videos_with_score.append({"video": video, "score": score})
            try:
                video_search.next()
            except:
                break
            yield [video_dict["video"] for video_dict in sorted(videos_with_score, key= lambda x: x["score"], reverse=True)[0: min(len(videos_with_score), num_videos)]]
        if videos_with_score:
            sorted_by_score: List[dict] = sorted(videos_with_score, key= lambda x: x["score"], reverse=True)[0: min(len(videos_with_score), num_videos)]
            most_pushed_videos = [video_dict["video"] for video_dict in sorted_by_score]
            yield most_pushed_videos

    def yield_old_videos(self, niche: str, language: str, region: str, num_videos: int = 100, time_delta: int = 2) -> Iterable[List[Video]]:
        self._set_language_region(language, region)
        video_search = VideosSearch(query=niche, language=language, region=region)
        videos: List[Video] = []
        while len(videos) < num_videos:
            videos_found = self._get_videos_from_search(video_search, language=self.language, region=self.region, max_videos=num_videos)
            if not videos_found:
                break
            for video in videos_found:
                if self._isOldVideo(video, time_delta):
                    videos.append(video)
            try:
                video_search.next()
            except:
                break
            yield videos
        yield videos

    def _get_comment_from_id(self, comment_id: str) -> Optional[Comment]:
        comment_info_list: List[Comment] = self.api.get_comment_by_id(comment_id=comment_id).items
        if len(comment_info_list) == 1:
            comment_info: Comment = comment_info_list[0]
            return comment_info
        else:
            return None

    def yield_comments(self, video_id: str, query: Optional[str] = None, num_comments: int = 100) -> Iterable[List[Comment]]:
        comment_search = Comments(video_id)
        while comment_search.hasMoreComments:
            try:
                comment_search.getNextComments()
                comment_result = comment_search.comments
                comment_ids = [comment["id"] for comment in comment_result["result"]]
                comments: List[Comment] = [self._get_comment_from_id(comment_id) for comment_id in comment_ids]
                if query:
                    seperated_query = query.lower().split(" ")
                    comments_with_query = [comment for comment in comments if comment.snippet.textDisplay and any([_query in comment.snippet.textDisplay.lower() for _query in seperated_query])]
                    yield comments_with_query
                else:
                    comments_with_text = [comment for comment in comments if comment.snippet.textDisplay]
                    yield comments_with_text
                if not isinstance(comment_result, dict) or "result" not in comment_result:
                    return []
                elif len(comment_result["result"]) > num_comments:
                    break
            except TypeError as err:
                print(err)
                break
        
        


            
