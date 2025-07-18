from time import sleep
import math
import serial

# Serial setup
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
breathing_amplitude = 15  
breathing_period = 4      
phase_diff = math.pi / 10  

def angle_to_pulse(angle):
    return int(base_position + (angle / 90.0) * 500)

def move_servo(sid, angle, duration=300):
    pulse = angle_to_pulse(angle)
    bus.write(f'#{sid}P{pulse}T{duration}\r'.encode('utf-8'))

t = 0
dt = 0.1  

try:
    while True:
        bus.write(b'#38WR15\r')  

        for idx, sid in enumerate(servo_ids[1:]):  
            phase = 2 * math.pi * (t / breathing_period) + idx * phase_diff
            angle = breathing_amplitude * math.sin(phase)
            move_servo(sid, angle, duration=300)

        t += dt
        sleep(dt)

except KeyboardInterrupt:
    print("Interrupted! Resetting servos...")

    bus.write(b'#38WR0\r')  

    for sid in servo_ids[1:]:
        move_servo(sid, 0, duration=500)

    bus.close()
    print("Bus closed.")
