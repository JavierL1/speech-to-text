import sys
import time
from pathlib import Path

from core.extract_audio import extract_and_save_audio
from core.speech_to_text import write_large_audio_transcription
from core.utils import seconds_to_human

if __name__ == '__main__':
    video_filename = input('Ingrese nombre del video. Ejemplo: video.mp4\n')
    start_time = time.time()
    video_filepath = Path('/data', video_filename)
    filename = video_filepath.with_suffix('').stem
    audio_path = video_filepath.parent / f'{filename}.mp3'
    text_path = video_filepath.parent / f'{filename}.txt'
    extract_and_save_audio(video_filepath, audio_path)
    write_large_audio_transcription(audio_path, text_path)
    elapsed_time_seconds = int(time.time() - start_time)
    print(f'Tiempo total de la ejecución: {seconds_to_human(elapsed_time_seconds)}')
