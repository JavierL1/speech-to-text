import os
import time
import pickle
from pathlib import Path
from typing import Generator

import speech_recognition as sr 
from pydub import AudioSegment
from tqdm import tqdm

from .subtitles import SRTEntry, write_srt_file
from .utils import AudioChunk, custom_split_on_silence, seconds_to_human

# create a speech recognition object
r = sr.Recognizer()

def write_text_to_file(file_path: Path, text: str):
    with open(file_path, 'a') as file:
        file.write(text)


def generate_srt_entries_from_audio_chunks(audio_chunks: list[AudioChunk]) -> Generator[SRTEntry]:

    folder_name = 'audio-chunks'

    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    print(f'Traduciendo {len(audio_chunks)} segmentos...\n')
    # process each chunk

    for i, audio_chunk in tqdm(enumerate(audio_chunks, start=1)):
        seconds_passed_str = str(audio_chunk.end)
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.audio.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                translation = r.recognize_google(audio_listened, language='pt-BR')
            except sr.UnknownValueError as e:
                yield SRTEntry(
                    start_time=audio_chunk.start,
                    end_time=audio_chunk.end,
                    content='No se pudo traducir este segmento :('
                )
            else:
                yield SRTEntry(
                    start_time=audio_chunk.start,
                    end_time=audio_chunk.end,
                    content=translation.capitalize()
                )

        if os.path.exists(chunk_filename):
            os.remove(chunk_filename)


# a function that splits the audio file into chunks
# and applies speech recognition
def write_large_audio_transcription(audio_path: Path, srt_path: Path):
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

    filename = audio_path.with_suffix('').stem
    pickle_path = audio_path.parent / f'{filename}.pkl'
    print(f'Audio completo dura: {seconds_to_human(sound.duration_seconds)}')
    print('Dividiendo audio completo según silencios encontrados')
    print('Revisando si audio ya fue segmentado...')
    if pickle_path.exists():
        print('Se encontraron segmentos. Cargando...')
        with open(pickle_path, 'rb') as pickle_file:
            audio_chunks = pickle.load(pickle_file)
            print('Segmentos cargados.')
    else:
        print('No se encontraron segmentos generados')
        print('Generando segmentos...')
        # split audio sound where silence is 700 miliseconds or more and get chunks
        audio_chunks = custom_split_on_silence(
            sound,
            # experiment with this value for your target audio file
            min_silence_len = 1000,
            silence_thresh=sound.dBFS-20,
            # keep the silence for 1 second, adjustable as well
            keep_silence=500,
        )
        seconds_generating_segments = int(time.time() - start_time)
        print(f'Se generaron {len(audio_chunks)} segmentos de audio en {seconds_to_human(seconds_generating_segments)}')

        print(f'Guardando segmentos en {pickle_path}')
        with open(pickle_path, 'wb') as pickle_file:
            pickle.dump(sound, pickle_file)
        print('Segmentos guardados')

    srt_entries = generate_srt_entries_from_audio_chunks(audio_chunks)
    write_srt_file(srt_path=srt_path, srt_entries=srt_entries)

    print('Traducción completada.')
    print(f'Texto escrito en {srt_path}')
