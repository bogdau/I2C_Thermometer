########################################################################
# Filename    : I2C_Thermometer.py
# Description : Use the LCD display data and themperature
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

import RPi.GPIO as GPIO
import math

from ADCDevice import *
from time import sleep, strftime
from datetime import datetime

adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
  
def get_time_now():     # get system time
    return datetime.now().strftime('  %H:%M:%S')
    
def give_temp():
    value = adc.analogRead(0)        # read ADC value A0 pin
    voltage = value / 255.0 * 3.3        # calculate voltage
    Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
    tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)
    tempC = tempK -273.15        # calculate temperature (Celsius)
    return tempC

def loop():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):
        lcd.clear()
        lcd.setCursor(0,0)  # set cursor position
        lcd.message('Themp: %.2f'%(give_temp())+ '\n')
        lcd.message('Time:'+str( get_time_now()) )   # display the time
        sleep(1)
        
def destroy():
    adc.close()
    GPIO.cleanup()
    lcd.clear()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()



