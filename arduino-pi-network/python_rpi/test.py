import serial
ser = serial.Serial('/dev/ttyUSB0')
ser2 = serial.Serial('/dev/ttyUSB1')

while 1:
	print("arduino1:%s", ser.readline())
	print("arduino2:%s ", ser2.readline())

