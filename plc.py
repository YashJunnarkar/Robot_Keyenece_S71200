from snap7.client import Client
from snap7.util import set_bool
import snap7

# PLC Connection Configuration
PLC_IP = '192.168.1.1'   # Update with your PLC IP
RACK = 0
SLOT = 1

# DB Settings
DB_NUM = 2              # Your target Data Block number
CAMERA_PROG_OFFSET = 0  # DBW0 — for camera program (2 bytes)
TRIGGER_BYTE = 2        # DBB2 — byte containing the trigger bit
TRIGGER_BIT = 0         # Bit index within DBB2

# Connect to PLC
plc = Client()

try:
    plc.connect(PLC_IP, RACK, SLOT)
    print("[PLC] Connected to PLC successfully.")
except Exception as e:
    print(f"[PLC] Failed to connect: {e}")

# ----------------------------------------

def write_camera_program(program_id: int):
    """Write camera program (int) to DBW0."""
    if not plc.get_connected():
        raise Exception("PLC not connected")

    data = program_id.to_bytes(2, byteorder='big')  # 2-byte integer
    plc.db_write(DB_NUM, CAMERA_PROG_OFFSET, data)
    print(f"[PLC] Wrote camera program ID {program_id} to DB{DB_NUM}.DBW{CAMERA_PROG_OFFSET}")

# ----------------------------------------

def trigger_camera():
    """Set a bit in DBB2 to trigger the camera."""
    if not plc.get_connected():
        raise Exception("PLC not connected")

    # Read DBB2 (1 byte)
    data = plc.db_read(DB_NUM, TRIGGER_BYTE, 1)
    set_bool(data, 0, TRIGGER_BIT, True)
    plc.db_write(DB_NUM, TRIGGER_BYTE, data)
    print(f"[PLC] Triggered camera bit in DB{DB_NUM}.DBB{TRIGGER_BYTE}.{TRIGGER_BIT}")

# ----------------------------------------

def get_status():
    """Return connection status of the PLC."""
    return {
        "connected": plc.get_connected()
    }

# ----------------------------------------

def disconnect():
    """Gracefully disconnect the PLC (optional)."""
    if plc.get_connected():
        plc.disconnect()
        print("[PLC] Disconnected from PLC.")


def read_camera_result():
    # Replace this with actual PLC reading logic
    # Example: reading from a data block and returning a test result
    return "PASS"  # or "FAIL"

