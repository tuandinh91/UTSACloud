#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    items = line.split(",")
    
    #skip the first line in file
    if items[0].isdigit() is False:
        continue
        
    crime = items[1]
    location = items[5]
    #emit a number to use combiner
    print '%s\t%s\t%d' % (location, crime, 1)