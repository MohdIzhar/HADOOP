#!/usr/bin/python36
import sys

for line in sys.stdin:
        #j = line.strip()
        k = line.split()
        if 'Data' in k:
                print(line,end="")
        else:
                pass
