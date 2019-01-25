# Video format converter

This repository contains a program that takes a list of video files or a path to a directory and converts every video file to a new target format specified by you. 

## Prerequisites
It is assumed that you have Python 3.5.2 or higher installed on your system and that a binary of the program [ffmpeg](https://www.ffmpeg.org/) is present on your system. 

## Example run
```bash
git clone https://github.com/steynvl/video-format-converter
cd video-format-converted
./main.py --help
```

### Converting files
Suppose in the directory `movies`, you have a file called `'Big Hero 6.avi'`, and your tv does not support .avi files, thus we want to convert it to a .mp4 file format. The command below will perform that action 

```bash
./main.py files .avi .mp4 ~/Desktop/movies/Big\ Hero\ 6.avi --delete-old
```

### Converting a directory
Suppose in the directory `series`, you have a directory called `'The Office (US)'` and you want to convert all of the .avi files in all of the subdirectories to .mkv. The command below will perform that action
```bash
./main.py dir .avi .mkv ~/Desktop/series/The\ Office\ \(US\)/ --delete-old
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.