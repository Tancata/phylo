from __future__ import print_function
import sys, re, numpy
from collections import defaultdict
from operator import itemgetter
from ete3 import Tree

#usage: python count_sister_taxa.py bootstrapFile outputFile

def map_species_to_cluster(cluster_file): #make a dict that links species name to the cluster to use for group compariosns
    spname_to_cluster = {}
    inh = open(cluster_file)
    for line in inh:
        if line.startswith("Names"):
            continue
        elements = re.split("\t", line)
        e2 = re.split("\|", elements[1])
        species = e2[-2]
        cluster = e2[0]
        spname_to_cluster[species] = cluster
    return spname_to_cluster

def parse_taxonomy(taxon_name): #given a taxon name, try to return whatever taxonomic info is available as a list starting with the highest level classification and going lower (or a map?)
    name_elements = re.split("\|", taxon_name)
    if (len(name_elements) < 8) or (len(name_elements) > 9):
        print(name_elements)
        print("Nonstandard!")
        quit()
    name_map = {}
    name_map['cluster'] = name_elements[0]
    name_map['domain'] = name_elements[1]
    name_map['phylum'] = name_elements[2]
    name_map['class'] = name_elements[3]
    name_map['order'] = name_elements[4]
    name_map['family'] = name_elements[5]
    name_map['genus'] = name_elements[6]
    name_map['species'] = name_elements[7]
    if len(name_elements) == 9:
        name_map['ncbi_id'] = name_elements[8]
    return name_map

def summarize_taxonomy(name_list, tax_level): #take a list of names from a clade and summarize taxonomic info (labels and their frequencies)
    total_size = len(name_list) #it perhaps makes sense to normalize by the size of the clade
    breakdown = {}
    for name in name_list:
        info = name_to_tax_info[name]
        if info[tax_level] in breakdown:
            breakdown[info[tax_level]] += 1.0 / float(total_size)
        else:
            breakdown[info[tax_level]] = 1.0 / float(total_size)
    return breakdown

#compute the most frequent sister group of each (monophyletic?) group on the tree, to identify trends in gene transfers, "unstable" taxa, etc.
labels = {}
name_to_tax_info = defaultdict(dict)
taxa_names = []
summary = defaultdict(dict)
groups = []
clades_per_group = defaultdict(list)

target_label = 'cluster' #edit this to make the comparisons at a desired taxonomic level

#clusters = map_species_to_cluster("names_to-replace3.txt") #should just be baked into the tree names now, as first element

treeNum = -1
tree_sample_handle = open(sys.argv[1])
for line in tree_sample_handle:
    treeNum += 1
    tree = Tree(line.rstrip())
    if len(taxa_names) == 0: #it's the first tree, so set up some things
        for leaf in tree:
            taxonomy = parse_taxonomy(leaf.name)
            name_to_tax_info[leaf.name] = taxonomy
            taxa_names.append(leaf.name)
            leaf.add_feature("tax", taxonomy[target_label]) #this adds a feature called tax to the leaf, with the attribute of the phylum name
            labels[taxonomy[target_label]] = 1 
        groups = labels.keys()
    else:
        for leaf in tree:
            leaf.add_feature("tax", taxonomy[target_label]) #this adds a feature called tax to the leaf, with the attribute of the phylum name
    for label in groups:
        clades_per_group[label].append(0.0) #setup the clade counting for this particular tree
    tree.unroot() 
    
#iterate over groups that are monophyletic for the taxon label of choice. Choose the smallest sister branch for the comparison. (Assume root is within the larger sister clade)
    for label in groups:
        #print label
        for node in tree.get_monophyletic(values=[label], target_attr="tax"):
            clades_per_group[label][treeNum] += 1.0 
            #print node.get_ascii()
            sisters = node.get_sisters()
            if node.is_root():
                continue
            elif len(sisters) == 1: #not at the trifurcation. Do something a bit hacky to find the bigger sister clade
                taxa_in_OG = []
                taxa_in_sister = []
                taxa_in_group = []
                for leaf in sisters[0]:
                    taxa_in_sister.append(leaf.name)
                for leaf in node:
                    taxa_in_group.append(leaf.name)
                size_sister = len(taxa_in_sister)
                for leaf_name in taxa_names:
                    if leaf_name in taxa_in_sister:
                        continue
                    elif leaf_name in taxa_in_group:
                        continue
                    else:
                        taxa_in_OG.append(leaf_name)
                size_OG = len(taxa_in_OG)
                sister_tax = {}
                if size_OG > size_sister:
                    sister_tax = summarize_taxonomy(taxa_in_sister, target_label)
                else:
                    sister_tax = summarize_taxonomy(taxa_in_OG, target_label)
                #store the tax info of the sister group        
                for element in sister_tax:
                    if element in summary[label]:
                        summary[label][element] += sister_tax[element]
                    else:
                        summary[label][element] = sister_tax[element]
            else: #trifurcation in tree. Just treat the two sisters in the same way.
                taxa_in_sisters0 = []
                taxa_in_sisters1 = []

                for leaf in sisters[0]:
                    taxa_in_sisters0.append(leaf.name)
                size_s0 = len(taxa_in_sisters0)
                for leaf in sisters[1]:
                    taxa_in_sisters1.append(leaf.name)
                size_s1 = len(taxa_in_sisters1)
            
                sister_tax = {}
                if size_s0 > size_s1:
                    sister_tax = summarize_taxonomy(taxa_in_sisters1, target_label)
                else:
                    sister_tax = summarize_taxonomy(taxa_in_sisters0, target_label)

                for element in sister_tax:
                    if element in summary[label]:
                        summary[label][element] += sister_tax[element]
                    else:
                        summary[label][element] = sister_tax[element]

#now print out some kind of summary. For each label, the sorted list of sister taxa and their frequencies?

outh = open(sys.argv[2], "w")

for label in summary:
    avg_num_clades = numpy.mean(clades_per_group[label])
    sorted_sisters = sorted(summary[label].items(), key=itemgetter(1), reverse=True)
    for tup in sorted_sisters:
        outh.write(label + "\t" + tup[0] + "\t" + str(tup[1]) + "\t" + str(avg_num_clades) + "\n")
outh.close()
