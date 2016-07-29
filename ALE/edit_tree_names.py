from Bio import Phylo
import os

to_edit = [file for file in os.listdir("trimmed/") if file.endswith("ufboot")]
for tree_f in to_edit:
    edited_trees = []
    trees = Phylo.parse("trimmed/" + tree_f, "newick")
    for tree in trees:
        for tip in tree.get_terminals():
            if tip.name.startswith("gnl"):
                tip.name = tip.name[4:]
        edited_trees.append(tree)
    Phylo.write(edited_trees, "edited_names/" + tree_f, "newick")
