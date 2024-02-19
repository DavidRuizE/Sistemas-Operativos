import os
import subprocess
from multiprocessing import Pool

def convert_audio(input_file, output_format='mp3'):
    output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-y",  # Overwrite output files without asking
        output_file
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Successfully converted {input_file} to {output_format}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed for {input_file} to {output_format}")
        return None
    return output_file

def process_file(file_path, formats):
    sizes = {}
    for fmt in formats:
        output_file = convert_audio(file_path, fmt)
        if output_file:
            sizes[fmt] = os.path.getsize(output_file)
    return sizes

def process_folder(folder_path, default_format):
    aif_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.aif')]
    with Pool() as p:
        sizes = p.starmap(process_file, [(file_path, [default_format]) for file_path in aif_files])
    return sizes

def main(file_or_folder, encoding=None):
    formats = ['mp3', 'wav', 'ogg']  # You can add more formats here
    if os.path.isfile(file_or_folder):
        sizes = process_file(file_or_folder, formats)
        # Here you would add the logic for the user to choose the format they want to keep
        chosen_format = max(sizes, key=sizes.get)  # Example: keep the largest file
        print(f"The file was kept in {chosen_format} format with size {sizes[chosen_format]} bytes")
    elif os.path.isdir(file_or_folder) and encoding:
        folder_sizes = process_folder(file_or_folder, encoding)
        print(f"Folder processed with files converted to {encoding} format")
    else:
        print("Error: Invalid input or missing encoding for folder")
        exit(1)

if __name__ == "__main__":
    # Example call, replace '/path/to/file_or_folder' with the actual path
    # and 'wav' with the desired default format if it's a folder
    main('Canciones', 'wav')
