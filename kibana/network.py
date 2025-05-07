import tkinter as tk
from tkinter import messagebox
import os
import ssl
import socket
import requests
import time
import psutil
import subprocess

# Function to ping a host
def ping_host():
    host = host_entry.get()
    host = host.replace("http://", "").replace("https://", "")
    response = os.system(f"ping {host}")
    
    if response == 0:
        messagebox.showinfo("Ping Successful", f"Host {host} is reachable!")
    else:
        messagebox.showerror("Ping Failed", f"Host {host} is not reachable!")

# Function to check HTTP response time with method, headers, and body
def check_http_response_time():
    url = api_entry.get()
    method = method_var.get()  # Get the selected HTTP method
    headers_text = header_entry.get("1.0", tk.END).strip()
    body_text = body_entry.get("1.0", tk.END).strip()

    # Parse headers from text input
    headers = {}
    if headers_text:
        try:
            headers = eval(headers_text)  # Convert string to dictionary
        except Exception as e:
            messagebox.showerror("Error", f"Invalid header format: {e}")
            return

    # Parse body from text input (for POST/PUT)
    body = None
    if body_text:
        try:
            body = eval(body_text)  # Convert string to dictionary for body
        except Exception as e:
            messagebox.showerror("Error", f"Invalid body format: {e}")
            return

    # Time the request
    try:
        start_time = time.time()  # Record start time
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=body, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=body, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)

        response_time = time.time() - start_time  # Calculate response time
        messagebox.showinfo("HTTP Response Time", f"Response Time: {response_time:.2f} seconds\nStatus Code: {response.status_code}\n")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("HTTP Error", f"An error occurred: {str(e)}")

# Function to perform Traceroute
def perform_traceroute():
    host = traceroute_entry.get()
    try:
        result = subprocess.run(['tracert', host], capture_output=True, text=True)
        messagebox.showinfo("Traceroute Results", result.stdout)
    except Exception as e:
        messagebox.showerror("Traceroute Error", f"An error occurred: {str(e)}")

# Function to check IP Geolocation
def check_ip_geolocation():
    ip = ip_geolocation_entry.get()
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        geolocation = f"IP: {data['ip']}\nLocation: {data['city']}, {data['region']}, {data['country']}"
        messagebox.showinfo("IP Geolocation", geolocation)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to check network interface status
def check_network_interface():
    interfaces = psutil.net_if_addrs()
    status_message = ""
    for interface, addrs in interfaces.items():
        status = "Up" if psutil.net_if_stats()[interface].isup else "Down"
        status_message += f"Interface: {interface}, Status: {status}\n"
    
    if not status_message:
        messagebox.showinfo("Network Interface Status", "No network interfaces found.")
    else:
        messagebox.showinfo("Network Interface Status", status_message)

# Function to monitor bandwidth
def monitor_bandwidth():
    old_stats = psutil.net_io_counters()
    time.sleep(1)
    new_stats = psutil.net_io_counters()

    bytes_sent = new_stats.bytes_sent - old_stats.bytes_sent
    bytes_recv = new_stats.bytes_recv - old_stats.bytes_recv

    messagebox.showinfo("Bandwidth Monitoring", f"Upload Speed: {bytes_sent / 1024:.2f} KB/s\nDownload Speed: {bytes_recv / 1024:.2f} KB/s")

# Function to get header detail
def check_http_headers():
    url = api_entry.get()
    try:
        response = requests.head(url)
        headers = response.headers
        header_message = "\n".join([f"{key}: {value}" for key, value in headers.items()])
        messagebox.showinfo("HTTP Headers", header_message)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to toggle the drawer (open/close)
def toggle_drawer():
    if drawer_frame.winfo_ismapped():
        drawer_frame.grid_forget()  # Hide the drawer
    else:
        drawer_frame.grid(row=8, column=0, columnspan=3, pady=10)  # Show the drawer

