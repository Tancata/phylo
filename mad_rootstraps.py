import os, sys

treelist = sys.argv[1]
outfile = sys.argv[1] + ".rooted"

if os.path.exists(outfile):
    os.unlink(outfile)


os.system("mad.py " + treelist + " -n") #needs mad.py to be in your path
#os.system("grep -v '^>>\|^<\|^>\|^$' " + outfile + ".rooted > " + finalfile)
