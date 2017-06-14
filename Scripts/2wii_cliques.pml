load /Users/anirudhtiwari/Documents/Thesis/Scripts/Test Dataset/2wii.pdb
select cluster_A, resi 13+14+32+33+34+13+14+33+34+35+45+46+47+55+56
select cluster_B, resi 64+65+66+87+88+65+66+67+87+88+80+81+82+83+90
select cluster_C, resi 99+100+101+125+126+100+101+102+123+124+127+128+129+149+150
select cluster_D, resi 201+202+203+217+218+214+215+216+230+231+233+234+237+238+239
select chain_C, chain C
select X, cluster_A & chain_C
select Y, cluster_B & chain_C
select Z, cluster_C & chain_C
select W, cluster_D & chain_C
color red, X
color green, Y
color blue, Z
color yellow, W
hide everything
show sticks, X
show sticks, Y
show sticks, Z
show sticks, W