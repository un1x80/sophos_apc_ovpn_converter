import tkinter as tk
from tkinter import filedialog, messagebox
import json

output_file = "client.ovpn"

def create_ovpn_file(apc_file, username_entry, password_entry):
    try:
        with open(apc_file, 'r') as file:
            data = json.load(file)

        server_address = data.get('server_address', [None])[0]
        server_port = data.get('server_port', None)
        certificate = data.get('certificate', None)
        ca_cert = data.get('ca_cert', None)
        client_key = data.get('key', None)
        username = data.get('username', "")
        password = data.get('password', "")

        if not server_address or not server_port or not certificate or not ca_cert or not client_key:
            messagebox.showerror("Error", "Missing required fields in the APC file.")
            return

        with open(output_file, 'w') as output:
            output.write("client\n")
            output.write("dev tun\n")
            output.write("proto tcp\n")
            output.write(f"remote {server_address} {server_port}\n")
            output.write("resolv-retry infinite\n")
            output.write("nobind\n")
            output.write("persist-key\n")
            output.write("persist-tun\n")

            output.write("<ca>\n")
            output.write(f"{ca_cert}\n")
            output.write("</ca>\n")

            output.write("<cert>\n")
            output.write(f"{certificate}\n")
            output.write("</cert>\n")

            output.write("<key>\n")
            output.write(f"{client_key}\n")
            output.write("</key>\n")

            output.write("auth SHA256\n")
            output.write("cipher AES-256-GBC\n")
            output.write("tls-client\n")
            output.write("comp-lzo\n")
            output.write("verb 3\n")

        username_entry.delete(0, tk.END)
        username_entry.insert(0, username)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        messagebox.showinfo("Success", f"The file {output_file} has been successfully created in current directory. ")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def select_apc_file(username_entry, password_entry):
    file_path = filedialog.askopenfilename(title="Select APC File", filetypes=[("APC Files", "*.apc")])
    if file_path:
        create_ovpn_file(file_path, username_entry, password_entry)

root = tk.Tk()
root.title("Sophos .apc to .ovpn Conveter")

root.geometry("400x300")

button = tk.Button(root, text="Select APC File", command=lambda: select_apc_file(username_entry, password_entry), height=2, width=20)
button.pack(pady=20)

username_label = tk.Label(root, text="Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(root, width=40)
username_entry.pack(pady=5)

password_label = tk.Label(root, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(root, width=40)
password_entry.pack(pady=5)

root.mainloop()
