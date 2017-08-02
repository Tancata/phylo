t = var.trees[0]
a = var.alignments[0]
t.data = Data()

t.model.dump()

print('\nAfter optimizing, the composition of the model for the non-root nodes is:') 
print(t.model.parts[0].comps[0].val)
print('...and the composition of the root model is:')
print(t.model.parts[0].comps[1].val)
t.write()
func.reseedCRandomizer(os.getpid())

# The char "symbols", AAs in this case, are available as a.symbols; that is why
# I gave a name to var.alignments[0].  Also available as
# d.parts[partNum].symbols, so d.parts[0].symbols are also 'arndcqeghilkmfpstwyv'

print a.symbols
quit()

counts = [0] * 20
for rep in range(100):
    ancSt = t.ancestralStateDraw()
    for i in range(20):
        ch = a.symbols[i] # 'arndcqeghilkmfpstwyv'
        cnt = ancSt.count(ch)
        counts[i] += cnt
        mySum = float(sum(counts))
print("\nsymbol optimized      draws")
for i in range(20):
    print("  %s      %.5f     %.4f" % (a.symbols[i], t.model.parts[0].comps[1].val[i], counts[i]/mySum))

#calculate predicted OGT according to Zeldovich
f_ivywrel = 0
for i in range(20):
    if a.symbols[i] in 'ivywrel':
        f_ivywrel += t.model.parts[0].comps[1].val[i]
print("F(IVYWREL) = " + str(f_ivywrel))
print("T_opt estimate according to Zeldovich: " + str(937.0*float(f_ivywrel) - 335.0))
