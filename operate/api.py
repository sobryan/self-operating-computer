from flask import Flask, request, jsonify
import uuid
import threading
import time

app = Flask(__name__)

tasks = {}

def long_running_task(task_id, user_input):
    # Simulate a long-running task
    time.sleep(10)
    tasks[task_id] = "completed"

@app.route('/submit_task', methods=['POST'])
def submit_task():
    user_input = request.json.get('input')
    task_id = str(uuid.uuid4())
    tasks[task_id] = "in_progress"
    threading.Thread(target=long_running_task, args=(task_id, user_input)).start()
    return jsonify({"task_id": task_id})

@app.route('/check_status/<task_id>', methods=['GET'])
def check_status(task_id):
    status = tasks.get(task_id, "not_found")
    return jsonify({"task_id": task_id, "status": status})

if __name__ == '__main__':
    app.run(debug=True)
