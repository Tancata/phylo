#phylo

Scripts for phylogenetics. See the wiki for some workflows.

###Some useful libraries

[Biopython](http://biopython.org/): Lots of useful libraries and functions for doing bioinformatics in Python.

[p4](http://p4.nhm.ac.uk): Peter Foster's Python package for phylogenetics. Implements complex substitution models, supertree methods, and a lot more.

[Gram](http://gram.nhm.ac.uk): Another Peter Foster package. Programmatically draw phylogenetic trees (and in principle other simple vector graphics) with LaTeX and Python.

####Some useful software

#####Phylogenetic trees, phylogenomics, comparative genomics

[PhyloBayes](http://www.phylobayes.org): Bayesian trees, implements various mixture models including the author's own CAT and CAT+GTR. Also some molecular dating stuff. Implementations currently faster (fastest? only?) of some of the models. Use the MPI version if at all possible.

[IQ-Tree](http://www.cibiv.at/software/iqtree/): Very efficient maximum likelihood tree program. Supports fancier models than other ML packages (e.g. profile and matrix mixture models).

[ALE](https://github.com/ssolo/ALE): Probabilistic gene tree-species reconciliation methods. Very nice.

#####Sequence alignment, masking
[MUSCLE](http://www.drive5.com/muscle/): Workhorse sequence aligner, pretty fast.

[MAFFT](http://mafft.cbrc.jp/alignment/software/): Flexible sequence aligner, many options depending on size, other properties of the dataset.

[Seqtools](http://www.sanger.ac.uk/science/tools/seqtools): Alignment viewer and editor (graphical), among other things.
