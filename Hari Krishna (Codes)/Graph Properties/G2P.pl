@fn=<*.graph>;
foreach(@fn)
{
system("./D1 $_ > $_.txt");
}
