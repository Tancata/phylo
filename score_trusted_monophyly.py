from __future__ import print_function
import sys, re, numpy
from collections import defaultdict
from operator import itemgetter
from ete3 import Tree

#usage: python score_trusted_monophyly.py MLFile 

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

def check_for_favourite_taxonomy(name): #given a leaf name, return the favourite taxonomy label (a trusted group) or none if it is not part of the trusted group.
    for label in believed:
        if re.search(label, name.rstrip()):
            return label
    return "none"

#check, in an ML tree, whether a set of favourite groups (a) are represented, (b) are monophyletic. Print a score for the tree corresponding to monoProp/totalProp

believed = ['Thaumarchaeota', 'Crenarchaeota'] #add trusted groups to check here

labels = {}
name_to_tax_info = defaultdict(dict)
taxa_names = []
summary = defaultdict(dict)
groups = []
clades_per_group = defaultdict(list)

target_label = 'cluster' #edit this to make the comparisons at a desired taxonomic level

#read the ML tree, set up the taxonomy stuff, and calculate the number of clades per label, and the sizes of those clades (to report at the end)
#might need to alter taxonomy assignment so that we check for the presence of the believed groups at all levels of the taxonomy.
ml_tree = Tree(sys.argv[1])
for leaf in ml_tree:
    taxonomy = check_for_favourite_taxonomy(leaf.name)
    taxa_names.append(leaf.name)
    leaf.add_feature("tax", taxonomy) #this needs to label with the favoured group, or else "none" or something. TODO.
    if taxonomy == "none":
        continue
    else:
        labels[taxonomy] = 1
groups = labels.keys()
#need to add something above to get a list of the believed labels which are actually found in the tree. For the moment, we'll use groups (=labels.keys()).
#for each of our favourite believed groups, ask whether all sequences from that group are monophyletic.

total_believed_groups = len(groups)
mono_believed_groups = 0
for label in groups:
    val = ml_tree.check_monophyly(values=[label], target_attr="tax", unrooted=True)
    #print(val)
    print(label + "\t" + str(val[0]) + "\t" + str(val[1]))
    if val[0] == True:
        mono_believed_groups += 1
    else:
        for ele in val[2]:
            print(ele.get_ascii())
    #    mono_believed_groups += 1
    #    print(label)

print(sys.argv[1] + " score: " + str(float(mono_believed_groups)/float(total_believed_groups)))
