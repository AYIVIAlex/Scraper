import tkinter as tk
from tkinter import filedialog

def select_directory():
    # Crée une instance de la fenêtre tkinter
    root = tk.Tk()
    # Masque la fenêtre principale
    root.withdraw()
    # Ouvre la boîte de dialogue pour sélectionner un répertoire
    folder_selected = filedialog.askdirectory()
    return folder_selected
