import requests
import os
import logging
from googleapiclient.discovery import build
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

API_KEY = os.getenv("API_KEY")
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/'
logger = logging.getLogger(__name__)


def search_last_videos_by_category(category_id: int, max_results: int) -> dict | None:
    url = f'{YOUTUBE_API_URL}search'
    params = {
        'part': 'snippet',
        'type': 'video',
        'videoCategoryId': str(category_id),
        'maxResults': max_results,
        'order': 'date',
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return None


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
            'publishedAt': video_info['snippet']['publishedAt'],
            'title': video_info['snippet']['title'],
            'description': video_info['snippet']['description'],
            'thumbnail': video_info['snippet']['thumbnails']['default']['url'],
            'channelTitle': video_info['snippet']['channelTitle'],
            'tags': video_info['snippet'].get(['tags'], []),
            'liveBroadcastContent': video_info['snippet']['liveBroadcastContent'],
            'defaultLanguage': video_info['snippet'].get('defaultLanguage', None),
            'defaultAudioLanguage': video_info['snippet'].get('defaultAudioLanguage', None),
            'category_id': video_info['snippet']['categoryId'],
            'duration': video_info['contentDetails']['duration'],
            'dimension': video_info['contentDetails']['dimension'],
            'definition': video_info['contentDetails']['definition'],
            'caption': video_info['contentDetails']['caption'],
            'licensedContent': video_info['contentDetails']['licensedContent'],
            'uploadStatus': video_info['status']['uploadStatus'],
            'privacyStatus': video_info['status']['privacyStatus'],
            'license': video_info['status']['license'],
            'embeddable': video_info['status']['embeddable'],
            'publicStatsViewable': video_info['status']['publicStatsViewable'],
            'madeForKids': video_info['status']['madeForKids'],
            'viewsCount': video_info['statistics'].get('viewCount', 0),
            'likesCount': video_info['statistics'].get('likeCount', 0),
            'favoriteCount': video_info['statistics'].get('favoriteCount', 0),
            'comment_count': video_info['statistics'].get('commentCount', 0),
            }
        return answer
    else:
        print(f'Error: {response.status_code}')
        return None


def deserialize_comment(comment: dict) -> dict:
    return {
                'authorDisplayName': comment['authorDisplayName'],
                'authorProfileImageUrl': comment['authorProfileImageUrl'],
                'authorChannelUrl': comment['authorChannelUrl'],
                'authorChannelId': comment['authorChannelId']['value'],
                'channelId': comment['channelId'],
                'textDisplay': comment['textDisplay'],
                'textOriginal': comment['textOriginal'],
                'parentId': comment.get('parentId', None),
                'canRate': comment['canRate'],
                'viewerRating': comment['viewerRating'],
                'likeCount': comment['likeCount'],
                'publishedAt': comment['publishedAt'],
                'updatedAt': comment['updatedAt'],
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


def get_info_from_last_videos_in_category(category_id: int, max_results=10) -> None:
    list_of_videos = search_last_videos_by_category(category_id, max_results)

    if list_of_videos:
        for idx, item in enumerate(list_of_videos['items'], start=1):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            print(f'{idx}. Video ID: {video_id}, Title: {title}')
            video_details = get_video_details(video_id)
            print(video_details)

            print("Comments")
            video_comments = fetch_comments(video_id)
            print(video_comments)

            print("Transcript")
            transcript = get_transcript(video_id)
            print(transcript)


if __name__ == '__main__':
    get_info_from_last_videos_in_category(28, 1)
