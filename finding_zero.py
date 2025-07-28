from time import sleep
import serial

bus = serial.Serial(
    port = '/dev/ttyS0', 
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits =serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

servo_id='3' 


print('Moving to 0 degrees')
bus.write(f'#{servo_id}D0\r'.encode()) 
sleep(3)

bus.close()
del bus