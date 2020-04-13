#!/bin/sh

# Dzen2 toolbar/statusbar execution file.
# Options:
# -xs = which Xinerama screen
# -l  = number of lines in slave (dropdown) window
# -u update continually
# -p <n> timed termination; w/o n seconds, persist forever.
# retval: 0 = EOF; 1 = error; or exit:n where n=user-defined retval.
# -e event... -e 'event1=action1:option1:...option<n>,...,action<m>;...;event<l>'
#    event... -e 'button1=exec:xterm:firefox;entertitle=uncollapse,unhide;button3=exit'
# Supported events: (see latest README or online docs)
#    onstart             Perform actions right after startup
#    onexit              Perform actions just before exiting
#    onnewinput          Perform actions if there is new input for the slave window
#    button1             Mouse button1 released
#    button2             Mouse button2 released
#    button3             Mouse button3 released
#    button4             Mouse button4 released (usually scrollwheel)
#    button5             Mouse button5 released (usually scrollwheel)
#    entertitle          Mouse enters the title window
#    leavetitle          Mouse leaves the title window
#    enterslave          Mouse enters the slave window
#    leaveslave          Mouse leaves the slave window
#    sigusr1             SIGUSR1 received
#    sigusr2             SIGUSR2 received
#    key_KEYNAME         Keyboard events (*)

# Kill previously launched bars and dzen2 instances:
kill -9 $(pgrep bar | grep -v $$)
kill -9 $(pgrep dzen2)

# Pre execution: see if 'stop' was passed as $1 and if so
# don't restart dzen2; just exit instead:
[ "$1" = 'stop' ] && exit 0

# Python bar generator runs in an endless loop and
# outputs the data for DZEN in stdout every second.
~/.config/dzen2/bar_generator.py | dzen2 -dock -ta l -u -p &