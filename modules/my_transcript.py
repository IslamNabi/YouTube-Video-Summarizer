from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
import re

def get_video_id(url: str) -> str:
    """Extract video ID from any YouTube URL format"""
    clean_url = url.split('&')[0].split('#')[0]
    
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",  # Standard URLs
        r"youtu.be\/([0-9A-Za-z_-]{11})",  # Short URLs
        r"embed\/([0-9A-Za-z_-]{11})",     # Embedded URLs
        r"shorts\/([0-9A-Za-z_-]{11})"     # Shorts URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_url)
        if match:
            return match.group(1)
    
    try:
        yt = YouTube(clean_url)
        if not yt.video_id:
            raise ValueError("Could not extract video ID")
        return yt.video_id
    except Exception as e:
        raise ValueError(f"Invalid YouTube URL: {str(e)}")

def get_transcript(video_url: str, languages: list = ['en']) -> str:
    try:
        video_id = get_video_id(video_url)
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=languages)
        return " ".join([entry.text for entry in transcript])
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as yt_err:
        raise Exception(f"Transcript not available: {str(yt_err)}")
    except Exception as e:
        raise Exception(f"Error getting transcript: {str(e)}")
