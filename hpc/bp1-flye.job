#! /bin/bash

#PBS -l select=1:ncpus=8:mem=512gb
#PBS -l walltime=48:00:00
#PBS -N flye_pseudotrichomonas_unmapped
#PBS -o pseudotrichomonas_unmapped_t4.out
#PBS -j oe

module add lang/python/anaconda/2.7-2019.03.bioconda
cd /work/tw15962/pseudotrichomonas

flye --pacbio-raw unmapped.fasta -g 220m --plasmids --meta -i 2 -t 4 -o flye_unmapped28m_t4
