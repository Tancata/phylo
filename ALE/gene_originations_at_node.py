#from ALE reconciliations, print a list of gene fams originating at a node with P > 0.5.
#python gene_copies_at_node.py reconciliation_file_dir node_number protein_outputfile 
import re, os, sys

directory = sys.argv[1]
node = int(sys.argv[2])
predicted_proteome_output_file = sys.argv[3]
ancestral_threshold = 0.5
total_num_gene_originations = 0

if os.path.exists(predicted_proteome_output_file):
    os.unlink(predicted_proteome_output_file)

to_parse = [file for file in os.listdir(directory) if file.endswith("uml_rec")]
print "GeneFam\tCopies"
for file in to_parse:
    name_fields = re.split("faa", file)
    fam_name = ''
    representative_name = ''
    fam_name = name_fields[0] + "faa"
    representative_name = name_fields[0] + "_representative.fa"
    inh = open(directory + file)
    for line in inh:
        fields = re.split("\t", line.rstrip())
        if len(fields) > 1:
            if fields[0] == "S_internal_branch" and int(fields[1]) == node:
                print fam_name + "\t" + str(fields[-2])
                total_num_gene_originations += float(fields[-2])
                #if above the threshold for including in the node protein content reconstruction, do so now
                if float(fields[-2]) > ancestral_threshold:
                    os.system("cat medoid/" + representative_name + " | { cat; echo; } >> " + predicted_proteome_output_file)

    inh.close()
print "Total gene originations at node: " + str(total_num_gene_originations)
