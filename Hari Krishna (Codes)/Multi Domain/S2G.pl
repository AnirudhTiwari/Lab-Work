sub Step1
{
$ii=0;
$ll=0;
$THERSHOLD=7;
$t2fn=$_[0];

sub parsingPDBFile
{
	$inFileName=$_[0];
	print "Processing $inFileName\n";
        open(INFILE,"$inFileName") or die " file not opened";
        while($line=<INFILE>)
        {
                chomp($line);
                if($line=~/ATOM.*CA\s*\w*\s*[a-zA-Z]*\s*\d*\s*(.*)/g)
                {       #print "$1\n";
                        @temp=split('\s+',$1);
                        push @coOrdinates,[$temp[0],$temp[1],$temp[2]];
                        #print OUT "$temp[0]\t$temp[1]\t$temp[2]\n";
			$ii++;
                }

                if($line=~/HETATM.*CA\s*\w*\s*[a-zA-Z]*\s*\d*\s*(.*)/g)
                {       @temp=split('\s+',$1);
                        push @coOrdinates,[$temp[0],$temp[1],$temp[2]];
                        #print OUT "$temp[0]\t$temp[1]\t$temp[2]\n";
			$ii++;
                }

                if($line=~/ENDMDL/)
                {
                        last;
                }
        }
        close INFILE;

}
$iii;
@edge;
sub adjacencyDistanceMatrix()
{
        my $nR=$ii;
	$l;
	
	$ttt=$nR+1;	
	$tempfn=$inFileName.".graph";
     	open(EDGEMATRIX,">$tempfn") or die " distance matrix file not created\n";
        for($i=0;$i<$nR;$i++)
        {
                for($j=0;$j<$nR;$j++)
                {
                        $sum=($coOrdinates[$i][0]-$coOrdinates[$j][0])*($coOrdinates[$i][0]-$coOrdinates[$j][0]);
                        $sum+=($coOrdinates[$i][1]-$coOrdinates[$j][1])*($coOrdinates[$i][1]-$coOrdinates[$j][1]);
                        $sum+=($coOrdinates[$i][2]-$coOrdinates[$j][2])*($coOrdinates[$i][2]-$coOrdinates[$j][2]);
                        $distance[$i][$j]=sqrt($sum);
                        if($distance[$i][$j]<=$THERSHOLD && $i!=$j)
                        {
                                $adjancency[$i][$j]=1;
                        }
                        else
                        {
                                $adjancency[$i][$j]=0;
                        }
                        
                        if($j!=$nR-1)
                        {
                                
				                        
			}
                }
               
        }
        close ADJMATRIX;
        close DISMATRIX;

	for($i=0;$i<$nR;$i++)
        {
                for($j=0;$j<$nR;$j++)
                {
			if($adjancency[$i][$j]==1)
			{
				print EDGEMATRIX "$i"." ";
				$l++;				
				print EDGEMATRIX "$j\n";
				$l++;
			}
		}
	}

close EDGEMATRIX;

}
parsingPDBFile($t2fn);
adjacencyDistanceMatrix();
}

@fn=<*.pdb>;
$fc=@fn;
for($ic=0;$ic<$fc;$ic++)
{
$tfn=$fn[$ic];
Step1($tfn);
}
