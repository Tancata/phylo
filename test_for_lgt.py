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

for leaf in tree:
    if re.search('Eukaryota', leaf.name):
        eukaryote_seqs.append(leaf.name)
    elif re.search(target_sequence_tag, leaf.name):
        eukaryote_seqs.append(leaf.name)
#print eukaryote_seqs
#test the various phylogenetic criteria for LGT.

#euk sequence is a singleton nested within a clade of bacteria, and there is only one eukaryote sequence in the tree
if len(eukaryote_seqs) == 1: #this is, I guess, an LGT candidate
    print sys.argv[1] + "\tSingleton"
#euk sequence is a singleton nested within a clade of bacteria, and the eukaryotes are not monophyletic in the tree
#print len(eukaryote_seqs)
else:
    try:
        if tree.check_monophyly(values=eukaryote_seqs, target_attr="name"):
            ca = tree.get_common_ancestor(eukaryote_seqs)
            print sys.argv[1] + "\tEuks monophyletic\t" + str(len(eukaryote_seqs)) + "\t" + str(ca.support) 
        else:
            print sys.argv[1] + "\tEuks not monophyletic" #this could, in itself, be a possible criterion for LGT --- or gene loss/transfer. Perhaps a condition that the target gene is not in the largest eukaryotic sub-clade (get_monophyletic() method will return subclades with a particular attribute that are monophyletic)
#If euks are monophyletic, what is the max. number allowed for the gene to be considered a candidate LGT?
#euk sequence is part of a euk clade nested within bacteria, and the eukaryotes are not monophyletic in the tree [what about the case where the LGT is the only copy in euks?]
#tree.render(out_tree)
    except:
        print sys.argv[1] + "\t" + "\tEuks not monophyletic\t" + str(len(eukaryote_seqs))
#uncomment the following to make a PDF of the tree
#tree.render(out_tree)
