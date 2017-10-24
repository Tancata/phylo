from ete3 import Tree, NodeStyle, TreeStyle
import sys, re

#Visualise trees programmatically for Cedric's project
#python annotate_tree_figures.py NewickTree

#It's also possible to have this script produce a PDF of the tree programmatically, without the interactive part

inh = open(sys.argv[1])
treestring = inh.readline()
treestr = treestring.replace(';','')
treestr = treestr + ";" 
inh.close()

if len(treestr) == 0:
    print sys.argv[1] + "\tEmpty tree"
    quit()

t = Tree(treestr)

#define basic tree style

ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True

#for n in t.traverse()
#    if n.is_leaf():

#Here, we set up the annotations we want on the tree. For example, let's make the leaves with eukaryote sequences large red balls.
for leaf in t.get_leaves():
    if re.search('Eukaryota', leaf.name):
        leaf_style = NodeStyle()
        leaf_style["fgcolor"] = "red"
        leaf_style["size"] = 15
        leaf.set_style(leaf_style)
t.show(tree_style=ts)
