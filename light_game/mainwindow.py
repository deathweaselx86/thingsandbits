#!/usr/bin/python
#
#

import pygtk
pygtk.require('2.0')
import gtk
import random
import frac 
	
class LightGUI:
	#callback functions start HERE	
	def resetEv(self,widget,data):
		print "Reset pressed"
		b = 0
		offset = 0
		self.buttonsPushed = []
		self.canModifySwitchboard = True
		self.lightConfiguration = []
		while b < self.n:
			self.buttonList[b].set_flags(gtk.SENSITIVE)
			if(b == self.k*offset + offset):
				self.buttonList[b].set_active(True)
				offset = offset + 1
			else:
				self.buttonList[b].set_active(False)
			b = b + 1
		b = 0
		while b < self.k:
			self.lightImages[b].set_from_file("onbulb.xpm")
			b = b + 1
            
	def safeLightEv(self,widget,data):
		if(self.canModifySwitchboard == False):
			print "redo-ing button press %s " % data
			self.lightImages[data].set_from_file("offbulb.xpm")
			b=0
			while b < self.k:
				if(self.buttonList[data*self.k+b].get_active() == True):
					if(b != data):
						print "turn %s on!" % b
						self.lightImages[b].set_from_file("onbulb.xpm")
				b = b+1
		else:
			print "Not in play mode"

	def lightEv(self,widget,data):
		if(self.canModifySwitchboard == False):
			print "Light switch %s was pressed" % data
			self.buttonsPushed.append(data)
			self.lightImages[data].set_from_file("offbulb.xpm")
			b = 0
			while b < self.k:
				if(self.buttonList[data*self.k+b].get_active() == True):
					if(b != data):
						print "turn %s on!" % b 
						self.lightImages[b].set_from_file("onbulb.xpm")
				b = b + 1
		else:
			print "Not in play mode"
			
	def playModeEv(self,widget,data):
		print "Play Mode pressed"
		self.canModifySwitchboard = False
		self.lightConfiguration = []
		b = 0
		while b < self.k:
			m = 0
			self.lightConfiguration.append([])
			while m < 2:
				self.lightConfiguration[b].append([])
				m = m+1
			b = b+1
		b = 0
		while b < self.n:
			if(self.buttonList[b].get_active() == True):
				self.lightConfiguration[b/self.k][0].append(frac.Frac(1))
			else:
				self.lightConfiguration[b/self.k][0].append(frac.Frac(0))
			self.buttonList[b].unset_flags(gtk.SENSITIVE)
			b = b + 1
		b = 0
		while b < self.k:
			self.lightConfiguration[b][1].append(frac.Frac(0))
			b = b + 1	
		
		if(self.doesWork() == True):
			print "It works"
		else:
			print "It does not work"
			a = gtk.Window(gtk.WINDOW_TOPLEVEL);
			a.set_title("Invalid Configuration")
			a.set_border_width(10)
			
			box = gtk.HBox(False,0)
			box.set_border_width(2)
			image = gtk.Image()
			image.set_from_file("no.png")
			label = gtk.Label("Reset Bad Configuration")
			box.pack_start(image,False,False,3)
			box.pack_start(label,False,False,3)
			image.show()
			label.show()
			
			b = gtk.Button()
			b.connect("clicked",self.resetEv,None)
			b.connect_object("clicked",gtk.Widget.destroy,a)
			
			b.add(box)
			box.show()
			a.add(b)
			b.show()
			a.show()

	def doesWork(self):
		b = 0
		frac.rref(self.lightConfiguration)
		while b < self.k:
			if(self.lightConfiguration[b][0][b] != frac.Frac(1)):
				return False
			b = b+1
			
		return True

	def undoEv(self,widget,data):
		if(len(self.buttonsPushed) > 0):
		
			d = self.buttonsPushed.pop()
			print "Undo pressed! must undo the effects of button %s" % d
			b = 0
			while b < self.k:
				self.lightImages[b].set_from_file("onbulb.xpm")
				b = b+1
			b=0
			while b < len(self.buttonsPushed):
				self.safeLightEv(self.lightSwitchList[self.buttonsPushed[b]],self.buttonsPushed[b])
				b = b+1

	def delete_event(self,widget,event,data=None):
		return False
		
	def destroy(self, widget, data=None):
		gtk.main_quit()
		
	def __init__(self):
		#this list contains all of the checkboxes
		self.buttonList = []
		#this list contains the buttons that correspond to the switches
		self.lightSwitchList = []
		#This contains the order that the buttons were pushed
		self.buttonsPushed = []
		#This contains pointers to the images that show the user
		#whether a given light is off or on
		self.lightImages = []
		#keeps track of the configuration of the switchoard
		self.lightConfiguration = []
		
		self.k = 5 # make this selectable soon 
		self.n = self.k*self.k
		self.canModifySwitchboard = True
		
		#This initializes the main window, adds the title
		#and some basic events
		self.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.mainWindow.set_title("Switchboard")
		
		self.mainWindow.connect("delete_event",self.delete_event)
		self.mainWindow.connect("destroy",self.destroy)
		self.mainWindow.set_border_width(10)
	
		#vertical pane for checkboxes and buttons
		self.vpane = gtk.VPaned()
		self.mainWindow.add(self.vpane)
		
		#Widget box for buttons et cetera
		self.widgetbox = gtk.HBox(False, 0)
		#self.mainWindow.add(self.widgetbox)
		self.vpane.add2(self.widgetbox)
		
		#widgetbox for check boxes
		self.checkboxtable = gtk.Table(self.k+1,self.k+1,True)
		#self.widgetbox.pack_start(self.checkboxtable,True,True,0)
		self.vpane.add1(self.checkboxtable)

		#reset button
		self.reset = gtk.Button("Reset")
		self.reset.connect("clicked",self.resetEv,"reset")
		self.widgetbox.pack_start(self.reset,True,True,0)
		self.reset.show()
	
		#play button
		self.play = gtk.Button("Play Mode")
		self.play.connect("clicked",self.playModeEv,"play")
		self.widgetbox.pack_start(self.play,True,True,0)
		self.play.show()

		#undo button
		self.undo = gtk.Button("Undo")
		self.undo.connect("clicked",self.undoEv,"undo")
		self.widgetbox.pack_start(self.undo,True,True,0)
		self.undo.show()

		#quit button
		self.quit = gtk.Button("Quit",)
		self.quit.connect("clicked",self.destroy,None)
		self.widgetbox.pack_start(self.quit,True,True,0)
		self.quit.show()

		#check buttons?
		b = 0
		offset = 0
		while b < self.n:
			a = gtk.CheckButton()
			self.buttonList.insert(b,a)
			self.checkboxtable.attach(self.buttonList[b],b%self.k+1,b%self.k+2,b/self.k+1,b/self.k+2)
			if(b == self.k*offset + offset):
				self.buttonList[b].set_active(True)
				offset = offset+1
			self.buttonList[b].show()
			b = b + 1
		
		#labels for the check buttons
		b = 0
		while b < self.k:
			a = gtk.Button("Light " + str(b))
			self.lightSwitchList.insert(b,a)
			self.checkboxtable.attach(self.lightSwitchList[b],0,1,b+1,b+2)
			self.lightSwitchList[b].connect("clicked",self.lightEv,b)
			self.lightSwitchList[b].show()
			b = b + 1
	
		#lights showing status
		b = 0
		while b < self.k:
			a = gtk.Image()
			a.set_from_file("onbulb.xpm")
			a.show()
			self.lightImages.insert(b,a)
			self.checkboxtable.attach(self.lightImages[b],b+1,b+2,0,1)
			self.lightImages[b].show()
			b = b + 1
		#show the final window
		self.vpane.show()
		self.widgetbox.show()
		self.checkboxtable.show()
		self.mainWindow.show()

	def main(self):
		gtk.main()
	
if __name__ == "__main__":
	lightgui = LightGUI()
	lightgui.main()
