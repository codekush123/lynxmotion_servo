from time import sleep
import serial

# Initialize serial connection
bus = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Define servo IDs (9 motors)
servo_ids = ['38', '33', '39', '35', '05', '29', '32', '31', '30']

# Define variables
flex = 45  # Angle to flex a joint
delay_time = 0.005  # Delay between phases (5 ms)
smoothness_delay = 0.015  # Delay for smooth transitions (15 ms)
start_pause = 3  # Initial delay (3 s)
base_position = 1500  # Center position in microseconds (90 degrees)

# Convert angle to pulse width (0-180 degrees to 500-2500 µs)
def angle_to_pulse(angle):
    return int(500 + (angle / 180) * 2000)

# Send servo command over UART
def send_servo_command(servo_id, position, time_ms=15):
    command = f"#{servo_id}P{position}T{time_ms}\r"
    bus.write(command.encode())

# Set initial snake position
def set_initial_position():
    send_servo_command(servo_ids[0], angle_to_pulse(0), 1000)  # s1 at 0 degrees
    for i in range(1, 9):  # s2-s9 at 90 degrees
        send_servo_command(servo_ids[i], angle_to_pulse(90), 1000)
    sleep(start_pause)

# Rectilinear forward motion
def forward_motion():
    # Phase 1: s9, s8, s7
    for pos in range(flex + 1):
        s9_angle = 90 - pos
        s8_angle = 90 + 2 * pos
        s7_angle = 90 - pos
        send_servo_command(servo_ids[8], angle_to_pulse(s9_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[7], angle_to_pulse(s8_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[6], angle_to_pulse(s7_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    # Phase 2: s9, s8, s7, s6
    for pos in range(flex + 1):
        s9_angle = 90 - flex + pos
        s8_angle = 90 + 2 * flex - 3 * pos
        s7_angle = 90 - flex + 3 * pos
        s6_angle = 90 - pos
        send_servo_command(servo_ids[8], angle_to_pulse(s9_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[7], angle_to_pulse(s8_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[6], angle_to_pulse(s7_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[5], angle_to_pulse(s6_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    # Phase 3: s8, s7, s6, s5
    for pos in range(flex + 1):
        s8_angle = 90 - flex + pos
        s7_angle = 90 + 2 * flex - 3 * pos
        s6_angle = 90 - flex + 3 * pos
        s5_angle = 90 - pos
        send_servo_command(servo_ids[7], angle_to_pulse(s8_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[6], angle_to_pulse(s7_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[5], angle_to_pulse(s6_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[4], angle_to_pulse(s5_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    # Phase 4: s7, s6, s5, s4
    for pos in range(flex + 1):
        s7_angle = 90 - flex + pos
        s6_angle = 90 + 2 * flex - 3 * pos
        s5_angle = 90 - flex + 3 * pos
        s4_angle = 90 - pos
        send_servo_command(servo_ids[6], angle_to_pulse(s7_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[5], angle_to_pulse(s6_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[4], angle_to_pulse(s5_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[3], angle_to_pulse(s4_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    # Phase 5: s6, s5, s4, s3
    for pos in range(flex + 1):
        s6_angle = 90 - flex + pos
        s5_angle = 90 + 2 * flex - 3 * pos
        s4_angle = 90 - flex + 3 * pos
        s3_angle = 90 - pos
        send_servo_command(servo_ids[5], angle_to_pulse(s6_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[4], angle_to_pulse(s5_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[3], angle_to_pulse(s4_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[2], angle_to_pulse(s3_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    # Phase 6: s5, s4, s3, s2
    for pos in range(flex + 1):
        s5_angle = 90 - flex + pos
        s4_angle = 90 + 2 * flex - 3 * pos
        s3_angle = 90 - flex + 3 * pos
        s2_angle = 90 - pos
        send_servo_command(servo_ids[4], angle_to_pulse(s5_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[3], angle_to_pulse(s4_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[2], angle_to_pulse(s3_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[1], angle_to_pulse(s2_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    # Phase 7: s4, s3, s2
    for pos in range(flex + 1):
        s4_angle = 90 - flex + pos
        s3_angle = 90 + 2 * flex - 2 * pos
        s2_angle = 90 - flex + pos
        send_servo_command(servo_ids[3], angle_to_pulse(s4_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[2], angle_to_pulse(s3_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[1], angle_to_pulse(s2_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

# Main execution
def main():
    try:
        set_initial_position()
        while True:
            forward_motion()
    except KeyboardInterrupt:
        pass
    finally:
        bus.close()

if __name__ == "__main__":
    main()