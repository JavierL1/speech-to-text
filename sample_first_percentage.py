import sys
from pathlib import Path

from pydub import AudioSegment

INPUT_AUDIO_PATH = Path(sys.argv[1])
SAMPLE_PERCENTAGE = int(sys.argv[2])

sound = AudioSegment.from_mp3(INPUT_AUDIO_PATH)

full_length = len(sound)
sample_length = (len(sound) // 100) * SAMPLE_PERCENTAGE

print(full_length)
print(sample_length)

first_chunk = sound[:sample_length]

# create a new file "first_half.mp3":
first_chunk.export(INPUT_AUDIO_PATH.parent / 'chunk.mp3', format="mp3")
