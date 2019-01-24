#!/usr/bin/env python3


import argparse
import sys
import os
import re
from command import Command
import utils


def main(args):
    file_format = re.compile(r'^\.\w+$')

    # ensure that the program ffmpeg is installed on the system
    utils.check_ffmpeg_installed()

    convert_dir = args.type == 'dir'

    from_format = args.from_format
    print(from_format)
    if file_format.match(from_format) is None:
        raise argparse.ArgumentTypeError('The from format should be a . '
                                         'followed by alphabetic characters, for example, '
                                         '.avi .mkv')

    to = args.to
    if file_format.match(to) is None:
        raise argparse.ArgumentTypeError('The target format is not valid, should be a '
                                         '. followed by alphabetic characters, for example, '
                                         '.mp4')

    target = args.target
    if convert_dir:
        if not os.path.isdir(target[0]):
            raise argparse.ArgumentTypeError('\'{}\' is not a directory'.format(target[0]))
    else:
        for f in target:
            if not os.path.isfile(f):
                raise argparse.ArgumentTypeError('\'{}\' is not a file'.format(f))

    delete_old = args.delete_old

    if convert_dir:
        utils.convert_directory(target, from_format, to, delete_original=delete_old)
    else:
        for f in target:
            utils.convert_file(f, from_format, to, delete_original=delete_old)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is the CLI for a video format '
                                                 'converter program. The program takes '
                                                 'a file, files, or directory and converts '
                                                 'the media to the targeted format.')

    parser.add_argument('type', type=str,
                        choices=['files', 'dir'],
                        help='Whether you will be converting specific files or a '
                             ' directory of files')

    parser.add_argument('from_format', type=str, metavar='from',
                        help='Format that should be converted from, for example, '
                             '\'.avi\', \'.mkv\'')

    parser.add_argument('to', type=str,
                        help='Format the files should be converted to, for example, '
                             '\'.mp4\'')

    parser.add_argument('target', type=str, nargs='+',
                        help='The files to be converted or the path to the directory where each '
                             'file in the directory and subdirectories will be converted.')

    parser.add_argument('--delete-old', '-d', action='store_true',
                        help='If this argument is given, the original files '
                             'will be deleted.')

    options = parser.parse_args()
    sys.exit(main(options))
