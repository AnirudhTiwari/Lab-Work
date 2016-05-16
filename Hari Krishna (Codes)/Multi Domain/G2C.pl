@fn=<*.graph>;
foreach(@fn)
{
system("./MD $_ > $_.txt");
}
