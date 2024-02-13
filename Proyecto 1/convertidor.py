import os
import subprocess

def convert_to_mp3(input_file, output_file):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        output_file
        ]   
    
    try:
        subprocess.run(ffmpeg_cmd, check= True)
        print("Sucessfully converted")
    except subprocess.CalledProcessError as e:
        print("conversion failed!")

convert_to_mp3("OneThing.aif", "audio.mp3")