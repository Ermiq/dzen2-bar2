# dzen2-bar2
A bit more advanced setup and complicated code base than the other simple basic version in the "Dzen2-bar" repository:
( https://github.com/Ermiq/Dzen2-bar ).

GitHub said "Add a ReadMe". So, I'm adding...

Just a basic dzen2 bar, written in Python. With exception of one Bash script that is used to start the bar.
I failed when I tried to figure out how to make it all in Python. Bar just dooesn't update when started from Python code.
I'm a total noob in both Python and Bash, so...

If you're looking for an example of a dzen2 panel/bar setup, not overwhelmed with different icon packs,
without sparkles and whistles, just a basic stuff that will probably start successfully on another machine and not just
on the one it has been developed on, then you're in right place.

What's there:

* i3 workspaces indicator;
* WiFi - shows SSID and connection quality;
* Volume indicator;
* RAM usage bar;
* Battery bar
* Time/date.

Installation:

- Clone or download this repository;
- Put 'dzen2' folder in your '$HOME/.config' directory;
- Give all the files execution permissions;
- Run 'dzen2-startup.sh' script.

Requirements:

- Python (probably version 3+);
- amixer - for volume indicator;
- acpi - for battery indicator (I think it's installed by default on every distribution);
- for WiFi check out your interface names (run '/sbin/iwconfig'). By default 'wifi.py' script uses "wlp2s0" name for WiFi adapter. On some distros you'll need to change it to "wlan0" (see 'wifi.py' file);
- i3 window manager - for i3 workspaces indication, haha.
