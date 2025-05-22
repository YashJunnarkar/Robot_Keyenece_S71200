import tkinter as tk
from snap7 import Client
from snap7.util import set_bool, get_bool

# --- PLC config ---
PLC_IP = "192.168.1.1"
RACK = 0
SLOT = 1
DB_NUMBER = 2
BYTE_INDEX = 0
BIT_INDEX = 0

# --- PLC Client ---
plc = Client()

def connect_plc():
    try:
        plc.connect(PLC_IP, RACK, SLOT)
        if plc.get_connected():
            status_label.config(text="✅ Connected to PLC", fg="green")
        else:
            status_label.config(text="❌ Failed to connect", fg="red")
    except Exception as e:
        status_label.config(text=f"❌ Error: {e}", fg="red")

def toggle_bit():
    if not plc.get_connected():
        status_label.config(text="⚠️ Not connected to PLC", fg="orange")
        return

    data = plc.db_read(DB_NUMBER, BYTE_INDEX, 1)
    current_state = get_bool(data, 0, BIT_INDEX)
    new_state = not current_state

    set_bool(data, 0, BIT_INDEX, new_state)
    plc.db_write(DB_NUMBER, BYTE_INDEX, data)

    status_label.config(
        text=f"Bit set to {new_state}", fg="blue"
    )

# --- GUI Setup ---
window = tk.Tk()
window.title("PLC Dashboard")

connect_btn = tk.Button(window, text="Connect to PLC", command=connect_plc)
connect_btn.pack(pady=10)

toggle_btn = tk.Button(window, text="Toggle Bit", command=toggle_bit)
toggle_btn.pack(pady=10)

status_label = tk.Label(window, text="Not connected", fg="gray")
status_label.pack(pady=10)

window.mainloop()
