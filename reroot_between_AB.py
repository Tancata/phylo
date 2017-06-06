from ete3 import Tree
import sys, re

#read in mapping of IDs to domain (Bacteria or Archaea)
id_to_domain = {}
f = open("outputfileABlist")
for line in f:
	if line.startswith("Species"):
		continue
	else:
		fields = re.split(",", line.rstrip())
		id_to_domain[fields[1]] = fields[2]
f.close()

tree = Tree(sys.argv[1])
print tree

archaea = [] #make a list of archaea that are in the tree
bacteria = []
#check the domain of each taxon in the tree
for taxon in tree:
	print taxon.name + "\t" + id_to_domain[taxon.name]
	if id_to_domain[taxon.name] == 'Archaea':
		archaea.append(taxon.name)
	else:
		bacteria.append(taxon.name)

#first, check if archaea are monophyletic in the tree

if tree.check_monophyly(values=archaea, target_attr="name")[0] == True:

	#find the branch separating archaea and bacteria, and reroot the tree on that
	archaea_ancestor = tree.get_common_ancestor(archaea) 
	tree.set_outgroup(archaea_ancestor)
elif tree.check_monophyly(values=bacteria, target_attr="name")[0] == True:
	bacteria_ancestor = tree.get_common_ancestor(bacteria)
	tree.set_outgroup(bacteria_ancestor)
else:
	#neither archaea nor bacteria were monophyletic, so print some error and quit
	print sys.argv[1] + ": neither A nor B monophyletic."
	quit()

outfile_name = sys.argv[1] + "_rerooted"
tree.write(outfile=outfile_name)

