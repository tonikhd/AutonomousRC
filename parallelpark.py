#import modules
import os
import time
import sys
import signal
import RPi.GPIO as GPIO
import Adafruit_PCA9685
from t6_encoder import RotaryEncoder
sys.path.insert(0,'VL53L0X_rasp_python/python')


import VL53L0X

#RotaryEncoder(mm_per_tick=22.1600, pin=4, poll_delay=0.1166, debug=False)
#
# this entry is for 3 magnets on the Exceed Magnet drive shaft gear
rpm_sensor = RotaryEncoder(22.1600, 4, True)

#initialize modules
tof = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
tof.open()
tof.start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
pwm = Adafruit_PCA9685.PCA9685()

#define values
servo_min = 255
servo_max = 407
servo_center = 331
alpha = 255
beta = 407

throttle_center = 360
throttle_forward = 370
throttle_back = 350
distance_old = 0
#time_traveled = 0.00
#keep going if no parking space or space too small
pwm.set_pwm(1, 0, servo_center)
while True:
    pwm.set_pwm(2, 0, throttle_forward)
    distance1 = tof.get_distance()
    difference = distance1 - distance_old
    if(difference > 120):
        print("edge 1 detected")
        start = time.time()
    if(difference < -120):
        print("edge 2 detected")
        end = time.time()
        time_traveled = end - start
        print("time traveled ", time_traveled)
        if(time_traveled > 0.5):
            print("Parking spot found ")
            pwm.set_pwm(2, 0, throttle_center)
            time.sleep(0.05)
            pwm.set_pwm(2, 0, throttle_back)
            time.sleep(0.05)
            pwm.set_pwm(2, 0, throttle_center)
            time.sleep(0.05)
            #pwm.set_pwm(2, 0, throttle_back)
            #print("parking spot found")
            #time.sleep(1)
            break
        else:
            print("spot too small!")

    distance_old = distance1
print("Start parallel parking...")
#back up for 1 sec
#pwm.set_pwm(2, 0, throttle_back)
#time.sleep(0.05)
#pwm.set_pwm(2, 0, throttle_center)
#time.sleep(0.05)
pwm.set_pwm(2, 0, throttle_back)
time.sleep(0.9)

#turn right and back up for 1 sec
pwm.set_pwm(1, 0, alpha)
time.sleep(0.6)
#turn left and back up for 1 sec
pwm.set_pwm(1, 0, beta)
time.sleep(0.8)
#finish
pwm.set_pwm(2, 0, throttle_center)
pwm.set_pwm(1, 0, servo_center)
time.sleep(0.05)
pwm.set_pwm(2, 0, throttle_forward)
time.sleep(0.05)
pwm.set_pwm(2, 0, throttle_center)
time.sleep(0.05)
pwm.set_pwm(2, 0, throttle_forward)
time.sleep(0.1)
pwm.set_pwm(2, 0, throttle_center)
print("parking completed!")
