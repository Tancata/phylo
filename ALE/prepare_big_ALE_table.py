import re, os, sys, glob

roots = []
aln_lengths = {}
#.ufboot.ale.uml_rec
def get_aln_length(recfile):
	alnfile = recfile[:-19]
	inh = open(alnfile) #needs to be modified to reflect where they are
	aln = inh.readlines()
	inh.close()
	aln_length = len(aln[1])
	aln_lengths[recfile] = aln_length


to_parse = glob.glob("*/*uml_rec")
for file in to_parse:
	name_bits = re.split("\/", file.rstrip())
	genefam = name_bits[1].rstrip()
	alen = "NA"
	if genefam in aln_lengths:
		alen = aln_lengths[genefam]
	else:
		get_aln_length(genefam)
		alen = aln_lengths[genefam]

	logl = "NA"
	dups = "NA"
	transfers = "NA"
	losses = "NA"
	speciations = "NA"
	copies_at_tips = 0
	species_with_copies = 0
	#parse relevant data from the uml_rec file
	inh = open(file)
	for line in inh:
		if line.startswith(">logl"):
			logl = line.split()[-1]
		if line.startswith("Total"):
			fields = re.split("\t", line.rstrip())
			dups = float(fields[1])
			transfers = float(fields[2])
			losses = float(fields[3])
			speciations = float(fields[4])
		if line.startswith("S_terminal"):
			fields = re.split("\t", line.rstrip())
			copy = float(fields[-1])
			if copy > 0.0:
				species_with_copies += 1
			copies_at_tips += copy
	print genefam + "\t" + name_bits[0] + "\t" + "logl\t" + str(logl)
	print genefam + "\t" + name_bits[0] + "\t" + "duplications\t" + str(dups)
	print genefam + "\t" + name_bits[0] + "\t" + "transfers\t" + str(transfers)
	print genefam + "\t" + name_bits[0] + "\t" + "losses\t" + str(losses)
	print genefam + "\t" + name_bits[0] + "\t" + "speciations\t" + str(speciations)
	print genefam + "\t" + name_bits[0] + "\t" + "copies_at_tips\t" + str(copies_at_tips)
	print genefam + "\t" + name_bits[0] + "\t" + "species_with_copies\t" + str(species_with_copies)
	print genefam + "\t" + name_bits[0] + "\t" + "alignment_length\t" + str(alen)
			
