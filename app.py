from flask import Flask, render_template, request, jsonify
import plc
import robot

app = Flask(__name__)

selected_robot_program = 1
selected_camera_program = 1

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start', methods=['POST'])
def start_sequence():
    global selected_robot_program, selected_camera_program

    data = request.get_json()
    selected_robot_program = int(data['robot_program'])
    selected_camera_program = int(data['camera_program'])

    try:
        robot.run_robot_program(selected_robot_program)
        plc.write_camera_program(selected_camera_program)
        plc.send_trigger()
        robot.move_home()

        return jsonify({"message": "✅ Sequence completed successfully!"})
    except Exception as e:
        return jsonify({"message": f"❌ Error: {str(e)}"}), 500

@app.route('/update_status')
def update_status():
    robot_data = robot.get_robot_status()
    camera_result = plc.read_camera_result()
    plc_status = "Connected" if plc.get_status() else "Disconnected"

    pose_info = ""
    if isinstance(robot_data, dict) and "variables" in robot_data:
        for var in robot_data["variables"]:
            pose_info += f"<strong>{var['name']}</strong>: {var['type']}<br>"
            if var['type'] == "jointPose":
                pose_info += f"Joint Angles: {var['value']}<br><br>"
            elif var['type'] == "cartesianPose":
                pose_info += f"Position: {var['value']['position']}<br>Orientation: {var['value']['orientation']}<br><br>"
    elif "error" in robot_data:
        pose_info = robot_data['error']

    return jsonify({
        "robot_pose": pose_info,
        "camera_result": camera_result,
        "plc_status": plc_status
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
