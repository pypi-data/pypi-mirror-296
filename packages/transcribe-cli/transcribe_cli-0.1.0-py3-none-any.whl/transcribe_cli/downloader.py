from urllib.parse import urlparse, parse_qs
from typing import Union

def extract_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube URL.
    
    Args:
        url (str): YouTube video URL
    
    Returns:
        str: Video ID
    
    Raises:
        ValueError: If the video ID cannot be extracted from the URL
    """
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.netloc in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            p = parse_qs(parsed_url.query)
            return p['v'][0]
        if parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        if parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]
    raise ValueError(f"Could not extract video ID from URL: {url}")

def create_youtube_timestamp_link(video_id: str, start_ms: Union[int, str]) -> str:
    """
    Create a YouTube timestamp link.
    
    Args:
        video_id (str): YouTube video ID
        start_ms (Union[int, str]): Start time in milliseconds or HH:MM:SS format
    
    Returns:
        str: YouTube timestamp link
    """
    if isinstance(start_ms, str):
        # If start_ms is in HH:MM:SS format, convert it to seconds
        h, m, s = map(int, start_ms.split(':'))
        start_seconds = h * 3600 + m * 60 + s
    else:
        # If start_ms is in milliseconds, convert it to seconds
        start_seconds = int(start_ms / 1000)
    return f"https://www.youtube.com/watch?v={video_id}&t={start_seconds}s"
