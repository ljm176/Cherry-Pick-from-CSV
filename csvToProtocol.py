# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 09:47:29 2020

@author: lajamu
"""
import sys
import csv

csv_file = sys.argv[1]

def get_nested_list(c):
    with open(c, "r") as f:
        csvread = csv.reader(f, delimiter = ";")
        t = [row for row in csvread]
    return (t)

x = get_nested_list(csv_file)

prot = open("protocol.txt", "r")

new_prot = open("new_prot.py", "w")
new_prot.write("t_list = " + str(x))
for line in prot:
    new_prot.write(line)

new_prot.close()