# Function to check SSL certificate for a given host
def check_ssl_certificate():
    host = ssl_host_entry.get()
    host = host.replace("http://", "").replace("https://", "")
    port = 443 
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as conn:
            with context.wrap_socket(conn, server_hostname=host) as ssl_conn:
                cert = ssl_conn.getpeercert()
                cert_info = f"Certificate details for {host}:\n"
                cert_info += f"Subject: {cert.get('subject')}\n\n"
                cert_info += f"Issuer: {cert.get('issuer')}\n\n"
                cert_info += f"Not Before: {cert.get('notBefore')}\n\n"
                cert_info += f"Not After: {cert.get('notAfter')}\n\n"
                messagebox.showinfo("SSL Certificate", cert_info)
    except Exception as e:
        messagebox.showerror("SSL Certificate Error", f"Could not retrieve certificate: {e}")

root = tk.Tk()
root.title("Network Testing Tool")

# Ping Section
tk.Label(root, text="Ping Host:").grid(row=0, column=0, sticky="w")
host_entry = tk.Entry(root, width=50)
host_entry.grid(row=0, column=1)
tk.Button(root, text="Ping", command=ping_host, width=16).grid(row=0, column=2)

# HTTP Headers Check Section
tk.Label(root, text="API URL (for headers check):").grid(row=1, column=0, sticky="w")
api_entry = tk.Entry(root, width=40)
api_entry.grid(row=1, column=1)
tk.Button(root, text="Check HTTP Headers", command=check_http_headers, width=20).grid(row=1, column=2, padx=10)

# Traceroute Section
tk.Label(root, text="Traceroute to Host:").grid(row=2, column=0, sticky="w")
traceroute_entry = tk.Entry(root, width=40)
traceroute_entry.grid(row=2, column=1)
tk.Button(root, text="Perform Traceroute", command=perform_traceroute, width=20).grid(row=2, column=2, padx=10)

# SSL Certificate Check Section
tk.Label(root, text="Check SSL Certificate:").grid(row=3, column=0, sticky="w")
ssl_host_entry = tk.Entry(root, width=50)
ssl_host_entry.grid(row=3, column=1)
tk.Button(root, text="Check SSL Certificate", command=check_ssl_certificate).grid(row=3, column=2)

# Button to toggle the drawer
toggle_button = tk.Button(root, text="Toggle HTTP Response Time", command=toggle_drawer)
toggle_button.grid(row=4, column=0, columnspan=3, pady=10)

# Drawer (hidden initially)
drawer_frame = tk.Frame(root)

# HTTP Response Time Section inside the drawer
tk.Label(drawer_frame, text="API URL:").grid(row=0, column=0, sticky="w")
api_entry = tk.Entry(drawer_frame, width=40)
api_entry.grid(row=0, column=1)

# HTTP Method dropdown
method_label = tk.Label(drawer_frame, text="HTTP Method:").grid(row=1, column=0, sticky="w")
method_var = tk.StringVar(value="GET")
method_menu = tk.OptionMenu(drawer_frame, method_var, "GET", "POST", "PUT", "DELETE")
method_menu.grid(row=1, column=1)

# Headers section (JSON format)
header_label = tk.Label(drawer_frame, text="Headers (key = value format):").grid(row=2, column=0, sticky="w")
header_entry = tk.Text(drawer_frame, height=5, width=40)
header_entry.grid(row=2, column=1)

# Request Body section (for POST/PUT)
body_label = tk.Label(drawer_frame, text="Request Body (JSON):").grid(row=3, column=0, sticky="w")
body_entry = tk.Text(drawer_frame, height=5, width=40)
body_entry.grid(row=3, column=1)

# Button to trigger HTTP response time check
tk.Button(drawer_frame, text="Check Response Time", command=check_http_response_time, width=20).grid(row=4, column=0, columnspan=3, pady=10)

# Move these sections to the bottom of the screen by setting row positions
tk.Button(root, text="Check Network Interface Status", command=check_network_interface, width=30).grid(row=5, column=0, columnspan=3, pady=10)
tk.Button(root, text="Monitor Bandwidth", command=monitor_bandwidth, width=20).grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
