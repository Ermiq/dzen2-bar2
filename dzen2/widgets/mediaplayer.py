#!/bin/python

from widgets.WidgetBase.WidgetBase import WidgetBase
from helpers import shellHelper
from config import config

class MediaPlayerWidget(WidgetBase):
	"""Requires playerctl binary to be in your path (except cmus)
	See: https://github.com/acrisci/playerctl"""

	PLAYER_NAME = ""

	def __init__(self, width, action = ""):
		WidgetBase.__init__(self, width, action)
	
	def Update(self):
		# If the player name has not been specified as an argument,
		# check out media players that are currently open and running,
		# and try to find any that matches the given list of audio players.
		self.PLAYER_NAME == ""
		# Get all currently running players
		runningPlayers = shellHelper.ExecOneLine("playerctl -l")
		# Magic...
		runningPlayers = runningPlayers.split()
		for line in runningPlayers:
			for p in config.PLAYERS:
				if p in line:
					self.PLAYER_NAME = line
		
		if self.PLAYER_NAME != "":
			#For 'playerctl' the player argument must be as '--player=audacious'
			self.PLAYER_NAME = "--player=" + self.PLAYER_NAME

			# Mouse button clicks on current track text
			'''case $BLOCK_BUTTON in
				1) playerctl $player_arg previous;;		# left mouse button
				2) playerctl $player_arg play-pause;;	# middle button click
				3) playerctl $player_arg next;;			# right button click
			esac'''

			artist = shellHelper.ExecSplit(["playerctl", self.PLAYER_NAME, "metadata", "artist"])
			title = shellHelper.ExecSplit(["playerctl", self.PLAYER_NAME, "metadata", "title"])

			if config.SONG_FIRST:
				self.TEXT = title + " - " + artist
			else:
				self.TEXT = artist + " - " + title

	def Dzen(self):
		self.TextFormat()
		self.DZEN2LINE = self.TEXT
		self.AddAction()
		return self.DZEN2LINE
	
	def WidthPxl(self, font):
		w = WidgetBase.WidthPxl(self, font)
		return w
