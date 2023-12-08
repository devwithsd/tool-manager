#!/data/data/com.termux/files/usr/bin/python
from os import system
class BASE:
	LINK = "https://raw.githubusercontent.com/devwithsd/tool-manager/main"

## installation part...
print("Installing, please wait patiently...")
system("wget -q " + BASE.LINK + "/tool.py -O $PREFIX/bin/tool")
system("wget -q " + BASE.LINK + "/registry.ini -O ~/registry.ini")
system("chmod +x $PREFIX/bin/tool")
print("Successfully installed, run 'tool -i' command for more information.")
exit()
