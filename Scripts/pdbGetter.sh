files=0
for line in $(cat ../Output\ Data/twoDomainProteins.txt) 
do	
	if [ $files -gt 500 ]
	then
		break
	fi
	a="http://rcsb.org/pdb/files/"
	b=".pdb"
	a+=$line
	a+=$b
	wget $a	 
	mv $line$b ../Output\ Data/One\ To\ Five\ Domains\ Proteins/
done

