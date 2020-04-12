#!/bin/python

import subprocess

def GetFromShell(listOfCommands):
	'''Run Linux shell command.
	As an arument it takes a list of strings, e.g., [ "sudo", "apt", "update" ].
	Use it for single commands only. For piped commands use 'GetFromShellLong()' instead.
	Returns the result as string.'''
	out = subprocess.check_output(
		listOfCommands, universal_newlines=True).strip()
	return out
	
def GetFromShellLong(command):
	'''Run Linux shell command.
	This is for complicated combinations of commands, such as "echo "Hello world" | grep Hello".
	Returns the result as string.'''
	out = subprocess.check_output(
		command, shell=True, universal_newlines=True).strip()
	return out