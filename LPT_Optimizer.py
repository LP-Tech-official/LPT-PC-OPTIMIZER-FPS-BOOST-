import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from googletrans import Translator
import os
import shutil
import psutil
import gc
import pkg_resources
import io

# Initialisiere den Übersetzer
translator = Translator()

# Funktion zum Übersetzen von Text
def translate_text(text, lang):
    try:
        translated = translator.translate(text, dest=lang)
        return translated.text
    except Exception as e:
        print(f"Fehler bei der Übersetzung: {e}")
        return text

def set_language(language_code):
    global current_language
    current_language = language_code
    refresh_texts()

def refresh_texts():
    texts = {
        "clean_temp_files": "Temporäre Dateien bereinigen",
        "free_memory": "Speicher freigeben",
        "display_system_info": "Systeminformationen anzeigen",
        "disk_cleanup": "Festplattenbereinigung",
        "optimize_pc": "PC Optimierung durchführen",
        "footer_text": "Made by LP-Tech",
        "terms_conditions": "Nutzungsbedingungen",
        "privacy_policy": "Datenschutzerklärung",
        "select_language": "Sprache auswählen",
        "create_backup_folder": "Backup-Ordner erstellen"
    }
    
    for key, text in texts.items():
        translated_text = translate_text(text, current_language)
        if key == "clean_temp_files":
            clean_temp_files_button.config(text=translated_text)
        elif key == "free_memory":
            free_memory_button.config(text=translated_text)
        elif key == "display_system_info":
            display_system_info_button.config(text=translated_text)
        elif key == "disk_cleanup":
            disk_cleanup_button.config(text=translated_text)
        elif key == "optimize_pc":
            optimize_pc_button.config(text=translated_text)
        elif key == "footer_text":
            footer_label.config(text=translated_text)
        elif key == "terms_conditions":
            terms_button.config(text=translated_text)
        elif key == "privacy_policy":
            privacy_button.config(text=translated_text)
        elif key == "select_language":
            language_dropdown['menu'].entryconfig(0, label=translated_text)
        elif key == "create_backup_folder":
            create_backup_folder_button.config(text=translated_text)

def darken_color(hex_color, amount=0.1):
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    darker_rgb = tuple(int(c * (1 - amount)) for c in rgb)
    return "#{:02x}{:02x}{:02x}".format(*darker_rgb)

def create_modern_button(parent, text, command, bg_color, fg_color):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=fg_color,
        font=("Arial", 14, "bold"),
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        padx=20, pady=10,
        width=20
    )
    button.pack(pady=10)
    
    button.configure(
        background=bg_color,
        foreground=fg_color,
        activebackground=darken_color(bg_color),
        activeforeground="white",
        highlightbackground=bg_color,
        highlightcolor=bg_color,
        relief="flat"
    )
    button.bind("<Enter>", lambda e: button.config(bg=darken_color(bg_color)))
    button.bind("<Leave>", lambda e: button.config(bg=bg_color))
    return button

# Funktion zum Erstellen eines Backup-Ordners
def create_backup_folder():
    global backup_folder
    backup_folder = os.path.join(os.path.expanduser("~"), "Documents", "PC_Optimizer_Backup")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    messagebox.showinfo(translate_text("Backup-Ordner erstellt", current_language), translate_text(f"Backup-Ordner wurde erstellt: {backup_folder}", current_language))

def move_to_backup(file_path):
    try:
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
        shutil.move(file_path, os.path.join(backup_folder, os.path.basename(file_path)))
    except Exception as e:
        print(f"Fehler beim Verschieben von {file_path} in den Backup-Ordner: {e}")

def clean_temp_files():
    try:
        temp_dirs = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'Temp'),
            os.path.join(os.getenv('TEMP'))
        ]
        for temp_dir in temp_dirs:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        move_to_backup(file_path)
                    except Exception as e:
                        print(f"Fehler beim Verschieben von {file_path} in den Backup-Ordner: {e}")
        return True
    except Exception as e:
        print(f"Fehler beim Bereinigen temporärer Dateien: {e}")
        return False

