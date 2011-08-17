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
  
	def led_set(self, widget, led, value):
		s = led + str(hex(value).replace("0x","").rjust(2,'0'))
		u.sendData(arg["transmit-endpoint"], s)
		if arg["debug"]: print s
    
	def led_scale(self, adj, led):
		self.led_set(adj, led, int(adj.value))
    
	def led_set_all(self, widget, value):
		s = str(hex(value).replace("0x","").rjust(2,'0'))
		u.sendData(arg["transmit-endpoint"],"A" + s + s + s)
		if arg["debug"]: print "A" + s + s + s
    
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.destroy)
		self.window.set_border_width(10)
	
		self.button_red_off = gtk.Button("Red Off")
		self.button_red_on = gtk.Button("Red On")
		self.button_red_off.connect("clicked", self.led_set, self.LED_RED, 0)
		self.button_red_on.connect("clicked", self.led_set, self.LED_RED, 255)
		self.button_box_red = gtk.HBox(False,0)
		self.button_box_red.pack_start(self.button_red_on, True, True, 0)
		self.button_box_red.pack_start(self.button_red_off, True, True, 0)
		self.button_red_off.show()
		self.button_red_on.show()
		self.button_box_red.show()
	
		self.button_green_off = gtk.Button("Green Off")
		self.button_green_on = gtk.Button("Green On")
		self.button_green_off.connect("clicked", self.led_set, self.LED_GREEN, 0)
		self.button_green_on.connect("clicked", self.led_set, self.LED_GREEN, 255)
		self.button_box_green = gtk.HBox(False,0)
		self.button_box_green.pack_start(self.button_green_on, True, True, 0)
		self.button_box_green.pack_start(self.button_green_off, True, True, 0)
		self.button_green_off.show()
		self.button_green_on.show()
		self.button_box_green.show()
	
		self.button_blue_off = gtk.Button("Blue Off")
		self.button_blue_on = gtk.Button("Blue On")
		self.button_blue_off.connect("clicked", self.led_set, self.LED_BLUE, 0)
		self.button_blue_on.connect("clicked", self.led_set, self.LED_BLUE, 255)
		self.button_box_blue = gtk.HBox(False,0)
		self.button_box_blue.pack_start(self.button_blue_on, True, True, 0)
		self.button_box_blue.pack_start(self.button_blue_off, True, True, 0)
		self.button_blue_off.show()
		self.button_blue_on.show()
		self.button_box_blue.show()
	
		self.button_all_off = gtk.Button("All Off")
		self.button_all_on = gtk.Button("All On")
		self.button_all_off.connect("clicked", self.led_set_all, 0)
		self.button_all_on.connect("clicked", self.led_set_all, 255)
		self.button_box_all = gtk.HBox(False,0)
		self.button_box_all.pack_start(self.button_all_on, True, True, 0)
		self.button_box_all.pack_start(self.button_all_off, True, True, 0)
		self.button_all_off.show()
		self.button_all_on.show()
		self.button_box_all.show()
	
	
		self.button_box = gtk.VBox(False,0)
		self.button_box.pack_start(self.button_box_all)
		self.button_box.pack_start(self.button_box_red)
		self.button_box.pack_start(self.button_box_green)
		self.button_box.pack_start(self.button_box_blue)
		self.button_box.show()
	
		self.adjustment_red = gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=8, page_size=0)
		self.adjustment_red.emit("changed")
		self.adjustment_red.connect("value_changed", self.led_scale, self.LED_RED)
		self.slider_red = gtk.VScale(adjustment=self.adjustment_red)
		self.slider_red.show()
		self.slider_red.set_digits(0)
		self.slider_red.set_update_policy(gtk.UPDATE_CONTINUOUS)
	
		self.adjustment_green = gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=8, page_size=0)
		self.adjustment_green.emit("changed")
		self.adjustment_green.connect("value_changed", self.led_scale, self.LED_GREEN)
		self.slider_green = gtk.VScale(adjustment=self.adjustment_green)
		self.slider_green.show()
		self.slider_green.set_digits(0)
		self.slider_green.set_update_policy(gtk.UPDATE_CONTINUOUS)
	
		self.adjustment_blue = gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=8, page_size=0)
		self.adjustment_blue.emit("changed")
		self.adjustment_blue.connect("value_changed", self.led_scale, self.LED_BLUE)
		self.slider_blue = gtk.VScale(adjustment=self.adjustment_blue)
		self.slider_blue.show()
		self.slider_blue.set_digits(0)
		self.slider_blue.set_update_policy(gtk.UPDATE_CONTINUOUS)
	
		self.slider_box = gtk.HBox(False,0)
		self.slider_box.show()
		self.slider_box.pack_start(self.slider_red)
		self.slider_box.pack_start(self.slider_green)
		self.slider_box.pack_start(self.slider_blue)
	
		self.gui_box = gtk.HBox(False, 0)
		self.gui_box.show()
		self.gui_box.pack_start(self.button_box)
		self.gui_box.pack_start(self.slider_box)
	
		self.window.add(self.gui_box)
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
