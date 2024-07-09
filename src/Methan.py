from Dcel import Vertex
from IntersectionManager import Intersection_Manager
from Sphere import Sphere
import plotly.graph_objects as go
from Common import plot

C = Sphere(c=[0,0,0], r=1700, name="Kohlenstoff", color="black")
C.triangulate(4)

H1 = Sphere(c=[630, 630, 630], r = 1200, name="Wasserstoff1", color="blue")
H1.triangulate(4)

H2 = Sphere(c=[-630, -630, 630], r=1200, name="Wasserstoff2", color="blue")
H2.triangulate(4)

H3 = Sphere(c=[-630, 630, -630], r=1200, name="Wasserstoff3", color="blue")
H3.triangulate(4)

H4 = Sphere(c=[630, -630, -630], r=1200, name="Wasserstoff4", color="blue")
H4.triangulate(4)

manager = Intersection_Manager(C, H1)
manager.add_sphere3(H2)
manager.add_sphere3(H3)
manager.add_sphere3(H4)

for circle in manager.circles:
  circle.color = "black"

traces = manager.get_line_traces()

plot(traces)
