import RPi.GPIO as GPIO
from time import time, gmtime, sleep, strftime
import sys
from os import system
from pathlib import Path
import datetime
import os,random

GM1 = 24
GM2 = 25

pins = [4, 17, 27, 5, 6, 13, 26, 18, 23, 24, 25, 12, 16]

GPIO.setmode(GPIO.BCM)

GPIO.setup(22,GPIO.OUT)

def flashled ():
	GPIO.output(22,GPIO.HIGH)
	sleep(1)
	GPIO.output(22,GPIO.LOW)

def count(pin):
  print ("count: ", pin)
  flashled()
	# if found_match < 0.0009 and found_match >= 0:
	# 	print ("Detected ", found_match, strftime("%X", gmtime()), "GM1_time: ", GM1_TIMES[-1], "GM2_time: ", GM2_TIMES[-1])
	# 	flashled()

start_time = time()
for pin in pins:
  try:
    GPIO.setup(pin, GPIO.IN)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=count)
  except RuntimeError:
    print("could not setup pin: ", pin)

try:
  print("Let's Rock!")
  while True:
    sleep(1)
except KeyboardInterrupt:
	print("Quitting!")
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

print("Bye!")
GPIO.cleanup()           # clean up GPIO on normal exit  
