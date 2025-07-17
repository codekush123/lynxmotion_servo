from time import sleep
import math
import serial

bus = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

servo_ids = ['38', '33', '39', '35', '05', '32']

base_position = 1500
amplitude = 90
period = 1
lift_offset = 30
phase_diff = math.pi / 5
t = 0
dt = 0.05

def angle_to_pulse(angle):
    return int(base_position + (angle / 90.0) * 500)

def move_servo(sid, angle, duration=50):
    pulse = angle_to_pulse(angle)
    bus.write(f'#{sid}P{pulse}T{duration}\r'.encode('utf-8'))

try:
    while True:
        for idx, sid in enumerate(servo_ids[1:]):
            phase = 2 * math.pi * (t / period) + idx * phase_diff
            angle = amplitude * math.sin(phase) + lift_offset

            if sid in ['39', '35']:
                lift = lift_offset*math.exp(-((math.sin(phase))**2))
                angle += lift
            
            move_servo(sid, angle, duration=50)

        t += dt
        sleep(dt)

except KeyboardInterrupt:
    print("Interrupted! Returning all servos to neutral...")

    for sid in servo_ids[1:]:
        move_servo(sid, 0, duration=500)

    bus.close()
    print("Bus closed.")