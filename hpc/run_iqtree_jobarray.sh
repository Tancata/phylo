#!/bin/sh
#PBS -l walltime=23:59:59
#PBS -N iqtreejobarray
#PBS -j oe
#PBS -l select=1:ncpus=1:mem=6gb
#PBS -J 1-10000
module load apps/iqtree/1.6.10
cd /work/tw15962/eukfams_nometas/renamed2/

mkdir $PBS_ARRAY_INDEX

cp ${PBS_ARRAY_INDEX}.bmge $PBS_ARRAY_INDEX
cd $PBS_ARRAY_INDEX

iqtree -s ${PBS_ARRAY_INDEX}.bmge -m MFP -mset LG -madd LG+C20,LG+C20+F,LG+C60,LG+C60+F -bb 1000 -wbtl -bnni
