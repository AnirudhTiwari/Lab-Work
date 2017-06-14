load /Users/anirudhtiwari/Documents/Thesis/Scripts/Test Dataset/1e88.pdb
select cluster_A, resi 2+3+4+13+14+3+4+5+11+12+27+28+29+38+39
select cluster_B, resi 47+48+49+95+96+48+49+50+51+52+56+57+83+84+85
select cluster_C, resi 103+104+105+115+116+105+106+113+114+115+106+107+111+113+114
select chain_A, chain A
select X, cluster_A & chain_A
select Y, cluster_B & chain_A
select Z, cluster_C & chain_A
color red, X
color green, Y
color blue, Z
hide everything
show sticks, X
show sticks, Y
show sticks, Z