import subprocess 
from concurrent.futures import ThreadPoolExecutor #Paralelismo
import os #Manejo de los archivos/carpetas
import time


def get_file_size(input_file, audio_format):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-f", audio_format,
        "-"
    ]
    
    try:
        # Capturamos la salida del proceso de conversión
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()

        # Calculamos el tamaño del flujo de salida
        file_size = len(output)
        return file_size
    except subprocess.CalledProcessError:
        return -1

# Función para realizar la conversión de archivos
def convert_to_audio(input_file, audio_format, output_file):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame" if audio_format == "mp3" else "pcm_s16le" if audio_format == "wav" else "flac" if audio_format == "flac" else "libvorbis" if audio_format == "ogg" else "aac",
        "-ar", "44100" if audio_format == "mp3" or audio_format == "ogg" or audio_format == "aac" else "48000", # Sample rate adjustment if necessary
        "-f", audio_format,
        output_file
    ]   
    
    try:
        start_time = time.time()  # Tiempo inicial
        # Ejecutamos el comando ffmpeg y redirigimos la salida al archivo de salida
        subprocess.run(ffmpeg_cmd, check=True)
        end_time = time.time()  # Tiempo final
        elapsed_time = end_time - start_time  # Tiempo transcurrido
        print(f"Successfully converted to {audio_format}. Elapsed time: {elapsed_time:.2f} seconds")
    except subprocess.CalledProcessError:
        print(f"Conversion to {audio_format} failed!")

# Función para procesar el archivo y obtener su tamaño antes de la conversión
def process_file(input_file, audio_format):
    file_size = get_file_size(input_file, audio_format)
    if file_size > 0:
        print(f"Size of {input_file} converted to {audio_format}: {file_size / (1024 * 1024):.2f} MB")

# Función para obtener la lista de archivos de audio en una carpeta
def get_audio_files_in_folder(folder_path):
    audio_files = []
    for file in os.listdir(folder_path):
        if file.endswith(('.mp3', '.wav', '.flac', '.ogg', '.aif')):
            audio_files.append(os.path.join(folder_path, file))
    return audio_files

# Función para convertir archivos en paralelo
def convert_files_in_parallel(audio_files, audio_format):
    with ThreadPoolExecutor(max_workers=len(audio_files)) as executor:
        for file in audio_files:
            output_file = os.path.splitext(file)[0] + f".{audio_format}"
            executor.submit(convert_to_audio, file, audio_format, output_file)

# Función para calcular los tamaños de los archivos en paralelo
def calculate_file_sizes(input_file, formats):
    with ThreadPoolExecutor(max_workers=len(formats)) as executor:
        for format in formats:
            executor.submit(process_file, input_file, format)

# Función principal
def main():
    conversion_type = input("¿Desea convertir un solo archivo (A) o una carpeta entera (B)? (A/B): ").upper()
    
    if conversion_type == 'A':
        input_file = input("Ingrese el nombre del archivo que desea convertir: ")
        formats = ["mp3", "wav", "flac", "ogg"]
        calculate_file_sizes(input_file, formats)
        audio_format = input("Ingrese el formato al cual desea convertir la canción (mp3, wav, flac, ogg): ")
        convert_to_audio(input_file, audio_format, f"audio.{audio_format}")
        print("La conversión ha sido completada.")
    
    elif conversion_type == 'B':
        folder_path = input("Ingrese la ruta de la carpeta que desea convertir: ").strip()  # Eliminar espacios en blanco alrededor de la ruta
        formats = ["mp3", "wav", "flac", "ogg"]
        audio_format = input("Ingrese el formato al cual desea convertir las canciones (mp3, wav, flac, ogg): ")
        audio_files = get_audio_files_in_folder(folder_path)
        convert_files_in_parallel(audio_files, audio_format)
        print("La conversión de la carpeta ha sido completada.")
    
    else:
        print("Opción no válida. Por favor, seleccione 'A' o 'B'.")

if __name__ == "__main__":
    main()
