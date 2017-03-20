#Read in a tree and chop it in two on branches greater than some length, as long as there are 4+ sequences on the shorter end of the branch. usage: python script.py length_cutoff newick_tree
import sys
from ete3 import Tree

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


length_cutoff = float(sys.argv[1])

tree = Tree(sys.argv[2])

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

#Write out the results
counter = 0
for tree in trees_done:
    tree.write(outfile=sys.argv[2][:-4] + "_" + str(counter) + ".tre")
    counter += 1
