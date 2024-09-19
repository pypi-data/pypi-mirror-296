import sys
import pathlib
import operator
from typing import Literal

import librosa
import soundfile as sf


if sys.version_info < (3, 12):
    get_birthtime = operator.attrgetter('st_ctime')
else:
    get_birthtime = operator.attrgetter('st_birthtime')


class UsageError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @property
    def message(self) -> str:
        return self.args[0]


def find_files(
    source: pathlib.Path,
    sort_by: "Literal['name', 'created', 'modified'] | str",
    notify_user=print
) -> 'list[pathlib.Path]':
    if not source.is_dir():
        if source.is_file():
            notify_user('%s: assume is only source file' % source)
            return [source]
        raise UsageError('%s is not a directory.' % source)

    filenames: 'list[pathlib.Path]' = []
    for filepath in source.glob('*'):
        if filepath.is_file():
            filenames.append(filepath)
        else:
            notify_user('%s is not a file, skipped' % filepath)

    if sort_by == 'name':
        filenames.sort(key=lambda p: p.name)
    elif sort_by == 'created':
        filenames.sort(key=lambda p: get_birthtime(p.stat()))
    elif sort_by == 'modified':
        filenames.sort(key=lambda p: p.stat().st_mtime)
    else:
        raise UsageError('Unknown sort method "%s"' % sort_by)

    return filenames


def join_and_write(
    filenames: 'list[pathlib.Path]',
    sample_rate: 'int | None',
    target_filename: 'pathlib.Path',
    notify_user=print,
):
    def open_target_file(first_file_sr):
        if not sample_rate:
            if not isinstance(first_file_sr, int):
                raise UsageError(
                    'Sample rate of %s is not integer (%s). '
                    'Run with --sample-rate argument.' % (fname, first_file_sr)
                )
            target_sr = first_file_sr
            notify_user('Sample rate set to %dhz' % target_sr)
        else:
            target_sr = sample_rate

        return sf.SoundFile(
            target_filename,
            mode='w',
            samplerate=target_sr,
            channels=1,
        )

    target = None

    for fname in filenames:
        try:
            file = sf.SoundFile(fname)
        except sf.LibsndfileError as e:
            notify_user('%s skipped: %s' % (fname, e.error_string))
            continue

        if target is None:
            target = open_target_file(file.samplerate)

        for block in file.blocks(blocksize=1024):
            if block.ndim != 1:
                block = librosa.to_mono(block)

            if file.samplerate != target.samplerate:
                block = librosa.resample(
                    block,
                    orig_sr=file.samplerate,
                    target_sr=target.samplerate,
                )
            target.write(block)

        notify_user('%s written to target' % fname)

    if target is None:
        raise UsageError('No audio files found.')

    target.close()
