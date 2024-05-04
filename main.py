from pytube import YouTube
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
import os

def download_youtube_audio(youtube_url, output_path):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename='./uploads/temp_audio.mp4')
    clip = mp.AudioFileClip('./uploads/temp_audio.mp4')
    clip.write_audiofile(output_path)
    clip.close()
    os.remove("./uploads/temp_audio.mp4")

youtube_url = input("Youtube Link: ")

output_path = './uploads/output_file.mp3'
download_youtube_audio(youtube_url, output_path)


# convert mp3 file to wav 
src=("./uploads/output_file.mp3")
sound = AudioSegment.from_mp3(src)
sound.export("./uploads/output_file.wav", format="wav")

file_audio = sr.AudioFile("./uploads/output_file.wav")

# use the audio file as the audio source                                        
r = sr.Recognizer()
with file_audio as source:
  audio_text = r.record(source)
  os.remove(src)

transcript = r.recognize_whisper(audio_text)
print(transcript)

# def chunk_audio_and_save(audio_path, chunk_length=60000):  # chunk_length in milliseconds
#     audio = AudioSegment.from_wav(audio_path)
#     length_audio = len(audio)
#     chunk_paths = []
#     for i, chunk in enumerate(range(0, length_audio, chunk_length)):
#         chunk_audio = audio[chunk:chunk + chunk_length]
#         chunk_path = f"temp_chunk_{i}.wav"
#         chunk_audio.export(chunk_path, format="wav")
#         chunk_paths.append(chunk_path)
#         # print(type(chunk_audio))
#         # print(r.recognize_google(chunk_audio))
#         # os.remove(chunk_audio)
        
#     return chunk_paths

# chunk_file_paths=chunk_audio_and_save('output_file.wav')

# for i, file_path in enumerate(chunk_file_paths):
#     print(f"Transcribing chunk {i+1}/{len(chunk_file_paths)}...")
#     transcript = r.recognize_whisper(file_path)
#     print(transcript)
#     os.remove(file_path)  # Clean up chunk file