import datetime
import os
import sys
from pathlib import Path

import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence

INPUT_AUDIO_PATH = Path(sys.argv[1])
OUTPUT_TEXT_PATH = Path(sys.argv[2])

# create a speech recognition object
r = sr.Recognizer()

def write_text_to_file(file_path, text):
    with open(file_path, 'a') as file:
        file.write(text)

# a function that splits the audio file into chunks
# and applies speech recognition
def write_large_audio_transcription(audio_path, text_path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_mp3(audio_path)
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

    seconds_passed = 0

    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        print(f'Chunk: {i}')
        seconds_passed += audio_chunk.duration_seconds
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
                print("Error:", str(e))
            else:
                print(text)
                write_text_to_file(text_path, f'{text.capitalize()}. \n')
                write_text_to_file(text_path, f'{str(datetime.timedelta(seconds=round(seconds_passed)))}. \n')


if __name__ == '__main__':
    write_large_audio_transcription(INPUT_AUDIO_PATH, OUTPUT_TEXT_PATH)
