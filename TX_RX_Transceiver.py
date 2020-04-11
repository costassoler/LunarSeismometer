import serial
import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyS0",baudrate=115200,timeout=.01)
DataString=''
for i in range (0,100):
    port.write(str.encode('A'))
    rcv = port.read(50)
    DataString+=rcv.decode() #DataString is an object that contains all recorded data
    #print(rcv)
print(DataString)
