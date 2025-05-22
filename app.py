from flask import Flask, render_template, redirect, url_for
import plc
import Robot

app = Flask(__name__)

is_connected = False
status_message = ""

@app.route('/')
def index():
    global status_message, is_connected
    msg = status_message
    status_message = ""
    return render_template('index.html', status=msg, connected=is_connected)

@app.route('/connect')
def connect():
    global status_message, is_connected
    try:
        is_connected = plc.connect()
        if is_connected:
            status_message = "PLC connected successfully."
        else:
            status_message = "PLC connection failed."
    except Exception as e:
        is_connected = False
        status_message = f"PLC connection error: {e}"
    return redirect(url_for('index'))

@app.route('/disconnect')
def disconnect():
    global status_message, is_connected
    try:
        plc.disconnect()
        is_connected = False
        status_message = "PLC disconnected."
    except Exception as e:
        status_message = f"PLC disconnect error: {e}"
    return redirect(url_for('index'))

@app.route('/toggle')
def toggle():
    global status_message, is_connected
    if not is_connected:
        status_message = "PLC not connected! Connect first."
        return redirect(url_for('index'))
    try:
        new_state = plc.toggle_bit()
        status_message = f"Bit toggled to {new_state}"
    except Exception as e:
        status_message = f"Toggle failed: {e}"
    return redirect(url_for('index'))

@app.route('/run_sequence')
def run_sequence():
    global status_message, is_connected
    if not is_connected:
        status_message = "PLC not connected! Connect first."
        return redirect(url_for('index'))
    try:
        Robot.move_to_object()
        plc.set_bit(True)  # e.g. take picture
        Robot.move_home()
        plc.set_bit(False)
        status_message = "Full sequence executed successfully."
    except Exception as e:
        status_message = f"Sequence error: {e}"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
