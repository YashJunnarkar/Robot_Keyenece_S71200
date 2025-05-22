# robot.py

import requests

ROBOT_IP = "192.168.1.4"

# Replace these with actual flow UUIDs from your robot controller
ROBOT_PROGRAMS = {
    1: "acab861e-b286-4413-88e2-203d559fd88c",
    2: "prog-uuid-2",
    3: "prog-uuid-3"
}

HOME_FLOW_UUID = "898d01d5-f931-45ab-82d4-a5caeb2a28a3"

def run_robot_program(program_id):
    flow_id = ROBOT_PROGRAMS.get(program_id)
    if not flow_id:
        raise ValueError("Invalid robot program ID")

    url = f"http://{ROBOT_IP}/api/v3.0/flows/{flow_id}/run"
    response = requests.put(url)
    response.raise_for_status()
    return response.json()

def move_home():
    url = f"http://{ROBOT_IP}/api/v3.0/flows/{HOME_FLOW_UUID}/run"
    response = requests.put(url)
    response.raise_for_status()
    return response.json()

def get_robot_status():
    url = f"http://{ROBOT_IP}/api/v3.0/variables"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # Expected to return variable list with joint/cartesian data
    except requests.exceptions.RequestException:
        return {"error": "Robot status not available"}

