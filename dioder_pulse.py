#!/usr/bin/env python
#
#+	Copyright (c) 2011 Rikard Lindstrom <ornotermes@gmail.com>
#
#	This software is a modified version of Impulse by Ian Halpern ( http://impulse.ian-halpern.com/ ).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from dioder_lib import *
import argparse
import sys, gobject, os, time, math

class DioderImpulse () :

	def __init__ ( self, args, **keyword_args ):
	
		self.arg = args
	
		self.samp_r_old = [0] * self.arg["average-red"]
		self.samp_g_old = [0] * self.arg["average-green"]
		self.samp_b_old = [0] * self.arg["average-blue"]

		import impulse

		sys.modules[ __name__ ].impulse = impulse
		self.setAudioSource( self.arg["audio-source"] )

	def update (self):
	
		samp_r = 0
		samp_g = 0
		samp_b = 0

		audio_sample_array = impulse.getSnapshot( True )
		
		sections = audio_sample_array.__len__() / self.arg["sample-sections"]
		
		start_r = self.arg["sample-section-bottom-red"]
		start_g = self.arg["sample-section-bottom-green"]
		start_b = self.arg["sample-section-bottom-blue"]
		len_r = self.arg["sample-section-top-red"] - start_r
		len_g = self.arg["sample-section-top-green"] - start_g
		len_b = self.arg["sample-section-top-blue"] - start_b
		
#		samp_x = sum of sample section / size of sample section
		try:
			samp_r = math.fsum(audio_sample_array[sections*start_r : sections*(start_r+len_r)]) / sections * len_r
			samp_g = math.fsum(audio_sample_array[sections*start_g : sections*(start_g+len_g)]) / sections * len_g
			samp_b = math.fsum(audio_sample_array[sections*start_b : sections*(start_b+len_b)]) / sections * len_b
		except:
			pass
		
		self.samp_r_old.pop(0) #remove oldest sample
		self.samp_g_old.pop(0)
		self.samp_b_old.pop(0)
		
		self.samp_r_old.append(samp_r) #append new sample
		self.samp_g_old.append(samp_g)
		self.samp_b_old.append(samp_b)
		
#		samp_x = sum of sample value buffer / lenght of sample value buffer
		samp_r_avg = sum(self.samp_r_old) / self.samp_r_old.__len__()
		samp_g_avg = sum(self.samp_g_old) / self.samp_g_old.__len__()
		samp_b_avg = sum(self.samp_b_old) / self.samp_b_old.__len__()
		
#		if sample < sample avrage then sample = sample avrage, else sample buffer is all set to sample
#		This creates a nice effect of light comming at same time as sound and then fading out
		if (samp_r < samp_r_avg): samp_r = samp_r_avg
		else: self.samp_r_old = [samp_r]*self.samp_r_old.__len__()
		if (samp_g < samp_g_avg): samp_g = samp_g_avg
		else: self.samp_g_old = [samp_g]*self.samp_g_old.__len__()
		if (samp_b < samp_b_avg): samp_b = samp_b_avg
		else: self.samp_b_old = [samp_b]*self.samp_b_old.__len__()
		
		samp_r *= self.arg["gain"] * self.arg["gain-red"]
		samp_g *= self.arg["gain"] * self.arg["gain-green"]
		samp_b *= self.arg["gain"] * self.arg["gain-blue"]
			
		if (samp_r > self.arg["output-top-red"]): samp_r = self.arg["output-top-red"]
		if (samp_g > self.arg["output-top-green"]): samp_g = self.arg["output-top-green"]
		if (samp_b > self.arg["output-top-blue"]): samp_b = self.arg["output-top-blue"]
		
		if (samp_r < self.arg["output-bottom-red"]): samp_r = self.arg["output-bottom-red"]
		if (samp_g < self.arg["output-bottom-green"]): samp_g = self.arg["output-bottom-green"]
		if (samp_b < self.arg["output-bottom-blue"]): samp_b = self.arg["output-bottom-blue"]
		
		if (self.arg["invert-red"]): samp_r = 255 - samp_r
		if (self.arg["invert-green"]): samp_g = 255 - samp_g
		if (self.arg["invert-blue"]): samp_b = 255 - samp_b
		
		if (self.arg["hsv"]):
			import colorsys
			if arg["debug"]: print ("hsv: " + str(samp_r) + " " + str(samp_g) + " " + str(samp_b) + " = " + str(float(samp_r) / 255) +" "+ str(float(samp_g) / 255) +" "+ str(float(samp_b) / 255))
			samp = colorsys.hsv_to_rgb( float(samp_r) / 255, float(samp_g) / 255, float(samp_b) / 255 )
			samp_r = 255 * samp[0]
			samp_g = 255 * samp[1]
			samp_b = 255 * samp[2]
			if arg["debug"]: print ("rgb: " + str(samp_r) + " " + str(samp_g) + " " + str(samp_b))
		
		output_r = str(hex(int(samp_r)).replace("0x","").rjust(2,'0'))
		output_g = str(hex(int(samp_g)).replace("0x","").rjust(2,'0'))
		output_b = str(hex(int(samp_b)).replace("0x","").rjust(2,'0'))
		
		u.sendData(arg["transmit-endpoint"], "A" + output_r + output_g + output_b)
		if arg["debug"]: print("output: A" + output_r + output_g + output_b)
		
		
		
		return True # keep running this event

	def setAudioSource( self, source, *args, **kwargs ):
		impulse.setSourceIndex( source )
		
