#!/bin/bash
files=0
# for line in $(cat cath_scop_final_pdb)
# for line in $(cat multi_domain_balanced_classes_chains.txt) 
for line in $(cat ASTRAL_SCOP30_CHAINS) 
# for line in $(cat hari_krishna_dataset.txt) 
do	
	if [ $files -gt 8000 ]
	then
		break
	fi
	line=${line:0:4}
	a="https://files.rcsb.org/download/"
	b=".pdb.gz"
	a+=$line
	a+=$b
	c=".pdb"
	d="ASTRAL_SCOP30_DATASET/"$line$c
	
	if [ -f $d ]
	then
		echo $d
	else
		wget --no-check-certificate $a
		fileName=$line$b
		gunzip $fileName
		mv $line".pdb" ASTRAL_SCOP30_DATASET/
	fi
done
