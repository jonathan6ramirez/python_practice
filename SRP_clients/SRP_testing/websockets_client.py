import asyncio
import websockets
import tkinter as tk
from tkinter import messagebox

WS_SERVER = "ws://localhost:8764"  # WebSocket Server Address


async def listen_for_alerts():
    """Connects to WebSocket and listens for alerts."""
    async with websockets.connect(WS_SERVER) as websocket:
        while True:
            alert = await websocket.recv()
            print(f"🚨 Received Alert: {alert}")
            show_popup(alert)


def show_popup(message):
    """Displays an alert popup using Tkinter."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showwarning("🚨 ALERT 🚨", message)
    root.destroy()


if __name__ == "__main__":
    asyncio.run(listen_for_alerts())
