from time import sleep
import serial

bus = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)                                                                                                                          # List of all servo IDs
servo_ids = ['27', '05', '33', '35', '29', '39', '32', '25', '24']
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

def cobra_movement(cycles=3, speed=100):
    print("Starting cobra movement...")
    cobra_ids = ['05', '33', '35']  

    wave_angles = [90, 80, 40, 80, 70, 70, 50, 10]  
    for _ in range(cycles):
        for offset in range(len(wave_angles)):
            for i, sid in enumerate(cobra_ids):
                angle_index = (offset + i) % len(wave_angles)
                angle = wave_angles[angle_index]
                send_servo_command(sid, angle, speed)
            sleep(speed / 1000.0)

        for offset in reversed(range(len(wave_angles))):
            for i, sid in enumerate(cobra_ids):
                angle_index = (offset + i) % len(wave_angles)
                angle = wave_angles[angle_index]
                send_servo_command(sid, angle, speed)
            sleep(speed / 1000.0)
def main():
    try:
        set_initial_pose()
        while True:
            cobra_movement()
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