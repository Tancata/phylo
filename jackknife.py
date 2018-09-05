from Bio import AlignIO
import sys
import random

align = AlignIO.read(sys.argv[1], "fasta")

alignment_length = len(str(align[0].seq))

num_taxa = len(align)

picked_sites = []
desired_site_num = int(sys.argv[2]) #number of sampled sites (without replacement) desired in the output alignment

while(len(picked_sites) < desired_site_num):
#pick a site number, then add it to some list to slice
    site_index = random.randint(0,alignment_length)
    if site_index in picked_sites:
        continue
    else:
        picked_sites.append(site_index)

#make a subset alignment
for i in range(num_taxa):
    new_seq = ''
    print ">" + str(align[i].description)
    for site in picked_sites:
        new_seq += str(align[i].seq)[site]
    print new_seq
