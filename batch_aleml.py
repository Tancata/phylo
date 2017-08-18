import os, sys
from multiprocessing import Pool

#Usage: python batch_aleml.py path_to_species_tree
#Runs ALEml jobs across a certain number of cores (set to 12 at the moment) on a particular species tree. The .ale files should be in the current directory. Hopefully fails nicely to get around the error exits from ALEml jobs when the consensus tree trivially can't be built.

def do_tree(infile):
    os.system("ALEml " + species_tree + " " + infile)
    return

to_do = [file for file in os.listdir(".") if file.endswith(".ale")]
species_tree = sys.argv[1]
if __name__ == "__main__":
    pool = Pool(processes=12)
    pool.map(do_tree, to_do)
