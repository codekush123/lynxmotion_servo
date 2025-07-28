from time import sleep
import math
import serial
import keyboard

bus = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

servo_ids = ['38', '33', '39', '35', '05', '29', '32', '31', '30']

base_position = 1500  # Neutral position in microseconds (90 degrees)
amplitude = 40 * (1000 / 90)  # Amplitude in microseconds (40 degrees)
lag = 0.5712  # Phase shift in radians
frequency = 1  # Oscillation frequency
right_offset = 5 * (1000 / 90)  # Right turn offset in microseconds
left_offset = -5 * (1000 / 90)  # Left turn offset in microseconds
offset = 6 * (1000 / 90)  # Offset for first three servos in microseconds
delay_time = 0.007  # Time between movements in seconds
start_pause = 3  # Initial pause in seconds

def angle_to_pulse(angle):
    return int(500 + (angle / 180) * 2000)

def send_servo_command(servo_id, position, time_ms=7):
    command = f"#{servo_id}P{position}T{time_ms}\r"
    bus.write(command.encode())

def set_initial_position():
    for i, servo_id in enumerate(servo_ids):
        phase = (4 - i) * lag  # Phases from 4*lag to -4*lag for 9 servos
        servo_offset = offset if i in [0, 1, 2] else 0
        angle = 90 + (servo_offset / (1000 / 90)) + (amplitude / (1000 / 90)) * math.cos(phase)
        pulse = angle_to_pulse(angle)
        send_servo_command(servo_id, pulse, 1000)
    sleep(start_pause)

def serpentine_motion(direction='forward'):
    counter = 0
    step = 1
    if direction == 'reverse':
        counter = 360
        step = -1
    
    for counter in range(counter, 360 if step == 1 else 0, step):
        for i, servo_id in enumerate(servo_ids):
            phase = (4 - i) * lag  
            turn_offset = 0
            if direction == 'right':
                if counter < 10:
                    turn_offset = 0.1 * counter * right_offset
                elif counter < 350:
                    turn_offset = right_offset
                else:
                    turn_offset = 0.1 * (360 - counter) * right_offset
            elif direction == 'left':
                if counter < 10:
                    turn_offset = 0.1 * counter * left_offset
                elif counter < 350:
                    turn_offset = left_offset
                else:
                    turn_offset = 0.1 * (360 - counter) * left_offset
            servo_offset = offset if i in [0, 1, 2] else 0
            angle = 90 + (servo_offset / (1000 / 90)) + (turn_offset / (1000 / 90)) + \
                    (amplitude / (1000 / 90)) * math.cos(frequency * counter * math.pi / 180 + phase)
            pulse = angle_to_pulse(angle)
            send_servo_command(servo_id, pulse, int(delay_time * 1000))
        sleep(delay_time)
    
    return direction if direction in ['forward', 'reverse'] else 'forward'

def main():
    try:
        set_initial_position()
        current_direction = 'forward'
        while True:
            if keyboard.is_pressed('f'):
                current_direction = 'forward'
            elif keyboard.is_pressed('v'):
                current_direction = 'reverse'
            elif keyboard.is_pressed('l'):
                current_direction = 'left'
            elif keyboard.is_pressed('r'):
                current_direction = 'right'
            elif keyboard.is_pressed('s'):
                break
            current_direction = serpentine_motion(current_direction)
    except KeyboardInterrupt:
        pass
    finally:
        bus.close()

if __name__ == "__main__":
    main()