files=0
for line in $(cat ../Final_dataset_without_chain.txt) 
do	
	if [ $files -gt 1285 ]
	then
		break
	fi
	a="rsync://rsync.cmbi.ru.nl/dssp/"
	b=".dssp"
	a+=$line
	a+=$b
	rsync -a $a $(pwd)	 
done

