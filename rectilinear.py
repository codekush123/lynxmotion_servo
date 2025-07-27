from time import sleep
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

flex = 45  # Angle to flex a joint
delay_time = 0.005  # Delay between phases (5 ms)
smoothness_delay = 0.015  # Delay for smooth transitions (15 ms)
start_pause = 3  # Initial delay (5 s)
base_position = 1500  # Center position in microseconds (90 degrees)

def angle_to_pulse(angle):
    return int(500 + (angle / 180) * 2000)

def send_servo_command(servo_id, position, time_ms=15):
    command = f"#{servo_id}P{position}T{time_ms}\r"
    bus.write(command.encode())

def set_initial_position():
    send_servo_command(servo_ids[0], angle_to_pulse(0), 1000)  
    for i in range(1, 12):  
        send_servo_command(servo_ids[i], angle_to_pulse(90), 1000)
    sleep(start_pause)

def forward_motion():
    for pos in range(flex + 1):
        s12_angle = 90 - pos
        s11_angle = 90 + 2 * pos
        s10_angle = 90 - pos
        send_servo_command(servo_ids[11], angle_to_pulse(s12_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[10], angle_to_pulse(s11_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[9], angle_to_pulse(s10_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    for pos in range(flex + 1):
        s12_angle = 90 - flex + pos
        s11_angle = 90 + 2 * flex - 3 * pos
        s10_angle = 90 - flex + 3 * pos
        s9_angle = 90 - pos
        send_servo_command(servo_ids[11], angle_to_pulse(s12_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[10], angle_to_pulse(s11_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[9], angle_to_pulse(s10_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[8], angle_to_pulse(s9_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    for pos in range(flex + 1):
        s11_angle = 90 - flex + pos
        s10_angle = 90 + 2 * flex - 3 * pos
        s9_angle = 90 - flex + 3 * pos
        s8_angle = 90 - pos
        send_servo_command(servo_ids[10], angle_to_pulse(s11_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[9], angle_to_pulse(s10_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[8], angle_to_pulse(s9_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[7], angle_to_pulse(s8_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

    for pos in range(flex + 1):
        s10_angle = 90 - flex + pos
        s9_angle = 90 + 2 * flex - 3 * pos
        s8_angle = 90 - flex + 3 * pos
        s7_angle = 90 - pos
        send_servo_command(servo_ids[9], angle_to_pulse(s10_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[8], angle_to_pulse(s9_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[7], angle_to_pulse(s8_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[6], angle_to_pulse(s7_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

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

    for pos in range(flex + 1):
        s6_angle = 90 - flex + pos
        s5_angle = 90 + 2 * flex - 3 * pos
        s4_angle = 90 - flex + 3 * pos
        s3_angle = 90 - pos
        send_servo_command(servo_ids[5], angle_to_pulse(s6_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[4], angle_to_pulse(s5_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[2], angle_to_pulse(s3_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

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

    for pos in range(flex + 1):
        s4_angle = 90 - flex + pos
        s3_angle = 90 + 2 * flex - 2 * pos
        s2_angle = 90 - flex + pos
        send_servo_command(servo_ids[3], angle_to_pulse(s4_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[2], angle_to_pulse(s3_angle), int(smoothness_delay * 1000))
        send_servo_command(servo_ids[1], angle_to_pulse(s2_angle), int(smoothness_delay * 1000))
        sleep(smoothness_delay)
    sleep(delay_time)

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