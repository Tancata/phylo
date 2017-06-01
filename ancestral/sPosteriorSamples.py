#modified from p4 example script of the same name
import sys
import numpy as np

rNum = sys.argv[4]
var.strictRunNumberChecking = False
var.nexus_allowAllDigitNames = True   # put it somewhere else
read(sys.argv[2])
read(sys.argv[3])
d = Data()
t = var.trees[0]
a = var.alignments[0]
t.data = d

pNum = 0
#  comp for each node
for n in t.iterNodes():
    c = t.newComp(partNum=pNum, free=1, spec='empirical', symbol="-")
    t.setModelThing(c, node=n, clade=False)
t.newRMatrix(partNum=pNum, free=0, spec='lg')
t.setNGammaCat(partNum=pNum, nGammaCat=4)
t.newGdasrv(free=1, val=0.5)
t.setPInvar(partNum=pNum, free=0, val=0.0)
t.model.parts[pNum].ndch2 = True
t.model.parts[pNum].ndch2_writeComps = True

t.calcLogLike(verbose=False)

func.reseedCRandomizer(os.getpid())

# Instantiate
ps = PosteriorSamples(t, runNum=0, program='p4', verbose=0)

# If I were to do simulations, then it would be more complicated because I would
# need to have a separate Data object in which to keep the reference data.
# However, since I am not doing simulations, I am doing ancestral state
# reconstructions on the root node, it is straightforward.  

counts = [0] * 20
ogt_est = []
# In this example we have 2000 samples.
for sampNum in range(100,200):
    print(sampNum)
    t2 = ps.getSample(sampNum)
    t2.data = d
    asd = t2.ancestralStateDraw()
    f_ivywrel = 0
    # At this point we can do something useful with the ancestral state draw.
    # Or just look at the composition, as is done here.
    for i in range(20):
        ch = a.symbols[i]
        cnt = asd.count(ch)
        counts[i] += cnt
        if a.symbols[i] in 'ivywrel':
            freq = float(cnt) / float(len(asd))
            f_ivywrel += freq
    ogt_z = 937.0*f_ivywrel - 335.0
    print(f_ivywrel)
    ogt_est.append(ogt_z)
            
mySum = float(sum(counts))
print()
f_ivywrel = 0
for i in range(20):
    print("%s %.4f" % (a.symbols[i], counts[i]/mySum))
    if a.symbols[i] in 'ivywrel':
        f_ivywrel += counts[i]/mySum
print("Point estimate OGT: " + str(937.0*f_ivywrel - 335.0))
for est in ogt_est:
    print(est)
print("Mean estimate OGT: " + str(np.mean(ogt_est)))
print("SD OGT: " + str(np.std(ogt_est)))

