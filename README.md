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

Fonts:
dzen2 uses the old and kinda obsolete fonts management system (X Logical Font Description), and it only able to work with
fonts registered by this X system. Usually it's just fonts located in '/usr/share/fonts/X11' directory. It doesn't know about any other fonts installed on your system and it doesn't support tools like 'fontconfig'.
As an example, there's no monospace fonts in X fonts, so you can't get stable line that stays aligned and nice, it will twitch and jerk everytime when some text is changed on the bar line. To eliminate this problem, need to use some monospace font in dzen2.
How to do that:
Find out which font you'd like to use and where it is stored in your system. Usually, fonts could be found in '/usr/share/fonts' directory. Also, you could have put some additional fonts to your '$HOME/.fonts'.
To make a font available for X fonts system and dzen2, gotta do the following:
  1. navigate to the directory with font files. e.g.:
    $ cd /usr/share/fonts/truetype/liberation
  2. generate two special files in this directory (need sudo if it's in '/usr/share'):
    $ mkfontscale
    $ mkfontdir
  3. Add the folder to X fonts system roster:
    $ xset +fp /usr/share/fonts/truetype/liberation
  4. Force X fonts to rescan:
    $ xset fp rehash
Now the font should work with dzen2. To check out fonts recognized by X fonts system, you can use the tool 'xfontsel'. It represents the font and shows the font code usefull in dzen2 config (e.g., -*-liberation mono-*-*-*-*-*-*-*-*-m-*-*-* ).
The dropdown menus will have grayed out option for unsupported features of the font (like unsupported spacing modes: mono, regular), sizes, etc. Check out some Arch Wiki info:
  https://wiki.archlinux.org/index.php/Fonts#Older_applications
  https://wiki.archlinux.org/index.php/X_Logical_Font_Description
