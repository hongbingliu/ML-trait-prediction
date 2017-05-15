#!/usr/bin/env python

import sys, getopt
import re
import time

def get_option():
	opts, args = getopt.getopt(sys.argv[1:], "hi:o:e:")
	input_file = ""
	output_file = ""
	export = ""
	h = ""
	for op, value in opts:
		if op == "-i":
			input_file = value
		elif op == "-o":
			output_file = value
		elif op == "-e":
			export = value
		elif op == "-h":
			h = 'useages:\nremove the sequence which contain "N"\n-i : inputfile\n-o : outputfile\n'
	return input_file,output_file,export,h

def main(input_file, output_file, export):
	fout = open(output_file, 'w')
	ex = open(export, 'w')
	all = []
	count = 1
	with open (input_file) as f:
		_, *i = f
		ex.write(_)
		for each in i:
			more = each[:-1].split('\t')
			name = more[0]
			fout.write(name + "\t")
			content = more[4:]
			total = len(content)
			fr = len(re.findall("0",''.join(content)))
			fout.write(str(fr) + "\t")
			fout.write(str(len(re.findall("1",''.join(content)))) + "\t")
			fout.write(str(len(re.findall("2",''.join(content)))) + "\t")
			if 1-fr/total < 0.05:
				fout.write("False\t")
			else:
				ex.write(each)	
			fout.write(str(1-fr/total) + "\n")
			#break
			
	fout.close()

if __name__ == "__main__":
	time_start = time.time()

	input_file,output_file,export,h = get_option()
	if str(h) == "":
		main(input_file, output_file, export)
		print ("time: " + str (time.time()-time_start))
	else:
		print (h)
