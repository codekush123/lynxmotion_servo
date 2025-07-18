from time import sleep
import math
import serial
import threading

servo_bus = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

bt_bus = serial.Serial('/dev/rfcomm0', 9600, timeout=1)  

servo_ids = ['38', '33', '39', '35', '05', '32']
base_position = 1500
amplitude = 90
period = 1
phase_diff = math.pi / 5

t = 0
dt = 0.05

run_animation = True  

def angle_to_pulse(angle):
    return int(base_position + (angle / 90.0) * 500)

def move_servo(sid, angle, duration=50):
    pulse = angle_to_pulse(angle)
    cmd = f'#{sid}P{pulse}T{duration}\r'
    servo_bus.write(cmd.encode('utf-8'))

def animation_loop():
    global t
    while True:
        if run_animation:
            servo_bus.write(f'#38WR60\r'.encode('utf-8'))

            for idx, sid in enumerate(servo_ids[1:]):  
                phase = 2 * math.pi * (t / period) + idx * phase_diff
                angle = amplitude * math.sin(phase)
                move_servo(sid, angle, duration=50)

            t += dt

        sleep(dt)

def bluetooth_command_listener():
    global run_animation

    print("Listening for Bluetooth commands...")

    while True:
        if bt_bus.in_waiting:
            cmd = bt_bus.readline().decode().strip()
            print(f"[Bluetooth] Received: {cmd}")

            if cmd.lower() == "stop":
                run_animation = False
                servo_bus.write(f'#38WR0\r'.encode('utf-8'))  
                for sid in servo_ids[1:]:
                    move_servo(sid, 0, duration=500)

            elif cmd.lower() == "start":
                run_animation = True

            elif cmd.lower() == "rest":
                run_animation = False
                servo_bus.write(f'#38WR0\r'.encode('utf-8'))
                for sid in servo_ids[1:]:
                    move_servo(sid, -20 if sid in ['33', '39'] else 0, duration=600)

        sleep(0.1)

try:
    threading.Thread(target=animation_loop, daemon=True).start()
    threading.Thread(target=bluetooth_command_listener, daemon=True).start()

    while True:
        sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    run_animation = False
    servo_bus.write(f'#38WR0\r'.encode('utf-8'))
    for sid in servo_ids[1:]:
        move_servo(sid, 0, duration=500)
    servo_bus.close()
    bt_bus.close()
    print("Ports closed.")
