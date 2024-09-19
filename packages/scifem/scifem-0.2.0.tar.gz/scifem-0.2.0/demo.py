from mpi4py import MPI
import dolfinx
import ufl
import basix
import scifem

mesh = dolfinx.mesh.create_unit_square(MPI.COMM_WORLD, 10, 10)
# breakpoint()
# V = dolfinx.fem.functionspace(mesh, ("DG", 0))
V = scifem.create_real_functionspace(mesh)
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)
a = ufl.inner(u, v) * ufl.dx

A = dolfinx.fem.assemble_matrix(dolfinx.fem.form(a), bcs=[])
# assert A.to_dense()
breakpoint()
