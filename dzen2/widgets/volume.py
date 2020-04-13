#!/bin/python

from widgets.WidgetBase.WidgetBase import WidgetBase
from helpers import shellHelper
from config import config

class VolumeWidget(WidgetBase):

	def __init__(self, width, action = ""):
		WidgetBase.__init__(self, width, action)
		self.HEADER = config.VOLUME_HEADER

	def Update(self):
		amixerData = shellHelper.ExecOneLine("amixer sget Master")
		self.TEXT = shellHelper.ExecOneLine(
			"echo '" + amixerData + "' | grep -m 1 -oP '(?<= \[).*?(?=%\] )'")
		STATUS = shellHelper.ExecOneLine("echo '" + amixerData +
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

	def Dzen(self):
		self.TextFormat()
		self.DZEN2LINE = self.HEADER + self.TEXT
		self.AddAction()
		return self.DZEN2LINE

	def WidthPxl(self, font):
		w = WidgetBase.WidthPxl(self, font)
		return w

	#-------------------------------------------------------------
	# Volume change functions:

	def IncreaseVolume(self, step):
		shellHelper.ExecOneLine("amixer -q sset Master " + step + "%+ unmute")
		self.Update()

	def DecreaseVolume(self, step):
		shellHelper.ExecOneLine("amixer -q sset Master " + step + "%- unmute")
		self.Update()

	def MuteVolume(self):
		shellHelper.ExecOneLine("amixer -q sset Master toggle")

	def SetVolume(self, newVolume):
		shellHelper.ExecOneLine("amixer -q sset Master " + newVolume + "% unmute")
		self.Update()
