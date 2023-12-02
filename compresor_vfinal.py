from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import zipfile
import rarfile
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import tempfile
import heapq
from collections import Counter
import bitarray
import shutil
from collections import defaultdict

def compress_text(input_path, output_path):
    # Abrir el archivo de entrada para leer el texto original
    with open(input_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # En este momento, el texto comprimido es idéntico al original
    compressed_text = original_text  

    # Abrir el archivo de salida para escribir el texto comprimido
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(compressed_text)

def decompress_text(input_path, output_path):
    # Abrir el archivo de entrada para leer el texto comprimido
    with open(input_path, 'r', encoding='utf-8') as file:
        compressed_text = file.read()

    # En este punto, el texto descomprimido es idéntico al comprimido
    decompressed_text = compressed_text 

    # Abrir el archivo de salida para escribir el texto descomprimido
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(decompressed_text)

def compress_image(input_path, output_path):
    try:
        # Abrir la imagen desde la ruta de entrada
        image = Image.open(input_path)
        # Crear una nueva ruta para la imagen comprimida
        compressed_image_path = os.path.splitext(input_path)[0] + "_compressed.jpg"
        # Guardar la imagen comprimida en la nueva ruta
        image.save(compressed_image_path, quality=85)

        # Crear un archivo zip que contendrá la imagen comprimida
        zip_filename = output_path + ".zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_STORED) as zipf:
            # Agregar la imagen comprimida al archivo zip
            zipf.write(compressed_image_path, os.path.basename(compressed_image_path))

        messagebox.showinfo("Comprimir Imagen", f"Imagen comprimida y guardada en {zip_filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al comprimir la imagen: {str(e)}")

def decompress_image(input_path, output_path):
    try:
        zip_filename = filedialog.askopenfilename(title="Seleccionar archivo .zip", filetypes=[("ZIP files", "*.zip")])

        if not zip_filename:
            return

        # Abrir el archivo ZIP y extraer todos los archivos en la carpeta de salida
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            # Obtener el nombre del archivo comprimido dentro del ZIP
            compressed_image_name = os.path.basename(zipf.namelist()[0])
            # Extraer todos los archivos en la carpeta de salida
            zipf.extractall(output_path)

        # Construir la ruta completa del archivo de imagen comprimida
        compressed_image_path = os.path.join(output_path, compressed_image_name)
        # Abrir la imagen comprimida
        compressed_image = Image.open(compressed_image_path)
        # Construir la ruta del archivo para la imagen descomprimida
        decompressed_image_path = os.path.splitext(zip_filename)[0] + "_decompressed.png"
        # Guardar la imagen descomprimida en la nueva ruta
        compressed_image.save(decompressed_image_path)
        messagebox.showinfo("Descomprimir Imagen", f"Imagen descomprimida y guardada en {decompressed_image_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al descomprimir la imagen: {str(e)}")


def compress_video(input_path, output_path):
    try:
        video_clip = VideoFileClip(input_path)
        # Crear una nueva ruta para el video comprimido
        compressed_video_path = os.path.splitext(input_path)[0] + "_compressed.mp4"
        # Escribir el video comprimido 
        video_clip.write_videofile(compressed_video_path, codec='libx264', audio_codec='aac')

        # Crear un archivo zip que contendrá el video comprimido
        zip_filename = output_path + ".zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_STORED) as zipf:
            zipf.write(compressed_video_path, os.path.basename(compressed_video_path))

        messagebox.showinfo("Comprimir Video", f"Video comprimido y guardado en {zip_filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al comprimir el video: {str(e)}")

    finally:
        # Eliminar el video comprimido después de la compresión
        if os.path.exists(compressed_video_path):
            os.remove(compressed_video_path)
            
def decompress_video(input_path, output_path):
    try:
        zip_filename = filedialog.askopenfilename(title="Seleccionar archivo .zip", filetypes=[("ZIP files", "*.zip")])

        if not zip_filename:
            return

        # Leer el contenido del archivo ZIP y obtener el nombre del video comprimido
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            compressed_video_name = os.path.basename(zipf.namelist()[0])
            compressed_video_data = zipf.read(compressed_video_name)

        # Crear un directorio temporal y escribir el video comprimido dentro de él
        temp_dir = tempfile.mkdtemp()
        compressed_video_path = os.path.join(temp_dir, compressed_video_name)

        with open(compressed_video_path, 'wb') as video_file:
            video_file.write(compressed_video_data)

        # Abrir el video comprimido
        video_clip = VideoFileClip(compressed_video_path)
        # Construir la ruta del archivo para el video descomprimido
        decompressed_video_path = os.path.splitext(zip_filename)[0] + "_decompressed.mp4"
        # Escribir el video descomprimido 
        video_clip.write_videofile(decompressed_video_path, codec='libx264')
        messagebox.showinfo("Descomprimir Video", f"Video descomprimido y guardado en {decompressed_video_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al descomprimir el video: {str(e)}")

    finally:
        # Eliminar el video comprimido y el directorio temporal
        if os.path.exists(compressed_video_path):
            os.remove(compressed_video_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor de archivos universal")

        self.label = tk.Label(root, text="Selecciona, por favor, el archivo que deseas comprimir/descomprimir:")
        self.label.pack(pady=10)

        self.button_choose_file = tk.Button(root, text="Seleccionar archivo", command=self.choose_file)
        self.button_choose_file.pack(pady=10)

        self.compress_text_button = tk.Button(root, text="Comprimir texto", command=self.compress_text_gui)
        self.compress_text_button.pack(pady=5)

        self.decompress_text_button = tk.Button(root, text="Descomprimir texto", command=self.decompress_text_gui)
        self.decompress_text_button.pack(pady=5)

        self.compress_image_button = tk.Button(root, text="Comprimir imagen", command=self.compress_image_gui)
        self.compress_image_button.pack(pady=5)

        self.decompress_image_button = tk.Button(root, text="Descomprimir imagen", command=self.decompress_image_gui)
        self.decompress_image_button.pack(pady=5)
        
       
        self.compress_video_button = tk.Button(root, text="Comprimir video", command=self.compress_video_gui)
        self.compress_video_button.pack(pady=5)

        self.decompress_video_button = tk.Button(root, text="Descomprimir video", command=self.decompress_video_gui)
        self.decompress_video_button.pack(pady=5)

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        self.selected_file = file_path
        self.label.config(text=f"Archivo seleccionado: {file_path}")

    def compress_text_gui(self):
        if hasattr(self, 'selected_file'):
            output_path = filedialog.asksaveasfilename(defaultextension=".huff")
            compress_text(self.selected_file, output_path)
            messagebox.showinfo("Comprimir Texto", "Texto comprimido con éxito.")
        else:
            messagebox.showwarning("Comprimir Texto", "Seleccione un archivo de texto antes de comprimir.")

    def decompress_text_gui(self):
        if hasattr(self, 'selected_file'):
            output_path = filedialog.asksaveasfilename(defaultextension=".txt")
            decompress_text(self.selected_file, output_path)
            messagebox.showinfo("Descomprimir Texto", "Texto descomprimido con éxito.")
        else:
            messagebox.showwarning("Descomprimir Texto", "Seleccione un archivo de texto antes de descomprimir.")

    def compress_image_gui(self):
        if hasattr(self, 'selected_file'):
            output_path = filedialog.asksaveasfilename(defaultextension=".png")
            compress_image(self.selected_file, output_path)
            messagebox.showinfo("Comprimir Imagen", "Imagen comprimida con éxito.")
        else:
            messagebox.showwarning("Comprimir Imagen", "Seleccione un archivo de imagen antes de comprimir.")

    def decompress_image_gui(self):
        if hasattr(self, 'selected_file'):
            output_path = filedialog.asksaveasfilename(defaultextension=".png")
            decompress_image(self.selected_file, output_path)
            messagebox.showinfo("Descomprimir Imagen", "Imagen descomprimida con éxito.")
        else:
            messagebox.showwarning("Descomprimir Imagen", "Seleccione un archivo de imagen antes de descomprimir.")

    
    def compress_video_gui(self):
        if hasattr(self, 'selected_file'):
            output_path = filedialog.asksaveasfilename(defaultextension=".mp4")
            compress_video(self.selected_file, output_path)
            messagebox.showinfo("Comprimir Video", "Video comprimido con éxito.")
        else:
            messagebox.showwarning("Comprimir Video", "Seleccione un archivo de video antes de comprimir.")

    def decompress_video_gui(self):
        if hasattr(self, 'selected_file'):
            output_path = filedialog.asksaveasfilename(defaultextension=".mp4")
            decompress_video(self.selected_file, output_path)
            messagebox.showinfo("Descomprimir Video", "Video descomprimido con éxito.")
        else:
            messagebox.showwarning("Descomprimir Video", "Seleccione un archivo de video antes de descomprimir.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()