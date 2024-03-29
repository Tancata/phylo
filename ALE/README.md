# README: ALE helper scripts

22/11/22 --- Note: some of these scripts are now out of date, as newer versions of ALE include additional fields in the output files which provide a more direct way to perform some of the tasks below. Check https://github.com/ak-andromeda/ALE_methods for some more up to date parsing scripts.

### Some notes on using the scripts in this folder for extracting information from analyses using ALE (https://github.com/ssolo/ALE).

### Usage/installation/dependency notes

Unless otherwise indicated, these are simple Python 2.7.x scripts for parsing output from ALEml_undated runs, or for preparing input files for other programs, such as CONSEL (http://stat.sys.i.kyoto-u.ac.jp/prog/consel/). All of the scripts except those for medoid (representative sequence selection) run with just the Python standard library. The `pick_medoid_for_gene_cluster.py` script requires Biopython to be installed. Some of these scripts were used in the analyses reported in Sheridan et al. (2020), as indicated below. The usage lines below assume the scripts are executable, but they can be also run by invoking python (or python2 on some systems) --- `python branchwise_numbers_of_events.py > DTLO_table`, for example. They should be run from a bash prompt on a Linux/UNIX system; Mac OS X should work but has not been tested. 

All of these scripts should take <1s to run on a single core machine, except for the medoid computation, which took 4m9s on the files in "Example_data.tar.gz".

#### Sample data for testing workflows

To test that things are working as expected, it may be convenient to experiment with the files in New_example_data.tar.gz in this repository.


#### Estimate numbers and types of genome content change
To produce a table with the number of duplications, transfers, losses and originations on each branch.

From within a directory containing the ALE output files suffix “.uml_rec”:
```
./branchwise_numbers_of_events.py > DTLO_table
```

#### Use ALE to compare likelihoods of rooted species trees

To produce a consel input file from gene tree-species tree reconciliations for testing likelihood of different species trees, use the following command. `<ALE_output_with_species_tree_*>` refers to a directory containing all of the ALE output files (uml_rec files) obtained from running ALEml_undated with a given rooted species tree.

```
./write_consel_file.py  <ALE_output_with_species_tree_A> <ALE_output_with_species_tree_B> > <Consel_input.mt>
```
This command writes a ".mt" file that can be used as input to CONSEL, which implements various statistical phylogenetic tree selection tests. The idea of linking ALE to CONSEL (and then, for example, performing an approximately-unbiased (AU) test) is to treat the ALE gene family likelihoods estimated under a particular rooted species tree in the same way as site likelihoods under a particular unrooted tree in a regular tree selection setting. That is, the gene family likelihoods associated with a set of rooted species trees can be used estimate a confidence set of trees.  

*NOTE:* The order of the "items" in the resulting CONSEL input file is arbitrary (in the current version). CONSEL numbers the "items" being compared from 1..n in the order they appear in the input file, so make sure to check this when interpreting the eventual CONSEL output. 

#### Pick representative (medoid) sequences for each gene family

Creates a protein fasta file containing the medoid of each gene family.

From within a directory containing the directory “fasta” containing gene family protein fasta sequences with the suffix “.fa”.
```
./pick_medoid_for_gene_cluster.py
```

#### Create reconciliation-based ancestral gene content reconstructions

In Sheridan et al. (2020) (submitted), the following approach was used. Note that node numbers refer to the numbering used in the rooted species tree map that appears at the beginning of any ALEml_undated .uml_rec output file. If you want a set of protein sequences at the node to functionally annotate, then the directory in which the script is run should contain a "medoid" directory, containing representative sequences for each gene family (for subsequent functional annotation). If you do not require this functionality, the associated code can be commented out of the script. The script can, of course, be edited to change the setup in terms of directory names.

To produce an ancestor reconstruction at a given branch:

```
gene_copies_at_node.py <reconciled_directory> <node_of_interest> <representative_sequences> <copy_number_cutoff> > <score_of_each_gene_family_at_given_node>
```

Here, `<reconciled_directory>` refers to a directory containing the ALEml_undated output files (uml_rec files) associated with an optimal rooted species tree. Node of interest is the node number for which the gene content probabilities should be obtained. `<representative_sequences>` refers to an (optional) set of representative sequences, for use in subsequent annotation. `<copy_number_cutoff>` indicates the minimum copy number needed to consider a gene family to have been present at a node (0.5 was used in Sheridan et al. (2020).)

To create a protein fasta file (containing medoid representatives, for example for annotation) of genes gained between two branches:

```
./genes_gained_on_branch.py <ancestral_reconstruction_at_node_A> <ancestral_reconstruction_at_node_B> <output_fasta_file> <copy_number_increase_that_qualifes_as_gain> > <output_table>
```

Note that, in the above, `ancestral_reconstruction_at_node_A` refers to the output of running `gene_copies_at_node.py` on the node at one end of the branch of interest.

To create a protein fasta file consisting of the medoids of gene families predicted to have originated on a given branch: 

```
./gene_originations_at_node.py <ALE_output_directory> <branch_of_interest> <protein_fasta_output>
```
