import requests
import os
import logging
from googleapiclient.discovery import build
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from save_info import save_channel_info, save_video_info, save_comments, check_exists_channel_by_id

load_dotenv()
logger = logging.getLogger(__name__)
API_KEY = os.getenv("API_KEY")
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/'
youtube = build('youtube', 'v3', developerKey=API_KEY)


def get_video_details(video_id: str) -> bool | None:
    url = f'{YOUTUBE_API_URL}videos'
    params = {
        'part': 'snippet,contentDetails,status,statistics,paidProductPlacementDetails',
        'id': video_id,
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        video_info = response.json()['items'][0]
        channel_id = video_info['snippet']['channelId']
        if not check_exists_channel_by_id(channel_id):
            get_channel_info(channel_id)
        save_video_info(video_info, channel_id, video_id)
        return True
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
    save_channel_info(channel_info, channel_id)


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
            comment_id = item['snippet']['topLevelComment']['id']
            comment = item['snippet']['topLevelComment']['snippet']
            save_comments(comment, comment_id)
            counter += 1
            if 'replies' in item:
                for reply in item['replies']['comments']:
                    reply_comment_id = reply['id']
                    reply_comment = reply['snippet']
                    save_comments(reply_comment, reply_comment_id)
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
