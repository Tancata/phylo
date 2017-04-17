import os, sys
from multiprocessing import Pool

def do_tree(infile):
    os.system("ALEml " + species_tree + " " + infile)
    return

to_do = [file for file in os.listdir(".") if file.endswith(".ale")]
species_tree = sys.argv[1]
if __name__ == "__main__":
    pool = Pool(processes=12)
    pool.map(do_tree, to_do)
