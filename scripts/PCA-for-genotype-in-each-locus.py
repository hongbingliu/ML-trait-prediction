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

def main(input_file, ref, output_file):
	fout = open(output_file, 'w')
	all = []

	genotype = pd.read_table(input_file)
	
	print ("---------------pandas read OK!--------------")
	
	_1, _2, _3, _4, *samples = os.popen('head -1 ' + input_file).read()[:-1].split('\t')
#	print (samples[-1])
	
	gene_distance = []
	with open(ref) as fh:
		for i in fh:
			ds = i.split('\t')
			gene_distance.append([ds[3],ds[4]])
	print ("--------------gene distance read OK!---------------")
	#print (gene_distance[1])
	ju = True
	ju_pca = True
	for n in range(genotype.shape[0]):
	#	print (gene_distance[0])
		if int(genotype.loc[n,'posi']) >= int(gene_distance[0][0]) and int(genotype.loc[n,'posi']) <= int(gene_distance[0][1]) and ju:
			row_start = n
			ju = False
			ju_pca = True
			print ("Row " + str(n) + ":" + str(genotype.loc[n,'posi']) + " appended..." + str(gene_distance[0]))

		elif int(genotype.loc[n,'posi']) > int(gene_distance[0][1]):
			row_end = n
			ju_pca = pca_calculate(samples,genotype,row_start,row_end,fout,ju_pca)
			ju = True
			if ju_pca:
				gene_distance.pop(0)
				break
			if int(genotype.loc[n,'posi']) >= int(gene_distance[0][0]) and int(genotype.loc[n,'posi']) <= int(gene_distance[0][1]):
				row_start = n
			else:
				while True:
					if (int(genotype.loc[n,'posi']) > int(gene_distance[0][1])):
						gene_distance.pop(0)
						print ("pop OK!" + str(gene_distance[0]))
					else:
						break
				if int(genotype.loc[n,'posi']) < int(gene_distance[0][0]):
					pass
				else:
					row_start = n
					ju = False
					ju_pca = True
					print ("Row " + str(n) + ":" + str(genotype.loc[n,'posi']) + " appended...")
					
				print ("Row " + str(n) + ":" + str(genotype.loc[n,'posi']) + " out of the distance...1" + str(gene_distance[0]))

		elif int(genotype.loc[n,'posi']) < int(gene_distance[0][0]):
			print ("Row " + str(n) + ":" + str(genotype.loc[n,'posi']) + " out of the distance...2" + str(gene_distance[0]))

		else:
			print ("Row " + str(n) + " appended...-----" + str(gene_distance[0]))
			

	fout.close()

def pca_calculate(samples,genotype,row_start,row_end,fout,ju_pca):
	if row_end - row_start < 4 or not ju_pca:
		print ("from " + str(row_start) + " to " + str(row_end) + " snp number is less...")
		return False
	all = []
	for i in samples:

			all.append(np.array(genotype.loc[row_start:row_end,i]))
	print ("from " + str(row_start) + " to " + str(row_end))
	print ("--------------np array append OK!-------------------")
	
	X = np.array(all)
	print (X)

	pca = decomposition.PCA()
	pca.fit(X)
	pca.n_components = 5
	X_reduced = pca.fit_transform(X)

	print ("---------------pca transform OK!--------------------")
	print(pca.explained_variance_ratio_) 	
	num = 0
	for each in X_reduced:
		each = each.tolist()
		#print (type(each))
		fout.write(samples[num] + "\t" + str("\t".join(str(v) for v in each))  + "\n")
		num += 1

if __name__ == "__main__":
	time_start = time.time()

	input_file,ref,output_file,h = get_option()
	if str(h) == "":
		main(input_file, ref, output_file)
		print ("time: " + str (time.time()-time_start))
	else:
		print (h)
