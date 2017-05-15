#!/usr/bin/env python

import sys, getopt
import re
import time
import os

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
	name = os.popen('head -6210 ' + input_file + ' |cut -f1').read().split('\n')
	for each in name[:-1]:
		fout.write(each + "\t")
		p = os.popen('grep "' + each + '" ' + input_file).read().split('\n')
		for i in p[:-1]:
		#	print (i.split('\t'))
			_, *content, _final = i.split('\t')
			fout.write('\t'.join(content))
			fout.write('\t')
		fout.write(''.join(_final) + '\n')
		
		
	fout.close()

if __name__ == "__main__":
	time_start = time.time()

	input_file,output_file,h = get_option()
	if str(h) == "":
		main(input_file, output_file)
		print ("time: " + str (time.time()-time_start))
	else:
		print (h)
