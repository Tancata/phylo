#read in a set of ALE reconciliation files and sum up the number of events on each branch, averaged across the dataset
import os, sys, re
from collections import defaultdict

branchwise = defaultdict(list) #0th element: duplications, 1st element: transfers, second element: losses, third element: gene copy number
input = [file for file in os.listdir(".") if file.endswith("uml_rec")]

for file in input:
    inhandle = open(file)
    for line in inhandle:
        line_elements = re.split("\t", line.rstrip())
        #print len(line_elements)
        #print line_elements
        if (line_elements[0] == "S_terminal_branch") or (line_elements[0] == "S_internal_branch"): #this means it's an interesting line, and we want to extract info about the numbers of events on this branch
            if len(branchwise[line_elements[1]]) == 0: #means the list has no elements, it's the first time we have read any info about this branch
                branchwise[line_elements[1]].append(float(line_elements[2]))
                branchwise[line_elements[1]].append(float(line_elements[3]))
                branchwise[line_elements[1]].append(float(line_elements[4]))
                branchwise[line_elements[1]].append(float(line_elements[5]))
                branchwise[line_elements[1]].append(float(line_elements[6]))
            else:
                branchwise[line_elements[1]][0] += float(line_elements[2])
                branchwise[line_elements[1]][1] += float(line_elements[3])
                branchwise[line_elements[1]][2] += float(line_elements[4])
                branchwise[line_elements[1]][3] += float(line_elements[5])
                branchwise[line_elements[1]][4] += float(line_elements[6])

#having looped over all reconciliation files, print out the total summary
print "Branch\tDuplications\tTransfers\tLosses\tOriginations\tCopyNum"
for entry in branchwise:
    print entry + "\t" + str(branchwise[entry][0]) + "\t" + str(branchwise[entry][1]) + "\t" + str(branchwise[entry][2]) + "\t" + str(branchwise[entry][3]) + "\t" + str(branchwise[entry][4])
