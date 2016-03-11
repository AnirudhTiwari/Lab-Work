files=0
for line in $(cat cath_scop_final_pdb) 
do	
	if [ $files -gt 920 ]
	then
		break
	fi
	a="http://rcsb.org/pdb/files/"
	b=".pdb"
	a+=$line
	a+=$b
	wget $a	 
	mv $line$b temp
done

