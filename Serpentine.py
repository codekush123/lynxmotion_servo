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

servo_ids = ['38', '33', '39', '35', '05', '29', '32', '31', '30', '34', '36', '37']
base_position = 1500  # Neutral position for servos
amplitude = 40 * (1000 / 90)  #wave in degrees
lag = 0.5712  #phase shift in radians
frequency = 1 #speed
right_offset = 5 * (1000 / 90)  #right turn
left_offset = -5 * (1000 / 90)  #left turn
offset = 6 * (1000 / 90)  #first three servos offset
delay_time = 0.007  #time between movements in seconds
start_pause = 3 #initial pause

def angle_to_pulse(angle):
    return int(500 + (angle / 180) * 2000)

def send_servo_command(servo_id, position, time_ms=7):
    command = f"#{servo_id}P{position}T{time_ms}\r"
    bus.write(command.encode())

def set_initial_position():
    for i, servo_id in enumerate(servo_ids):
        phase = (5 - i) * lag  
        angle = 90 + (offset / (1000 / 90)) + (amplitude / (1000 / 90)) * math.cos(phase)
        pulse = angle_to_pulse(angle)
        send_servo_command(servo_id, pulse, 1000)  
    sleep(start_pause)

def serpentine_motion(direction='forward'):
    counter = 0
    if direction == 'reverse':
        counter = 360
        step = -1
    else:
        step = 1

    while True:
        for counter in range(0, 360, step) if direction != 'reverse' else range(360, 0, -1):
            for i, servo_id in enumerate(servo_ids):
                phase = (5 - i) * lag
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
        if direction not in ['forward', 'reverse']:
            break 

def main():
    try:
        set_initial_position()
        print("Snake robot ready. Enter command (forward/reverse/right/left/stop):")
        while True:
            command = input().strip().lower()
            if command == 'stop':
                break
            if command in ['forward', 'reverse', 'right', 'left']:
                serpentine_motion(command)
            else:
                print("Invalid command. Use forward, reverse, right, left, or stop.")
    finally:
        bus.close()

if __name__ == "__main__":
    main()