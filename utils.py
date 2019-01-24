import sys
import os
import shutil
import shlex
from command import Command


def check_ffmpeg_installed():
    if shutil.which('ffmpeg') is None:
        print('The program \'ffmpeg\' is not installed in your system.\n'
              'You can install it by visiting http://ffmpeg.org/download.html')
        sys.exit(0)


def convert_file(path: str, from_format: str, to: str, delete_original=False):
    assert path.endswith(from_format)

    path = shlex.quote(path)
    new_name = path.replace(from_format, to)

    cmd = Command('/snap/bin/ffmpeg -i {} {}'.format(path, new_name), os.getcwd())

    sig, out, err = cmd.run()

    if sig != 0:
        pass # TODO 

    if delete_original:
        pass # TODO


def convert_directory(path: str, from_format: str, to: str, delete_original=False):
    for dirpath, _, files in os.walk(path):
        for f in filter(lambda f: f.endswith(from_format), files):
            convert_file('{}/{}'.format(dirpath, f), from_format,
                         to, delete_original)