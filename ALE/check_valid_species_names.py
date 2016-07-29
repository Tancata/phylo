#validate gene tree names against the species tree and flag up any discrepencies.
#usage: python check_valid_species_names.py species_tree genetreedir/

from Bio import Phylo
import os, sys, re

spnames = []
odd_names = {}

sptree = Phylo.read(sys.argv[1], "newick")
for taxa in sptree.get_terminals():
    spnames.append(taxa.name)

#now scan gene trees for any unexpected species names
to_check = [file for file in os.listdir(sys.argv[2]) if file.endswith("ufboot")]
for file in to_check:
    trees = Phylo.parse(sys.argv[2] + file, "newick")
    for t in trees:
        for tip in t.get_terminals():
            fields = re.split("_", tip.name)
            if fields[0] in spnames:
                continue
            else:
                odd_names[fields[0]] = 1

for element in odd_names.keys():
    print element
