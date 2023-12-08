#!/data/data/com.termux/files/usr/bin/python


from configparser import ConfigParser as editor
import getopt, getpass, hashlib, os, re, sys, time


## storing variables...
class BASE:
	ALL = "DEFAULT"
	CYAN = "\033[1;36m"
	FILE = "/data/data/com.termux/files/home/registry.ini"
	NORMAL = "\033[0m"
	PASSWORD = "SECURITY"
	RED = "\033[1;31m"
	UNDEFINED = "???"
	YELLOW = "\033[1;33m"



## all usable functions...
def view_about(everything):
	name = string_chopper(everything, "left")
	specific = string_chopper(everything, "right")
	if not specific:
		print("About this tool:")
		print()
		print("Directory: " + BASE.YELLOW + manage_data("get", name, "directory", BASE.CYAN + BASE.UNDEFINED) + BASE.NORMAL)
		print("Executable: " + BASE.YELLOW + manage_data("get", name, "executable", BASE.CYAN + BASE.UNDEFINED) + BASE.NORMAL)
		print("Last used: " + BASE.YELLOW + manage_data("get", name, "lastused", "Never been used before.") + BASE.NORMAL)
		print("Operator: " + BASE.YELLOW + manage_data("get", name, "operator", BASE.CYAN + BASE.UNDEFINED) + BASE.NORMAL)
	elif specific == "d":
		return manage_data("get", name, "directory", "")
	elif specific == "e":
		return manage_data("get", name, "executable", "")
	elif specific == "l":
		return manage_data("get", name, "lastused", "")
	elif specific == "o":
		return manage_data("get", name, "operator", "")
	else:
		return throw_error("not available right now")

def throw_error(message):
	print("There's an error occurred or maybe something happened there, which is: " + BASE.RED + str(message) + BASE.NORMAL)
	exit()

def string_chopper(component, request):
	RegExp = ".*"
	if request == "left":
		RegExp = "=" + RegExp
	elif request == "right":
		RegExp += "="
	else:
		throw_error("invalid request has pushed")
	using_once = re.sub("=.*", "", component)
	raw_material = re.sub(RegExp, "", component)
	if request == "right" and raw_material.startswith(using_once):
		return raw_material.replace(using_once, "")
	else:
		return raw_material

def run_tool(everything):
	x = string_chopper(everything, "left")
	y = string_chopper(everything, "right")
	name = manage_data("get", x, "", "")
	if not manage_data("check", x, "password", "Authentication required, pass the test to continue."):
		print()
		print()
		print("Yours one isn't right, can't run this.")
		exit()
	print("Starting up: '" + name + "'...")
	print()
	status = os.system(manage_data("get", x, "operator", "") + " " + manage_data("get", x, "directory", "") + manage_data("get", x, "executable", "") + " " + y)
	manage_data("set", x, "lastused", time.ctime())
	print()
	print()
	print()
	print("Process terminated with code: " + str(status))

def manage_data(worker, title, item, extras):
	ball = editor()
	ball.read(BASE.FILE)
	search = ball.get(BASE.ALL, title, fallback=False)
	if item == "password":
		if worker == "check":
			exist = ball.get(BASE.PASSWORD, title, fallback=False)
			if exist == False:
				return True
			else:
				print(extras)
				print()
				verify = getpass.getpass("Password: ")
				if exist == encode_text(verify):
					return True
				else:
					return False
		elif worker == "set":
			ball.set(BASE.PASSWORD, title, encode_text(extras))
		else:
			throw_error("you've ran out to nothing")
	else:
		part = ""
		if item:
			part += "."
		if worker == "add":
			if not search == False:
				print("A tool already registered before with that title.")
				print()
				print(BASE.YELLOW + "Note: " + BASE.NORMAL + "Editing feature will be published in the next update.")
			else:
				if title + part + item == title:
					part = title + "."
					print("You're going to add a new tool as '" + title + "' that will be in the registry.")
					print()
					d = input("Directory: ")
					e = input("Executable: ")
					n = input("Name: ")
					o = input("Operator: ")
					ball.set(BASE.ALL, title, n)
					ball.set(BASE.ALL, part + "directory", d)
					ball.set(BASE.ALL, part + "executable", e)
					ball.set(BASE.ALL, part + "operator", o)
					print()
					print("For more security, you can also add a password to protect your tool from others. (leave blank to keep unlocked)")
					print()
					while(True):
						first_type = getpass.getpass("New password: ")
						second_type = getpass.getpass("Confirm password: ")
						print()
						if first_type == second_type:
							if second_type:
								ball.set(BASE.PASSWORD, title, encode_text(second_type))
								print("Password setting was successful!")
							else:
								print("Keeping it unlocked.")
							break
						else:
							print("Password don't match, try again.")
							print()
							continue
		elif worker == "get":
			if search == False:
				throw_error("no tool found with that name")
			else:
				fixme = ball.get(BASE.ALL, title + part + item, fallback=extras)
				if not fixme == extras and item == "directory":
					if not fixme.endswith("/"):
						fixme += "/"
				return fixme
		elif worker == "remove":
			if search == False:
				throw_error("no tool found with that name")
			else:
				if title + part + item == title:
					part = title + "."
					getpass.getpass("Are you seriously want to remove '" + search + "' from registry? [You can press Ctrl+C to cancel] ")
					locked = ball.get(BASE.PASSWORD, title, fallback=False)
					if not locked == False:
						print("Need the permission to remove this, verify that it's your.")
						print()
						verify = getpass.getpass("Password: ")
						if locked == encode_text(verify):
							ball.remove_option(BASE.PASSWORD, title)
						else:
							print()
							print()
							print("Wrong password, access denied.")
							exit()
					print()
					ball.remove_option(BASE.ALL, title)
					ball.remove_option(BASE.ALL, part + "operator")
					ball.remove_option(BASE.ALL, part + "lastused")
					ball.remove_option(BASE.ALL, part + "executable")
					ball.remove_option(BASE.ALL, part + "directory")
					print("Removing '" + search + "' has succeeded.")
		elif worker == "set":
			ball.set(BASE.ALL, title + part + item, extras)
		else:
			throw_error("you've ran out to nothing")
	next = open(BASE.FILE, "w")
	ball.write(next)
	next.close()

def encode_text(content):
	return hashlib.sha256(content.encode()).hexdigest()




## game on!
## removing the first argument,
## which is the file's name...
argument_list = sys.argv[1:]
length = len(argument_list)
short_form = "ailr"
long_form = ["add", "information", "launch", "remove"]
try:
	argument, value = getopt.getopt(argument_list, short_form, long_form)
	for currentArgument, currentValue in argument:
		if currentArgument in ("-a", "--add"):
			manage_data("add", argument_list[1], "", "")
		elif currentArgument in ("-i", "--information"):
			if length <= 1:
				print("Tool Manager (" + BASE.CYAN + "V1.0" + BASE.NORMAL + ")")
				print()
				print("Manage your tools easily with")
				print("new look and fashion of commands!")
				print()
				print("Made by " + BASE.YELLOW + "@devwithsd" + BASE.NORMAL + ", and thanks for using!")
			else:
				view_about(argument_list[1])
		elif currentArgument in ("-l", "--launch"):
			run_tool(argument_list[1])
		elif currentArgument in ("-r", "--remove"):
			manage_data("remove", argument_list[1], "", "")
except getopt.error as raised_problem:
	throw_error(raised_problem)
except KeyboardInterrupt:
	exit()