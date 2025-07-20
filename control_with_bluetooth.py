from time import sleep
import math
import serial

# Setup UART Serial (for Bluetooth serial, use /dev/rfcomm0)
bus = serial.Serial(
    port='/dev/rfcomm0',  # Change from /dev/ttyS0 to /dev/rfcomm0
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
    bus.write(f'#38WR0\r'.encode('utf-8'))  # Disable servo power
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
            bus.write(f'#38WR60\r'.encode('utf-8'))  # Enable servo power
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
