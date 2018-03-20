from __future__ import absolute_import, division, print_function
from ete3 import Tree
import sys

#read in a rooted treelist, print out a .trees file that RootAnnotator might (?) like
trees = []

inh = open(sys.argv[1])
for line in inh:
    ct = Tree(line.rstrip())    
    trees.append(ct)
inh.close()

leaf_names = []

for leaf in trees[0]:
    leaf_names.append(leaf.name)

num_taxa = str(len(leaf_names))

leaf_map = {}
index = 0

for element in leaf_names:
    index += 1
    leaf_map[element] = str(index)


#now print some basic guff
print('#NEXUS\n\nBegin taxa\n\tDimensions ntax=' + num_taxa + ';\n\tTaxlabels')
for taxon in leaf_names:
    print('\t\t' + taxon)
print('\t\t;\nEnd;\n\nBegin trees;\n\tTranslate')

for taxon in leaf_names:
    if taxon == leaf_names[-1]:
        print('\t\t' + leaf_map[taxon] + ' ' + taxon)
    else:
        print('\t\t' + leaf_map[taxon] + ' ' + taxon + ',')
print('\t\t;')

tree_count = 0
for t in trees:
    tree_count += 1
    for leaf in t:
        leaf.name = leaf_map[leaf.name]
    print('tree ' + str(tree_count) + ' = ' + str(t.write()))
print('End;')
