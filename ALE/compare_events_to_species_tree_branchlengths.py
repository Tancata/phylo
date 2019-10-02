#compare branch lengths on species tree to inferred events (per gene copy) --- read a species tree with branch lengths and a set of uml_rec files

import os, re, sys, glob
from collections import defaultdict
import numpy as np
import scipy 
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd

per_branch_rates = defaultdict(dict) #keys will be each of the rate types, and the branch length
tree_ALE = sys.argv[1]
tree_branch_lengths = sys.argv[2]


def get_branch_lengths_by_label(tree_newick,tree_ALE):
#map branch labels to branch lengths
#get labels in order from ALE tree
	branches = {} #key = label, value = length
	inh = open(tree_ALE)
	ale_tree = inh.readline()
	labels = re.findall('[\w0-9]+\:', ale_tree)		
	inh.close()
	inh = open(tree_newick)
	newick = inh.readline()	
	brlens = re.findall(':[0-9\.]+', newick)
	for i in range(len(labels)):
		branches[labels[i][:-1]] = brlens[i][1:]	
	return branches

branches = get_branch_lengths_by_label(tree_branch_lengths,tree_ALE)

#recfiles = [file for file in os.listdir(".") if file.endswith(".ale.uml_rec")]
recfiles = glob.glob("R1_Miss_uml_rec/*ale.uml_rec")
for file in recfiles:
	inh = open(file)
	for line in inh:
		if line.startswith("S_"):
			bits = re.split("\t", line.rstrip())
			branch_label = bits[1]
			gene_copies = float(bits[-1])
			if gene_copies > 0.0:
				dup_rate = float(bits[2])/gene_copies
				transfer_rate = float(bits[3])/gene_copies
				loss_rate = float(bits[4])/gene_copies
				origination_rate = float(bits[5])/gene_copies
				if 'duplication_rate' in per_branch_rates[branch_label]:
					per_branch_rates[branch_label]['duplication_rate'].append(dup_rate)
				else:
					per_branch_rates[branch_label]['duplication_rate'] = [dup_rate]
				if 'loss_rate' in per_branch_rates[branch_label]:
					per_branch_rates[branch_label]['loss_rate'].append(loss_rate)
				else:
					per_branch_rates[branch_label]['loss_rate'] = [loss_rate]
				if 'transfer_rate' in per_branch_rates[branch_label]:
					per_branch_rates[branch_label]['transfer_rate'].append(transfer_rate)
				else:
					per_branch_rates[branch_label]['transfer_rate'] = [transfer_rate]
				if 'origination_rate' in per_branch_rates[branch_label]:
					per_branch_rates[branch_label]['origination_rate'].append(origination_rate)
				else:
					per_branch_rates[branch_label]['origination_rate'] = [origination_rate]
xvals = []
yvals = []
parameter = []
for branch in per_branch_rates:
	#print branch
	#print branches[branch]
	#print per_branch_rates[branch]
	for value in per_branch_rates[branch]['duplication_rate']:
		if branch in branches:
			xvals.append(float(branches[branch]))
			yvals.append(value)
			parameter.append('Duplications')
	for value in per_branch_rates[branch]['transfer_rate']:
		if branch in branches:
			xvals.append(float(branches[branch]))
			yvals.append(value)
			parameter.append('Transfers')
	for value in per_branch_rates[branch]['loss_rate']:
		if branch in branches:
			xvals.append(float(branches[branch]))
			yvals.append(value)
			parameter.append('Losses')
	for value in per_branch_rates[branch]['origination_rate']:
		if branch in branches:
			xvals.append(float(branches[branch]))
			yvals.append(value)
			parameter.append('Originations')
#plotting
df = pd.DataFrame()
df['x'] = np.array(xvals)
df['y'] = np.array(yvals)
df['parameter'] = np.array(parameter)

snsplot = sns.lmplot(x='x', y='y', hue='parameter', col='parameter', data=df, x_estimator=np.mean, sharey=False)
#fig = snsplot.get_figure()
snsplot.savefig("dup_plot.png")

#correlations
dup_df = df.loc[df['parameter']=='Duplications']
trans_df = df.loc[df['parameter']=='Transfers']
loss_df = df.loc[df['parameter']=='Losses']
ori_df = df.loc[df['parameter']=='Originations']
print scipy.stats.pearsonr(dup_df['x'],dup_df['y'])
print scipy.stats.pearsonr(trans_df['x'],trans_df['y'])
print scipy.stats.pearsonr(loss_df['x'],loss_df['y'])
print scipy.stats.pearsonr(ori_df['x'],ori_df['y'])
