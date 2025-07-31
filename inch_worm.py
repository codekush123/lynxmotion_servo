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

servo_ids = ['27', '05', '33', '35', '29', '39', '32', '25', '23']
front = servo_ids[0:3]    # Head
middle = servo_ids[3:6]   # Body
rear = servo_ids[6:9]     # Tail

neutral = 0               # 0.0 degrees
contract_angle = 400      # 40.0 degrees in tenths
arch_angle = 200          # 20.0 degrees arch
extend_angle = -400       # -40.0 degrees for opposite extension
move_duration = 800       # ms for smooth transition
step_delay = 0.9          # seconds between steps

def move_servo_deg(sid, angle, duration=move_duration):
    cmd = f"#{sid}D{angle}T{duration}\r"
    bus.write(cmd.encode('utf-8'))

def set_group(group, angle, duration=move_duration):
    for sid in group:
        move_servo_deg(sid, angle, duration)

try:
    print("Starting inchworm locomotion... Press Ctrl+C to stop.")
    while True:
        set_group(front, neutral)
        set_group(middle, arch_angle)
        set_group(rear, contract_angle)
        sleep(step_delay)

        set_group(front, extend_angle)
        set_group(middle, neutral)
        set_group(rear, neutral)
        sleep(step_delay)

        set_group(front, neutral)
        set_group(middle, neutral)
        set_group(rear, neutral)
        sleep(3)

except KeyboardInterrupt:
    print("\nInterrupted. Resetting all servos to neutral.")
    set_group(servo_ids, neutral)
    bus.close()
    print("Bus closed. Done.")
