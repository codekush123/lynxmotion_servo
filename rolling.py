from time import sleep
import serial
import math

# Serial bus configuration
bus = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# IDs of 9 servos in order (assumed clockwise or counterclockwise layout)
servo_ids = ['27', '05', '33', '35', '29', '39', '32', '25', '24']

# Parameters
flex = 45              # Circle amplitude
delay_time = 0.15      # 150 ms between rolling steps
smoothnessDelay = 40   # 40 ms between micro-steps
rollState = 0          # Start state

def angle_to_pulse(angle):
    angle = max(0, min(180, angle))
    return int(500 + (angle / 180) * 2000)

def send_servo_command(servo_id, angle, duration):
    pulse = angle_to_pulse(angle)
    command = f"#{servo_id}P{pulse}T{duration}\r"
    print(f"Sending to servo {servo_id}: angle={angle:.2f}, pulse={pulse}")
    bus.write(command.encode())
    bus.flush()

def set_initial_pose():
    print("Setting all servos to neutral position (90°)...")
    for sid in servo_ids:
        send_servo_command(sid, 90, 1000)
    sleep(2)

def form_circle_pose(center_angle=90):
    print("Forming circular pose with inward-facing servos...")
    n = len(servo_ids)
    radius = 1  # Assume unit radius; only angle matters

    for i, sid in enumerate(servo_ids):
        angle_rad = 2 * math.pi * i / n
        x = radius * math.cos(angle_rad)
        y = radius * math.sin(angle_rad)

        # Calculate angle pointing toward the center (invert x and y)
        servo_angle = center_angle + math.degrees(math.atan2(-y, -x))

        # Clamp to servo limits (0–180)
        servo_angle = max(0, min(180, servo_angle))
        send_servo_command(sid, servo_angle, 500)

    sleep(2)

def roll_forward():
    global rollState
    s = {i+1: servo_ids[i] for i in range(len(servo_ids))}

    # Step 0: Form circle before rolling
    if rollState == 0:
        form_circle_pose()
        rollState = 1
        sleep(1)

    # Rolling steps
    for step in range(1, 9):
        print(f"Rolling step {step}")
        sleep(delay_time / 1000)
        for pos in range(flex):
            if step == 1:
                send_servo_command(s[9], 90-pos, smoothnessDelay)
                send_servo_command(s[8], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[7], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[6], 90-flex+pos, smoothnessDelay)
                send_servo_command(s[5], 90-pos, smoothnessDelay)
                send_servo_command(s[4], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[3], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[2], 90-flex+pos, smoothnessDelay)
            elif step == 2:
                send_servo_command(s[1], 90-pos, smoothnessDelay)
                send_servo_command(s[9], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[8], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[7], 90-flex+pos, smoothnessDelay)
                send_servo_command(s[6], 90-pos, smoothnessDelay)
                send_servo_command(s[5], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[4], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[3], 90-flex+pos, smoothnessDelay)
            elif step == 3:
                send_servo_command(s[2], 90-pos, smoothnessDelay)
                send_servo_command(s[1], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[9], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[8], 90-flex+pos, smoothnessDelay)
                send_servo_command(s[7], 90-pos, smoothnessDelay)
                send_servo_command(s[6], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[5], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[4], 90-flex+pos, smoothnessDelay)
            elif step == 4:
                send_servo_command(s[3], 90-pos, smoothnessDelay)
                send_servo_command(s[2], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[1], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[9], 90-flex+pos, smoothnessDelay)
                send_servo_command(s[8], 90-pos, smoothnessDelay)
                send_servo_command(s[7], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[6], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[5], 90-flex+pos, smoothnessDelay)
            elif step == 5:
                send_servo_command(s[4], 90-pos, smoothnessDelay)
                send_servo_command(s[3], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[2], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[1], 90-flex+pos, smoothnessDelay)
                send_servo_command(s[9], 90-pos, smoothnessDelay)
                send_servo_command(s[8], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[7], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[6], 90-flex+pos, smoothnessDelay)
            elif step == 6:
                send_servo_command(s[5], 90-pos, smoothnessDelay)
                send_servo_command(s[4], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[3], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[2], 90-flex+pos, smoothnessDelay)
                send_servo_command(s[1], 90-pos, smoothnessDelay)
                send_servo_command(s[9], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[8], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[7], 90-flex+pos, smoothnessDelay)
            elif step == 7:
                send_servo_command(s[6], 90-pos, smoothnessDelay)
                send_servo_command(s[5], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[4], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[3], 90-flex+pos, smoothnessDelay)
                send_servo_command(s[2], 90-pos, smoothnessDelay)
                send_servo_command(s[1], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[9], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[8], 90-flex+pos, smoothnessDelay)
            elif step == 8:
                send_servo_command(s[7], 90-pos, smoothnessDelay)
                send_servo_command(s[6], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[5], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[4], 90-flex+pos, smoothnessDelay)
                send_servo_command(s[3], 90-pos, smoothnessDelay)
                send_servo_command(s[2], 90-flex-pos, smoothnessDelay)
                send_servo_command(s[1], 90-2*flex+pos, smoothnessDelay)
                send_servo_command(s[9], 90-flex+pos, smoothnessDelay)
            sleep(smoothnessDelay / 1000)

    rollState = 0  # Reset to re-form circle next time
    sleep(1)

def main():
    try:
        set_initial_pose()
        while True:
            roll_forward()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("Returning all servos to neutral...")
        for servo_id in servo_ids:
            send_servo_command(servo_id, 90, 1000)
        bus.close()
        print("Bus closed.")

if __name__ == "__main__":
    main()
