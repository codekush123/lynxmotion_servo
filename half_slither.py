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

servo_ids = ['27', '05', '33', '35', '29', '39', '32', '25', '23']

base_position = 1500          # Neutral pulse width
amplitude = 40                # Adjust for servo range, stay within limits
max_amplitude = 40
period = 1                    # Wave period in seconds 
phase_diff = math.pi / 2      # Phase difference between servos
dt = 0.05                     # Time between updates (seconds)
t = 0

def angle_to_pulse(angle):
    """Convert angle in degrees to PWM pulse value."""
    return int(base_position + (angle / 90.0) * 500)

def move_servo(sid, angle, duration=70):
    """Send command to move servo sid to given angle over specified duration."""
    pulse = angle_to_pulse(angle)
    cmd = f'#{sid}P{pulse}T{duration}\r'
    bus.write(cmd.encode('utf-8'))

try:
    print("Running smooth sine wave motion. Ctrl+C to stop.")
    while True:
        for idx, sid in enumerate(servo_ids):
            phase = 2 * math.pi * (t / period) + idx * phase_diff
            angle = (amplitude / 2) * (math.sin(phase) + 1)
            move_servo(sid, angle, duration=int(dt * 1000 * 1.5))
        t += dt
        sleep(dt)

except KeyboardInterrupt:
    print("\nInterrupted. Resetting servos to center.")
    for sid in servo_ids:
        move_servo(sid, 0, duration=500)
    bus.close()
    print("Bus closed. Exiting.")

except Exception as e:
    print(f"\nError: {e}")
    bus.close()
