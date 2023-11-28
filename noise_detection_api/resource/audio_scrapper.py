import os
from moviepy.editor import VideoFileClip

class AudioScrapper():
    def __str__(self):
        """Returns a string representation of the class."""

    def scrape_audio(video_file, output_ext="mp3"):
        filename, ext = os.path.splitext(video_file) # get file path without extension
        video = VideoFileClip(video_file) # load video file
        audio = video.audio # get audio from video
        filename = filename.replace("video_files", "audio_files")
        audio.write_audiofile(f"{filename}.{output_ext}")
        filename = os.path.basename(filename) # get file name
        return f"audio_files/{filename}.{output_ext}" # return audio file.