# GoPro Timestamp Extractor

This script is designed to extract and process metadata from GoPro MP4 files. It specifically targets files with a naming convention of 'GXzzxxxx.mp4', where 'X' indicates HEVC encoding, 'zz' is the chapter number, and 'xxxx' is the file number.

## Features

- Parsing the filename to extract chapter and session information.
- Retrieving the creation time and duration of the video file.
- Listing all MP4 files in a given directory.
- Grouping files by session.
- Processing files in a session to calculate start and stop times.

## Dependencies

This script requires the following Python packages:

- ffmpeg-python
- pandas
- numpy
- python-dateutil
- pytz
- future
- tzdata
- six

You can install these dependencies using pip:

```sh
pip install -r requirements.txt
````
## Usage

```sh
python gopro_timestamp_extractor.py <input_directory> --recursive -- json --output <filename>
```

## Options

- `--recursive` - Recursively search the input directory for MP4 files.
- `--json` - Output the results as JSON.
- `--output` - Write results to a file.

