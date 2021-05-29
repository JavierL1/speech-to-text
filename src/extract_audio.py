import sys
import time
from pathlib import Path

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip

from .utils import seconds_to_human

INPUT_VIDEO_PATH = Path(sys.argv[1])
OUTPUT_AUDIO_PATH = Path(sys.argv[2])


def extract_audio(video_path: Path) -> AudioFileClip:
    video = VideoFileClip(video_path)
    return video.audio


def save_audio(audio: AudioFileClip, audio_path: Path):
    audio.write_audiofile(audio_path)


def extract_and_save_audio(video_path: Path, audio_path: Path):
    start_time = time.time()
    print('Extrayendo audio desde el video...')
    audio = extract_audio(video_path)
    save_audio(audio, audio_path)
    print(f'Audio extraido se encuentra en {audio_path}')
    time_elapsed_seconds = int(time.time() - start_time)
    print(f'Operación completada en {seconds_to_human(time_elapsed_seconds)}')


if __name__ == '__main__':
    extract_and_save_audio(INPUT_VIDEO_PATH.as_posix(), OUTPUT_AUDIO_PATH.as_posix())
