from time import sleep
import math
import serial

# Configure serial port
bus = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

servo_ids = ['24', '39', '27', '34', '38']

# Parameters
amplitude = 20         # Starting amplitude in degrees
max_amplitude = 30
period = 2             # seconds per full cycle
base_position = 1500   # center pulse width

spatial_phase = math.pi / 4  # spatial phase offset between segments

def angle_to_pulse(angle):
    scale = 500  # ±500us for ±90°
    return int(base_position + (angle / 90.0) * scale)

def ramp_amplitude(current, target, step=1):
    if current > target:
        return max(current - step, target)
    elif current < target:
        return min(current + step, target)
    else:
        return current

t = 0
dt = 0.1

try:
    while True:
        amplitude = ramp_amplitude(amplitude, max_amplitude, step=1)

        for idx, sid in enumerate(servo_ids):
            # Traveling wave phase: time-based and spatial-based
            wave_phase = 2 * math.pi * (t / period) - idx * spatial_phase
            angle = amplitude * math.sin(wave_phase)
            pulse = angle_to_pulse(angle)

            # Debug print
            print(f"Servo {sid}: angle={angle:.2f}°, pulse={pulse}")

            bus.write(f'#{sid}P{pulse}T100\r'.encode('utf-8'))

        t += dt
        sleep(dt)

except KeyboardInterrupt:
    print("\nProgram interrupted! Ramping down...")

    while amplitude > 0:
        amplitude = ramp_amplitude(amplitude, 0, step=1)

        for idx, sid in enumerate(servo_ids):
            wave_phase = 2 * math.pi * (t / period) - idx * spatial_phase
            angle = amplitude * math.sin(wave_phase)
            pulse = angle_to_pulse(angle)

            print(f"Servo {sid}: angle={angle:.2f}°, pulse={pulse}")

            bus.write(f'#{sid}P{pulse}T100\r'.encode('utf-8'))

        t += dt
        sleep(dt)

    # Move servos back to center
    for sid in servo_ids:
        print(f"Servo {sid}: returning to center.")
        bus.write(f'#{sid}P{base_position}T500\r'.encode('utf-8'))

finally:
    bus.close()
    del bus
    print("Serial bus closed. Finished!!")
