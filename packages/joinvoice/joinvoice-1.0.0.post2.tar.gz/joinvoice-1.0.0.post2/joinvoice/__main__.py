import sys
import os.path
import pathlib
import argparse

import joinvoice


parser = argparse.ArgumentParser(
    'joinvoice',
    description='Join multiple audio files into one.'
)
parser.add_argument(
    'source',
    help='All files in this directory will be merged.'
)
parser.add_argument(
    '--target', '-O',
    help='Name of the resulted audiofile, by default name of source + .ogg',
    default=None
)
parser.add_argument(
    '--sample-rate',
    action='store',
    default=None,
    type=int,
    help='All files will be loaded with specified sample rate. '
    'If not specified, sample rate of first audiofile will be used.'
)
# parser.add_argument(
#     '--stereo',
#     action='store_true',
#     help='If specified, output will contain 2 channels.'
# )
parser.add_argument(
    '--sort',
    action='store',
    default='name',
    help='How files should be sorted. Default is by name. '
    'One of "name", "created", "modified"'
)
parsed_args = parser.parse_args()

try:
    source_dir = parsed_args.source

    filenames = joinvoice.find_files(
        pathlib.Path(source_dir),
        sort_by=parsed_args.sort
    )

    target_filename = parsed_args.target
    if target_filename is None:
        target_filename = source_dir + '.ogg'
    else:
        base = os.path.basename(target_filename)
        _, _, ext = base.rpartition('.')
        if not ext:
            target_filename += '.ogg'

    joinvoice.join_and_write(
        filenames,
        sample_rate=parsed_args.sample_rate,
        target_filename=pathlib.Path(target_filename)
    )

    print('Result saved to %s' % target_filename)
except joinvoice.UsageError as e:
    print(e.message)
    sys.exit(1)
