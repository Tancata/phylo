from ete3 import Tree
import sys

tree = Tree(sys.argv[1])
centroid_tips = []
reference_tips = []
for leaf in tree:
    if leaf.name.startswith("centroid"):
        centroid_tips.append(leaf.name)
    else:
        reference_tips.append(leaf.name)
#print("CENTROIDS:")
#print(centroid_tips)
#print("REFERENCES:")
#print(reference_tips)

#run the algorithm once per tip. Inefficient...
for tipname in centroid_tips:
    to_keep = []
    to_keep.extend(reference_tips)
    to_keep.append(tipname)
    #print("TO KEEP:")
    #print(to_keep)
    this_tree = tree.copy()
    pruned_tree = this_tree.prune(to_keep)
    #print(this_tree.write())
    target_node = this_tree.get_leaves_by_name(tipname)[0] #assumes the names of the tips are unique.
    sisters = target_node.get_sisters()
    print(target_node.name + "\t" + sisters[0].name) #looks at just the 0th sister

