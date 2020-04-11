#!/bin/python

import json
from .widgetBase import Widget

class i3WorkspacesWidget(Widget):

    WORKSPACES = [""]
    TX1 = '#DBDADA'     # medium grey text
    TX2 = '#F9F9F9'     # light grey text
    GRY = '#909090'     # dark grey text
    BAR = '#A6F09D'     # green background of bar-graphs
    GRN = '#65A765'     # light green (normal)
    BGR = '#00FF00'		# bright green
    YEL = '#FFFFBF'     # light yellow (caution)
    RED = '#FF0000'     # light red/pink (warning)
    WHT = '#FFFFFF'     # white
    BLK = '#000000'     # black

    def __init__(self, width):
        Widget.__init__(self, width)

    def Update(self):
        self.TEXT = ""
        self.WORKSPACES.clear()

        x = json.loads(self.GetFromShell("i3-msg -t get_workspaces"))

        # This may return more than 1 workspace if you have more than one monitor.
        for workspace in x:
            self.TEXT += workspace["name"]
            if workspace["focused"]:
                self.WORKSPACES.append("^fg({})^bg({}){}".format(
                    self.BGR, self.BAR, workspace["name"]))
            else:
                self.WORKSPACES.append("^fg({})^bg({}){}".format(
                    self.GRY, self.BLK, workspace["name"]))
        self.TEXT = self.AlignCenter(self.TEXT, self.WIDTH)

    def Dzen(self):
        return self.WORKSPACES

    def Width(self):
        return self.WIDTH

    def WidthPxl(self, font):
        w = self.GetFromShell("dzen2-textwidth " +
                              font + ' "' + self.TEXT + '"')
        return int(w)
