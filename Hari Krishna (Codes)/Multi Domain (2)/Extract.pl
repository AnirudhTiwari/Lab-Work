@fn=<*.txt>;
@c1;
@c2;
@c3;
@c4;
@c5;
@c6;
@c7;
@c8;
@c9;
foreach(@fn)
{
open(FR,"$_");
print "$_\n";
@a=<FR>;
$l=@a;
for($i=0;$i<$l;$i++)
{
if($a[$i]=~/^F/)
{
if($c1[0] >=1)
{
print "Cluster:1"."\n"."@c1"."\n";
}
if($c2[0] >=1)
{
print "Cluster:2"."\n"."@c2"."\n";
}
if($c3[0] >=1)
{
print "Cluster:3"."\n"."@c3"."\n";
}
if($c4[0] >=1)
{
print "Cluster:4"."\n"."@c4"."\n";
}
if($c5[0] >=1)
{
print "Cluster:5"."\n"."@c5"."\n";
}
if($c6[0] >=1)
{
print "Cluster:6"."\n"."@c6"."\n";
}
if($c7[0] >=1)
{
print "Cluster:7"."\n"."@c7"."\n";
}
if($c8[0] >=1)
{
print "Cluster:8"."\n"."@c8"."\n";
}
if($c9[0] >=1)
{
print "Cluster:9"."\n"."@c9"."\n";
}
print "**********************************************************************************************************\n";
print "$a[$i]\n";
undef(@c1);undef(@c2);undef(@c3);undef(@c4);undef(@c5);undef(@c6);undef(@c7);undef(@c8);undef(@c9);
}
else
{
@b=split(/\s+/,$a[$i]);
if($b[1]==1)
{
push(@c1,$b[0]);
}
if($b[1]==2)
{
push(@c2,$b[0]);
}
if($b[1]==3)
{
push(@c3,$b[0]);
}
if($b[1]==4)
{
push(@c4,$b[0]);
}
if($b[1]==5)
{
push(@c5,$b[0]);
}
if($b[1]==6)
{
push(@c6,$b[0]);
}
if($b[1]==7)
{
push(@c7,$b[0]);
}
if($b[1]==8)
{
push(@c8,$b[0]);
}
if($b[1]==9)
{
push(@c9,$b[0]);
}
}
}
close(FR);
}
