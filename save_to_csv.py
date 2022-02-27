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
import pandas as pd
from pyyoutube import Video, Channel, Comment
from typing import List, Optional, Dict

from ytapi.explorer_app import ExplorerApp

class StoredYoutubeData:
    def __init__(self) -> None:
        ...

    def get_videos_dict(self, videos: List[Video]) -> Dict[str, list]:
        video_ids: List[str] = []
        video_titles: List[str] = []
        channel_ids_titles: List[str] = []
        published_ats: List[Optional[str]] = []
        view_counts: List[Optional[int]] = []
        like_counts: List[Optional[int]] = []
        comment_counts: List[Optional[int]] = []
        for video in videos:
            video_ids.append(video.id)
            video_titles.append(video.snippet.title)
            channel_id_title = f"{video.snippet.channelTitle}:{video.snippet.channelId}"
            channel_ids_titles.append(channel_id_title)
            published_ats.append(video.snippet.publishedAt)
            view_counts.append(video.statistics.viewCount)
            like_counts.append(video.statistics.likeCount)
            comment_counts.append(video.statistics.commentCount)
        video_dict: Dict[str, list] = {
            "Video ID": video_ids,
            "Video Title": video_titles,
            "Upload date": published_ats,
            "Views": view_counts,
            "Likes": like_counts,
            "Number of Comments": comment_counts,
            "Channel ID: Name": channel_ids_titles,
        }
        return video_dict

    def save_videos_to_file(self, videos: List[Video]) -> None:
        video_dict=self.get_videos_dict(videos)
        video_dataframe = pd.DataFrame(video_dict)
        path = ExplorerApp().saveFilePathDialog(
            nameFilter="CSV Files (*.csv);; Excel Files (*.xlsx)",
            title="Save Videos details found",
        )
        if not path:
            return None
        if path.suffix == ".csv":
            video_dataframe.to_csv(path)
        elif path.suffix == ".xlsx":
            video_dataframe.to_excel(path)
        else:
            raise Exception("File saved in the wrong format.")

    def get_channels_dict(self, channels: List[Channel]) -> Dict[str, list]:
        channel_ids: List[str] = []
        channel_titles: List[str] = []
        subscriber_counts: List[Optional[int]] = []
        view_counts: List[Optional[int]] = []
        video_counts: List[Optional[int]] = []
        countrys: List[Optional[str]] = []
        for channel in channels:
            channel_ids.append(channel.id)
            channel_titles.append(channel.snippet.title)
            subscriber_counts.append(channel.statistics.subscriberCount)
            view_counts.append(channel.statistics.viewCount)
            video_counts.append(channel.statistics.videoCount)
            countrys.append(channel.snippet.country)
        channel_dict: Dict[str, list] = {
            "Channel ID": channel_ids,
            "Channel Name": channel_titles,
            "Subscribers": subscriber_counts,
            "Views": view_counts,
            "Number of Videos": video_counts,
            "Country": countrys
        }
        return channel_dict

    def save_channels_to_file(self, channels: List[Channel]) -> None:
        channel_dict = self.get_channels_dict(channels)
        channel_dataframe = pd.DataFrame(channel_dict)
        path = ExplorerApp().saveFilePathDialog(
            nameFilter="CSV Files (*.csv);; Excel Files (*.xlsx)",
            title="Save Channels details found",
        )
        if not path:
            return None
        if path.suffix == ".csv":
            channel_dataframe.to_csv(path)
        elif path.suffix == ".xlsx":
            channel_dataframe.to_excel(path)
        else:
            raise Exception("File saved in the wrong format.")

    def get_comments_dict(self, comments: List[Comment]) -> Dict[str, list]:
        author_names: List[Optional[str]] = []
        display_texts: List[Optional[str]] = []
        like_counts: List[Optional[int]] = []
        viewer_ratings: List[Optional[str]] = []
        for comment in comments:
            author_names.append(comment.snippet.authorDisplayName)
            display_texts.append(comment.snippet.textDisplay)
            like_counts.append(comment.snippet.likeCount)
            viewer_ratings.append(comment.snippet.viewerRating)
        comments_dict: Dict[str, list] = {
            "Author Name": author_names,
            "Text": display_texts,
            "Likes": like_counts,
            "Viewer Rating": viewer_ratings,
        }
        return comments_dict

    def save_comments_to_file(self, comments: List[Comment]) -> None:
        comments_dict = self.get_comments_dict(comments)
        comments_dataframe = pd.DataFrame(comments_dict)
        path = ExplorerApp().saveFilePathDialog(
            nameFilter="CSV Files (*.csv);; Excel Files (*.xlsx)",
            title="Save Comments found",
        )
        if not path:
            return None
        if path.suffix == ".csv":
            comments_dataframe.to_csv(path)
        elif path.suffix == ".xlsx":
            comments_dataframe.to_excel(path)
        else:
            raise Exception("File saved in the wrong format.")


        

        