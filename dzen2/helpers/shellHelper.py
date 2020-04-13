#!/bin/python

import json

'''
Has a couple of functions used to execute Linux shell commands.
The functions are not complicated, but need to type a whole line of code,
so, I packed them to a separate functions.
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
	out = subprocess.check_output(
		listOfCommands, universal_newlines=True).strip()
	return out

def ExecOneLine(command):
	'''Run Linux shell command. Return result as string.

	Usefull for simple commands with no variables (e.g.: ExecOneLine("date +"%d %m %H:%M:%S"))
	and for complicated combinations of multiple commands, such as
	"echo 'Hello world' | grep -E -oP 'Hello' | awk {blahblah}".'''
	out = subprocess.check_output(
		command, shell=True, universal_newlines=True).strip()
	return out