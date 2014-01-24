if 0:
    # First prepare the tree
    t = func.readAndPop("29dpann_catgtr_pretty.tre")
    n = t.addNodeBetweenNodes(25,26)
    t.reRoot(n)
    t.rotateAround(t.root)
    t.writePhylip('rearrangedTree.phy')

if 1:
    from Gram import TreeGram
    t = func.readAndPop('rearrangedTree.phy')
    # tg = TreeGram(t, yScale=0.4, widthToHeight=1.2, doNodeNums=(var.argvAfterDoubleDash[2] == "True"))
    tg = TreeGram(t, yScale=0.45, doNodeNums=False)

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
    tg.documentFontSize=11
    tg.pdfViewer = 'open'
    if 1:
        g = tg.setBracket(31,48, text = "Eukaryotes", leftNode=30)
        g.fill = 'euka3'
        g = tg.setBracket(59,71, text = "Crenarchaeota", leftNode=57)
        g.fill = 'cren3'
        g = tg.setBracket(53,55, text = "Thaumarchaeota", leftNode=51)
        g.fill = 'thau3'
        g = tg.setBracket(56,56, text = "Aigarchaeota", leftNode=50)
        g.fill = 'aiga3'
        g = tg.setBracket(5,14, text = "DPANN", leftNode=2)
        g.fill = 'dpan3'
        g = tg.setBracket(74,86, text = "Bacteria", leftNode=72)
        g.fill = 'bact3'
        g = tg.setBracket(17,26, text = "Euryarchaeota", leftNode=16)
        g.fill = 'eury3'
        g = tg.setBracket(29,29, text = "Korarchaeota", leftNode=28)
        g.fill = 'kora3'
        tg.bracketsLineUp = False

    #tg.leafLabelSize = 'normalsize'
    #tg.internalNodeLabelSize = 'normalsize'
    tg.branchLabelSize = tg.internalNodeLabelSize
    tg.tgDefaultLineThickness = 'thick' # default 'semithick'
    #tg.setScaleBar(yOffset = -1.0,length=0.2)
    tg.setScaleBar(length=0.2)
    tg.setBrokenBranch(72)

    n = t.node(1)
    tg.setBranchLabel(n, "1")

    # Only one tweak needed, for node 16.
    # Note that the label is adjusted, not the node.
    t.node(16).label.xShift = -0.25

    tg.render()
    st = tg.tikzStyleDict['bracket label']
    st.textShape = 'itshape'
    st.textSize = 'large'
    st = tg.tikzStyleDict['leaf']
    st.textShape = 'itshape'

    tg.epdf()
