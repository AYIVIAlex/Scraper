import tkinter as tk
from tkinter import filedialog

def select_file():
    # Crée une instance de la fenêtre tkinter
    root = tk.Tk()
    # Masque la fenêtre principale
    root.withdraw()
    # Ouvre la boîte de dialogue pour sélectionner un fichier
    file_selected = filedialog.askopenfilename(
        title="Select a file",  # Titre de la boîte de dialogue
        filetypes=(("All files", "*.*"), ("Text files", "*.txt"), ("CSV files", "*.csv"))  # Types de fichiers à afficher
    )
    return file_selected

def select_directory():
    # Crée une instance de la fenêtre tkinter
    root = tk.Tk()
    # Masque la fenêtre principale
    root.withdraw()
    # Ouvre la boîte de dialogue pour sélectionner un répertoire
    folder_selected = filedialog.askdirectory()
    return folder_selected
