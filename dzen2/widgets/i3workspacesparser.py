#!/bin/python

import json
from widgets.WidgetBase.WidgetBase import WidgetBase
from helpers import shellHelper
from config import config

class i3WorkspacesWidget(WidgetBase):

	WORKSPACES = [""]
	
	def __init__(self, width, action = ""):
		WidgetBase.__init__(self, width, action)
		self.HEADER = config.WORKSPACE_HEADER

	def Update(self):
		self.TEXT = ""
		self.WORKSPACES.clear()

		x = json.loads(shellHelper.ExecOneLine("i3-msg -t get_workspaces"))
		
		'''
		json parser will return workspace names with no quotes.
		But to switch to an i3 workspace with shell command
		( i3-msg workspace "someName" ) we need the quotes.
		More over, the quoted name itself should be placed in another pair
		of quotes to pass through dzen2 to Linux shell properly.
		So, in the end, to switch to a workspace that has its name declaired as
		" 2 " in i3 config file, gotta execute the command:
		i3-msg workspace '" 2 "'
		Same method will work with workspace names declared in i3 config without
		quotes as well. Names like this:
		set $ws3 Firefox
		So, to pass the correct command to dzen2 line using a name variable from
		json we'll do a lot of quotes and pluses dark magic here.
		'''
		for workspace in x:
			self.TEXT += workspace["name"]
			if workspace["focused"]:
				# ^ib(1) - ignore bar background, so widget will get it's own bg color.
				self.WORKSPACES.append("^ca({})^ib(0)^fg({})^bg({}){}^ib(1)^ca()".format(
					"1, i3-msg workspace " + "'" + '"' + str(workspace["name"] + '"' + "'"),
					config.clrBLK,
					config.clrGRN,
					workspace["name"]
					))
			else:
				self.WORKSPACES.append("^ca({})^fg({})^bg({}){}^ca()".format(
					"1, i3-msg workspace " + "'" + '"' + str(workspace["name"] + '"' + "'"),
					config.clrGRY,
					config.clrBLK,
					workspace["name"]
					))

	def Dzen(self):
		self.TextFormat()
		self.WORKSPACES.insert(0, self.HEADER) # Put the HEADER as the first element
		return self.WORKSPACES
	
	def WidthPxl(self, font):
		w = WidgetBase.WidthPxl(self, font)
		return w
