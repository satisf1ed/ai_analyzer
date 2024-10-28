import requests
import os
import logging
from googleapiclient.discovery import build
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
logger = logging.getLogger(__name__)
API_KEY = os.getenv("API_KEY")
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/'
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_video_details(video_id: str) -> dict | None:
    url = f'{YOUTUBE_API_URL}videos'
    params = {
        'part': 'snippet,contentDetails,status,statistics,paidProductPlacementDetails',
        'id': video_id,
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(type(response.json()))
        video_info = response.json()['items'][0]
        answer = {
            'publishedAt': video_info.get('snippet', {}).get('publishedAt', None),
            'title': video_info.get('snippet', {}).get('title', None),
            'description': video_info.get('snippet', {}).get('description', None),
            'thumbnail': video_info.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', None),
            'channelTitle': video_info.get('snippet', {}).get('channelTitle', None),
            'tags': video_info.get('snippet', {}).get('tags', None),
            'liveBroadcastContent': video_info.get('snippet', {}).get('liveBroadcastContent', None),
            'defaultLanguage': video_info.get('snippet', {}).get('defaultLanguage', None),
            'defaultAudioLanguage': video_info.get('snippet', {}).get('defaultAudioLanguage', None),
            'category_id': video_info.get('snippet', {}).get('categoryId', None),
            'duration': video_info.get('contentDetails', {}).get('duration', None),
            'dimension': video_info.get('contentDetails', {}).get('dimension', None),
            'definition': video_info.get('contentDetails', {}).get('definition', None),
            'caption': video_info.get('contentDetails', {}).get('caption', None),
            'licensedContent': video_info.get('contentDetails', {}).get('licensedContent', None),
            'uploadStatus': video_info.get('status', {}).get('uploadStatus', None),
            'privacyStatus': video_info.get('status', {}).get('privacyStatus', None),
            'license': video_info.get('status', {}).get('license', None),
            'embeddable': video_info.get('status', {}).get('embeddable', None),
            'publicStatsViewable': video_info.get('status', {}).get('publicStatsViewable', None),
            'madeForKids': video_info.get('status', {}).get('madeForKids', None),
            'viewsCount': video_info.get('statistics', {}).get('viewCount', None),
            'likesCount': video_info.get('statistics', {}).get('likeCount', None),
            'favoriteCount': video_info.get('statistics', {}).get('favoriteCount', None),
            'comment_count': video_info.get('statistics', {}).get('commentCount', None),
        }
        return answer
    else:
        print(f'Error: {response.status_code}')
        return None


def get_channel_info(channel_id):
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics,topicDetails,status,brandingSettings,contentOwnerDetails,localizations',
        id=channel_id)

    # auditDetails - doesn't have permission;
    # defaultLanguage, selfDeclaredMadeForKids, trackingAnalyticsAccountId, contentOwner, timeLinked - None

    response = request.execute()
    channel_info = response['items'][0]
    return {
        'title': channel_info.get('snippet', {}).get('title', None),
        'description': channel_info.get('snippet', {}).get('description', None),
        'customUrl': channel_info.get('snippet', {}).get('customUrl', None),
        'publishedAt': channel_info.get('snippet', {}).get('publishedAt', None),
        'thumbnail': channel_info.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', None),
        'localizedTitle': channel_info.get('snippet', {}).get('localized', {}).get('title', None),
        'localizedDescription': channel_info.get('snippet', {}).get('localized', {}).get('description', None),
        'country': channel_info.get('snippet', {}).get('country', None),
        'relatedPlaylistsLikes': channel_info.get('contentDetails', {}).get('relatedPlaylists', {}).get('likes', None),
        'relatedPlaylistsUploads': channel_info.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads',
                                                                                                          None),
        'viewCount': channel_info.get('statistics', {}).get('viewCount', None),
        'subscribersCount': channel_info.get('statistics', {}).get('subscriberCount', None),
        'hiddenSubscriberCount': channel_info.get('statistics', {}).get('hiddenSubscriberCount', None),
        'videoCount': channel_info.get('statistics', {}).get('videoCount', None),
        'topicCategories': channel_info.get('topicDetails', {}).get('topicCategories', None),
        'privacyStatus': channel_info.get('status', {}).get('privacyStatus', None),
        'isLinked': channel_info.get('status', {}).get('isLinked', None),
        'longUploadsStatus': channel_info.get('status', {}).get('longUploadsStatus', None),
        'madeForKids': channel_info.get('status', {}).get('madeForKids', None),
        'brandingSettingsChannelTitle': channel_info.get('brandingSettings', {}).get('channel', {}).get('title', None),
        'brandingSettingsChannelDescription': channel_info.get('brandingSettings', {}).get('channel', {}).get(
            'description', None),
        'brandingSettingsChannelKeywords': channel_info.get('brandingSettings', {}).get('channel', {}).get('keywords',
                                                                                                           None),
        'brandingSettingsChannelUnsubscribedTrailer': channel_info.get('brandingSettings', {}).get('channel', {}).get(
            'unsubscribedTrailer', None),
    }


def deserialize_comment(comment: dict) -> dict:
    return {
        'authorDisplayName': comment.get('authorDisplayName', None),
        'authorProfileImageUrl': comment.get('authorProfileImageUrl', None),
        'authorChannelUrl': comment.get('authorChannelUrl', None),
        'authorChannelId': comment.get('authorChannelId', {}).get('value', None),
        'channelId': comment.get('channelId', None),
        'textDisplay': comment.get('textDisplay', None),
        'textOriginal': comment.get('textOriginal', None),
        'parentId': comment.get('parentId', None),
        'canRate': comment.get('canRate', None),
        'viewerRating': comment.get('viewerRating', None),
        'likeCount': comment.get('likeCount', None),
        'publishedAt': comment.get('publishedAt', None),
        'updatedAt': comment.get('updatedAt', None),
    }


def fetch_comments(video_id: str) -> list[dict]:
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    comments = []
    counter = 0
    response = youtube.commentThreads().list(
        part='snippet, replies',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100
    ).execute()
    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append(deserialize_comment(comment))
            counter += 1
            if 'replies' in item:
                for reply in item['replies']['comments']:
                    reply_comment = reply['snippet']
                    comments.append(deserialize_comment(reply_comment))
                    counter += 1
        logger.info(' Parsing successfully {counter} comments for video_id - {video_id}'.format(
            counter=counter, video_id=video_id))
        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=100,
                pageToken=response['nextPageToken']
            ).execute()
        else:
            break
    return comments


def get_transcript(video_id: str) -> list[dict]:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript
