# README: ALE helper scripts

### Some notes on using the scripts in this folder for extracting information from analyses using ALE (https://github.com/ssolo/ALE).

### Usage/installation/dependency notes

All of these scripts run with just the Python 2.7.x standard library available. Unless otherwise indicated, they are simple scripts for parsing output from ALEml_undated runs, or for preparing input files for other programs, such as CONSEL (http://stat.sys.i.kyoto-u.ac.jp/prog/consel/).

#### Quantify mechanisms of genome content change
To produce a table with the number of duplications, transfers, losses and originations on each branch.
Usage:
From within a directory containing the ALE output files suffix “.uml_rec”:
```
./branchwise_numbers_of_events.py > DTLO_table
```

#### Use ALE to compare likelihoods of rooted species trees
To produce a consel input file from gene tree-species tree reconciliations for testing likelihood of different species trees
Usage:	
./write_consel_file.py  <ALE_output_with_species_tree_A> <ALE_output_with_species_tree_B> > <Consel_input.mt>
Pick representative sequences for each gene family
Creates a protein fasta file containing the medoid of each gene family
Usage:
From within a directory containing the directory “fasta” containing gene family protein fasta sequences with the suffix “.fa”
./pick_medoid_for_gene_cluster.py
Create reconciliation-based ancestral reconstructions
To produce an ancestor reconstruction at a given branch
Usage:
gene_copies_at_node.py <reconciled_directory> <branch_of_interest> <representative_sequences> <probablistic_cutoff> > <score_of_each_HG_at_given_node>
Predict gene gains between two ancestral reconstructions
Creates protein fasta file of genes gained between two branches 
Usage:
./genes_gained_on_branch.py <ancestral_reconstruction_at_branch_A> <ancestral_reconstruction_at_branch_B> <output_fasta_file> <copy_number_increase_that_qualifes_as_gain> > <output_table>
Predict the gene families that originated on a branch
Create a protein fasta file consisting of the medoids of gene families predicted to have originated on this branch. 
Usage:
./gene_originations_at_node.py <ALE_output_directory branch_of_interest> <protein_fasta_output>
