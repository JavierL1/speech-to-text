import sys
import time
from pathlib import Path

from .extract_audio import extract_and_save_audio
from .speech_to_text import write_large_audio_transcription
from .utils import seconds_to_human

INPUT_VIDEO_FILE_PATH = Path(sys.argv[1])


if __name__ == '__main__':
    start_time = time.time()
    filename = INPUT_VIDEO_FILE_PATH.with_suffix('').stem
    audio_path = INPUT_VIDEO_FILE_PATH.parent / filename / '.mp3'
    text_path = INPUT_VIDEO_FILE_PATH.parent / filename / '.txt'
    extract_and_save_audio(INPUT_VIDEO_FILE_PATH, audio_path)
    write_large_audio_transcription(audio_path, text_path)
    elapsed_time_seconds = int(time.time() - start_time)
    print(f'Tiempo total de la ejecución: {seconds_to_human(elapsed_time_seconds)}')