def argParser():

	p = argparse.ArgumentParser()
	
	p.add_argument( "-vid", "--vendor-id", dest="vendor-id", default="0x03eb", metavar="0xABCD", help="Vendor Id for device to connect to as 16bit hex.")
	p.add_argument( "-pid", "--product-id", dest="product-id", default="0x204f", metavar="0xABCD", help="Product Id for device to connect to as 16bit hex.")
	p.add_argument( "-i", "--instance", dest="instance", default="0", metavar="N", type=int, help="Instance of device with correct VID/PID to use.")
	p.add_argument( "-tx", "--transmit-endpoint", dest="transmit-endpoint", default="2", type=int, metavar="N", help="Endpoint for transmitting data to device.")
	p.add_argument( "-rx", "--receive-endpoint", dest="receive-endpoint", default="129", type=int,  metavar="N", help="Endpoint to receive data from device.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	p.add_argument( "-l", "--list", dest="list", action="store_const", default=False, const=True, help="Show available devices.")
	
	p.add_argument( "-as", "--audio-source", dest="audio-source", type=int, default=0, metavar="N", help="Audio source index.")
	
	p.add_argument( "-g", "--gain", dest="gain", type=float, default=100, metavar="float", help="Gain for all channels.")
	p.add_argument( "-gr", "--gain-red", dest="gain-red", type=float, default=1, metavar="float", help="Extra gain for red.")
	p.add_argument( "-gg", "--gain-green", dest="gain-green", type=float, default=1, metavar="float", help="Extra gain for green.")
	p.add_argument( "-gb", "--gain-blue", dest="gain-blue", type=float, default=1, metavar="float", help="Extra gain for blue.")
	
	p.add_argument( "-ar", "--average-red", dest="average-red", type=int, default=48, metavar="N", help="Number of samples for red average.")
	p.add_argument( "-ag", "--average-green", dest="average-green", type=int, default=48, metavar="N", help="Number of samples for green average.")
	p.add_argument( "-ab", "--average-blue", dest="average-blue", type=int, default=48, metavar="N", help="Number of samples for blue average.")
	
	p.add_argument( "-ss", "--sample-sections", dest="sample-sections", type=int, default=3, metavar="N", help="Split sample in N sections.")
	p.add_argument( "-ssbr", "--sample-section-bottom-red", dest="sample-section-bottom-red", type=int, default=0, metavar="N", help="Bottom section for red.")
	p.add_argument( "-sstr", "--sample-section-top-red", dest="sample-section-top-red", type=int, default=1, metavar="N", help="Top section for red.")
	p.add_argument( "-ssbg", "--sample-section-bottom-green", dest="sample-section-bottom-green", type=int, default=1, metavar="N", help="Bottom section for green.")
	p.add_argument( "-sstg", "--sample-section-top-green", dest="sample-section-top-green", type=int, default=2, metavar="N", help="Top section for green.")
	p.add_argument( "-ssbb", "--sample-section-bottom-blue", dest="sample-section-bottom-blue", type=int, default=2, metavar="N", help="Bottom section for blue.")
	p.add_argument( "-sstb", "--sample-section-top-blue", dest="sample-section-top-blue", type=int, default=3, metavar="N", help="Top section for blue.")
	p.add_argument( "-otr", "--output-top-red", dest="output-top-red", type=int, default=255, metavar="N", help="Output top value for red.")
	p.add_argument( "-obr", "--output-bottom-red", dest="output-bottom-red", type=int, default=0, metavar="N", help="Output bottom value for red.")
	p.add_argument( "-otg", "--output-top-green", dest="output-top-green", type=int, default=255, metavar="N", help="Output top value for green.")
	p.add_argument( "-obg", "--output-bottom-green", dest="output-bottom-green", type=int, default=0, metavar="N", help="Output bottom value for green.")
	p.add_argument( "-otb", "--output-top-blue", dest="output-top-blue", type=int, default=255, metavar="N", help="Output top value for blue.")
	p.add_argument( "-obb", "--output-bottom-blue", dest="output-bottom-blue", type=int, default=0, metavar="N", help="Output bottom value for blue.")
	
	p.add_argument( "-ofr", "--output-floor-red", dest="output-floor-red", type=int, default=0, metavar="N", help="Add floor to red channel.")
	p.add_argument( "-ofg", "--output-floor-green", dest="output-floor-green", type=int, default=0, metavar="N", help="Add floor to green channel.")
	p.add_argument( "-ofb", "--output-floor-blue", dest="output-floor-blue", type=int, default=0, metavar="N", help="Add floor to blue channel.")
	
	p.add_argument( "-ir", "--invert-red", dest="invert-red", action="store_const", default=False, const=True, help="Invert red, full brightness when silent")
	p.add_argument( "-ig", "--invert-green", dest="invert-green", action="store_const", default=False, const=True, help="Invert green, full brightness when silent")
	p.add_argument( "-ib", "--invert-blue", dest="invert-blue", action="store_const", default=False, const=True, help="Invert blue, full brightness when silent")
	
	p.add_argument( "-s", "--hsv", dest="hsv", action="store_const", default=False, const=True, help="Remap colors (red = hue, green = saturation, blue = value).")
	
	arg = vars(p.parse_args())
	
	#sanity check
	if (0 > arg["sample-section-top-red"] > arg["sample-sections"]): arg["sample-section-top-red"] = arg["sample-sections"]
	if (0 > arg["sample-section-top-green"] > arg["sample-sections"]): arg["sample-section-top-green"] = arg["sample-sections"]
	if (0 > arg["sample-section-top-blue"] > arg["sample-sections"]): arg["sample-section-top-blue"] = arg["sample-sections"]
	
	if (0 > arg["sample-section-bottom-red"] > arg["sample-section-top-red"]): arg["sample-section-bottom-red"] = 0
	if (0 > arg["sample-section-bottom-green"] > arg["sample-section-top-green"]): arg["sample-section-bottom-green"] = 0
	if (0 > arg["sample-section-bottom-blue"] > arg["sample-section-top-blue"]): arg["sample-section-bottom-blue"] = 0
	
	if (0 > arg["output-top-red"] > 255): arg["output-top-red"] = 255
	if (0 > arg["output-top-green"] > 255): arg["output-top-green"] = 255
	if (0 > arg["output-top-blue"] > 255): arg["output-top-blue"] = 255
		
	if (0 > arg["output-bottom-red"] > 255): arg["output-bottom-red"] = 0
	if (0 > arg["output-bottom-green"] > 255): arg["output-bottom-green"] = 0
	if (0 > arg["output-bottom-blue"] > 255): arg["output-bottom-blue"] = 0
	
	return arg
			
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":

	try:
		import ctypes
		libc = ctypes.CDLL('libc.so.6')
		libc.prctl(15, os.path.split( sys.argv[ 0 ] )[ 1 ], 0, 0, 0)
	except Exception:
		pass
		
	arg = argParser()
	
	if arg["debug"]: print arg
	
	u = hidUSB()
	if arg["list"]: u.listDevices(int(arg["vendor-id"],16), int(arg["product-id"],16))
	else:
		u.connect(int(arg["vendor-id"],16), int(arg["product-id"],16), arg["instance"])
		d = DioderImpulse(arg)
	
		while True:
			time.sleep(0.01)
			d.update()
