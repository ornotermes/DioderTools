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

import argparse
from dioder_lib import *

def argParser():

	p = argparse.ArgumentParser()
	
	p.add_argument( "-vid", "--vendor-id", dest="vendor-id", default="0x03eb", metavar="0xABCD", help="Vendor Id for device to connect to as 16bit hex.")
	p.add_argument( "-pid", "--product-id", dest="product-id", default="0x204f", metavar="0xABCD", help="Product Id for device to connect to as 16bit hex.")
	p.add_argument( "-i", "--instance", dest="instance", default="0", metavar="N", type=int, help="Instance of device with correct VID/PID to use.")
	p.add_argument( "-tx", "--transmit-endpoint", dest="transmit-endpoint", default="2", type=int, metavar="N", help="Endpoint for transmitting data to device.")
	p.add_argument( "-rx", "--receive-endpoint", dest="receive-endpoint", default="129", type=int,  metavar="N", help="Endpoint to receive data from device.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	p.add_argument( "-l", "--list", dest="list", action="store_const", default=False, const=True, help="Show available devices.")
	
	p.add_argument( "-c", "--command", dest="command", default="A000000", metavar="ABC", help="What to send to the device.")
	
	return vars(p.parse_args())

if __name__ == '__main__':

	arg = argParser()
	
	if arg["debug"]: print arg
	
	u = hidUSB()
	if arg["list"]: u.listDevices(int(arg["vendor-id"],16), int(arg["product-id"],16))
	else:
		u.connect(int(arg["vendor-id"],16), int(arg["product-id"],16), arg["instance"])
		u.sendData(arg["transmit-endpoint"], arg["command"])
  
