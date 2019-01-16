import sys
import shutil


def check_ffmpeg_installed():
    if shutil.which('ffmpeg') is None:
        print('The program \'ffmpeg\' is not installed in your system.\n'
              'You can install it by visiting http://ffmpeg.org/download.html')
        sys.exit(0)
