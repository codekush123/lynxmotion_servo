from time import sleep
import serial

bus = serial.Serial(
    port='/dev/serial0',  
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

servo_ids = ['38', '33', '39', '35', '05', '29', '32', '31', '30']

flex = 45  # Angle to flex a joint
delay_time = 0.01  # Increased delay between phases
smoothness_delay = 0.03  # Increased smooth transition time
start_pause = 3  # Initial delay (3 s)

def angle_to_pulse(angle):
    angle = max(0, min(180, angle))  # Clamp to valid range
    return int(500 + (angle / 180) * 2000)

def send_servo_command(servo_id, position, time_ms=15):
    command = f"#{servo_id}P{position}T{time_ms}\r"
    bus.write(command.encode())
    bus.flush()  # Ensure transmission
    # print(f"Sent to Servo {servo_id}: {command.strip()}")  

def set_initial_position():
    send_servo_command(servo_ids[0], angle_to_pulse(0), 1000)  # s1 at 0 degrees
    for i in range(1, 9):  # s2-s9 at 90 degrees
        send_servo_command(servo_ids[i], angle_to_pulse(90), 1000)
    sleep(start_pause)

def forward_motion():
    phases = [
        (8, 7, 6),
        (8, 7, 6, 5),
        (7, 6, 5, 4),
        (6, 5, 4, 3),
        (5, 4, 3, 2),
        (4, 3, 2, 1),
        (3, 2, 1)
    ]
    
    for phase_index, phase in enumerate(phases):
        for pos in range(flex + 1):
            angles = []
            if phase_index == 0:
                angles = [90 - pos, 90 + 2 * pos, 90 - pos]
            elif phase_index == 1:
                angles = [90 - flex + pos, 90 + 2 * flex - 3 * pos,
                          90 - flex + 3 * pos, 90 - pos]
            elif phase_index == 2:
                angles = [90 - flex + pos, 90 + 2 * flex - 3 * pos,
                          90 - flex + 3 * pos, 90 - pos]
            elif phase_index == 3:
                angles = [90 - flex + pos, 90 + 2 * flex - 3 * pos,
                          90 - flex + 3 * pos, 90 - pos]
            elif phase_index == 4:
                angles = [90 - flex + pos, 90 + 2 * flex - 3 * pos,
                          90 - flex + 3 * pos, 90 - pos]
            elif phase_index == 5:
                angles = [90 - flex + pos, 90 + 2 * flex - 3 * pos,
                          90 - flex + 3 * pos, 90 - pos]
            elif phase_index == 6:
                angles = [90 - flex + pos, 90 + 2 * flex - 2 * pos,
                          90 - flex + pos]

            for i, sid in enumerate(phase):
                pulse = angle_to_pulse(angles[i])
                send_servo_command(servo_ids[sid], pulse, int(smoothness_delay * 1000))
            sleep(smoothness_delay)
        sleep(delay_time)

def main():
    try:
        set_initial_position()
        while True:
            forward_motion()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        bus.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()
