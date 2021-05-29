import sys
import time
from pathlib import Path

from core.extract_audio import extract_and_save_audio
from core.speech_to_text import write_large_audio_transcription
from core.utils import seconds_to_human

def translate_one_video_file(video_filename: str):
    start_time = time.time()
    video_filepath = Path('/data', video_filename)
    filename = video_filepath.with_suffix('').stem
    audio_path = video_filepath.parent / f'{filename}.mp3'
    text_path = video_filepath.parent / f'{filename}.txt'
    extract_and_save_audio(video_filepath, audio_path)
    write_large_audio_transcription(audio_path, text_path)
    elapsed_time_seconds = int(time.time() - start_time)
    print(f'Tiempo total de la ejecución: {seconds_to_human(elapsed_time_seconds)}')

if __name__ == '__main__':
    user_input = str(input('Ingrese nombre del video a traducir o escriba "todo" para traducir todos los videos en la carpeta. Ejemplo: video.mp4\n'))
    if user_input == 'todo':
        data_path = Path('/data')
        video_filenames = [p.name for p in data_path.iterdir() if p.name.endswith('.mp4')]
        print(f'Beginning to translate these videos: {video_filenames}')
        for filename in video_filenames:
            translate_one_video_file(filename)
    else:
        translate_one_video_file(user_input)
