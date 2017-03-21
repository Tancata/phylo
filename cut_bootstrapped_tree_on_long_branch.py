#Read in a ufboot file and chop each tree on internal branches greater than some length, as long as there are 4+ sequences on the shorter end of the branch. usage: python script.py length_cutoff newick_tree
#addition: have some store of tree bits; after chopping a new tree, compare the bits to the existing store of bits to see if any are entirely compatible, and if so, add them to "that" list; at end, print out each list as a separate ufboot-derived file
import sys
from ete3 import Tree
from collections import defaultdict

def bissect_tree(treeObj):
    subtree1 = ''
    subtree2 = ''
    for node in treeObj.traverse("postorder"):
        if node.dist > length_cutoff: #split the tree here
            if node.is_leaf():
                continue
            elif len(node) < 4: #edit this to change the minimum number of sequences in the smaller subtree
                continue
            else:
                subtree1 = node.detach()
                subtree2 = treeObj
                return (subtree1, subtree2)
    return (treeObj, 'Zilch')

def get_leaf_names(treeObj):
    names = []
    for leaf in treeObj:
        names.append(leaf.name)
    return names

length_cutoff = float(sys.argv[1])

#tree = Tree(sys.argv[2])

tree_bits = [] #holds the contents of the ufboot-esque files to print out at end

ufbootfile = open(sys.argv[2])
count_lines = 0
for line in ufbootfile:
    count_lines += 1
    tree = Tree(line.rstrip())
    trees_done = []
    trees_todo = []
    trees_todo.append(tree)
    while len(trees_todo) > 0:
        (s1, s2) = bissect_tree(trees_todo.pop())
        if s2 == 'Zilch': #no problem branches
            trees_done.append(s1)
        else:
            trees_done.append(s1) #This relies on postorder and levelorder (gradually go deeper into tree), to prevent an infinite loop when cutting
            trees_todo.append(s2)
    if len(tree_bits) == 0: #first bootstrap, so just write the bits
        for t in trees_done:
            tree_bits.append([t])
    else:
        #check to see if compatible with existing tree bits from earlier bootstraps
        for t in trees_done:
            matched = 0
            tree_names = get_leaf_names(t)
            #for element in tree_bits:
            for i in range(len(tree_bits)):
                element_taxa = get_leaf_names(tree_bits[i][0])
                if set(tree_names) == set(element_taxa): #they are compatible
                    tree_bits[i].append(t)
                    matched = 1
            if matched == 0:
                tree_bits.append([t])

#Write out the results
counter = 0
#for tree in trees_done:
#    tree.write(outfile=sys.argv[2][:-4] + "_" + str(counter) + ".tre")
#    counter += 1

for trees in tree_bits:
    outfile_name = sys.argv[2][:-7] + "_" + str(counter) + ".boot"
    counter += 1
    outh = open(outfile_name, "w")
    for t in trees:
        outh.write(t.write() + "\n")
    outh.close()
