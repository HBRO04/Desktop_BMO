import tkinter as tk
import random
import sys
import os

root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "white")

# --- Helper for PyInstaller resource path ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Load GIF frames ---
def load_frames(filename):
    frames = []
    i = 0
    while True:
        try:
            frame = tk.PhotoImage(file=resource_path(filename), format=f"gif - {i}")
            frames.append(frame)
            i += 1
        except tk.TclError:
            break
    return frames

# Load animations
walking_right_frames = load_frames("BMO_walking_right.gif")
walking_left_frames = load_frames("BMO_walking_left.gif")
idle_frames = load_frames("BMO_idle.gif")
jumping_frames = load_frames("BMO_jumping.gif")
sleeping_frames = load_frames("BMO_sleeping.gif")
waving_frames = load_frames("BMO_waving.gif")
blinking_frames = load_frames("BMO_blinking.gif")
dragging_frames = load_frames("BMO_dragging.gif")

# BMO label
label = tk.Label(root, bd=0, bg="white")
label.pack()

# --- Variables ---
frame_index = 0
behavior = "walking"
behavior_timer = 0
direction = "right"
waving_flag = False
sleeping_toggle = False

# Movement
x, y = 200, 200
dx, dy = 2, 2
dragging = False
offset_x = 0
offset_y = 0

frames_dict = {
    "walking_right": walking_right_frames,
    "walking_left": walking_left_frames,
    "idle": idle_frames,
    "jumping": jumping_frames,
    "sleeping": sleeping_frames,
    "waving": waving_frames,
    "blinking": blinking_frames,
    "dragging": dragging_frames
}

# --- Animation ---
def animate():
    global frame_index
    if sleeping_toggle:
        current_frames = frames_dict["sleeping"]
        delay = 300
    else:
        if behavior == "walking":
            current_frames = frames_dict[f"walking_{direction}"]
            delay = 100
        elif behavior == "idle" and random.random() < 0.02:
            current_frames = frames_dict.get("blinking", frames_dict["idle"])
            delay = 100
        elif behavior == "idle":
            current_frames = frames_dict.get("idle", [])
            delay = 300
        else:
            current_frames = frames_dict.get(behavior, [])
            delay = 150

    if current_frames:
        frame = current_frames[frame_index % len(current_frames)]
        label.config(image=frame)
        frame_index = (frame_index + 1) % len(current_frames)

    root.after(delay, animate)

# --- Movement & behavior ---
def move_pet():
    global x, y, dx, dy, behavior, behavior_timer, direction, waving_flag, frame_index

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    mouse_x = root.winfo_pointerx()
    mouse_y = root.winfo_pointery()

    if not dragging and not sleeping_toggle:
        # Handle waving
        if waving_flag:
            behavior_timer -= 1
            if behavior_timer <= 0:
                waving_flag = False
                behavior = "walking"
        else:
            if behavior_timer > 0:
                behavior_timer -= 1
            else:
                if abs(mouse_x - x) < 200 and abs(mouse_y - y) < 200 and random.random() < 0.2:
                    behavior = "waving"
                    behavior_timer = len(frames_dict["waving"]) * 2
                    frame_index = 0
                    waving_flag = True
                else:
                    behavior = random.choices(
                        ["walking", "idle", "jumping", "sleeping"],
                        weights=[50, 20, 20, 10], k=1
                    )[0]
                    if behavior == "walking":
                        behavior_timer = random.randint(50, 150)
                    elif behavior == "idle":
                        behavior_timer = random.randint(30, 80)
                    elif behavior == "jumping":
                        behavior_timer = random.randint(20, 40)
                    elif behavior == "sleeping":
                        behavior_timer = random.randint(100, 200)

        # Normal movement
        if behavior == "walking":
            x += dx
            y += dy
            if x <= 0 or x >= screen_w - 128:
                dx = -dx
            if y <= 0 or y >= screen_h - 128:
                dy = -dy
            direction = "right" if dx > 0 else "left"
        elif behavior == "jumping":
            y -= 5
            root.after(100, restore_jump)

    # Update window position
    root.geometry(f"+{x}+{y}")
    root.after(30, move_pet)

def restore_jump():
    global y
    y += 5

# --- Dragging ---
def start_drag(event):
    global dragging, offset_x, offset_y, behavior, frame_index, dx, dy
    dragging = True
    behavior = "dragging"
    frame_index = 0
    offset_x = event.x
    offset_y = event.y

def do_drag(event):
    global x, y
    x = event.x_root - offset_x
    y = event.y_root - offset_y
    root.geometry(f"+{x}+{y}")

def stop_drag(event):
    global dragging, behavior, frame_index, dx, dy
    dragging = False
    behavior = "walking"
    frame_index = 0
    dx = 2
    dy = 2

# --- Right-click sleep toggle ---
def toggle_sleep(event):
    global behavior, sleeping_toggle, frame_index, dx, dy
    if not sleeping_toggle:
        sleeping_toggle = True
        behavior = "sleeping"
        frame_index = 0
        dx = 0
        dy = 0
    else:
        sleeping_toggle = False
        behavior = "walking"
        frame_index = 0
        dx = 2
        dy = 2

# --- Middle-click exit ---
def exit_program(event):
    root.destroy()

# --- Bindings ---
label.bind("<Button-1>", start_drag)
label.bind("<B1-Motion>", do_drag)
label.bind("<ButtonRelease-1>", stop_drag)
label.bind("<Button-3>", toggle_sleep)
label.bind("<Button-2>", exit_program)

# --- Start loops ---
animate()
move_pet()
root.mainloop()
