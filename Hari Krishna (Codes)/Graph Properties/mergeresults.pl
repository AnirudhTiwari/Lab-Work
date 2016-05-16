@fn=<*.txt>;
open(FW,">Results");
close(FW);
foreach(@fn)
{
open(FR,"$_");
open(FW,">>Results");
@b=<FR>;
print FW "$_\n";
print FW "@b"."\n";
close(FW);
close(FR);
}
