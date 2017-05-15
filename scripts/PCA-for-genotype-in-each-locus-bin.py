#!/usr/bin/env python

import sys, getopt
import re
import time
import numpy as np
import pandas as pd
from sklearn import decomposition
import os

def get_option():
	opts, args = getopt.getopt(sys.argv[1:], "hi:o:f:")
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

def get_num(n):
	for i in range(0,n,200):
		yield i, i+200

def main(input_file, ref, output_file):
	fout = open(output_file, 'w')
	all = []

	genotype = pd.read_table(input_file)
	
	print ("---------------pandas read OK!--------------")
	
	_1, _2, _3, _4, *samples = os.popen('head -1 ' + input_file).read()[:-1].split('\t')
#	print (samples[-1])
	#fout.write('\t'.join(samples) + '\n')
	for a,b in get_num(genotype.shape[0]):
		print (str(a) + "\t" + str(b))
		for i in samples:
			all.append(np.array(genotype.loc[a:b,i]))
#	print ("from " + str(row_start) + " to " + str(row_end))
		print ("--------------np array append OK!-------------------")
	
		X = np.array(all)
		print (X.shape[1]//4)

		pca = decomposition.PCA()
		pca.fit(X)
		if (X.shape[1]//4) < 50:
			pca.n_components = X.shape[1]//4
		else:
			pca.n_components = 50
		X_reduced = pca.fit_transform(X)

#	print ("---------------pca transform OK!--------------------")
		pca_ratio = 0
		for a in pca.explained_variance_ratio_:
			pca_ratio += float(a)
			print (pca_ratio)
			#print (a)
		num = 0
		print (len(samples))
		print (len(X_reduced))
		new = []
		for each in X_reduced:
			each = each.tolist()
			new.append(each)
		#print (type(each))
#			fout.write(samples[num] + "\t" + str("\t".join(str(v) for v in each))  + "\n")
			num += 1
		for a in zip(*new):
			fout.write('\t'.join(str(v) for v in a) + '\n')
		
		all = []

if __name__ == "__main__":
	time_start = time.time()

	input_file,ref,output_file,h = get_option()
	if str(h) == "":
		main(input_file, ref, output_file)
		print ("time: " + str (time.time()-time_start))
	else:
		print (h)
