#!/bin/python

import subprocess

def Run(processStr):
    out = subprocess.check_output(
        processStr, shell=True, universal_newlines=True).strip()
    return out