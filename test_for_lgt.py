from ete3 import Tree
import sys, re

#read in the bootstrapped consensus tree from one of Cedric's families. Ask whether the candidate LGT has phylogenetic support at some bootstrap threshold by checking various tree-based criteria for LGTs

#Arguments: treefile target_sequence_tag


tree = Tree(sys.argv[1])
target_sequence_tag = sys.argv[2]

#setup a list of the eukaryotic sequences in the tree
eukaryote_seqs = []

for leaf in tree:
    if re.search('Eukaryota', leaf.name):
        eukaryote_seqs.append(leaf.name)
    elif re.search(target_sequence_tag, leaf.name):
        eukaryote_seqs.append(leaf.name)

#test the various phylogenetic criteria for LGT.

#euk sequence is a singleton nested within a clade of bacteria, and there is only one eukaryote sequence in the tree
#euk sequence is a singleton nested within a clade of bacteria, and the eukaryotes are not monophyletic in the tree
#euk sequence is part of a euk clade nested within bacteria, and the eukaryotes are not monophyletic in the tree [what about the case where the LGT is the only copy in euks?]

