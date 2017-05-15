#!/usr/bin/env python

import sys, getopt
import re
import time

def get_option():
	opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
	input_file = ""
	output_file = ""
	h = ""
	for op, value in opts:
		if op == "-i":
			input_file = value
		elif op == "-o":
			output_file = value
		elif op == "-h":
			h = 'useages:\nremove the sequence which contain "N"\n-i : inputfile\n-o : outputfile\n'
	return input_file,output_file,h

def main(input_file, output_file):
	fout = open(output_file, 'w')
	all = []
	count = 1
	with open (input_file) as f:
		_, *i = f
		fout.write(_)
		for each in i:
			al = str(each.split('\t')[1])
			al = al.split('/')
			zero = al[0] + al[0]
			one = al[1] + al[1]
			two = al[0] + al[1]
			each = re.sub(zero, '0', each)
			each = re.sub(two, '1', each)
			each = re.sub(one, '2', each)
			fout.write(each)
			#break
	fout.close()

if __name__ == "__main__":
	time_start = time.time()

	input_file,output_file,h = get_option()
	if str(h) == "":
		main(input_file, output_file)
		print ("time: " + str (time.time()-time_start))
	else:
		print (h)
