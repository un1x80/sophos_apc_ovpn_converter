import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os

# Percorso della directory contenente gli script
BIN_DIR = "bin"

class App:
    def __init__(self, master):
        self.master = master
        master.title("Convertitore APC/OVPN")

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.btn_apc_to_ovpn = tk.Button(self.button_frame, text="Converti da APC a OVPN", command=self.run_apc_to_ovpn)
        self.btn_apc_to_ovpn.pack(side=tk.LEFT, padx=5)

        self.btn_ovpn_to_apc = tk.Button(self.button_frame, text="Converti da OVPN a APC", command=self.run_ovpn_to_apc)
        self.btn_ovpn_to_apc.pack(side=tk.LEFT, padx=5)
        
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(padx=10, pady=10)

    def run_script(self, script_name):
        script_path = os.path.join(BIN_DIR, script_name)
        
        if not os.path.isfile(script_path):
            self.output_text.insert(tk.END, f"Errore: lo script {script_name} non è stato trovato nella cartella bin.\n")
            return

        try:
            result = subprocess.run(["python3", script_path], capture_output=True, text=True, check=True)
            self.output_text.insert(tk.END, f"Output di {script_name}:\n{result.stdout}\n")
            if result.stderr:
                self.output_text.insert(tk.END, f"Errori:\n{result.stderr}\n")
        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Si è verificato un errore nell'esecuzione di {script_name}: {e.stderr}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Errore imprevisto: {e}\n")
        
        self.output_text.see(tk.END) 

    def run_apc_to_ovpn(self):
        self.run_script("apc_to_ovpn.py")

    def run_ovpn_to_apc(self):
        self.run_script("ovpn_to_apc.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
