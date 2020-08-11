# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:56:59 2020

@author: JOAO VICTOR
"""
import os
import sys

try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError:
    user_paths = []

print("PYTHONPATH: "), user_paths
print ("sys.path: "), sys.path
