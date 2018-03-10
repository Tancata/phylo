import os, sys
#use MAD to root a MCMC sample of trees, outputting a sample of rooted trees (for analysis with e.g. RootAnnotator)
#python3 combine_treelists.py 300 treelist1 treelist2 treelist3 ...

burnin = int(sys.argv[1]) + 1
treelists = sys.argv[2:]
outfile = sys.argv[2] + ".combined"
finalfile = sys.argv[2] + ".rooted_sample"
if os.path.exists(outfile):
    os.unlink(outfile)

for t in treelists:
    os.system("tail -n +" + str(burnin) + " " + t + " >> " + outfile + ".tmp1")

os.system("awk '!(NR%10)' " + outfile + ".tmp1 > " + outfile) #thins the chain to take every 10th tree
os.unlink(outfile + ".tmp1")
os.system("mad.py " + outfile + " -m") #needs mad.py to be in your path
os.system("grep -v '^>>\|^<' " + outfile + ".rooted > " + finalfile)
