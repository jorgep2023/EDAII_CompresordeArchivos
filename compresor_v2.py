from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import zipfile
import rarfile
import os


def compress_text(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    compressed_text = original_text  

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(compressed_text)

def decompress_text(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        compressed_text = file.read()

    decompressed_text = compressed_text 

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(decompressed_text)

def compress_image(input_path, output_path):
    try:
        image = Image.open(input_path)
        compressed_image_path = os.path.splitext(input_path)[0] + "_compressed.jpg"
        image.save(compressed_image_path, quality=85) 

   
        zip_filename = output_path + ".zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_STORED) as zipf:
            zipf.write(compressed_image_path, os.path.basename(compressed_image_path))

        messagebox.showinfo("Comprimir Imagen", f"Imagen comprimida y guardada en {zip_filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al comprimir la imagen: {str(e)}")

def decompress_image(input_path, output_path):
    try:
       
        zip_filename = filedialog.askopenfilename(title="Seleccionar archivo .zip", filetypes=[("ZIP files", "*.zip")])
        if not zip_filename:
            return

        with zipfile.ZipFile(zip_filename, 'r') as zipf:
       
            compressed_image_name = os.path.basename(zipf.namelist()[0])

            zipf.extractall(output_path)


        compressed_image_path = os.path.join(output_path, compressed_image_name)
        compressed_image = Image.open(compressed_image_path)


        decompressed_image_path = os.path.splitext(zip_filename)[0] + "_decompressed.png"
        compressed_image.save(decompressed_image_path)

        messagebox.showinfo("Descomprimir Imagen", f"Imagen descomprimida y guardada en {decompressed_image_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descomprimir la imagen: {str(e)}")





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

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()
