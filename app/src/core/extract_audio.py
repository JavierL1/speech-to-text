import time
from pathlib import Path

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip

from .utils import seconds_to_human


def extract_audio(video_path: Path) -> AudioFileClip:
    video = VideoFileClip(video_path)
    return video.audio


def save_audio(audio: AudioFileClip, audio_path: Path):
    audio.write_audiofile(audio_path, fps=16000)


def extract_and_save_audio(video_path: Path, audio_path: Path):
    start_time = time.time()
    print('Revisando si audio ya fue extraído...')
    if audio_path.exists():
        print('Se encontró audio extraido')
        return

    print('No se encontró audio')
    print(f'Extrayendo audio desde el video {video_path.as_posix()}...')
    audio = extract_audio(video_path.as_posix())
    save_audio(audio, audio_path.as_posix())
    print(f'Audio extraido se encuentra en {audio_path}')
    time_elapsed_seconds = int(time.time() - start_time)
    print(f'Operación completada en {seconds_to_human(time_elapsed_seconds)}')
