#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip()
    items = line.split(",")
    
    #skip the first line in file
    if items[0].isdigit() is False:
        continue
        
    crime = items[1]
    date = items[2]
    month = date.split("/",1)[0]
    
    #if month is not found then skip to next line
    try:
        month = int(month)
    except ValueError:
        continue
        
    #emit a number to use combiner
    print '%s\t%d\t%d' % (crime, month, 1)