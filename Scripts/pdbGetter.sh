for line in $(cat ../Output\ Data/twoDomainProteins.txt) 
do	
	a="http://rcsb.org/pdb/files/"
	b=".pdb"
	a+=$line
	a+=$b
	wget $a	 
	mv $line$b ../Output\ Data/Two\ Domain\ Proteins/
done

