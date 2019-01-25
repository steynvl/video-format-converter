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

    escaped = shlex.quote(path)
    new_name = escaped.replace(from_format, to)
    ffmpeg = shutil.which('ffmpeg')

    filename = path[path.rfind('/') + 1:]
    print('Converting \'{}\''.format(filename))

    cmd = Command('{} -i {} {}'.format(ffmpeg, escaped, new_name), os.getcwd())
    sig, _, err = cmd.run()

    if sig != 0:
        print('\'{}\' could not be converted'.format(filename))
        print('>>> ERR >>>')
        print(err)

    if delete_original:
        os.remove(path)


def convert_directory(path: str, from_format: str, to: str, delete_original=False):
    for dirpath, _, files in os.walk(path):
        for f in filter(lambda f: f.endswith(from_format), files):
            print('{}/{}'.format(dirpath, f))
            convert_file('{}/{}'.format(dirpath, f), from_format,
                         to, delete_original)