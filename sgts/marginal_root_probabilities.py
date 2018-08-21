from __future__ import absolute_import, division, print_function
from ete3 import Tree
import sys
import operator

#read in a rooted treelist, print out a table of the most probable root splits and their probabilities
trees = []
inh = open(sys.argv[1])
for line in inh:
    ct = Tree(line.rstrip())    
    trees.append(ct)
inh.close()
num_trees = len(trees)

leaf_names = []

for leaf in trees[0]:
    leaf_names.append(leaf.name)

num_taxa = str(len(leaf_names))
roots = [] #a list of sets...hmm
for t in trees:
    #get the taxa on either side of the root node
    sides = t.get_children()
    side1 = set()
    side2 = set()
    the_other = []
    for leaf in sides[0]:
        side1.add(leaf.name)
#        print("Side0\t" + str(leaf.name))
    for leaf in sides[1]:
        side2.add(leaf.name)
#        print("Side1\t" + str(leaf.name))
    if len(side1) <= len(side2): #use the smaller set as the label for this root position
        roots.append(side1)
    else:
        roots.append(side2)

root_probs = {}
#now count how many times each unique set occurs
#get unique sets
unique_roots = set(frozenset(i) for i in roots)
print(len(unique_roots))
print(unique_roots)
for root in unique_roots:
    sampled = 0
    for rset in roots:
        if root == rset:
            sampled += 1
    root_probs[root] = sampled
sorted_root_probs = sorted(root_probs.items(), key=operator.itemgetter(1), reverse = True)
for element in sorted_root_probs:
    print(str(element[0]) + "\t" + str(float(element[1])/float(num_trees)))
