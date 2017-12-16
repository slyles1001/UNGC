# p = 1
p11 = 1739357
p12 = 1570501
p13 = 1495584
# p = 2
p21 = 1248151
p22 = 1057910
p23 = 954984
# p = 3
p31 = 831526
p32 = 663521
p33 = 664736

mat = matrix(c(p11, p12, p13, p21, p22, p23, p31, p32, p33), ncol = 3)

chemp = 1259935
formp = 504312
pharmp = 1143364

nchem = 49
nfor = 35
npharm = 46
secs = c(nchem, nfor, npharm)

scaled = mat/secs

mat[1,1]/mat[1,2] # compare chem p1 to chem p2
mat[1,1]/mat[1,3] # and so forth
mat[2,1]/mat[2,2]
mat[2,1]/mat[2,3]
mat[3,1]/mat[3,2]
mat[3,1]/mat[3,3]
mat[1,2]/mat[1,3]
mat[2,2]/mat[2,3]
mat[3,2]/mat[3,3]


