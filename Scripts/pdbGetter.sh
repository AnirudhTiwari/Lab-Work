#!/bin/bash
files=0
# for line in $(cat cath_scop_final_pdb)
for line in $(cat single_domain_training_dataset.txt) 
do	
	if [ $files -gt 156 ]
	then
		break
	fi
	line=${line:0:4}
	a="https://files.rcsb.org/download/"
	b=".pdb.gz"
	a+=$line
	a+=$b
	c=".pdb"
	d="TrainingDataset/"$line$c
	
	if [ -f $d ]
	then
		echo $d
	else
		wget --no-check-certificate $a
		fileName=$line$b
		gunzip $fileName
		mv $line".pdb" TrainingDataset/
	fi

done
