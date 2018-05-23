from ete3 import Tree, TreeStyle
import sys, re

#read in the bootstrapped consensus tree from one of Cedric's families. Ask whether the candidate LGT has phylogenetic support at some bootstrap threshold by checking various tree-based criteria for LGTs

#Arguments: treefile target_sequence_tag

#euk_supergroups = ['Viridiplantae','Oxymonadida','Alveolata'] #add more...
euk_supergroups = []
inh = open("List_that_matters.txt")
for line in inh:
    euk_supergroups.append(line.rstrip())
inh.close()

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

#setup group assignments
group_assignments = {}

inh = open("Annotation_file_for_trees.txt")
for line in inh:
    fields = re.split("\s+", line.rstrip())
    if len(fields) >= 2:
        group_assignments[fields[0]] = fields[1] #key = sequence ID, value = group assignment (e.g. Viridiplantae)

#setup a list of the eukaryotic sequences in the tree
eukaryote_seqs = []
target_leaf = ''
for node in tree:
    node.add_features(domain="Other")
for leaf in tree:
    if re.search(target_sequence_tag, leaf.name):
        leaf.add_features(domain="Eukaryote")
        eukaryote_seqs.append(leaf.name)
        target_leaf = leaf
    elif leaf.name in group_assignments:
        if group_assignments[leaf.name] in euk_supergroups:
            eukaryote_seqs.append(leaf.name)
            leaf.add_features(domain="Eukaryote")
        else:
            leaf.add_features(domain="Other")
    else:
        leaf.add_features(domain="Other")
#print eukaryote_seqs


#root the tree on a clade (the biggest?) of bacteria, to avoid ridiculous problems with arbitrary roots on trees
biggest_other_node = 0
for node in tree.get_monophyletic(values=['Other'], target_attr="domain"):
    if len(node) > biggest_other_node:
        biggest_other_node = len(node)
        tree.set_outgroup(node) 
#test the various phylogenetic criteria for LGT.

print "Tree\tResult\tEuksInTree\tSupportEukMonophyly\tEuksInTargetGroup\tDistanceToClosestEukClade\tSupergroupsInTargetGroup"
#euk sequence is a singleton nested within a clade of bacteria, and there is only one eukaryote sequence in the tree
if len(eukaryote_seqs) == 1: #this is, I guess, an LGT candidate
    print sys.argv[1] + "\tSingleton\t1\tN/A\tN/A\tN/A\t1"
#euk sequence is a singleton nested within a clade of bacteria, and the eukaryotes are not monophyletic in the tree
#print len(eukaryote_seqs)
else:
    try:
        answer = tree.check_monophyly(values=eukaryote_seqs, target_attr="name")
        if answer[0] == True:
            ca = tree.get_common_ancestor(eukaryote_seqs)
            target_group_sgs = {}
            for leaf in ca:
                if leaf.name in group_assignments:
                    leaf_supergroup = group_assignments[leaf.name]
                    if leaf_supergroup in euk_supergroups:
                        target_group_sgs[leaf_supergroup] = 1
                else:
                    print "Warning: a sequence in this tree doesn't have a supergroup assignment: " + str(leaf.name)
            num_sgs = len(target_group_sgs.keys())
            print sys.argv[1] + "\tEuks monophyletic\t" + str(len(eukaryote_seqs)) + "\t" + str(ca.support) + "\tN/A\tN/A\t" + str(num_sgs) 
        elif answer[0] == False:
            mono_groups = []
            target_group = ''
            for node in tree.get_monophyletic(values=['Eukaryote'], target_attr="domain"):
                for leaf in node:
                    if leaf.name == target_leaf.name:
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
            #find out what supergroups of eukaryotes are represented in the target group
            target_group_sgs = {}
            tg_names = []
            for leaf in target_group:
                tg_names.append(leaf.name)
                if leaf.name in group_assignments:
                    leaf_supergroup = group_assignments[leaf.name]
                    if leaf_supergroup in euk_supergroups:
                        target_group_sgs[leaf_supergroup] = 1
                else:
                    print "Warning: a sequence in this tree doesn't have a supergroup assignment: " + str(leaf.name)
            num_sgs = len(target_group_sgs.keys())
            print tg_names
            c_a = tree.get_common_ancestor(tg_names)
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
            print sys.argv[1] + "\tEuks not monophyletic\t" + str(len(eukaryote_seqs)) + "\t" + str(c_a.support) + "\t" + str(size_target_group) + "\t" + str(shortest_distance) + "\t" + str(num_sgs) 
        else:
            print sys.argv[1] + "\t" + answer[0]
#If euks are monophyletic, what is the max. number allowed for the gene to be considered a candidate LGT?
#euk sequence is part of a euk clade nested within bacteria, and the eukaryotes are not monophyletic in the tree [what about the case where the LGT is the only copy in euks?]
#tree.render(out_tree)
    except:
        raise
#uncomment the following to make a PDF of the tree
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True
ts.show_branch_length = False
tree.render(out_tree, tree_style=ts)
