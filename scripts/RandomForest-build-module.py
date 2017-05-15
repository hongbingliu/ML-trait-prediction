#!/usr/bin/env python

import sys, getopt
import re
import time
import numpy as np
import pandas as pd
from sklearn import decomposition
import os
from sklearn import cross_validation, metrics
from sklearn.ensemble import RandomForestRegressor
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

	print ("------------------------ time : " + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + "------------------------------")

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
	
#	rf = RandomForestRegressor()
#	rf.fit(X[:3500], ph[:3500])
	
#	results = rf.predict(X[3501:])
#	res = np.array(ph[3501:])
#	for num in range(20):
#		print (str(float(results[num])/float(res[num])))
	#print (ph)
	#print (X.shape[0])


#--------------------------param test for min_samples_split:17 and min_samples_leaf:7 :---------------------------------

#	param_test3 = {'min_samples_split':list(range(11,20,2)), 'min_samples_leaf':[5,7,9,12]}
#	gsearch3 = GridSearchCV(estimator = RandomForestRegressor(n_estimators= 150, max_depth=30,max_features='sqrt' , random_state=10, n_jobs = -1),param_grid = param_test3, cv=5)
#	gsearch3.fit(X,ph)
#	print (gsearch3.grid_scores_, gsearch3.best_params_, gsearch3.best_score_)



#--------------------------param test for max_depth:20 :---------------------------------------------------------------	

#	param_test2 = {'max_depth':list(range(20,90,10))}
#	gsearch2 = GridSearchCV(estimator = RandomForestRegressor(n_estimators= 150, min_samples_leaf=5,min_samples_split=5,max_features='sqrt' , random_state=10,n_jobs = -1),param_grid = param_test2, cv=5)
#	gsearch2.fit(X,ph)
#	print (gsearch2.grid_scores_, gsearch2.best_params_, gsearch2.best_score_)


#--------------------------param test for n_estimators :---------------------------------------------------------------

#	param_test1 = {'n_estimators':list(range(80,201,10))}
#	print (param_test1)
#	gsearch1 = GridSearchCV(estimator = RandomForestRegressor(min_samples_split=8,min_samples_leaf=5,max_depth=100,max_features='sqrt' ,random_state=10,n_jobs = -1),param_grid = param_test1,cv=5)
#	gsearch1.fit(X,ph)
#	print (gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_)


	print ('train begin..')

	print ('--------------------------parament setting---------------------------')

	random_state=10
	n_estimators=600
	max_features=800
	n_jobs=-1
	max_depth=25
	min_samples_split=40
	min_samples_leaf=80
	
	print ("random_state=" + str(random_state) + "\n" + "n_estimators=" + str(n_estimators) + "\n" + "max_features=" + str(max_features) + "\n" + "n_jobs=" + str(n_jobs) + "\n" + "max_depth=" + str(max_depth) + "\n" + "min_samples_split=" + str(min_samples_split) + "\n" + "min_samples_leaf=" + str(min_samples_leaf))
	print ("---------------------------------------------------------------------")


	alg = RandomForestRegressor(random_state=random_state, n_estimators=n_estimators, max_features=max_features, n_jobs=n_jobs, max_depth=max_depth, min_samples_split=min_samples_split,min_samples_leaf=min_samples_leaf)
	kf = cross_validation.KFold(X.shape[0], n_folds=5, random_state=1)
	ftwo_scorer = make_scorer(pea)

#--------------------------------------- cross validation process ---------------------------------		
#	for train, test in kf:
#		alg.fit(X[train],ph1[train])
#		y_predict = alg.predict(X[test])
#		print (pearsonr(list(ph1[test]),y_predict))
#--------------------------------------------------------------------------------------------------	

	#scores = cross_validation.cross_val_score(alg, X, ph1, cv=kf)
	#print (scores)
	scores1 = cross_validation.cross_val_score(alg, X, ph1, cv=kf, scoring = ftwo_scorer)
	print ("trait 1: " + str(scores1) + " ; trait 1 scores mean:" + str(scores1.mean()))
	scores2 = cross_validation.cross_val_score(alg, X, ph2, cv=kf, scoring = ftwo_scorer)
	print ("trait 2: " + str(scores2) + " ; trait 2 scores mean:" + str(scores2.mean()))
	scores3 = cross_validation.cross_val_score(alg, X, ph3, cv=kf, scoring = ftwo_scorer)
	print ("trait 3: " + str(scores3) + " ; trait 3 scores mean:" + str(scores3.mean()))

	fout.close()

def pea(x, y):
	k = pearsonr(x,y)
	return k[0]

if __name__ == "__main__":
	print ("########################################## start ################################################")
	time_start = time.time()

	input_file,ref,output_file,h = get_option()
	if str(h) == "":
		main(input_file, ref, output_file)
		print ("time: " + str (time.time()-time_start))
		print ("############################################ end #############################################")
	else:
		print (h)
