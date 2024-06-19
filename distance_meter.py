import machine
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
import utime

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)


# Define GPIO pins
trig_pin = machine.Pin(27, machine.Pin.OUT)  # Trig pin
echo_pin = machine.Pin(26, machine.Pin.IN)   # Echo pin

def get_distance():
    # Trigger pulse
    trig_pin.value(1)
    utime.sleep_us(10)
    trig_pin.value(0)

    # Wait for the echo pulse
    while echo_pin.value() == 0:
        pulse_start = utime.ticks_us()

    while echo_pin.value() == 1:
        pulse_end = utime.ticks_us()

    # Calculate distance in centimeters
    pulse_duration = utime.ticks_diff(pulse_end, pulse_start)
    distance_cm = pulse_duration / 58.0

    return distance_cm

try:
    while True:
        # Get distance
        distance = get_distance()

        # Print distance on LCD
        lcd.clear()
        lcd.putstr("Distance:")
        lcd.move_to(0, 1)
        lcd.putstr("{:.2f} cm".format(distance))

        sleep(0.5)

except KeyboardInterrupt:
    pass