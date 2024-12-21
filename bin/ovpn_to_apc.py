import tkinter as tk
from tkinter import filedialog, messagebox
import re
import json

def parse_ovpn_file(ovpn_file):
    with open(ovpn_file, 'r') as f:
        ovpn_content = f.read()

    server_addresses = re.findall(r"remote\s([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s([0-9]+)", ovpn_content)
    server_addresses = [address[0] for address in server_addresses]

    server_port = re.search(r"remote\s[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\s([0-9]+)", ovpn_content)
    server_port = server_port.group(1) if server_port else None

    ca_cert = re.search(r"<ca>(.*?)</ca>", ovpn_content, re.DOTALL)
    ca_cert = ca_cert.group(1).strip() if ca_cert else None

    client_cert = re.search(r"<cert>(.*?)</cert>", ovpn_content, re.DOTALL)
    client_cert = client_cert.group(1).strip() if client_cert else None

    client_key = re.search(r"<key>(.*?)</key>", ovpn_content, re.DOTALL)
    client_key = client_key.group(1).strip() if client_key else None

    auth_algo = re.search(r"auth\s([A-Za-z0-9]+)", ovpn_content)
    auth_algo = auth_algo.group(1) if auth_algo else None

    cipher_algo = re.search(r"cipher\s([A-Za-z0-9\-]+)", ovpn_content)
    cipher_algo = cipher_algo.group(1) if cipher_algo else None

    apc_config = {
        "server_address": server_addresses,
        "server_port": server_port,
        "authentication_algorithm": auth_algo,
        "encryption_algorithm": cipher_algo,
        "certificate": client_cert,
        "ca_cert": ca_cert,
        "key": client_key
    }

    return apc_config

def save_apc_file(apc_config, output_file):
    with open(output_file, 'w') as f:
        json.dump(apc_config, f, indent=4)

def open_file_dialog():
    filepath = filedialog.askopenfilename(
        filetypes=[("OpenVPN Configuration Files", "*.ovpn"), ("All Files", "*.*")]
    )
    return filepath

def save_file_dialog():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".apc", filetypes=[("JSON Files", "*.apc"), ("All Files", "*.*")]
    )
    return filepath

def convert_file():
    ovpn_filepath = open_file_dialog()
    if not ovpn_filepath:
        return

    output_filepath = save_file_dialog()
    if not output_filepath:
        return

    try:
        apc_config = parse_ovpn_file(ovpn_filepath)
        
        save_apc_file(apc_config, output_filepath)
        
        messagebox.showinfo("Success", f"File APC : {output_filepath}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Conversion Error: {str(e)}")

root = tk.Tk()
root.title("Converter OVPN -> APC")
root.geometry("400x200")

convert_button = tk.Button(root, text="Convert OVPN -> APC", command=convert_file, width=30)
convert_button.pack(pady=50)

root.mainloop()
