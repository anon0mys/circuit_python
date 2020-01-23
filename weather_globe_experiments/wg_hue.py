# Code for Circuit Playground Express
# This file needs to be renamed to code.py when
# added to the playground express

# This casts temperature in F to hue first to select a color
# then converts hue to RGB to set the LEDs on the board.
# Brightness of the lights is set by converting the value
# read by the light sensor

import time

import adafruit_thermistor
import board
import neopixel
import analogio
import simpleio

# Setting the min and max Farenheit values
# will adjust how sensative the conversion from temp to hue is.
# Values below min and above max will be cast to min or max.
f_max = 90
f_min = 60

light_sensor = analogio.AnalogIn(board.LIGHT)

# Thermistor(pin, resitor, resistance, nominal_temp, b_coefficient)
thermistor = adafruit_thermistor.Thermistor(
    board.TEMPERATURE, 10000, 10000, 25, 3950)

# NeoPixel(pin, number_of_lights, bytes_per_pixel=3,
#          brightness=1.0, auto_write=True, pixel_order=None)
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1,
                           auto_write=False, pixel_order='RGB')

while True:
    light = light_sensor.value
    temp_f = thermistor.temperature * 9 / 5 + 32
    # Ensure temperature is not outside of range
    temp_f = min(temp_f, f_max)
    temp_f = max(temp_f, f_min)

    # Map temperature to hue. Hue range is 0 to 360
    hue = simpleio.map_range(temp_f, f_min, f_max, 0, 360)
    rgb = (0, 0, 0)
    # Converting hue to rgb: https://en.wikipedia.org/wiki/HSL_and_HSV
    # This is assuming saturation and value are both 1
    h1 = (hue / 60)
    x = 1 - abs((h1 % 2) - 1)
    if h1 >= 0 and h1 < 1:
        rgb = (1, x, 0)
    elif h1 < 2:
        rgb = (x, 1, 0)
    elif h1 < 3:
        rgb = (0, 1, x)
    elif h1 < 4:
        rgb = (0, x, 1)
    elif h1 < 5:
        rgb = (x, 0, 1)
    elif h1 < 6:
        rgb = (1, 0, x)
    # Map light reading to brightness. Max light sensor reading is  62000
    # and brightness range is 0 to 1.
    brightness = light / 62000

    pixels.brightness = brigtness
    pixels.fill(rgb)
    pixels.show()
    time.sleep(0.25)
