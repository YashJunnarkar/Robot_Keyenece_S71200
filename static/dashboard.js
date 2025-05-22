function startSequence() {
  const robotProgram = document.getElementById("robot_program").value;
  const cameraProgram = document.getElementById("camera_program").value;

  fetch("/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ robot_program: robotProgram, camera_program: cameraProgram }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("status_message").style.display = "block";
      document.getElementById("status_message").innerText = data.message;
      updateStatus(); // refresh after completion
    });
}

function updateStatus() {
  fetch("/update_status")
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("robot_pose").innerHTML = data.robot_pose;
      document.getElementById("camera_result").innerText = data.camera_result;
      document.getElementById("plc_status").innerText = data.plc_status;
    });
}

// Auto-refresh every 5 seconds
setInterval(updateStatus, 5000);
window.onload = updateStatus;
