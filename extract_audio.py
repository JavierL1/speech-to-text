import sys
from pathlib import Path

from moviepy.editor import VideoFileClip


INPUT_VIDEO_PATH = Path(sys.argv[1])
OUTPUT_AUDIO_PATH = Path(sys.argv[2])


def extract_audio(video_path):
    video = VideoFileClip(video_path)
    return video.audio


def save_audio(audio, audio_path):
    audio.write_audiofile(audio_path)


def extract_and_save_audio(video_path, audio_path):
    audio = extract_audio(video_path)
    save_audio(audio, audio_path)


if __name__ == '__main__':
    extract_and_save_audio(INPUT_VIDEO_PATH.as_posix(), OUTPUT_AUDIO_PATH.as_posix())
