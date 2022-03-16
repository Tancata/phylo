from __future__ import print_function
import sys, re, numpy
from collections import defaultdict
from operator import itemgetter
from ete3 import Tree

#usage: python splitscore.py treefile

def map_species_to_cluster(cluster_file): #make a dict that links species name to the cluster to use for group compariosns
    spname_to_cluster = {}
    inh = open(cluster_file)
    for line in inh:
        if line.startswith("Names"):
            continue
        elements = re.split("\t", line)
        e2 = re.split("\_", elements[1])
        species = e2[0]
        cluster = e2[1]
        spname_to_cluster[species] = cluster
    return spname_to_cluster

def parse_taxonomy(taxon_name): #given a taxon name, try to return whatever taxonomic info is available as a list starting with the highest level classification and going lower (or a map?)
    name_elements = re.split("_", taxon_name)
    name_map = {}
    name_map['cluster'] = name_elements[1]
    name_map['class'] = name_elements[2]
    name_map['order'] = name_elements[3]
    name_map['species'] = name_elements[0]
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

#read the ML tree, set up the taxonomy stuff, and calculate the number of clades per label, and the sizes of those clades (to report at the end)
ml_tree = Tree(sys.argv[1])
total_sp = 0
for leaf in ml_tree:
    total_sp += 1
    taxonomy = parse_taxonomy(leaf.name)
    name_to_tax_info[leaf.name] = taxonomy
    taxa_names.append(leaf.name)
    leaf.add_feature("tax", taxonomy[target_label])
    labels[taxonomy[target_label]] = 1
groups = labels.keys()

#compute the number of clades per label in the ML tree, and their sizes
ML_groups = defaultdict(list) #the list is the size of each clade, len(list) is the number of clades for that label in the ML tree
#root on each tip, do naive calc, take min for each group
for tip in ml_tree:
    ml_tree.set_outgroup(str(tip.name))
    this_time = defaultdict(list)
    for label in groups:
        for node in ml_tree.get_monophyletic(values=[label], target_attr="tax"):
            size_clade = 0
            for leaf in node:
                size_clade += 1
            this_time[label].append(size_clade)
        ML_groups[label].append(len(this_time[label]))

#take the min for each group
    total_splits = 0
for label in ML_groups:
    total_splits = total_splits + min(ML_groups[label])
    print(label + "\t" + str(min(ML_groups[label])))
print("Total sp: " + str(total_sp) + "\t" + " Total splits: " + str(total_splits) + "\tSplitScore " + str(float(total_splits)*100.0/float(total_sp)))
