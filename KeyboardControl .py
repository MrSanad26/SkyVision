from djitellopy import tello
import KeyPressModule as kp
from time import sleep
kp.init()
me = tello.Tello()
me.connect()
me.streamon()

# Drone Movement
def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    # Move to the left using "a"
    if kp.getKey("a"):
        lr = -speed
    # Move to the rigth using "d"
    elif kp.getKey("d"):
        lr = speed
    # Move forward using "w"
    if kp.getKey("w"):
        fb = speed
    # Move backward using "s"
    elif kp.getKey("s"):
        fb = -speed
    # increase height
    if kp.getKey("UP"):
        ud = speed
    # Decrease heightt
    elif kp.getKey("DOWN"):
        ud = -speed
    # Routate to left
    if kp.getKey("q"):
        yv = -speed
    # Routate to right
    elif kp.getKey("e"):
        yv = speed
    # Landing
    if kp.getKey("l"):
        me.land()
        sleep(3)
    # Takeoff
    if kp.getKey("t"):
        me.takeoff()
    return [lr, fb, ud, yv]


while True:
    print(me.get_battery())
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)



    