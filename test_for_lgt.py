from ete3 import Tree
import sys, re

#read in the bootstrapped consensus tree from one of Cedric's families. Ask whether the candidate LGT has phylogenetic support at some bootstrap threshold by checking various tree-based criteria for LGTs

#Arguments: treefile target_sequence_tag

#check tree string for sanity first
inh = open(sys.argv[1])
treestring = inh.readline()
treestr = treestring.replace(';','')
treestr = treestr + ";"
inh.close()

if len(treestr) == 0:
    print sys.argv[1] + "\tEmpty tree"
    quit()

tree = Tree(treestr)
out_tree = sys.argv[1] + ".pdf"
#target_sequence_tag = sys.argv[2]
target_sequence_tag = 'xxx'

#setup a list of the eukaryotic sequences in the tree
eukaryote_seqs = []
target_leaf = ''
for node in tree:
    node.add_features(domain="Other")
for leaf in tree:
    if re.search('Eukaryota', leaf.name):
        eukaryote_seqs.append(leaf.name)
        leaf.add_features(domain="Eukaryote")
    elif re.search(target_sequence_tag, leaf.name):
        leaf.add_features(domain="Eukaryote")
        eukaryote_seqs.append(leaf.name)
        target_leaf = leaf
    else:
        leaf.add_features(domain="Other")
#print eukaryote_seqs
#test the various phylogenetic criteria for LGT.

#euk sequence is a singleton nested within a clade of bacteria, and there is only one eukaryote sequence in the tree
if len(eukaryote_seqs) == 1: #this is, I guess, an LGT candidate
    print sys.argv[1] + "\tSingleton"
#euk sequence is a singleton nested within a clade of bacteria, and the eukaryotes are not monophyletic in the tree
#print len(eukaryote_seqs)
else:
    try:
        answer = tree.check_monophyly(values=eukaryote_seqs, target_attr="name")
        if answer[0] == True:
            ca = tree.get_common_ancestor(eukaryote_seqs)
            print sys.argv[1] + "\tEuks monophyletic\t" + str(len(eukaryote_seqs)) + "\t" + str(ca.support) 
        elif answer[0] == False:
            mono_groups = []
            target_group = ''
            for node in tree.get_monophyletic(values=['Eukaryote'], target_attr="domain"):
                if target_leaf in node:
                    target_group = node
                else:
                    mono_groups.append(node)
            size_target_group = len(target_group)
            #get distance
            shortest_distance = 999999999999999.0
            closest_other_group = ''
            for subtree in mono_groups:
                curr_distance = tree.get_distance(target_group, subtree, topology_only=True)
                if curr_distance < shortest_distance:
                    shortest_distance = curr_distance
                    closest_other_group = subtree
            #attempt to calculate distance on a version of the tree in which branches below some support threshold have been deleted
#            closest_leaves = []
 #           for leaf in closest_other_group:
  #              closest_leaves.append(leaf.name)
   #         target_leaves = []
    #        for leaf in target_group:
     #           target_leaves.append(leaf.name)
      #      collapsed_tree = tree
       #     for node in collapsed_tree:
        #        if node.support < 0.5:
         #           node.delete()
          #  target_ca = collapsed_tree.get_common_ancestor(target_leaves)
           # closest_ca = collapsed_tree.get_common_ancestor(closest_leaves)
         #   collapsed_distance = collapsed_tree.get_distance(target_ca, closest_ca, topology_only=True)
            print sys.argv[1] + "\tEuks not monophyletic\t" + str(len(eukaryote_seqs)) + "\t" + str(size_target_group) + "\t" + str(shortest_distance) 
        else:
            print sys.argv[1] + "\t" + answer[0]
#If euks are monophyletic, what is the max. number allowed for the gene to be considered a candidate LGT?
#euk sequence is part of a euk clade nested within bacteria, and the eukaryotes are not monophyletic in the tree [what about the case where the LGT is the only copy in euks?]
#tree.render(out_tree)
    except:
        raise
#uncomment the following to make a PDF of the tree
tree.render(out_tree)
