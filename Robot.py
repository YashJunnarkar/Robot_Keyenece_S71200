# robot.py
import requests

robot_ip = "192.168.1.4"
go_to_object_flow = "acab861e-b286-4413-88e2-203d559fd88c"
go_home_flow = "898d01d5-f931-45ab-82d4-a5caeb2a28a3"

def run_flow(flow_id):
    url = f"http://{robot_ip}/api/v3.0/flows/{flow_id}/run"
    try:
        response = requests.put(url)
        response.raise_for_status()
        print(f"✅ Flow {flow_id} started successfully")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Robot flow error: {e}")
        return False

def move_to_object():
    return run_flow(go_to_object_flow)

def move_to_home():
    return run_flow(go_home_flow)
