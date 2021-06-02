import sys
from datetime import timedelta
from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import Iterator

@dataclass
class SRTEntry:
    start_time: timedelta
    end_time: timedelta
    content: str


SUBTITLE_TEMPLATE = '''{index}
{start} --> {end}
{subtitle}

'''

def format_timedelta(td: timedelta):
    td_str = str(td)
    [hms, ms] = td_str.split('.')
    [h, m, s] = [int(e) for e in hms.split(':')]
    return f'{h:02}:{m:02}:{s:02},{ms[0:3]}'

def format_srt_entry(srt_entry: SRTEntry, index: int):
    return SUBTITLE_TEMPLATE.format(
        index=index,
        start=format_timedelta(srt_entry.start_time),
        end=format_timedelta(srt_entry.end_time),
        subtitle=srt_entry.content,
    )


def write_srt_file(srt_path: Path, srt_entries: Iterator[SRTEntry]):
    with open(srt_path, 'w') as srt_file:
        for index, srt_entry in enumerate(srt_entries, start=1):
            srt_file.write(
                format_srt_entry(
                    index=index,
                    srt_entry=srt_entry,
                )
            )
