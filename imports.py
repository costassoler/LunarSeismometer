#modules 
import pyqtgraph
import serial
import RPi.GPIO as GPIO
import numpy as np
import os, time

#values 
CHUNK_SIZE = 1000    # 1 sec for processing serial data for now change later maybe
BAUD_RATE  = 115200  # baud rate for serial port


