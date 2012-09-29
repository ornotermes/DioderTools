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
import sys, gobject, os, time, math, colorsys

class DioderFade () :

	def __init__ ( self, args, **keyword_args ):
	
		self.arg = args
		self.hue = 0
		self.saturation = 1
		self.value = 1

	def update (self):
	
		self.hue += 0.0001
		if self.hue > 1:
			self.hue -= 1
		
		samp = colorsys.hsv_to_rgb( self.hue, self.saturation, self.value )
		samp_r = 255 * samp[0]
		samp_g = 255 * samp[1]
		samp_b = 255 * samp[2]
		
		output_r = str(hex(int(samp_r)).replace("0x","").rjust(2,'0'))
		output_g = str(hex(int(samp_g)).replace("0x","").rjust(2,'0'))
		output_b = str(hex(int(samp_b)).replace("0x","").rjust(2,'0'))
		
		u.sendData(arg["transmit-endpoint"], "A" + output_r + output_g + output_b)
		if arg["debug"]: print("output: A" + output_r + output_g + output_b)
				
		return True # keep running this event
		
def argParser():

	p = argparse.ArgumentParser()
	
	p.add_argument( "-vid", "--vendor-id", dest="vendor-id", default="0x03eb", metavar="0xABCD", help="Vendor Id for device to connect to as 16bit hex.")
	p.add_argument( "-pid", "--product-id", dest="product-id", default="0x204f", metavar="0xABCD", help="Product Id for device to connect to as 16bit hex.")
	p.add_argument( "-i", "--instance", dest="instance", default="0", metavar="N", type=int, help="Instance of device with correct VID/PID to use.")
	p.add_argument( "-tx", "--transmit-endpoint", dest="transmit-endpoint", default="2", type=int, metavar="N", help="Endpoint for transmitting data to device.")
	p.add_argument( "-rx", "--receive-endpoint", dest="receive-endpoint", default="129", type=int,  metavar="N", help="Endpoint to receive data from device.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	p.add_argument( "-l", "--list", dest="list", action="store_const", default=False, const=True, help="Show available devices.")
	
	return vars(p.parse_args())
			
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
		
	arg = argParser()
	
	if arg["debug"]: print arg
	
	u = hidUSB()
	if arg["list"]: u.listDevices(int(arg["vendor-id"],16), int(arg["product-id"],16))
	else:
		u.connect(int(arg["vendor-id"],16), int(arg["product-id"],16), arg["instance"])
		d = DioderFade(arg)
	
		while True:
			time.sleep(0.01)
			d.update()
