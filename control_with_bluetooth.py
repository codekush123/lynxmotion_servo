from time import sleep
import math
import serial

bus = serial.Serial(
    port='/dev/rfcomm0',  
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
phase_diff = math.pi / 5

def angle_to_pulse(angle):
    return int(base_position + (angle / 90.0) * 500)

def move_servo(sid, angle, duration=50):
    pulse = angle_to_pulse(angle)
    bus.write(f'#{sid}P{pulse}T{duration}\r'.encode('utf-8'))

def reset_servos():
    print("Resetting servos to neutral...")
    bus.write(f'#38LED0\r'.encode('utf-8'))
    bus.write(f'#33LED0\r'.encode('utf-8'))
    bus.write(f'#39LED0\r'.encode('utf-8'))
    bus.write(f'#35LED0\r'.encode('utf-8'))
    bus.write(f'#05LED0\r'.encode('utf-8'))
    bus.write(f'#32LED0\r'.encode('utf-8'))
    bus.write(f'#38WR0\r'.encode('utf-8'))  
    for sid in servo_ids[1:]:
        move_servo(sid, 0, duration=500)

print("Waiting for Bluetooth command... (type 'RUN' to start, 'STOP' to end)")

try:
    running = False
    t = 0
    dt = 0.05

    while True:
        if bus.in_waiting > 0:
            command = bus.readline().decode().strip().upper()
            print("Received:", command)

            if command == "RUN":
                print("Starting servo wave loop...")
                running = True
            elif command == "STOP":
                print("Stopping servo wave loop...")
                running = False
                reset_servos()

        if running:
            bus.write(f'#38LED5\r'.encode('utf-8'))
            bus.write(f'#33LED6\r'.encode('utf-8'))
            bus.write(f'#39LED5\r'.encode('utf-8'))
            bus.write(f'#35LED6\r'.encode('utf-8'))
            bus.write(f'#05LED5\r'.encode('utf-8'))
            bus.write(f'#32LED6\r'.encode('utf-8'))
            bus.write(f'#38WR60\r'.encode('utf-8'))  
            for idx, sid in enumerate(servo_ids[1:]):
                phase = 2 * math.pi * (t / period) + idx * phase_diff
                angle = amplitude * math.sin(phase)
                move_servo(sid, angle, duration=50)
            t += dt
            sleep(dt)
        else:
            sleep(0.1)

except KeyboardInterrupt:
    print("Interrupted by user.")
    reset_servos()
    bus.close()
