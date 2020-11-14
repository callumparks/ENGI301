"""
--------------------------------------------------------------------------
Guitar Tuner
--------------------------------------------------------------------------
License:   
Copyright 2020 Callum Parks

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use the HT16K33 Display and a button to create a digital people counter

Requirements:
  - Increment the note value in accordance to movement of the potentiometer

Uses:
  - HT16K33 display library developed in class
  - Adafruit libraries
  - time libraries

"""


import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM

import ht16k33 as HT16K33
import time 

#Initializing inputs
button   ="P2_2"
button2  ="P2_4"
servo    = "P2_1"
analog   = "P1_19"
buzzer   = "P2_3"

#Setup buttons
GPIO.setup(button, GPIO.IN)
GPIO.setup(button2, GPIO.IN)

#Setup pentiometer
ADC.setup()

#Setup display
i2c_bus=1
i2c_address=0x70
display    = HT16K33.HT16K33(i2c_bus, i2c_address)
display.set_digit_raw(0, 0x00) 
display.set_digit_raw(1, 0x00)
display.set_digit_raw(2, 0x00)
display.set_digit_raw(3, 0x00)

#Dictionaries for frequency values and screen outputs 
frequency_dict = {0:1, 1:82, 2:110, 3:147, 4:196, 5:247, 6:330}
letters_dict = {0:0x00, 1:0x79, 2:0x77, 3:0x5e, 4:0x6f, 5:0x7c, 6:0x79}


# Initialize Servo; Servo should be "off"
SERVO_FREQ   = 50                  # 20ms period (50Hz)
SERVO_POL    = 0                    # Rising Edge polarity
SERVO_OFF    = 7.5                # 0ms pulse -- Servo is inactive cc fast
SERVO_CLOSE  = 5                   # 1ms pulse (5% duty cycle)  -- All the way right
SERVO_OPEN   = 10
PWM.start(servo, SERVO_OFF, SERVO_FREQ, SERVO_POL)
PWM.set_duty_cycle(servo, 0)

#Set up variable for continuos loop
i = None

#Functions for turning servo clockwise and counter clockwise
def turning():
    PWM.set_duty_cycle(servo, 15)
    
def other_turning():
    PWM.set_duty_cycle(servo, 5)

#Run Function 
while i is None:
    '''1 = E, 82 hz
    2 = A, 110 hz
    3 = D, 147 hz
    4 = G, 196 hz
    5 = B, 247 hz
    6 = e, 330 hz'''
    
    while(GPIO.input(button) == 0):
        #for clockwise
        turning()
    
    while(GPIO.input(button2) == 0):
        #for counterclockwise
        other_turning()
   
    else:
        #Keep servo still
        PWM.set_duty_cycle(servo, 0)
        
        #Read potentiometer
        value = ADC.read_raw(analog)
        
        #find key vlaue 0-6 to correspond to dicionaries 
        key = int(value//587)
        
        #Get frequency
        freq = frequency_dict[key]
      
        #Play frequency
        PWM.start("P2_3", 4, freq)
        time.sleep(.3)
        
        #Set screen
        display.set_digit_raw(0, letters_dict[key]) 
        
      