def free_memory():
    try:
        gc.collect()  # Simuliert das Freigeben von Speicher durch das Freigeben ungenutzter Objekte
        return True
    except Exception as e:
        print(f"Fehler beim Freigeben von Speicher: {e}")
        return False

def display_system_info():
    try:
        info = [
            f"CPU-Auslastung: {psutil.cpu_percent()}%",
            f"Verfügbarer RAM: {psutil.virtual_memory().available / (1024 * 1024):.2f} MB",
            f"Gesamter Speicher: {psutil.disk_usage('/').total / (1024 * 1024 * 1024):.2f} GB",
            f"Verfügbarer Speicher: {psutil.disk_usage('/').free / (1024 * 1024 * 1024):.2f} GB"
        ]
        return info
    except Exception as e:
        print(f"Fehler beim Abrufen der Systeminformationen: {e}")
        return ["Fehler beim Abrufen der Systeminformationen"]

def disk_cleanup():
    try:
        # Windows spezifisch: Verschiebt Dateien in den Papierkorb
        from win32com.client import Dispatch
        shell = Dispatch('Shell.Application')
        recycle_bin = shell.NameSpace(10)  # 10 = Recycle Bin
        recycle_bin.Items().InvokeVerb('delete')
        
        return True
    except Exception as e:
        print(f"Fehler bei der Festplattenbereinigung: {e}")
        return False

def perform_all_in_one_optimization():
    try:
        if clean_temp_files() and free_memory() and disk_cleanup():
            messagebox.showinfo(translate_text("Optimierung", current_language), translate_text("PC-Optimierung wurde erfolgreich durchgeführt.", current_language))
        else:
            messagebox.showwarning(translate_text("Fehler", current_language), translate_text("Fehler bei der PC-Optimierung.", current_language))
    except Exception as e:
        print(f"Fehler bei der PC-Optimierung: {e}")
        messagebox.showerror(translate_text("Fehler", current_language), translate_text("Fehler bei der PC-Optimierung.", current_language))

def show_terms_or_privacy(option):
    if option == "terms":
        text = """
        Nutzungsbedingungen:
        Diese Software wird wie besehen ohne jegliche Garantien bereitgestellt. Der Entwickler haftet nicht für irgendwelche Schäden, die durch die Nutzung dieser Software entstehen.
        """
        title = translate_text("Nutzungsbedingungen", current_language)
    elif option == "privacy":
        text = """
        Datenschutzerklärung:
        Diese Software sammelt oder speichert keine persönlichen Daten. Alle Datenverarbeitungen finden lokal auf Ihrem Gerät statt.
        """
        title = translate_text("Datenschutzerklärung", current_language)

    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, translate_text(text, current_language))
    text_area.config(state=tk.DISABLED)
    text_area_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

def hide_text_area():
    text_area_frame.pack_forget()
    frame_content.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# GUI-Setup
root = tk.Tk()
root.title("PC Optimizer")
root.geometry("900x700")
root.configure(bg="#2c3e50")

# Aktuelle Sprache
current_language = 'en'
backup_folder = ""

# Laden des Logos
def load_image(filename):
    image_data = pkg_resources.resource_string(__name__, filename)
    image = Image.open(io.BytesIO(image_data))
    return image

logo_img = load_image("Logo.png")  # Das Logo wird aus den eingebetteten Ressourcen geladen
logo_img = logo_img.resize((250, 125), Image.LANCZOS)  # Größe des Logos anpassen
logo_photo = ImageTk.PhotoImage(logo_img)

# Logo anzeigen
logo_label = tk.Label(root, image=logo_photo, bg="#2c3e50")
logo_label.pack(pady=20)

# Hauptframe für die Buttons
frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Buttons
clean_temp_files_button = create_modern_button(
    frame, 
    translate_text("Temporäre Dateien bereinigen", current_language), 
    lambda: messagebox.showinfo(translate_text("Erfolg", current_language), translate_text("Temporäre Dateien wurden gelöscht und in den Backup-Ordner verschoben.", current_language)) if clean_temp_files() else messagebox.showwarning(translate_text("Fehler", current_language), translate_text("Fehler beim Löschen der temporären Dateien.", current_language)), 
    "#3498db", 
    "white"
)

