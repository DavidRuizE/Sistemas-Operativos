import subprocess

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
        # Ejecutamos el comando ffmpeg y redirigimos la salida al archivo de salida
        subprocess.run(ffmpeg_cmd, check=True)
        print("Successfully converted")
    except subprocess.CalledProcessError:
        print("Conversion failed!")

# Ejemplo de uso:
input_file = "Taken.aif"

formats = ["mp3", "wav", "flac", "ogg", "aac"]
for format in formats:
    file_size = get_file_size(input_file, format)
    if file_size > 0:
        print(f"Size of {input_file} converted to {format}: {file_size / (1024 * 1024):.2f} MB")

audio_format = input("Ingrese el formato al cual desea convertir la canción (mp3, wav, flac, ogg, aac): ")
output_file = f"audio.{audio_format}"
convert_to_audio(input_file, audio_format, output_file)

print(f"Archivo convertido guardado como {output_file}")
