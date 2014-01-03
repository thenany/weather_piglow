# -*- coding: utf8 -*-
# Allows to get weather basic information from OpenWeatherMap API

import json
import urllib
#from piglow import PiGlow
from time import sleep


# Configuration
url = "http://api.openweathermap.org/data/2.5/weather?q=Toulon"
brightness = 20
blink_duration = 1
period = 10


def getJDataFromURL(url):
	f = urllib.urlopen(url)
	return json.loads(f.read())

def kelvin2celsius(temperature):
	return float(temperature)-273.15

def getTemp(jdata):
	return kelvin2celsius(jdata["main"]["temp"])

def getMinTemp(jdata):
	return kelvin2celsius(jdata["main"]["temp_min"])

def getMaxTemp(jdata):
	return kelvin2celsius(jdata["main"]["temp_max"])

def getColor(temperature):
	temp = float(temperature)
	if temperature<0:
		return [2]
	if temperature<4:
		return [2,3]
	if temperature<8:
		return [3]
	if temperature<12:
		return [3,4]
	if temperature<16:
		return [4]
	if temperature<20:
		return [4,5]
	if temperature<24:
		return [5]
	if temperature<28:
		return [5,6]
	return [6]

def colors2leds(colors):
	color2leds = {
		2 : [5,11,17],
		3 : [4,10,16],
		4 : [3, 9,15],
		5 : [2, 8,14],
		6 : [1, 7,13],
	}
	leds = []
	for color in colors:
		leds.extend(color2leds[color])
	return leds

def simple_blinks(piglow, period, ratio, brightness, n, leds):
	piglow.all(0)
	for blink in range(n):
		for led in leds:
			piglow.led(led, brightness)
		sleep(period*ratio)
		for led in leds:
			piglow.led(led, 0)
		sleep(period*(1-ratio))
	piglow.all(0)

def soft_blink(piglow, duration, brightness, leds):
	piglow.all(0)
	for i in range(10):
		for led in leds:
			piglow.led(led, brightness*i/10)
		sleep(float(duration)/(2*10))
	for i in range(10):
		for led in leds:
			piglow.led(led, brightness*(10-i)/10)
		sleep(float(duration)/(2*10))
	piglow.all(0)

def dec2bin(dec):
	bin = [0,0,0,0,0]
	dec = int(dec)
	if dec >= 32:
		return [1,1,1,1,1]
	if dec >= 16:
		bin[0] = 1
		dec += -16
	if dec >= 8:
		bin[1] = 1
		dec += -8
	if dec >= 4:
		bin[2] = 1
		dec += -4
	if dec >= 2:
		bin[3] = 1
		dec += -2
	if dec >= 1:
		bin[4] = 1
	return bin

piglow = PiGlow()
while True:
 	jdata = getJDataFromURL(url)
 	temperature = getTemp(jdata)
 	print temperature
 	colors = getColor(temperature)
 	soft_blink(piglow,blink_duration,brightness,colors2leds(colors))
 	sleep(period)