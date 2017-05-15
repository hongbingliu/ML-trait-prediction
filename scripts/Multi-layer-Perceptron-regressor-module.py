#!/usr/bin/env python

import sys, getopt
import re
import time
import numpy as np
import pandas as pd
from sklearn import decomposition
import os
from sklearn import cross_validation, metrics
from sklearn.neural_network import MLPRegressor  
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.grid_search import GridSearchCV
from scipy.stats.stats import pearsonr
from sklearn.metrics import fbeta_score, make_scorer

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
#	print (samples[-1])
	for i in samples:
		#print (i)
		if i == "L4755":
			break
		all.append(np.array(genotype[i]))

	#print (all)	
	print ("np array append OK!")
	
	X = np.array(all)
	#print (len(X))
	
	phenotype = pd.read_table(ref)
	#print (
	ph1 = phenotype["trait1"][:4754]
	ph2 = phenotype["trait2"][:4754]
	ph3 = phenotype["trait3"][:4754]
	
	model_mlp = MLPRegressor(solver='adam', random_state=1)  	
	model_gbr_disorder=GradientBoostingRegressor()

	kf = cross_validation.KFold(X.shape[0], n_folds=5, random_state=1)
	ftwo_scorer = make_scorer(pea)
	scores1 = cross_validation.cross_val_score(model_mlp, X, ph1, cv=kf, scoring = ftwo_scorer)
	print (scores1.mean())
	scores2 = cross_validation.cross_val_score(model_mlp, X, ph2, cv=kf, scoring = ftwo_scorer)
	print (scores2.mean())
	scores3 = cross_validation.cross_val_score(model_mlp, X, ph3, cv=kf, scoring = ftwo_scorer)
	print (scores3.mean())
	#scores = cross_validation.cross_val_score(model_gbr_disorder, X, ph, cv=kf, scoring = ftwo_scorer)

def pea(x,y):
	t = pearsonr(x,y)
	return t[0]

if __name__ == "__main__":
	time_start = time.time()

	input_file,ref,output_file,h = get_option()
	if str(h) == "":
		main(input_file, ref, output_file)
		print ("time: " + str (time.time()-time_start))
	else:
		print (h)