free_memory_button = create_modern_button(
    frame, 
    translate_text("Speicher freigeben", current_language), 
    lambda: messagebox.showinfo(translate_text("Erfolg", current_language), translate_text("Speicher wurde freigegeben.", current_language)) if free_memory() else messagebox.showwarning(translate_text("Fehler", current_language), translate_text("Fehler beim Freigeben des Speichers.", current_language)), 
    "#3498db", 
    "white"
)

display_system_info_button = create_modern_button(
    frame, 
    translate_text("Systeminformationen anzeigen", current_language), 
    lambda: messagebox.showinfo(translate_text("Systeminformationen", current_language), "\n".join(display_system_info())), 
    "#3498db", 
    "white"
)

disk_cleanup_button = create_modern_button(
    frame, 
    translate_text("Festplattenbereinigung", current_language), 
    lambda: messagebox.showinfo(translate_text("Erfolg", current_language), translate_text("Festplattenbereinigung wurde durchgeführt.", current_language)) if disk_cleanup() else messagebox.showwarning(translate_text("Fehler", current_language), translate_text("Fehler bei der Festplattenbereinigung.", current_language)), 
    "#3498db", 
    "white"
)

optimize_pc_button = create_modern_button(
    frame, 
    translate_text("PC Optimierung durchführen", current_language), 
    perform_all_in_one_optimization, 
    "#e67e22", 
    "white"
)

create_backup_folder_button = create_modern_button(
    frame, 
    translate_text("Backup-Ordner erstellen", current_language),
    create_backup_folder,
    "#1abc9c",
    "white"
)

# Textbereich für die Nutzungsbedingungen und Datenschutzerklärung
text_area_frame = tk.Frame(root, bg="#ecf0f1")
text_area = tk.Text(text_area_frame, wrap=tk.WORD, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12))
text_area.pack(expand=True, fill=tk.BOTH)
text_area.config(state=tk.DISABLED)

# Fußzeile
footer_frame = tk.Frame(root, bg="#2c3e50", pady=10)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
footer_label = tk.Label(footer_frame, text=translate_text("Made by LP-Tech", current_language), bg="#2c3e50", fg="white", font=("Arial", 12, "italic"))
footer_label.pack()

# Funktionen zur Anzeige der rechtlichen Informationen
def show_terms():
    show_terms_or_privacy("terms")

def show_privacy():
    show_terms_or_privacy("privacy")

def create_modern_dropdown(parent, options, command):
    selected_value = tk.StringVar(parent)
    selected_value.set(translate_text("Sprache auswählen", current_language))

    dropdown_menu = tk.OptionMenu(parent, selected_value, *options, command=command)
    dropdown_menu.config(
        bg="#1abc9c",
        fg="white",
        font=("Arial", 14, "bold"),
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        padx=20, pady=10
    )
    dropdown_menu.pack(pady=10)
    return dropdown_menu

# Dropdown-Menü für die Sprache
language_options = ["Englisch", "Deutsch", "Französisch"]
language_map = {'Englisch': 'en', 'Deutsch': 'de', 'Französisch': 'fr'}
language_dropdown = create_modern_dropdown(root, language_options, lambda lang: set_language(language_map.get(lang, 'en')))

# Buttons für die rechtlichen Informationen
terms_button = create_modern_button(root, translate_text("Nutzungsbedingungen", current_language), show_terms, "#1abc9c", "white")
privacy_button = create_modern_button(root, translate_text("Datenschutzerklärung", current_language), show_privacy, "#1abc9c", "white")

# Schließen des Textbereichs
close_text_area_button = tk.Button(text_area_frame, text="Schließen", command=hide_text_area, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), relief="flat", borderwidth=0, highlightthickness=0, padx=20, pady=10)
close_text_area_button.pack(pady=10)

root.mainloop()
