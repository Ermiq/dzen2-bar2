#!/bin/python

from widgets.WidgetBase.WidgetBase import WidgetBase
from helpers import shellHelper
from config import config

class DateWidget(WidgetBase):

	def __init__(self, width, action = ""):
		WidgetBase.__init__(self, width, action)
	
	def Update(self):
		self.TEXT = shellHelper.ExecOneLine("date +'" + config.DATE_FORMAT + "'")

	def Dzen(self):
		WidgetBase.Dzen(self)
		self.TextFormat()
		self.DZEN2LINE = self.TEXT
		self.AddAction()
		return self.DZEN2LINE

	def WidthPxl(self, font):
		#s = "Su, 12 apr. 15:34:25"
		#w = shellHelper.ExecSplit(["dzen2-textwidth", font, s])
		w = WidgetBase.WidthPxl(self, font)
		return int(w)
