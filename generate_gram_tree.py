#Usage p4 generate_gram_tree.py -- mytree.tre group_label_tabdelimited_textfile [True|False (doNodeNums)] reroot_node1 reroot_node2 [y | n (rotatearound root)]

from Gram import TreeGram,Gram,TreeGramRadial
from collections import defaultdict
import re

groups = defaultdict(list)

#generate a table of groups to label from a tab-delimited text file
inh = open(var.argvAfterDoubleDash[1])
for line in inh:
	elements = re.split("\t", line.rstrip())
	groups[elements[1]].append(elements[0])	
inh.close()

grForTxDict = {}
for k,v in groups.iteritems():
    for vl in v:
            #allGVals.add(vl)
        ret = grForTxDict.get(vl)
        #assert not ret
        grForTxDict[vl] = k
                
#color By default None, implying black. Set to one of 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'gray', 'white', 'darkgray', 'lightgray', 'brown', 'orange', 'purple', 'violet', 'lime', 'olive', 'pink', and 'teal'. This uses the LATEX xcolor package, so you can also say, for example 'red!20' for a light pink, or 'black!10' for a light gray.

#setup shapes for group labels

dingB = r'{\large \ding{108}}' # empty shadow circle (109), or filled circle 108
dingA = r'{\large \ding{115}}' # triangle
dingE = r'{\large \ding{110}}' # square
dingOB = r'{\large \ding{108}}'
#colours need to be defined below

gColours = {
    'Bacteria': r'\textcolor{darkgray}',
    'Korarchaeota': r'\textcolor{magenta}',
    'Eukaryota': r'\textcolor{euka2}',
    'Firmicutes': r'\textcolor{darkgray}',
    'Chlamydiae': r'\textcolor{darkgray}',
    'Planctomycetes': r'\textcolor{darkgray}',
    'Cyanobacteria': r'\textcolor{darkgray}',
    'Thaumarchaeota': r'\textcolor{magenta}',
    'Aigarchaeota': r'\textcolor{aiga2}',
    'Epsilonproteobacteria': r'\textcolor{brown}',
    'Deltaproteobacteria': r'\textcolor{violet}',
    'Euryarchaeota': r'\textcolor{eury2}',
    'Crenarchaeota': r'\textcolor{cyan}',
    'Thermoplasmatales': r'\textcolor{ther2}',
    'Betaproteobacteria': r'\textcolor{orange}',
    'Alphaproteobacteria': r'\textcolor{red}',
    'Gammaproteobacteria': r'\textcolor{yellow}',
    'Actinobacteria': r'\textcolor{darkgray}',
    'DPANN': r'\textcolor{dpan2}',
    }

#start Gram stuff

var.newick_allowSpacesInNames = True
#var.doRepairDupedTaxonNames = 1
var.allowDupedTaxonNames = True

#read in tree and set up labels

input_tree = var.argvAfterDoubleDash[0] 
treename = input_tree[:-4] #only works if ending is dot and then three characters...so lazy...
var.trees = []
t = func.readAndPop(input_tree)
for n in t.iterLeavesNoRoot():
    ding = dingA
    ret = grForTxDict[n.name] #is taxon name in labels dictionary?
    assert ret
    print n.name + "\t" + ret
    if ret == "Eukaryota":
        ding = dingE
    elif ret == 'Crenarchaeota' or ret == 'Euryarchaeota' or ret == 'Thaumarchaeota' or ret == 'Korarchaeota' or ret == 'Aigarchaeota' or ret == "DPANN":
        ding = dingA
    else:
        ding = dingB
    ding_col = ''
    if ret in gColours:
        ding_col = gColours[ret]
    else:
        ding_col = r'\textcolor{darkgray}'
    n.name = r'\textit{%s} \raisebox{-1pt}{%s%s}' % (n.name, ding_col, ding)
    n.name = r'\textit{%s}' % (n.name)
#for skel in [False]:
#    if skel:
#        for n in t.iterLeavesNoRoot():
#            n.name = ' '

#transfer node labels to branches
for n in t.iterInternalsNoRoot():
    if n.name:
        n.br.uName = n.name
    n.name = None
#add new node and root on this node to create the proper effect
n = t.addNodeBetweenNodes(int(var.argvAfterDoubleDash[3]),int(var.argvAfterDoubleDash[4]))
t.reRoot(n)

if var.argvAfterDoubleDash[5] == "y":
    t.rotateAround(t.root)

#t.reRoot(int(var.argvAfterDoubleDash[2]))
tg = TreeGram(t, yScale=0.4, widthToHeight=1.2, doNodeNums=(var.argvAfterDoubleDash[2] == "True"))        
#tg = TreeGramRadial(t,maxLinesDim=10.,equalDaylight=False)
tg.latexUsePackages.append('pifont')
tg.latexUsePackages.append('xcolor')
tg.latexOtherPreambleCommands.append(r"\definecolor{bact2}{HTML}{A0522D}")  # Sienna
tg.latexOtherPreambleCommands.append(r"\definecolor{eury2}{HTML}{0000FF}")
tg.latexOtherPreambleCommands.append(r"\definecolor{euka2}{HTML}{31B34A}")
tg.latexOtherPreambleCommands.append(r"\definecolor{cren2}{HTML}{703E98}")
tg.latexOtherPreambleCommands.append(r"\definecolor{thau2}{HTML}{FF0000}") # Red
tg.latexOtherPreambleCommands.append(r"\definecolor{aiga2}{HTML}{FF8C00}") # Dark Orange
tg.latexOtherPreambleCommands.append(r"\definecolor{kora2}{HTML}{D11C7E}")
tg.latexOtherPreambleCommands.append(r"\definecolor{ther2}{HTML}{008080}")  # Teal
tg.latexOtherPreambleCommands.append(r"\definecolor{dpan2}{HTML}{FF1493}")  # Tealish


tg.latexOtherPreambleCommands.append(r"\colorlet{bact3}{bact2!20!white}")
tg.latexOtherPreambleCommands.append(r"\colorlet{eury3}{eury2!15!white}")
tg.latexOtherPreambleCommands.append(r"\colorlet{euka3}{euka2!30!white}")
tg.latexOtherPreambleCommands.append(r"\colorlet{cren3}{cren2!20!white}")
tg.latexOtherPreambleCommands.append(r"\colorlet{thau3}{thau2!30!white}")
tg.latexOtherPreambleCommands.append(r"\colorlet{aiga3}{aiga2!30!white}")
tg.latexOtherPreambleCommands.append(r"\colorlet{kora3}{kora2!30!white}")
tg.latexOtherPreambleCommands.append(r"\colorlet{ther3}{ther2!30!white}")
tg.latexOtherPreambleCommands.append(r"\colorlet{dpan3}{dpan2!30!white}")
    
tg.font = 'helvetica'
tg.documentFontSize=10
tg.dirName = 'Gram'
#tg.pdfViewer = 'ls' #'open'
tg.baseName = treename

tg.leafLabelSize = 'normalsize'
tg.internalNodeLabelSize = 'normalsize'
tg.branchLabelSize = 'small'
tg.tgDefaultLineThickness = 'thick' # default 'semithick'
tg.setScaleBar(yOffset = -1.0,length=0.2)
t.draw()
tg.bracketsLineUp = False
tg.render()
st = tg.tikzStyleDict['bracket label']
st.textShape = 'itshape'
st.textSize = 'large'

tg.fixTextOverlaps()   
tg.epdf()
os.system("open Gram/" + treename + ".pdf")
#tg.tweaker()
