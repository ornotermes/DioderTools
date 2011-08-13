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

import usb, atexit

class hidUSB:
		
	def connect(self, vid, pid, instance):
		self.device = self.getDevice(vid, pid, instance)
		if not self.device:
			raise Exception('No compatible device found!')
		else: self.handle = self.device.open()
		try:
			self.handle.detachKernelDriver(0)
		except:
			print "Not attached to kernel driver"
		self.handle.claimInterface(0)
		atexit.register(self.release)
    
	def getDevice(self, vid, pid, instance):
		for bus in usb.busses() :
			for device in bus.devices :
				if device.idVendor == vid and device.idProduct == pid:
					if instance:
						instance -= 1
					else:
						print "Device found"
						return device
		return None

	def sendData(self, ep, data):
		self.handle.interruptWrite(ep, data)
		
	def release(self):
		self.handle.releaseInterface()
		self.handle.reset()
		
	def listDevices(self, vid, pid):
		n = 0
		for bus in usb.busses() :
			for device in bus.devices :
				if device.idVendor == vid and device.idProduct == pid:
					h = device.open()
					print "instance: " + str(n) + ": Bus: " + str(bus.location) + " Dev: " + str(device.devnum) + " / " + h.getString(device.iManufacturer,32) + " " + h.getString(device.iProduct,32) + " " + h.getString(device.iSerialNumber,32)
					n+=1
