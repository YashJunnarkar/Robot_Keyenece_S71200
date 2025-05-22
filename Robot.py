import requests

ROBOT_IP = "192.168.1.4"
FLOW_UUID_MOVE_TO_OBJECT = "acab861e-b286-4413-88e2-203d559fd88c"
FLOW_UUID_MOVE_HOME = "898d01d5-f931-45ab-82d4-a5caeb2a28a3"

def move_to_object():
    url = f"http://{ROBOT_IP}/api/v3.0/flows/{FLOW_UUID_MOVE_TO_OBJECT}/run"
    response = requests.put(url)
    response.raise_for_status()

def move_home():
    url = f"http://{ROBOT_IP}/api/v3.0/flows/{FLOW_UUID_MOVE_HOME}/run"
    response = requests.put(url)
    response.raise_for_status()
