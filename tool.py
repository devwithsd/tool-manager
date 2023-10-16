#!/data/data/com.termux/files/usr/bin/python
from configparser import ConfigParser as manager
import getopt, getpass, hashlib, os, re, sys, time
class DATABASE:
	FILE = "/data/data/com.termux/files/home/registry.ini"
	BOX = "DEFAULT"
	PASSWORD = "SECURITY"
def throw(text):
	print("You may not using me according to rules or something else happened,")
	print("the mistake that you have done there: " + text)
def run(string):
	a = command("1", string)
	b = command("2", string)
	if get("1", a, False):
		if get("3", a, False):
			key = getpass.getpass("Password: ")
			if not get("3", a, "") == key:
				exit()
		message = "Starting " + get("1", a, "")
		directory = get("1", a + "-directory", "")
		if not directory.endswith("/"):
			directory = directory + "/"
		if string.endswith(a):
			message = message + "..."
		else:
			message = message + " with pushed external arguments..."
		print(message)
		print()
		code = os.system(get("1", a + "-operator", "") + " " + directory + get("1", a + "-executable", "") + " " + b)
		get("2", a + "lastused", time.ctime())
		print()
		print("Your tool's process is ended with code " + str(code) + ".")
	else:
		throw("no tool found with that name")
def get(worker, string, value):
	ball = manager()
	ball.read(DATABASE.FILE)
	if worker == "1":
		return ball.get(DATABASE.BOX, string, fallback=value)
	elif worker == "2":
		return ball.set(DATABASE.BOX, string, value)
	elif worker == "3":
		return ball.get(DATABASE.PASSWORD, string, fallback=value)
	else:
		throw("function not available")
def command(need, arguments):
	extra = re.sub(r"...*\=", "", arguments)
	main = arguments.replace("=" + extra, "")
	if need == "1":
		return main
	elif need == "2":
		if extra.startswith(main):
			return extra.replace(main, "")
		else:
			return extra
	else:
		throw("failed to understand you")
def about(string):
	a = command("1", string)
	b = command("2", string)
	if get("1", a, False):
		if string.endswith(a):
			print("About this tool:")
			print("Directory: " + get("1", a + "-directory", ""))
			print("Executable: " + get("1", a + "-executable", ""))
			print("Last used: " + get("1", a + "-lastused", ""))
			print("Operator: " + get("1", a + "-operator", ""))
		else:
			if b == "d":
				print(get("1", a + "-directory", ""))
			elif b == "e":
				print(get("1", a + "-executable", ""))
			elif b == "l":
				print(get("1", a + "-lastused", ""))
			elif b == "o":
				print(get("1", a + "-operator", ""))
			else:
				throw("character seems to be unknown")
	else:
		throw("no tool found with that name")
list = sys.argv[1:]
length = len(list)
short = "il"
long = ["information", "launch"]
try:
	argument, value = getopt.getopt(list, short, long)
	for currentArgument, currentValue in argument:
		if currentArgument in ("-i", "--information"):
			if length == 1:
				print("Tool Manager (v0.1-dev)")
				print()
				print("I can be used to manage")
				print("your tools smoothly with fashion!")
				print()
				print("Made by @devwithsd, and thanks to use me.")
			else:
				about(list[1])
		elif currentArgument in ("-l", "--launch"):
			run(list[1])
except getopt.error as problem:
	throw(problem)
