import mujoco
import mujoco.viewer
import numpy as np
import time

model_path = r"C:\Users\Bharaath\physical-ai-challange-2026\workshop\dev\docker\workspace\src\so101_mujoco\mujoco\scene.xml"

model = mujoco.MjModel.from_xml_path(model_path)
data = mujoco.MjData(model)

# cube geom id (NOT body)
geom_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, "red_box")

print("FINAL VISUAL PICK & PLACE (STABLE)")

def step():
    mujoco.mj_step(model, data)
    viewer.sync()
    time.sleep(0.01)

def move(target, steps=120):
    target = np.array(target)
    start = data.ctrl.copy()

    for i in range(steps):
        alpha = i / steps
        data.ctrl[:] = (1 - alpha) * start + alpha * target
        step()

# 🔥 VISIBILITY CONTROL (KEY FIX)
def hide_cube():
    model.geom_rgba[geom_id][3] = 0.0   # invisible

def show_cube():
    model.geom_rgba[geom_id][3] = 1.0   # visible

with mujoco.viewer.launch_passive(model, data) as viewer:

    while viewer.is_running():

        # 🟢 ALIGN
        move([0.293, -0.141, -0.02, 1.56, 0, 0.5])

        # 🔽 DOWN
        move([0.293, 0.62, -0.02, 1.56, 0, 0.5])

        # 🔴 CLOSE (PICK MOMENT)
        move([0.293, 0.62, -0.02, 1.56, 0, -0.7], 80)

        # 🔥 DISAPPEAR (PICK)
        hide_cube()

        # 🔼 LIFT
        move([0.293, 0.15, -0.02, 1.4, 0, -0.7])

        # 🔁 MOVE SIDE
        move([1.0, 0.15, -0.02, 1.4, 0, -0.7])

        # 🔽 PLACE DOWN
        move([1.0, 0.62, -0.02, 1.4, 0, -0.7])

        # 🟢 OPEN
        move([1.0, 0.62, -0.02, 1.4, 0, 0.5], 80)

        # 🔥 REAPPEAR (PLACE)
        show_cube()

        # 🔼 MOVE UP
        move([1.0, 0.15, -0.02, 1.4, 0, 0.5])

        print("PLACED")

        time.sleep(2)

        # 🔄 RESET (cube already in original place)
        show_cube()

        print("RESET")

        time.sleep(1)