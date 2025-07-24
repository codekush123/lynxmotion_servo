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

servo_ids = ['38', '33', '39', '35', '05', '32']
base_position = 1500
amplitude = 600  
base_period = 2.0  
speed_factor = 1.5  
phase_diff = math.pi / 3  
start_pause = 5.0  
smoothness_delay = 0.015  
command_delay = 0.005  

last_positions = {servo_id: base_position for servo_id in servo_ids}

def send_servo_command(servo_id, position):
    position = max(500, min(2500, int(position)))
    if abs(position - last_positions[servo_id]) > 10:
        command = f"#{servo_id}P{position}\r"
        bus.write(command.encode())
        print(f"Sent: {command.strip()}")  
        last_positions[servo_id] = position
        sleep(command_delay)  
    else:
        print(f"Skipped: {servo_id} at {position} (too close to {last_positions[servo_id]})")

def test_servo_range():
    print("Testing range for all servos...")
    for servo_id in servo_ids:
        print(f"Testing {servo_id} at max position (2100)")
        send_servo_command(servo_id, 2100)  
        sleep(2.0)  
        print(f"Returning {servo_id} to neutral (1500)")
        send_servo_command(servo_id, base_position)
        sleep(2.0)
    print("Servo range test complete.")

def half_sine_movement():
    try:
        print("Pausing to position robot...")
        sleep(start_pause)
        test_servo_range()
        print(f"Starting half sine water-like movement with speed factor {speed_factor}...")
        t = 0
        period = base_period / speed_factor 
        while True:
            for i, servo_id in enumerate(servo_ids):
                phase = i * phase_diff
                position = base_position + amplitude * abs(math.sin(2 * math.pi * t / period + phase))
                print(f"Calculated position for {servo_id}: {position:.1f}")  
                send_servo_command(servo_id, position)
            t += 0.05  
            sleep(smoothness_delay)  
    except KeyboardInterrupt:
        for servo_id in servo_ids:
            send_servo_command(servo_id, base_position)
        print("Stopped and servos returned to neutral position.")
    finally:
        bus.close()

if __name__ == "__main__":
    half_sine_movement()