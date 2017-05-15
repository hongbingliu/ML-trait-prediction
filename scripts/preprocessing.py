#!/usr/bin/env python

import sys, getopt
import re
import time
import numpy as np
import pandas as pd
import os
from scipy.stats.stats import pearsonr
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold

def get_option():
	opts, args = getopt.getopt(sys.argv[1:], "hi:f:o:")
	input_file = ""
	output_file = ""
	ref = ""
	h = ""
	for op, value in opts:
		if op == "-i":
			input_file = value
		elif op == "-o":
			output_file = value
		elif op == "-f":
			ref = value
		elif op == "-h":
			h = 'useages:\nremove the sequence which contain "N"\n-i : inputfile\n-o : outputfile\n'
	return input_file,ref,output_file,h

def main(input_file, ref, output_file):
	fout = open(output_file, 'w')
	all = []

	genotype = pd.read_table(input_file)
	
	print ("pandas read OK!")
	
	samples = os.popen('head -1 ' + input_file).read()[:-1].split('\t')

	for i in samples:
		if i == "L4755":
			break
		all.append(np.array(genotype[i]))
	
	print ("np array append OK!")
	
	X = np.array(all)
	
	phenotype = pd.read_table(ref)
	y = phenotype["trait1"][:4754]

	min_max_scaler = preprocessing.MinMaxScaler()
	X_scaler=min_max_scaler.fit_transform(X)
	
	print (X_scaler.shape)

	sel = VarianceThreshold(threshold=.06)
	X_sel = sel.fit_transform(X_scaler)
	print (X_sel.shape)
	
if __name__ == "__main__":
	time_start = time.time()

	input_file,ref,output_file,h = get_option()
	if str(h) == "":
		main(input_file, ref, output_file)
		print ("time: " + str (time.time()-time_start))
	else:
		print (h)
