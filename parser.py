# Title: Badboy Multiple File Result Parser
# Author: Allan Paul "Pogz" Sy Ortile
# Version: 0.1
# Previous Modification: 2017-07-05
# Last Modified: 2017-07-04
# Pre-requisites:
#   - Install Python 2.7
#   - Add path to environment variables
#   - Install Beautiful Soup via python setup.py install
# Notes:
#   - It is assumed that the result files are in the format 'xx Performance Test Results.html' where
#       xx is the number of result files
#   - It is assumed that these tests are inside a folder folder ie.
#       Folder/
#           |- parser.py
#           |- 94/
#               |- 1 Performance Test Results.html-images
#               |- 1 Performance Test Results.html
#   - The outer loop loops through all the folders
#   - The inner loop loops through all the html files and gets the summary values
#       average time, max time and warnings
#   - The target format is servers/folders as columns, instance number as rows (number of test runs)

from bs4 import BeautifulSoup
import os
import csv

NUMBER_OF_FILES = 10

# This walks through the directories and puts on a list
listStrDir = os.walk('.').next()[1]

# Lets convert the list to int so we can sort
listIntDir = map(int, listStrDir)
# Sort the list
listSortedIntDir = sorted(listIntDir)
# Convert back to string
listSortedStrDir = map(str, listSortedIntDir)

#print listSortedStrDir

for strDir in listSortedStrDir:
    #print strDir

    # LOOP FOLDERS HERE
    listWarnings = []
    listAverage = []
    listMax = []

    # LOOP FILES HERE
    for x in range (1,NUMBER_OF_FILES+1):

        filename = strDir + "/" + str(x) + ' Performance Test Results.html'
        soup = BeautifulSoup(open(filename), 'html.parser')

        table = soup.table
        rows = table.findAll('tr')

        # TODO: For some reason I cant strip out the unicode formatting
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]

        # This is the warnings
        listWarnings.append(data[1][3])
        # This is the average time
        listAverage.append(data[1][5])
        # This is the max time
        listMax.append(data[1][6])

    # Printing out for sanity
    strWarnings = ','.join(map(str, listWarnings)) 
    print strWarnings

    strAverage = ','.join(map(str, listAverage)) 
    print listAverage

    strMax = ','.join(map(str, listMax)) 
    print strMax

    # The new line is important in generating the csv file
    print "\n"

    # Write to CSV as a new row
    with open('warnings.csv', 'ab') as warningfile:
        writerwarning = csv.writer(warningfile)
        writerwarning.writerow(listWarnings)

    with open('average.csv', 'ab') as averagefile:
        writeraverage = csv.writer(averagefile)
        writeraverage.writerow(listAverage)

    with open('max.csv', 'ab') as maxfile:
        writermax = csv.writer(maxfile)
        writermax.writerow(listMax)

print "Done. Take note you have to TRANSPOSE THIS IN EXCEL."
# The csv will output in the reverse of the target order, instances as columns, folders as rows
print "For more information about transposing: https://youtu.be/4hSghWCuf6o" 
