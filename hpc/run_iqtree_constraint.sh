#!/bin/sh
#PBS -l walltime=23:59:59
#PBS -N iqtreejob
#PBS -j oe
#PBS -l select=1:ncpus=10:mem=2gb

module load apps/iqtree/1.6.10
cd /home/tw15962/iqtree_constraint
iqtree -nt 10 -s BHLH_trimmed_30.fasta -g FAMA_nobry.txt_hypothesis.treefile -m LG+C30+F -pre FAMA_nobry_constraint_LGC30F 

