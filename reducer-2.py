#!/usr/bin/python

from operator import itemgetter
import sys

#function to declare new array of month from 1 to 12
def newMonthArray():
    f = []
    for i in range(12):
        f.append(0)
    return f
    
#function to print out the crime and matrix in the same line
def printline(crime, month_list):
    for num in month_list:
        crime += ( " " + str(num))
    print crime    
    
current_crime = None
current_month_list = None
crime = None

for line in sys.stdin:
    line = line.strip()
    #crime, month, count = line.split('\t',2)
    items = line.split('\t',2)
    
    #invalid of input length
    if (len(items) != 3):
        continue
    else:
        crime =items[0]
        month = items[1]
        count = items[2]   
    
    try:
        count = int(count)
        month = int(month)
        #invalid month
        if (month < 0 or month > 12):
            continue
    except ValueError:
        continue

    #check if the same crime   
    if current_crime == crime:
        #increase the count in the matrix
        current_month_list[month-1] += count
        
    else:
        if current_month_list is not None:
            #different crime, then print out the matrix
            printline(current_crime, current_month_list)
            
        #initialize new crime
        current_crime = crime
        current_month_list = newMonthArray()
        current_month_list[month-1] += count

#print the last crime
printline(crime, current_month_list)