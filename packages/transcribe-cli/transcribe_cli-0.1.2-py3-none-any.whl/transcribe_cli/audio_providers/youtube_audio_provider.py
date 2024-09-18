import yt_dlp
import os
from typing import Optional
from .audio_provider import AudioProvider

class YouTubeDownloadError(Exception):
    """Custom exception for YouTube download errors."""
    pass

class YouTubeAudioProvider(AudioProvider):
    def __init__(self, video_id: str, force_download: bool = False):
        self.output_dir = '.audio'
        self.video_id = video_id
        self.force_download = force_download

    def download_audio(self) -> Optional[str]:
        """
        Download audio from a YouTube video and save it as an MP3 file.
        
        Returns:
            Optional[str]: The path of the downloaded audio file, or None if download fails
        
        Raises:
            YouTubeDownloadError: If there's an error during the download process
        """
        try:
            output_path = os.path.join(self.output_dir, self.video_id)
            
            if os.path.exists(f"{output_path}.mp3") and not self.force_download:
                print(f"Audio file already exists: {output_path}.mp3")
                return f"{output_path}.mp3"
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_path + '.%(ext)s',
            }
            
            url = f"https://www.youtube.com/watch?v={self.video_id}"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if os.path.exists(f"{output_path}.mp3"):
                return f"{output_path}.mp3"
            else:
                raise YouTubeDownloadError(f"Failed to download audio for video ID: {self.video_id}")
        
        except yt_dlp.utils.DownloadError as e:
            raise YouTubeDownloadError(f"Error downloading audio: {str(e)}")
        except Exception as e:
            raise YouTubeDownloadError(f"Unexpected error during audio download: {str(e)}")
