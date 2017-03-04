#!/usr/bin/env python

from operator import itemgetter
import sys

current_location = None
current_crime = None
current_dict = dict();

location = None
crime = None

best_location = None
best_count = 0;
best_dict = dict();

#count all crime from dict
def countCrime(dict):
    tCrime = 0;
    for val in dict.values():
        tCrime += val
    return tCrime

for line in sys.stdin:
    line = line.strip()
    location, crime, count = line.split('\t')
    
    try:
        count = int(count)
    except ValueError:
        continue
    #check if the same location    
    if current_location == location:
        #if the current array has the crime already
        if (current_dict.has_key(crime)) == True:
            #increase the crime by count
            current_dict[crime] += count
        else:
            #put the new crime to dict
            current_dict.update({crime:count})
    else:
        total_crime = countCrime(current_dict)
        #if current_location:
            #write result, is unneccsary
            #print '%s\t%d' % (current_location, total_crime);
            
        #save the best place
        if total_crime > best_count:
            best_count = total_crime
            best_location = current_location
            best_dict.update(current_dict)
            
        #initial new dict
        current_dict.clear()
        current_location = location
        current_dict.update({crime:count})

#in the end, show the best place
print "The best place is %s\nThe total crime: %d\nCrimes:%s" %(best_location, best_count, best_dict.keys())