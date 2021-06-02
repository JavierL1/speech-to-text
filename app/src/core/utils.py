import datetime
import itertools
from typing import List, Optional
from dataclasses import dataclass

from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def seconds_to_human(seconds: int) -> str:
    return str(datetime.timedelta(seconds=round(seconds)))

@dataclass
class AudioChunk:
    audio: AudioSegment
    start: datetime.timedelta
    end: datetime.timedelta


def custom_split_on_silence(
    audio_segment: AudioSegment,
    min_silence_len: int = 1000,
    silence_thresh: int = -16,
    keep_silence: int = 100,
    seek_step: int = 1
) -> List[AudioChunk]:
    """
    Returns list of audio segments from splitting audio_segment on silent sections

    audio_segment - original pydub.AudioSegment() object

    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms

    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS

    keep_silence - (in ms or True/False) leave some silence at the beginning
        and end of the chunks. Keeps the sound from sounding like it
        is abruptly cut off.
        When the length of the silence is less than the keep_silence duration
        it is split evenly between the preceding and following non-silent
        segments.
        If True is specified, all the silence is kept, if False none is kept.
        default: 100ms

    seek_step - step size for interating over the segment in ms
    """

    # from the itertools documentation
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    if isinstance(keep_silence, bool):
        keep_silence = len(audio_segment) if keep_silence else 0

    non_silent_segments = detect_nonsilent(
        audio_segment,
        min_silence_len,
        silence_thresh,
        seek_step,
    )

    output_ranges = [
        [start - keep_silence, end + keep_silence]
        for (start, end) in non_silent_segments
    ]

    for range_i, range_ii in pairwise(output_ranges):
        last_end = range_i[1]
        next_start = range_ii[0]
        if next_start < last_end:
            range_i[1] = (last_end+next_start)//2
            range_ii[0] = range_i[1]

    return [
        AudioChunk(
            audio=audio_segment[max(start,0) : min(end, len(audio_segment))],
            start=datetime.timedelta(milliseconds=non_silent_segments[index][0]),
            end=datetime.timedelta(milliseconds=non_silent_segments[index][1]),
        ) for index, (start, end) in enumerate(output_ranges)
    ]
