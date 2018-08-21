iqtree -s $1 -m LG+G+F -pre $1_guidetree
iqtree -s $1 -m LG+C20+G+F -bb 2000 -ft $1_guidetree.treefile -wbtl
