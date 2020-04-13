#!/bin/python

from widgets.WidgetBase.WidgetBase import WidgetBase
from helpers import shellHelper
from config import config

class MediaplayerWidget(WidgetBase):
	"""
	Requires playerctl binary to be in your path (except cmus).

	Usage:
		The player argument must be as '--player=audacious'
		Commands:
			playerctl -l	# Get list of currently running players
			playerctl player_argument previous
			playerctl player_argument play-pause
			playerctl player_argument next
			playerctl player_argument metadata artist
			playerctl player_argument metadata title

	See: https://github.com/acrisci/playerctl"""

	PLAYER_NAME = ""
	PREV_BTN = "<<<  "
	NEXT_BTN = "  >>>"

	def __init__(self, width, action = ""):
		WidgetBase.__init__(self, width, action)
		self.HEADER = self.PREV_BTN
		self.TAIL = self.NEXT_BTN
	
	def Update(self):
		self.PLAYER_NAME == ""
		title = ""
		artist = ""
		# If the player name has not been specified as an argument,
		# check out media players that are currently open and running,
		# and try to find any that matches the given list of audio players.
		runningPlayers = shellHelper.ExecOneLine("playerctl -l")
		runningPlayers = runningPlayers.split()
		for line in runningPlayers:
			for p in config.PLAYERS:
				if p in line:
					self.PLAYER_NAME = line
		
		if self.PLAYER_NAME != "":
			artist = shellHelper.ExecSplit(["playerctl", "--player=" + self.PLAYER_NAME, "metadata", "artist"])
			title = shellHelper.ExecSplit(["playerctl", "--player=" + self.PLAYER_NAME, "metadata", "title"])

		if artist == "" and title == "":
			self.TEXT = self.PLAYER_NAME
		else:
			if config.SONG_FIRST:
				self.TEXT = title + " - " + artist
			else:
				self.TEXT = artist + " - " + title

	def Dzen(self):
		self.TextFormat()
		self.DZEN2LINE = self.TEXT
		self.AddAction()
		clickZonePrev = self.ActionCustomZone(self.HEADER, "1, playerctl --player=" + self.PLAYER_NAME + " previous")
		clickZoneNext = self.ActionCustomZone(self.TAIL, "1, playerctl --player=" + self.PLAYER_NAME + " next")
		return clickZonePrev + self.DZEN2LINE + clickZoneNext
	
	def WidthPxl(self, font):
		w = WidgetBase.WidthPxl(self, font)
		return w
