#modules 
#import pyqtgraph
import serial
import RPi.GPIO as GPIO
import numpy as np
import os, time
import matplotlib.pyplot as plt
import wave
import datetime
import sys

#values 
CHUNK_SIZE = 100     # 1 sec for processing serial data for now change later maybe
BAUD_RATE  = 115200  # baud rate for serial port
