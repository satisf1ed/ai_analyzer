import json
import os
import re

from dotenv import load_dotenv
from googleapiclient.discovery import build
import requests
import get_info

load_dotenv()

API_KEY = os.getenv("API_KEY")
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/'
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_channel_info(channel_id):
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics,topicDetails,status,brandingSettings,contentOwnerDetails,localizations',
         id=channel_id)

    # auditDetails - doesn't have permission; defaultLanguage, selfDeclaredMadeForKids, trackingAnalyticsAccountId,
    # contentOwner, timeLinked - None

    response = request.execute()

    channel_info = response['items'][0]
    return {
        'title': channel_info['snippet']['title'],
        'description': channel_info['snippet']['description'],
        'customUrl': channel_info['snippet']['customUrl'],
        'publishedAt': channel_info['snippet']['publishedAt'],
        'thumbnail': channel_info['snippet']['thumbnails']['default']['url'],
        'localizedTitle': channel_info['snippet']['localized']['title'],
        'localizedDescription': channel_info['snippet']['localized']['description'],
        'county': channel_info['snippet']['country'],
        'relatedPlaylistsLikes': channel_info['contentDetails']['relatedPlaylists']['likes'],
        'relatedPlaylistsUploads': channel_info['contentDetails']['relatedPlaylists']['uploads'],
        'viewCount': channel_info['statistics']['viewCount'],
        'subscribersCount': channel_info['statistics']['subscriberCount'],
        'hiddenSubscriberCount': channel_info['statistics']['hiddenSubscriberCount'],
        'videoCount': channel_info['statistics']['videoCount'],
        'topicCategories': channel_info['topicDetails']['topicCategories'],
        'privacyStatus': channel_info['status']['privacyStatus'],
        'isLinked': channel_info['status']['isLinked'],
        'longUploadsStatus': channel_info['status']['longUploadsStatus'],
        'madeForKids': channel_info['status']['madeForKids'],
        'brandingSettingsChannelTitle': channel_info['brandingSettings']['channel']['title'],
        'brandingSettingsChannelDescription': channel_info['brandingSettings']['channel']['description'],
        'brandingSettingsChannelKeywords': channel_info['brandingSettings']['channel']['keywords'],
        'brandingSettingsChannelUnsubscribedTrailer':
            channel_info['brandingSettings']['channel'].get('unsubscribedTrailer', ''),
    }


def get_latest_videos(channel_id, max_results=10):
    request = youtube.search().list(part='id', channelId=channel_id, order='date', maxResults=max_results)
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']
    return video_ids


def get_channel_handle_by_url(channel_url: str) -> str | None:
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/@([a-zA-Z0-9_-]+)',
    ]

    for pattern in patterns:
        match = re.match(pattern, channel_url)
        if match:
            return match.group(1)
    return None


def get_channel_id(channel_handle: str):
    api_url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {'part': 'contentDetails',
              'forHandle': '@' + channel_handle,
              'key': API_KEY}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['id']
        else:
            print("Канал не найден.")
            return None
    else:
        print(f"Ошибка запроса: {response.status_code}")
        return None


def main(channel_url: str):
    channel_handle = get_channel_handle_by_url(channel_url)
    channel_id = get_channel_id(channel_handle)
    print(channel_id)

    channel_info = get_channel_info(channel_id)
    print("Channel Info:", channel_info)

    video_ids = get_latest_videos(channel_id)
    for video_id in video_ids:
        video_info = get_info.get_video_details(video_id)
        print(video_info)


youtube_channel_url = input("Введите url канала YouTube: ")
main(youtube_channel_url)
