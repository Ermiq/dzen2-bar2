#!/bin/python

from .widgetBase import Widget

class VolumeWidget(Widget):

	def __init__(self, width):
		Widget.__init__(self, width)
		self.HEADER = "VOL: "

	def Update(self):
		amixerData = self.GetFromShell("amixer sget Master")
		self.TEXT = self.GetFromShell(
			"echo '" + amixerData + "' | grep -m 1 -oP '(?<= \[).*?(?=%\] )'")
		STATUS = self.GetFromShell("echo '" + amixerData +
						  "' | grep -m 1 -oP '(?<=%\] \[).*?(?=\])'")
		'''
		if TEXT == 0:
			STATUS =   # level 0 (muted icon)
		elif STATUS == "off":
			STATUS =  # muted (muted icon)
		elif TEXT < 25:
			STATUS =  # 24 and less (low volume icon)
		elif TEXT < 50:
			STATUS =  # 49 and less (medium icon)
		elif TEXT < 75:
			STATUS =  # 74 and less (high volume icon)
		else: STATUS =  # full throttle (high volume icon)
		'''
		self.TEXT = self.AlignCenter(self.TEXT, self.WIDTH)



	def Dzen(self):
		return self.HEADER + self.TEXT

	def Width(self):
		return self.WIDTH

	def WidthPxl(self, font):
		w = self.GetFromShell("dzen2-textwidth " + font + " '" + self.HEADER + self.TEXT + "'")
		return int(w)

	#-------------------------------------------------------------
	# Volume change functions:

	def IncreaseVolume(self, step):
		self.GetFromShell("amixer -q sset Master " + step + "%+ unmute")
		self.Update()

	def DecreaseVolume(self, step):
		self.GetFromShell("amixer -q sset Master " + step + "%- unmute")
		self.Update()

	def MuteVolume(self):
		self.GetFromShell("amixer -q sset Master toggle")

	def SetVolume(self, newVolume):
		self.GetFromShell("amixer -q sset Master " + newVolume + "$1% unmute")
		self.Update()
