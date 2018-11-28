#given two concatenates, find the shared markers using the reciprocal best hit criterion
#arguments: dir1 dir2
import os, sys, re

def get_best_hits(directory, tag):
    to_read = [file for file in os.listdir(directory) if file.endswith(tag + ".txt")]
    for file in to_read:
        sig_hits = {}
        best_hit = "first"
        inh = open(file) #HMMer tblout
        for line in inh:
            if line.startswith("#"):
                continue
            else:
                fields = re.split("\t", line)
                if float(fields[4]) < 0.00001: #evalue cutoff for a significant hit
                    if best_hit == "first": #this is the first (best) hit
                        name_bits = re.split("_", fields[0])
                        best_hit = name_bits[1] #the gene ID from the other concatenate that matches
                        sig_hits[best_hit] = float(fields[4])
                    else:
                        name_bits = re.split("_", fields[0])
                        if name_bits[1] in sig_hits:
                            continue
                        else:
                            sig_hits[name_bits[1]] = float(fields[4])
        if len(sig_hits.keys()) == 0:
            #no hits
        elif len(sig_hits.keys()) == 1:
            #one unambiguous best hit
        else:
            #decide whether we can pick one, e.g. if one has evalue 10x better

dir1 = sys.argv[1]
dir2 = sys.argv[2]
tag1 = sys.argv[3] #the indicator for the hits against the other concatenate, e.g. "29cw"
tag2 = sys.argv[4]


c1_besthits = {}
c2_besthits = {}
recip_hits = {}

c1_besthits = get_best_hits(dir1, tag2)
c2_besthits = get_best_hits(dir2, tag1)
