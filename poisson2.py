####### Inhomogeneous Dirichlet BC######

# solve the Poisson equation -Delta u = f
# with Dirichlet boundary condition u = g

from netgen.meshing import *
from netgen.meshing import Element0D, Element1D, Element2D, MeshPoint, FaceDescriptor
from netgen.csg import Pnt

# generate a 1D mesh
m = Mesh(dim = 1)
nel = 10
pnums = []
for i in range(nel+1):
    pnums.append(m.Add(MeshPoint(Pnt(i/nel, 0, 0))))

# add segments
for i in range(nel):
    m.Add(Element1D([pnums[i],pnums[i+1]], index=1))

m.SetMaterial(1,'material')

# add points
m.Add (Element0D(pnums[0], index=1))
m.Add (Element0D(pnums[nel], index=2))

# set boundary condition names
m.SetBCName(0,'left')
m.SetBCName(1,'right')


import ngsolve
from ngsolve import *

ngsmesh = ngsolve.Mesh(m)
# print(ngsmesh.GetBoundaries())

# #Non-homogeneous Dirichlet on left and right
fes = H1(ngsmesh, order=2, dirichlet="left|right")
g = 1/2*x

#Putting g on the boundaries marked non-homogeneous Dirichlet
gfu = GridFunction(fes)
gfu.Set(g, BND)
#Draw(gfu)


#Bilinear form
u, v = fes.TnT()
a = BilinearForm(grad(u)*grad(v)*dx).Assemble();

#Linear Form
f = LinearForm(-1*v*dx).Assemble()
r = f.vec - a.mat * gfu.vec


#solving
gfu.vec.data += a.mat.Inverse(freedofs=fes.FreeDofs()) * r
# Draw(gfu)
# Draw (-grad(gfu), ngsmesh, "Flux")


#Error 
exact = 1/2 * x*x
print ("L2-error:", sqrt (Integrate ( (gfu-exact)*(gfu-exact), ngsmesh)))

