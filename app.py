import pyautogui
import math
import time
import threading
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure logging for detailed debug output.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Enable the fail-safe feature by moving the mouse to a screen corner.
pyautogui.FAILSAFE = True

movement_thread = None
stop_event = None


def move_cursor_circle(center_x, center_y, radius, steps, duration, stop_event):
    delay = duration / steps
    for i in range(steps):
        if stop_event.is_set():
            logging.info("Circle movement stopped by user.")
            break
        angle = 2 * math.pi * i / steps
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        pyautogui.moveTo(x, y)
        time.sleep(delay)


def move_cursor_figure_eight(center_x, center_y, radius, steps, duration, stop_event):
    delay = duration / steps
    for i in range(steps):
        if stop_event.is_set():
            logging.info("Figure-eight movement stopped by user.")
            break
        angle = 2 * math.pi * i / steps
        x = center_x + radius * math.sin(angle)
        y = center_y + radius * math.sin(angle) * math.cos(angle)
        pyautogui.moveTo(x, y)
        time.sleep(delay)


def move_cursor_spiral(center_x, center_y, max_radius, steps, duration, stop_event):
    delay = duration / steps
    for i in range(steps):
        if stop_event.is_set():
            logging.info("Spiral movement stopped by user.")
            break
        angle = 6 * math.pi * i / steps
        current_radius = max_radius * (i / steps)
        x = center_x + current_radius * math.cos(angle)
        y = center_y + current_radius * math.sin(angle)
        pyautogui.moveTo(x, y)
        time.sleep(delay)


def move_cursor_square(center_x, center_y, side_length, steps_per_side, duration, stop_event):
    total_steps = steps_per_side * 4
    delay = duration / total_steps
    half_side = side_length / 2
    corners = [
        (center_x - half_side, center_y - half_side),
        (center_x + half_side, center_y - half_side),
        (center_x + half_side, center_y + half_side),
        (center_x - half_side, center_y + half_side)
    ]
    for i in range(4):
        start_corner = corners[i]
        end_corner = corners[(i + 1) % 4]
        for step in range(steps_per_side):
            if stop_event.is_set():
                logging.info("Square movement stopped by user.")
                return
            progress = step / steps_per_side
            x = start_corner[0] + (end_corner[0] - start_corner[0]) * progress
            y = start_corner[1] + (end_corner[1] - start_corner[1]) * progress
            pyautogui.moveTo(x, y)
            time.sleep(delay)


def move_cursor_zigzag(center_x, center_y, width, height, steps, duration, stop_event):
    delay = duration / steps
    half_width = width / 2
    half_height = height / 2
    for i in range(steps):
        if stop_event.is_set():
            logging.info("Zigzag movement stopped by user.")
            break
        progress = i / steps
        x = center_x + half_width * math.sin(8 * math.pi * progress)
        y = center_y - half_height + height * progress
        pyautogui.moveTo(x, y)
        time.sleep(delay)


def run_movement(movement_type, size, duration, steps):
    global stop_event
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width / 2
    center_y = screen_height / 2
    try:
        if movement_type == "Circle":
            move_cursor_circle(center_x, center_y, size, steps, duration, stop_event)
        elif movement_type == "Figure Eight":
            move_cursor_figure_eight(center_x, center_y, size, steps, duration, stop_event)
        elif movement_type == "Spiral":
            move_cursor_spiral(center_x, center_y, size, steps, duration, stop_event)
        elif movement_type == "Square":
            move_cursor_square(center_x, center_y, size * 1.5, max(steps // 4, 1), duration, stop_event)
        elif movement_type == "Zigzag":
            move_cursor_zigzag(center_x, center_y, size * 2, size * 1.5, steps, duration, stop_event)
        logging.info(f"{movement_type} movement completed.")
    except Exception as e:
        logging.error(f"Error in movement: {e}")


@app.route('/start-movement', methods=['POST'])
def start_movement():
    global movement_thread, stop_event
    if movement_thread and movement_thread.is_alive():
        return jsonify({"status": "Movement already running."}), 400

    data = request.get_json()
    movement_type = data.get("movementType", "Circle")
    size = int(data.get("size", 100))
    duration = int(data.get("duration", 5))
    steps = int(data.get("steps", 100))

    logging.info(f"Starting movement: {movement_type} with size={size}, duration={duration}, steps={steps}")
    stop_event = threading.Event()
    movement_thread = threading.Thread(
        target=run_movement,
        args=(movement_type, size, duration, steps),
        daemon=True
    )
    movement_thread.start()

    return jsonify({"status": f"Started {movement_type} movement."})


@app.route('/stop-movement', methods=['POST'])
def stop_movement():
    global stop_event
    if stop_event:
        stop_event.set()
        logging.info("Stop event set. Movement stopping.")
        return jsonify({"status": "Stopping movement."})
    else:
        return jsonify({"status": "No movement to stop."}), 400

@app.route('/')
def home():
    return "Mouse Control API is running."


if __name__ == '__main__':
    # Run on localhost:5000 (adjust host/port as needed)
    app.run(debug=True)
