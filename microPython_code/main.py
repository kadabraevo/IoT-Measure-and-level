from machine import Pin, ADC, I2C
from pico_i2c_lcd import I2cLcd
from lcd_api import LcdApi
from time import sleep
from imu import MPU6050
import math

# Initialize pins 
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) # I2C bus 1, SDA pin 0, SCL pin 1, 400kHz
i2c1 = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)  # I2C bus 2, SDA pin 14, SCL pin 15, 400kHz
lcd = I2cLcd(i2c, 0x27, 2, 16)

mpu = MPU6050(i2c1)
pot = ADC(Pin(26))
led_green = Pin(3, Pin.OUT)
led_yellow = Pin(4, Pin.OUT)
led_red = Pin(5, Pin.OUT)


sampleAmount = 3 # samples for measure average
degConvert = 0.000657 #range 43 cm, 43/65535 = 0.000657

# Function to turn off all LEDs
def allLedOff():
    led_green.off()
    led_red.off()
    led_yellow.off()
    return None

while True:
    potValue = pot.read_u16() # read value, 0-65535 across voltage range 0.0v - 3.3v
    print(potValue)
    
    avgData = 0 # resets avgData

    # Gathers saples for avegering data
    for data in range(sampleAmount):
        avgData += potValue

    avgData /= sampleAmount
    degValue = (avgData * degConvert) # Converts read value to degrees (range 43 cm, 43/65535 = 0.000657)
    print(int(degValue))
    
    # Collects data from mpu
    xAccel=mpu.accel.x
    yAccel=mpu.accel.y
    zAccel=mpu.accel.z
    
    # Calculate pitch
    pitch=math.atan(yAccel/zAccel)
    pitchDeg=pitch/(2*math.pi)*360
    print('pitch: ',pitchDeg)
    
    # Converts pitch to integer and absolute value
    displayDeg = abs(int(pitchDeg))
    
    # Controls leds for angle
    if 15 >= displayDeg >= -15:
        led_red.on()
    if 5 >= displayDeg >= -5:
        led_yellow.on()
    if 1 >= displayDeg >= -1:
        led_green.on()
    
    # LCD output
    lcdValue = int(degValue)
    lcd.clear()
    lcd.putstr(f"Measure: {lcdValue} cm")
    lcd.move_to(0, 1)
    lcd.putstr(f"Degrees: {displayDeg}")
    sleep(0.5)
    allLedOff()

