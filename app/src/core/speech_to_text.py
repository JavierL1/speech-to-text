import os
import time
from pathlib import Path

import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm

from .utils import seconds_to_human

# create a speech recognition object
r = sr.Recognizer()

def write_text_to_file(file_path: Path, text: str):
    with open(file_path, 'a') as file:
        file.write(text)


# a function that splits the audio file into chunks
# and applies speech recognition
def write_large_audio_transcription(audio_path: Path, text_path: Path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    start_time = time.time()
    # open the audio file using pydub
    print('Cargando archivo de audio...')
    try:
        sound = AudioSegment.from_mp3(audio_path)
    except Exception as e:
        print(e)

    print(f'Audio completo dura: {seconds_to_human(sound.duration_seconds)}')
    print('Dividiendo audio completo según silencios encontrados')
    print('Esto demora bastante uwu...')
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(
        sound,
        # experiment with this value for your target audio file
        min_silence_len = 1000,
        silence_thresh=sound.dBFS-20,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    seconds_generating_segments = int(time.time() - start_time)
    print(f'Se generaron {len(chunks)} segmentos de audio en {seconds_to_human(seconds_generating_segments)}')
    seconds_passed = 0
    print('Traduciendo segmentos...\n')
    # process each chunk 
    for i, audio_chunk in tqdm(enumerate(chunks, start=1)):
        seconds_passed += audio_chunk.duration_seconds
        seconds_passed_str = seconds_to_human(seconds_passed)
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language='pt-BR')
            except sr.UnknownValueError as e:
                write_text_to_file('No se pudo traducir este segmento :( \n')
            else:
                write_text_to_file(text_path, f'{text.capitalize()}. \n')

            write_text_to_file(text_path, f'{seconds_passed_str}. \n')

        if os.path.exists(chunk_filename):
            os.remove(chunk_filename)
    print('Traducción completada.')
    print(f'Texto escrito en {text_path}')
