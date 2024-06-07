#from ALE reconciliations, extract the number of copies for each gene family at a specified node on the tree (supplied by a node number)
#python gene_copies_at_node.py reconciliation_file_dir node_number
import re, os, sys

directory = sys.argv[1]
node = int(sys.argv[2])
total_num_gene_copies = 0

to_parse = [file for file in os.listdir(directory) if file.endswith("uml_rec")]
print "GeneFam\tCopies"
for file in to_parse:
    inh = open(directory + file)
    for line in inh:
        fields = re.split("\t", line.rstrip())
        if len(fields) > 1:
            if fields[0] == "S_internal_branch" and int(fields[1]) == node:
                print fam_name + "\t" + str(fields[-1])
                total_num_gene_copies += float(fields[-1])
    inh.close()
print "Total gene copies at node: " + str(total_num_gene_copies)
