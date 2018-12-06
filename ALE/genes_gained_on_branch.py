#input is two files with gene copy info per node (ancestor and descendant), output of gene_copies_per_node.py. This script will calculate the change in copy number per family along the intervening branch.
import os,re,sys

anc_file = sys.argv[1]
dec_file = sys.argv[2]
predicted_proteome_output_file = sys.argv[3]
gained_cutoff = float(sys.argv[4]) #maybe 1 is sensible.

if os.path.exists(predicted_proteome_output_file):
    os.unlink(predicted_proteome_output_file)

anc_copy_num = {} #key = gene family, value = copy number in ancestor
inh = open(anc_file)
for line in inh:
    if line.startswith("GeneFam") or line.startswith("Total"):
        continue
    else:
        fields = re.split("\t", line.rstrip())
        anc_copy_num[fields[0]] = float(fields[1])
inh.close()

total_change = 0
#now compare with the descendant node
print "GeneFam\tChange"
dech = open(dec_file)
for line in dech:
    if line.startswith("GeneFam") or line.startswith("Total"):
        continue
    else:
        fields = re.split("\t", line.rstrip())
        if fields[0] in anc_copy_num:
            change = float(fields[1]) - anc_copy_num[fields[0]]
            print fields[0] + "\t" + str(change)
            representative_name = fields[0][:-3] + "_representative.fa"
            total_change += change
            if change >= gained_cutoff:
                os.system("cat ../medoid/" + representative_name + " | { cat; echo; } >> " + predicted_proteome_output_file)
        else:
            print "Some format error"
            print line.rstrip()
            quit()
print "Total change: " + str(total_change)
