# GoPro Timestamp Extractor

![Util badge](https://img.shields.io/badge/utility-blue) ![Active badge](https://img.shields.io/badge/active-red)

> [!NOTE]
> This script is still a work in progress. It is not yet ready for use.

## Why?

When doing continuous recording (session) with a GoPro, the video is split into multiple files. For some reason, the metadata regarding start time is the same for all files in a session. This makes it difficult to determine the start and stop times of each file.

This script is designed to extract and process the actual timestamp metadata from GoPro (Hero 12) MP4 files. It specifically targets files with a naming convention of 'GXzzxxxx.mp4', where 'X' indicates HEVC encoding, 'zz' is the chapter number, and 'xxxx' is the file number to indicate the order in which the files were recorded. Then, it uses the creation time and duration of the video file to calculate the start and stop times of each file.

## Progress/TODO

- [x] Extract metadata from MP4 files
- [x] Extract creation time and duration of video files
- [x] Calculate start and stop times of each file
- [x] Output results as JSON
- [x] ~~Output results to file~~
- [ ] ~~Output results to CSV~~
- [ ] KISS
  - [ ] Just output as JSON
  - [ ] Create a .pretty() method to convert to table
  - [ ] Remove stupid flags. Just use `> output.json` to save it to a file

## Dependencies

This script requires Python 3.10 or higher. `ffmpeg` is required to extract the metadata from the MP4 files, and `ffprobe` is required to extract the creation time and duration of the video files. Download and install these tools from the [FFmpeg website](https://ffmpeg.org/download.html).

## Installation

Clone this repository:

```sh
git clone https://github.com/hoeoek/gopro-timestamp-extractor.git
```

I recommend using a virtual environment to install the Python dependencies in the `requirements.txt` file. You can create and activate a virtual environment using the following commands:

```sh
cd gopro-timestamp-extractor
python -m venv venv
source venv/bin/activate
```

Then, install the dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### ⌨️ CLI

```sh
python gopro_timestamp_extractor.py <input_directory> --recursive --json --output <filename>
```

### 🐍 Python module

```python
from gopro_timestamp_extractor import GoProTimestampExtractor

extractor = GoProTimestampExtractor()
extractor.process_videos(input_directory, recursive=True, output_json=True, output_filename='output.json')
````

## Options

- `--recursive` - Recursively search the input directory for MP4 files.
- `--json` - Output the results as JSON.
- `--output` - Write results to a file.
