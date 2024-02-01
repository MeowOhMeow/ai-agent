import os

from moviepy.editor import AudioFileClip

video_dir = "Convertor/videos"
audio_dir = "Convertor/audios"

for video_file in os.listdir(video_dir):
    if video_file.endswith(".mp4"):
        video_path = os.path.join(video_dir, video_file)
        audio_path = os.path.join(audio_dir, video_file.replace(".mp4", ".mp3"))
        print(f"Converting {video_path} to {audio_path}")
        AudioFileClip(video_path).write_audiofile(audio_path)
