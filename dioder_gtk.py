#!/usr/bin/env python
#
#+	Copyright (c) 2011 Rikard Lindstrom <ornotermes@gmail.com>
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

import pygtk
pygtk.require('2.0')
import gtk
from dioder_lib import *
import argparse
		
class LedControl:

	LED_RED = 'r'
	LED_GREEN = 'g'
	LED_BLUE = 'b'			
			
	def delete_event(self, widget, event, data=None):
		return False;
   
	def destroy(self, widget, data=None):
		gtk.main_quit()
  
	def colorUpdate(self, widget):
		gdk_color = self.colorpick.get_current_color()
		red = gdk_color.red >> 8
		green = gdk_color.green >> 8
		blue = gdk_color.blue >> 8
		hex_color = "A%(red)02X%(green)02X%(blue)02X" % {"red": red, "green": green, "blue": blue}
		print (hex_color)
		u.sendData(arg["transmit-endpoint"], hex_color)
    
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.destroy)
		self.window.set_border_width(10)
		
		self.colorpick = gtk.ColorSelection()
		self.colorpick.connect("color-changed", self.colorUpdate)
		self.colorpick.show()
	
		self.window.add(self.colorpick)
		self.window.show()
		
	def main(self):
		gtk.main()
  	
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

if __name__ == '__main__':
	arg = argParser()
	  	
	if arg["debug"]: print arg
	  	
	u = hidUSB();
	if arg["list"]: u.listDevices(int(arg["vendor-id"],16), int(arg["product-id"],16))
	else:
		u.connect(int(arg["vendor-id"],16), int(arg["product-id"],16), arg["instance"])
		lc = LedControl()
		lc.main()
