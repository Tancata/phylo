#a version of ancestral sequence reconstruction where all we care about is F(IVYWREL), so alignment is recoded as 0s (non-IVYWREL) and 1s (IVYWREL). And we try to infer that on every branch of the tree and at the root...

import sys
#var.verboseRead = 1
var.warnReadNoFile = 0
var.nexus_allowAllDigitNames = True   # put it somewhere else
var.doCheckForDuplicateSequences = False

read(sys.argv[2])
d = Data()
d.compoSummary()

read(sys.argv[3])
t = var.trees[0]
t.data = d

one_side = ''
the_other = ''
for n in t.iterNodes():
    if n.nodeNum==0:
        one_side = n.leftChild.nodeNum
        z = n.rightmostChild()
        the_other = z.nodeNum
#    if n.nodeNum==0:
#        print(n.nodeNum)
#        print(n.leftChild.nodeNum)
#        z = n.rightmostChild()
#        print(z.nodeNum)
#    c = t.newComp(free=1, spec='empirical', symbol="-")
#    t.setModelThing(c, node=n, clade=0)

#c = t.newComp(free=1, spec='empirical')
#t.setModelThing(c, node=0, clade=0)
#c2 = t.newComp(free=1, spec='empirical')
# Put the c1 comp on all the nodes of the tree.  Then put c2 on the
# root, over-riding c1 that is already there.
#t.setModelThing(c2, node=0, clade=0)


#set comps. One for root, one each for LBCA and LACA, one each for archaeal domain and bacterial domain


c0 = t.newComp(free=1, spec='empirical')
t.setModelThing(c0, node=0, clade=1)

c1 = t.newComp(free=1, spec='empirical')
t.setModelThing(c1, node=one_side, clade=0)

c2 = t.newComp(free=1, spec='empirical')
t.setModelThing(c2, node=the_other, clade=0)

c3 = t.newComp(free=1, spec='empirical')
t.setModelThing(c3, node=0, clade=0)

t.newRMatrix(free=0, spec='ones') 
t.setNGammaCat(nGammaCat=4)
t.newGdasrv(free=1, val=1.0)
t.setPInvar(free=0, val=0.0)

t.optLogLike()
t.tPickle(sys.argv[3] + '_optTree')

