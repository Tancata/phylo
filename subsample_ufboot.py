#subsample an UFBoot, printing out bootstrap trees that preserve tree length (where possible) while containing only some target subset of the taxa

import sys, re
from ete3 import Tree

target_subset = ['Species1', 'Species2'] #create a list of the species that need to be printed out

inh = open(sys.argv[1])
for line in inh:
	current_tree = Tree(line.rstrip())
	tips_to_keep = []
	for tip in current_tree:
		tip_sp = re.split("_", tip.name) #keep all seqs from the species of interest
		if tip_sp[0] in target_subset:
			tips_to_keep.append(tip.name)		
	current_tree.prune(tips_to_keep, preserve_branch_length=True)
	print current_tree.write()
