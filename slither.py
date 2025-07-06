from time import sleep
import math
import serial


bus = serial.Serial(
    port = '/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

servo_ids = ['24', '39','27']

amplitude = 10
max_amplitude = 30
phase_offset = math.pi / 6
period = 2
base_position = 1500

def angle_to_pulse(angle):
    return int(base_position + (angle / 90.0) * 500)


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
            wave_phase = 2 * math.pi * (t / period)
            angle = amplitude * math.sin(wave_phase + idx * phase_offset)
            pulse = angle_to_pulse(angle)

            bus.write(f'#{sid}P{pulse}T100\r'.encode('utf-8'))

        t += dt
        sleep(dt)

except KeyboardInterrupt:
    print("Program terminated by user or keyboard interrupt!!")

    while amplitude > 0:
        amplitude = ramp_amplitude(amplitude, 0, step=1)

        for idx, sid in enumerate(servo_ids):
            wave_phase = 2 * math.pi * (t / period)
            angle = amplitude * math.sin(wave_phase + idx * phase_offset)
            pulse = angle_to_pulse(angle)

            bus.write(f'#{sid}P{pulse}T100\r'.encode('utf-8'))

        t += dt
        sleep(dt)


    for sid in servo_ids:
        bus.write(f'#{sid}P{base_position}T500\r'.encode('utf-8'))


print("Finished!!")
print("All servos returned to base position!!")
bus.close()
del bus

