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

servo_ids = ['27', '05', '33', '35', '29', '39', '32', '25', '24']
base_position = 1500  # Neutral position in microseconds (90 degrees)
amplitude = 90
period = 1.5
phase_diff = math.pi / 3

t = 0                                                           
dt = 0.05
def angle_to_pulse(angle):
    return int(base_position + (angle / 90.0) * 500)                        

def move_servo(sid, angle, duration=50):
    pulse = angle_to_pulse(angle)                                   
    bus.write(f'#{sid}P{pulse}T{duration}\r'.encode('utf-8'))


def fold_snake(duration=800):
    n = len(servo_ids)
    segment_angle = 360 / n

    def safe_angle(angle):
        a = a - 180 if a > 180 else a
        return max(-90, min(90, a))
    
    for sid in servo_ids:
        if sid == '29':
            angle = -safe_angle(segment_angle)
        else:
            angle = safe_angle(segment_angle)
        move_servo(sid, angle, duration)
    sleep(duration / 1000.0)

try:
    while True:
        for idx, sid in enumerate(servo_ids):
            phase = 2 * math.pi *(t /period) + idx * phase_diff
            angle = amplitude * math.sin(phase)
            move_servo(sid, angle, duration=50)
        t += dt
        sleep(dt)
except KeyboardInterrupt:
    target_angle = 90
    target_pulse = angle_to_pulse(target_angle)
    duration = 800

    for sid in servo_ids:
        bus.write(f'#{sid}P{target_pulse}T{duration}\r'.encode('utf-8'))
    sleep(1)
    bus.close()
    print("Bus Closed!!")