#from ALE reconciliations, extract the number of copies for each gene family at a specified node on the tree (supplied by a node number)
#python gene_copies_at_node.py reconciliation_file_dir node_number protein_outputfile anc_reconstruction_threshold(num copies) 
import re, os, sys

directory = sys.argv[1]
node = int(sys.argv[2])
predicted_proteome_output_file = sys.argv[3]
ancestral_threshold = float(sys.argv[4])
total_num_gene_copies = 0

if os.path.exists(predicted_proteome_output_file):
    os.unlink(predicted_proteome_output_file)

to_parse = [file for file in os.listdir(directory) if file.endswith("uml_rec")]
print "GeneFam\tCopies"
for file in to_parse:
    name_fields = re.split("_", file)
    fam_name = ''
    representative_name = ''
    if file.startswith("fix"):
        fam_name = name_fields[1] + ".fa"
        representative_name = name_fields[1] + "_representative.fa"
    else:
        fam_name = "small_" + name_fields[1] + ".fa"
        representative_name = "small_" + name_fields[1] + "_representative.fa"
    inh = open(directory + file)
    for line in inh:
        fields = re.split("\t", line.rstrip())
        if len(fields) > 1:
            if fields[0] == "S_internal_branch" and int(fields[1]) == node:
                print fam_name + "\t" + str(fields[-1])
                total_num_gene_copies += float(fields[-1])
                #if above the threshold for including in the node protein content reconstruction, do so now
                if float(fields[-1]) >= ancestral_threshold:
                    os.system("cat medoid/" + representative_name + " | { cat; echo; } >> " + predicted_proteome_output_file)

    inh.close()
print "Total gene copies at node: " + str(total_num_gene_copies)
