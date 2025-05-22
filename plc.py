# plc.py
from snap7 import Client
from snap7.util import set_bool, get_bool

PLC_IP = "192.168.1.1"
RACK = 0
SLOT = 1
DB_NUMBER = 2
BYTE_INDEX = 0
BIT_INDEX = 0

plc = Client()

def connect():
    plc.connect(PLC_IP, RACK, SLOT)
    return plc.get_connected()

def disconnect():
    plc.disconnect()

def is_connected():
    return plc.get_connected()

def toggle_bit():
    if not plc.get_connected():
        raise Exception("PLC not connected")
    data = plc.db_read(DB_NUMBER, BYTE_INDEX, 1)
    current_state = get_bool(data, 0, BIT_INDEX)
    new_state = not current_state
    set_bool(data, 0, BIT_INDEX, new_state)
    plc.db_write(DB_NUMBER, BYTE_INDEX, data)
    return new_state

def set_bit(value: bool = True):
    if not plc.get_connected():
        raise Exception("PLC not connected")
    data = plc.db_read(DB_NUMBER, BYTE_INDEX, 1)
    set_bool(data, 0, BIT_INDEX, value)
    plc.db_write(DB_NUMBER, BYTE_INDEX, data)
