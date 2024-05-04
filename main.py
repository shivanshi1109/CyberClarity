import re
from youtube_transcript_api import YouTubeTranscriptApi
import os
from pytube import YouTube
from pydub import AudioSegment
from io import BytesIO

# 




# def extract_video_id(youtube_url):
#     (?<=v=): This is a positive lookbehind assertion. It asserts that what immediately precedes the current position in the string is "v=". This is used to find the position right after "v=" in the URL, indicating the start of the video ID.
# [a-zA-Z0-9_-]+: This part matches one or more characters that are either uppercase letters (A-Z), lowercase letters (a-z), digits (0-9), underscore (_), or hyphen (-). This allows us to match the video ID, which typically consists of a combination of these characters.
# (?=&|\?|$): This is a lookahead assertion. It asserts that what immediately follows the current position in the string is either "&" or "?" or the end of the string. This is used to ensure that we capture only the characters up to the next "&" or "?" (which could indicate additional parameters in the URL) or until the end of the string.
#     # Regular expression to extract video ID from YouTube URL
    # pattern = r"(?<=v=)[a-zA-Z0-9_-]+(?=&|\?|$)"
    # match = re.search(pattern, youtube_url)
    # if match:
    #     return match.group(0)
    # else:
    #     return None

# Example usage
# youtube_url = input("Youtube Link: ")
# video_id = extract_video_id(youtube_url)
# transcript={}
# texts=[]
# transcript=YouTubeTranscriptApi.get_transcript(video_id)


# texts = [item['text'] for item in transcript if 'text' in item]

# print(transcript)

# Function to download YouTube audio as an MP3 file
import os
from pytube import YouTube
from pydub import AudioSegment

# Function to download YouTube audio and convert it to MP3
def download_youtube_audio_as_mp3(video_url, output_path):
    try:
        # Get YouTube video
        yt = YouTube(video_url)
        
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Download audio
        audio_stream.download(output_path=output_path, filename="audio")

        # Convert to MP3 using Pydub
        audio_path = os.path.join(output_path, "audio.mp4")
        audio_segment = AudioSegment.from_file(audio_path)
        audio_segment.export(output_path, format="mp3")
        
        print("Audio saved as MP3:", output_path)
    except Exception as e:
        print("Error downloading audio:", str(e))

# Example usage
video_url = input("Youtube Link: ")
output_path = "./uploads"

download_youtube_audio_as_mp3(video_url, output_path)