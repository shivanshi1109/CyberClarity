import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(youtube_url):
#     (?<=v=): This is a positive lookbehind assertion. It asserts that what immediately precedes the current position in the string is "v=". This is used to find the position right after "v=" in the URL, indicating the start of the video ID.
# [a-zA-Z0-9_-]+: This part matches one or more characters that are either uppercase letters (A-Z), lowercase letters (a-z), digits (0-9), underscore (_), or hyphen (-). This allows us to match the video ID, which typically consists of a combination of these characters.
# (?=&|\?|$): This is a lookahead assertion. It asserts that what immediately follows the current position in the string is either "&" or "?" or the end of the string. This is used to ensure that we capture only the characters up to the next "&" or "?" (which could indicate additional parameters in the URL) or until the end of the string.
#     # Regular expression to extract video ID from YouTube URL
    pattern = r"(?<=v=)[a-zA-Z0-9_-]+(?=&|\?|$)"
    match = re.search(pattern, youtube_url)
    if match:
        return match.group(0)
    else:
        return None

# Example usage
youtube_url = "https://www.youtube.com/watch?v=n7uwj04E0I4"
video_id = extract_video_id(youtube_url)
transcript={}
texts=[]
transcript=YouTubeTranscriptApi.get_transcript(video_id)


texts = [item['text'] for item in transcript if 'text' in item]

print(texts)