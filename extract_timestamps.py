"""
videometa.py

This script is designed to extract and process metadata from GoPro MP4 files. It specifically targets files with a naming convention of 'GXzzxxxx.mp4', where 'X' indicates HEVC encoding, 'zz' is the chapter number, and 'xxxx' is the file number.

The script provides the following functionalities:
- Parsing the filename to extract chapter and session information.
- Retrieving the creation time and duration of the video file.
- Listing all MP4 files in a given directory.
- Grouping files by session.
- Processing files in a session to calculate start and stop times.

The script can be run from the command line with the directory path as an argument. It also supports a recursive option for processing files in subdirectories and can output results in JSON format or to a specified output file.

Example usage:
python videometa.py /path/to/directory --recursive --json --output /path/to/output.csv

Dependencies:
- ffmpeg
- datetime
- os
- pandas
- re
- argparse
"""


# GoPro Hero 12 Naming convention:
# GXzzxxxx.mp4
# “X” = HEVC encoding
# "xxxx" = file number
# "zz" = chapter number


import ffmpeg
import datetime
import os
import pandas as pd
import re
import argparse
import json

class GoProTimestampExtractor:
    def __init__(self):
        pass

    def process_videos(self, directory, recursive=False, json_output=False, out_file=None):
        folder_path = directory
        files_metadata = self.get_file_metadata(folder_path, recursive=recursive)
        grouped_files = self.group_files_by_session(files_metadata)

        final_results = []
        for session_files in grouped_files.values():
            session_results = self.process_files_in_session(session_files)
            final_results.extend(session_results)

        df = pd.DataFrame(final_results, columns=['Filename', 'Start Time', 'Stop Time', 'Duration', 'Chapter', 'Session', 'Folder'])
        
        # Set pandas options
        pd.set_option('display.max_rows', None)  # This line will ensure all rows are printed
        pd.set_option('display.width', None)  # This line will ensure that each line of output doesn't wrap around
        pd.set_option('display.max_colwidth', None)  # This line will ensure that each column is wide enough to display all its content

        if out_file:
            df.to_csv(out_file, index=False)

        if json_output:
            return json.loads(df.to_json(orient="records", date_format="iso"))
        else:
            return df




    def parse_filename(self, filename):
        match = re.search(r'GX(\d{2})(\d{4})\.MP4', filename)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def get_creation_time_and_duration(self, file_path):
        probe = ffmpeg.probe(file_path)
        creation_time_str = probe['format']["tags"]["creation_time"]
        creation_time = datetime.datetime.strptime(creation_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        duration_sec = float(probe['format']["duration"])
        return creation_time, duration_sec

    def list_mp4_files_in_dir(self, directory, recursive):

        if recursive:
            mp4_files = []
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.MP4'):
                        chapter, session = self.parse_filename(file)
                        if chapter is not None and session is not None:
                            full_path = os.path.join(root, file)
                            mp4_files.append(full_path)
            return mp4_files
        else:
            return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.MP4')]



    def get_file_metadata(self, directory, recursive):
        files_metadata = []
        for file_path in self.list_mp4_files_in_dir(directory, recursive):
            creation_time, duration_sec = self.get_creation_time_and_duration(file_path)
            filename = os.path.basename(file_path)
            folder_path = os.path.relpath(os.path.dirname(file_path), directory)
            chapter, session = self.parse_filename(filename)
            files_metadata.append({"file": filename, 
                                "creation_time": creation_time, 
                                "duration": duration_sec, 
                                "chapter": chapter, 
                                "session": session,
                                "folder": folder_path})
        return files_metadata

    def group_files_by_session(self, files_metadata):
        grouped_files = {}
        for file_meta in files_metadata:
            key = file_meta["creation_time"].strftime("%Y-%m-%d %H:%M:%S")
            if key not in grouped_files:
                grouped_files[key] = []
            grouped_files[key].append(file_meta)
        return grouped_files

    def process_files_in_session(self, files):
        sorted_files = sorted(files, key=lambda x: x['chapter'])
        results = []
        start_time = None
        prev_duration = 0
        for file_meta in sorted_files:
            if start_time is None:
                start_time = file_meta["creation_time"]
            else:
                start_time += datetime.timedelta(seconds=prev_duration)

            stop_time = start_time + datetime.timedelta(seconds=file_meta["duration"])
            prev_duration = file_meta["duration"]

            results.append({
                "Filename": file_meta["file"],
                "Start Time": start_time,
                "Stop Time": stop_time,
                "Duration": str(datetime.timedelta(seconds=file_meta["duration"])),
                "Chapter": file_meta["chapter"],
                "Session": file_meta["session"],
                "Folder": file_meta["folder"]
            })
        return results

def main():
    args = parse_args()
    extractor = GoProTimestampExtractor()
    results = extractor.process_videos(args.folder, recursive=args.recursive, json_output=args.json, out_file=args.output)
    
    if args.output:
        with open(args.output, "w") as f:
            if args.json:
                json.dump(results, f, ensure_ascii=False, indent=4)
            else:
                results.to_csv(f, index=False)
    else:
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=4))
        else:
            print(results.to_string(index=False))
    

def parse_args():
    parser = argparse.ArgumentParser(description="Get timestamp metadata from GoPro Hero 12 video files in a folder", 
                                     epilog="")
    parser.add_argument("folder", type=str, help="Folder path containing the video files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Process files in subfolders recursively")
    parser.add_argument("-j", "--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("-o", "--output", type=str, help="Output file path")
    return parser.parse_args()

if __name__ == "__main__":
    main()
