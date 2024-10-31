import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
import get_info

load_dotenv()

API_KEY = os.getenv("API_KEY")
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/'
youtube = build('youtube', 'v3', developerKey=API_KEY)

video_id = input("Enter Video ID: ")
get_info.get_video_details(video_id)
get_info.fetch_comments(video_id)
