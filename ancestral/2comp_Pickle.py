import sys
var.verboseRead = 0
var.warnReadNoFile = 0
var.nexus_allowAllDigitNames = True   # put it somewhere else

read(sys.argv[2])
d = Data()
d.compoSummary()

read(sys.argv[3])
t = var.trees[0]
t.data = d
c1 = t.newComp(free=1, spec='empirical')
c2 = t.newComp(free=1, spec='empirical')

# Put the c1 comp on all the nodes of the tree.  Then put c2 on the
# root, over-riding c1 that is already there.
t.setModelThing(c1, node=0, clade=1)
t.setModelThing(c2, node=0, clade=0)

t.newRMatrix(free=0, spec='lg') #maybe try altering this
t.setNGammaCat(nGammaCat=4)
t.newGdasrv(free=1, val=1.0)
t.setPInvar(free=0, val=0.0)

t.optLogLike()
t.tPickle(sys.argv[3] + '_optTree')

