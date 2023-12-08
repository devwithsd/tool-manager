#!/data/data/com.termux/files/usr/bin/python

import os

class BASE:
	LINK = "https://raw.githubusercontent.com/devwithsd/tool-manager/main"


## installation part...
print("Installing, please wait patiently...")
print()
os.system("wget " + BASE.LINK + "/tool.py -O $PREFIX/bin/tool -q")
os.system("wget " + BASE.LINK + "/registry.ini -O ~/registry.ini -q")
print()
print()
print("Successfully installed, run 'tool -i' command.")
exit()