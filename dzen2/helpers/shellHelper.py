#!/bin/python

import json

'''
Has a couple of functions used to execute Linux shell commands.
If commands are passed with errors or packages are not installed,
the functions will return "0" and print the error in stdout.
'''

import subprocess

def ExecSplit(listOfCommands):
	'''Run Linux shell command. Return result as string.

	As an arument it takes a list of strings, e.g., [ "sudo", "apt", "update" ].
	Convy when need to run a command but the args are variables,
	with this function you don't have to mess up with quotes and plus signs to combine a command string.
	Warning: Use it for single commands only (with command arguments as elements in list).
	For complex piped commands like "echo smthing | grep 'thing' | awk {'whatever'}"
	use 'ExecOneLine()' instead.'''
	out = "0"
	try:
		out = subprocess.check_output(
			listOfCommands, universal_newlines=True).strip()
	except subprocess.CalledProcessError as e:
		if e.output.startswith('error'):
			error = json.loads(e.output[7:]) # Skip "error: "
			pass
	except FileNotFoundError as e:
		pass
	return out

def ExecOneLine(command):
	'''Run Linux shell command. Return result as string.

	Usefull for simple commands with no variables (e.g.: ExecOneLine("date +"%d %m %H:%M:%S"))
	and for complicated combinations of multiple commands, such as
	"echo 'Hello world' | grep -E -oP 'Hello' | awk {blahblah}".'''
	out = "0"
	try:
		out = subprocess.check_output(
			command, shell=True, universal_newlines=True).strip()
	except subprocess.CalledProcessError as e:
		if e.output.startswith('error'):
			error = json.loads(e.output[7:]) # Skip "error: "
			pass
	except FileNotFoundError as e:
		pass
	return out