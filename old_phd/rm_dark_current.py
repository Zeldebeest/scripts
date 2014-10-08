import os
import numpy as np
from StringIO import StringIO
import re
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('file',help='gets the folder name')
parser.add_argument('-dc', help='dark current', type=int)
parser.add_argument('-o', help='output file name', default='dc_subtracted.pgm')
args = parser.parse_args()

newData = []

with open(args.file, 'r') as inFile:
	with open(args.o, 'w') as outFile:
		outFile.write(inFile.readline()) # magic number
		outFile.write(inFile.readline()) # coment line
		outFile.write(inFile.readline()) # size
		outFile.write(inFile.readline()) # bit depth
		for line in inFile:
			ints_in_this_line = [int(i) for i in line.split()]
			for value in ints_in_this_line:
				newValue = value - args.dc
				if newValue > 0:
					newData.append(newValue)
				else:
					newData.append(0)
		for item in newData:
			print>>outFile, item
			