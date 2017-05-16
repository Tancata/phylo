#implement a Bayesian relative rates comparison
#obtain 95% credible intervals for branch lengths to particular taxa on the tree, from some common ancestor
#args: outgroup_textfile target_taxa_textfile treelist
import sys
from ete3 import Tree
from collections import defaultdict
from scipy import stats

outgroups = []
outg = open(sys.argv[1])
for line in outg:
    outgroups.append(line.rstrip())
outg.close()

target_taxa = []
tt = open(sys.argv[2])
for line in tt:
    target_taxa.append(line.rstrip())
tt.close()

#now read in a collection of trees, calc branch lengths over sample, summarise and print out
branch_lengths = defaultdict(list) #key = taxa, value = list of brlens
treefile = open(sys.argv[3])
for line in treefile:
    curr_tree = Tree(line.rstrip())
    root_node = curr_tree.get_common_ancestor(outgroups)
    if curr_tree != root_node:
        curr_tree.set_outgroup(root_node)
    print curr_tree
    #bundle = curr_tree.check_monophyly(values=outgroups,target_attr='name')
    #print bundle
    #if bundle[0] == False:
    #    continue
    #find common ancestor of the target taxa, and use this as the reference node for calculating branch lengths. This might not always be the measure you want!
    reference_node = curr_tree.get_common_ancestor(target_taxa)
    #if reference_node != curr_tree:
    #    curr_tree.set_outgroup(reference_node)
    #calc distance from root to each branch of interest
    for taxon in target_taxa:
        dist = curr_tree.get_distance(taxon, reference_node) 
        branch_lengths[taxon].append(dist)

#now compute the credible intervals of the branch length for each of the target taxa
for taxon in branch_lengths:
    mean, var, std = stats.bayes_mvs(branch_lengths[taxon], alpha=0.95)
    print taxon + "\t" + str(mean[0]) + "\t" + str(mean[1][0]) + "\t" + str(mean[1][1])
