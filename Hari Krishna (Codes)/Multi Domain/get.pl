@fn=<*.txt>;
foreach(@fn)
{
open(FF,"$_");
@a=<FF>;
print "@a";
print "\n";
close(FF);
}

