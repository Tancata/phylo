import os, sys
#python3 combine_treelists.py 300 treelist1 treelist2 treelist3 ...

burnin = int(sys.argv[1]) + 1
treelists = sys.argv[2:]
outfile = sys.argv[2] + ".combined"

for t in treelists:
    os.system("tail -n +" + str(burnin) + " >> " + outfile)
