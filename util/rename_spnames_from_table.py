#rename the tip names in a Newick tree based on a tab-delimited file linking name codes to full names
from ete3 import Tree
import re, sys

#arg1 - tree file
#arg2 - names mapping file 
#arg3 - output file with renamed Newick tree

names = {}

tree = Tree(sys.argv[1]) #Newick tree

#read in a tab-delimited species names file
tblfile = open(sys.argv[2])
for line in tblfile:
    fields = re.split("\t", line.rstrip())
    names[fields[0]] = fields[1]

for leaf in tree:
    if leaf.name in names:
        leaf.name = names[leaf.name]

tree.write(outfile=sys.argv[3])
