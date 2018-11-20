import os, re, sys

fams = {}

#read in the output of EggNOG mapper, then make protein families out of sequences which map to the same set of COG/KOG functional categories
inh = open("Para_sacc.fasta.emapper.annotations")
for line in inh:
    fields = re.split("\t", line.rstrip())
    #print fields[-4]
    cogs = re.split(",", fields[-4])
    for fam_id in cogs:
        bits = re.split("@", fam_id)
        if bits[0] in fams:
            fams[bits[0]].add(fields[0])
        else:
            fams[bits[0]] = {fields[0]}

all_keys = fams.keys()
setlist = []
#now loop over all of the COG/KOG/whatever IDs in the fam dictionary, and merge their sets if the sets have any common elements (sequences)
for key in fams.keys():
    setlist.append(fams[key])
merged = True
while merged:
    merged = False
    results = []
    while setlist:
        common, rest = setlist[0], setlist[1:]
        setlist = []
        for x in rest:
            if x.isdisjoint(common):
                setlist.append(x)
            else:
                merged = True
                common |= x
        results.append(common)
    setlist = results

groupnum = 0 #arbitrary numbering for the gene families
for element in setlist:
    groupnum += 1
    for seq in element:
        print str(groupnum) + "\t" + seq
