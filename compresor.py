import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def compress_file(input_path, output_path):

    with open(input_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    compressed_text = original_text

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(compressed_text)

def decompress_file(input_path, output_path):

    with open(input_path, 'r', encoding='utf-8') as file:
        compressed_text = file.read()


    decompressed_text = compressed_text

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(decompressed_text)

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor de archivos universal")

        self.label = tk.Label(root, text="Selecciona, por favor, el archivo que deseas comprimir/descomprimir:")
        self.label.pack(pady=10)

        self.button_choose_file = tk.Button(root, text="Seleccionar archivo", command=self.choose_file)
        self.button_choose_file.pack(pady=10)

        self.compress_button = tk.Button(root, text="Comprimir archivo", command=self.compress_file)
        self.compress_button.pack(pady=5)

        self.decompress_button = tk.Button(root, text="Descomprimir archivo", command=self.decompress_file)
        self.decompress_button.pack(pady=5)

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        self.selected_file = file_path
        self.label.config(text=f"Archivo seleccionado: {file_path}")

    def compress_file(self):
        if hasattr(self, 'selected_file'):
            output_path = filedialog.asksaveasfilename(defaultextension=".huff")
     
            compress_file(self.selected_file, output_path)
            messagebox.showinfo("Comprimir", "Archivo comprimido con éxito.")
        else:
            messagebox.showwarning("Comprimir", "Seleccione un archivo antes de comprimir.")

    def decompress_file(self):
        if hasattr(self, 'selected_file'):
            output_path = filedialog.asksaveasfilename(defaultextension=".txt")
   
            decompress_file(self.selected_file, output_path)
            messagebox.showinfo("Descomprimir", "Archivo descomprimido con éxito.")
        else:
            messagebox.showwarning("Descomprimir", "Seleccione un archivo antes de descomprimir.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()

