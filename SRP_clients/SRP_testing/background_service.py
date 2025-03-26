import tkinter as tk
from tkinter import messagebox
import zmq
import threading

# import pystray
from pystray import MenuItem as item, Icon
from PIL import Image

SERVER_IP = "127.0.0.1"
PORT = "8000"


def listen_for_alerts():
    """Listens for alerts from the ZMQ server and triggers a popup."""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{SERVER_IP}:{PORT}")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Listening for alerts...")

    while True:
        message = socket.recv_string()
        print(f"🚨 Alert received: {message}")
        show_popup(message)


def show_popup(message):
    """Displays an alert popup using Tkinter."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showwarning("🚨 ALERT 🚨", message)
    root.destroy()


def exit_program(icon, item):
    """Closes the background service when the tray icon is clicked."""
    print("Shutting down alert service...")
    icon.stop()


def run_system_tray():
    """Creates a system tray icon for the background service."""
    icon_image = Image.new("RGB", (64, 64), (255, 0, 0))  # Red square icon
    menu = (item("Exit", exit_program),)
    tray_icon = Icon("AlertService", icon_image, menu=menu)
    tray_icon.run()


if __name__ == "__main__":
    threading.Thread(target=listen_for_alerts, daemon=True).start()
    run_system_tray()
