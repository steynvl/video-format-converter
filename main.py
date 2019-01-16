#!/usr/bin/env python3


import argparse
import sys
import os
import re
from command import Command
from utils import check_ffmpeg_installed


def main(args):
    file_format = re.compile(r'^\.\w+$')

    # ensure that the program ffmpeg is installed on the system
    check_ffmpeg_installed()

    convert_dir = args.type == 'dir'

    from_formats = args.from_formats
    if not (len(from_formats) > 0 and \
            all(file_format.match(f) is not None for f in from_formats)):
        raise argparse.ArgumentTypeError('The from formats should be a . '
                                         'followed by alphabetic characters, for example, '
                                         '.avi .mkv')

    to = args.to
    if file_format.match(to) is None:
        raise argparse.ArgumentTypeError('The target format is not valid, should be a '
                                         '. followed by alphabetic characters, for example, '
                                         '.mp4')

    dest = args.dest
    if convert_dir:
        if not os.path.isdir(dest[0]):
            raise argparse.ArgumentTypeError('\'{}\' is not a directory'.format(dest[0]))
    else:
        for f in dest:
            if not os.path.isfile(f):
                raise argparse.ArgumentTypeError('\'{}\' is not a file'.format(f))

    print('is_dir = {}'.format(convert_dir))
    print('from_formats = {}'.format(from_formats))
    print('to = {}'.format(to))
    print('dest = {}'.format(dest))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is the CLI for a video format '
                                                 'converter program. The program takes '
                                                 'a file, files, or directory and converts '
                                                 'the media to the targeted format.')

    parser.add_argument('type', type=str,
                        choices=['files', 'dir'],
                        help='Whether you will be converting specific files or a '
                             ' directory of files')

    parser.add_argument('from_formats', type=str, nargs='+', metavar='from',
                        help='Formats that should be converted from, for example, '
                             '\'.avi\', \'.mkv\'')

    parser.add_argument('to', type=str,
                        help='Format the files should be converted to, for example, '
                             '\'.mp4\'')

    parser.add_argument('dest', type=str, nargs='+',
                        help='The files to be converted or the path to the directory where each '
                             'file in the directory and subdirectories will be converted.')
    #
    parser.add_argument('--delete-old', '-d', action='store_true',
                        help='If this argument is given, the original files '
                             'will be deleted.')

    options = parser.parse_args()
    sys.exit(main(options))
