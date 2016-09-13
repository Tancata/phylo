#!/usr/bin/env python
#given a tree and a number of taxa n, print the n taxa that maximize the representation of branch lengths on the tree. This is supposed to help with a question like "I want a subsampled representation of this 3,000 taxon tree which retains as much of the phylogenetic diversity as possible but contains only n taxa"
from Bio import Phylo
from collections import defaultdict
import sys

def tree_distances(t, tax): #calculate summed-branch length distances for all pairs of taxa on a tree
    distances = defaultdict(dict)
    smallest_dist = float(9999999)
    taxon_to_drop = ''
    for i in range(len(tax)-1):
        for j in range(len(tax)):
            new_dist = t.distance(tax[i],tax[j])
            if new_dist < smallest_dist:
                taxon_to_drop = tax[i] #can setup a more complex selection here, e.g. if have genome size or completness, could drop the least complete
                smallest_dist = new_dist
    return taxon_to_drop

#tree - first arg
#n - second arg

if len(sys.argv) < 2:
    print "Usage: subsample_tree_by_branchlengths.py NewickTreeFile NumToKeep"
    quit()
treefile = sys.argv[1]
taxa_to_keep = int(sys.argv[2])

tree = Phylo.read(sys.argv[1], "newick")
taxa = tree.get_terminals()

#calculate all distances, then drop taxa with the smallest distance repeatedly until remaining number of taxa is n.


#now do recursive drop
num_taxa = len(taxa)
while num_taxa > taxa_to_keep:
    #get smallest distance, and drop one of the two taxa according to some other property, maybe
    to_prune = tree_distances(tree, taxa)
    tree.prune(to_prune)
    taxa = tree.get_terminals()
    num_taxa = len(taxa)

for tip in taxa:
    print tip.name
Phylo.draw_ascii(tree)
