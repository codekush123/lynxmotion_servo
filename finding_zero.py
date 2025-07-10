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

servoID='3' 


print('Moving to 0 degrees')
bus.write(f'#{servoID}D0\r'.encode()) 
sleep(3)

print("Finished with the servo. Closing serial port.")
bus.close()
del bus