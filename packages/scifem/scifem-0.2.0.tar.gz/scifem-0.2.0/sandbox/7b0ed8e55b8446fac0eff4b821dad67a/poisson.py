
from basix.ufl import element
from ufl import (
    Coefficient,
    FacetNormal,
    FunctionSpace,
    Mesh,
    SpatialCoordinate,
    TestFunction,
    TrialFunction,
    cos,
    div,
    dot,
    ds,
    Measure,
    grad,
    inner,
    pi,
    sin,
)

e_u = element("Lagrange", "triangle", 1, discontinuous=False)
e_v = element("Lagrange", "triangle", 0, discontinuous=True)

coord_element = element("Lagrange", "triangle", 1, shape=(2,))
mesh = Mesh(coord_element)

V = FunctionSpace(mesh, e_u)
Q = FunctionSpace(mesh, e_v)

u = TrialFunction(V)
v = TestFunction(V)
c = TrialFunction(Q)
d = TestFunction(Q)

x = SpatialCoordinate(mesh)
u_ex = sin(x[0] * 2 * pi) * cos(x[1] * 4 * pi)
dx = Measure("dx", domain=mesh)
f = -div(grad(u_ex))
n = FacetNormal(mesh)
g = dot(grad(u_ex), n)
a00 = inner(grad(u), grad(v)) * dx
a01 = inner(c, v) * dx
a10 = inner(u, d) * dx

L = f * v * dx + g * v * ds

uh = Coefficient(V)
J = inner(u_ex - uh, u_ex - uh) * dx

forms = [a00, a01, a10, L, J]
