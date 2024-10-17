import requests
import json
import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

API_KEY = os.getenv("API_KEY")
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/'


def search_last_videos_by_category(category_id, max_results):
    url = f'{YOUTUBE_API_URL}search'
    params = {
        'part': 'snippet',
        'type': 'video',
        'videoCategoryId': category_id,
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


def get_video_details(video_id):
    url = f'{YOUTUBE_API_URL}videos'
    params = {
        'part': 'snippet,contentDetails,status,statistics,paidProductPlacementDetails',
        'id': video_id,
        'key': API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        video_info = response.json()['items'][0]
        answer = {
            'title': video_info['snippet']['title'],
            'description': video_info['snippet']['description'],
            'published_at': video_info['snippet']['publishedAt'],
            'duration': video_info['contentDetails']['duration'],
            'views': video_info['statistics'].get('viewCount', 0),
            'likes': video_info['statistics'].get('likeCount', 0),
            'dislikes': video_info['statistics'].get('dislikeCount', 0),
            'comment_count': video_info['statistics'].get('commentCount', 0),
            'tags': video_info['snippet'].get('tags', []),
            'category_id': video_info['snippet']['categoryId'],
            'thumbnail': video_info['snippet']['thumbnails']['default']['url']}
        return answer
    else:
        print(f'Error: {response.status_code}')
        return None


def fetch_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    while len(comments) < 10000:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=1
        ).execute()
        while response:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'User': comment['authorDisplayName'],
                    'Comment': comment['textDisplay']
                })
                if 'nextPageToken' in response:
                    response = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        textFormat='plainText',
                        maxResults=100,
                        pageToken=response['nextPageToken']
                    ).execute()
                    break
                else:
                    break
    return pd.DataFrame(comments)


def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript('QMbx0dTWJIQ')
    return transcript


def get_info_from_last_videos_in_category(category_id, max_results=10):
    list_of_videos = search_last_videos_by_category(category_id, max_results)

    if list_of_videos:
        for idx, item in enumerate(list_of_videos['items'], start=1):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            print(f'{idx}. Video ID: {video_id}, Title: {title}')
            video_details = get_video_details(video_id)
            print(video_details)

            print("Comments")
            video_comments = fetch_comments(video_id, API_KEY)
            video_comments.head()

            print("Transcript")
            transcript = get_transcript(video_id)
            print(transcript)


get_info_from_last_videos_in_category(28, 3)