@fn=<*edge_list>;
foreach(@fn)
{
system("./MD $_ > $_.txt");
}
