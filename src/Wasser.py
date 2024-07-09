from Dcel import Vertex
from IntersectionManager import Intersection_Manager
from Sphere import Sphere
import plotly.graph_objects as go
from Common import plot
from Dcel import Vertex

O = Sphere(c=[0,0,0], r=1520, name="Sauerstoff", color="red")
O.triangulate(4)

H1 = Sphere(c=[-760, 580, 0], r = 1200, name="Wasserstoff1", color="blue")
H1.triangulate(4)

H2 = Sphere(c=[760, 580, 0], r=1200, name="Wasserstoff2", color="blue")
H2.triangulate(4)

manager = Intersection_Manager(O, H1)
manager.add_sphere3(H2)

for circle in manager.circles:
  circle.color = "red"

traces = manager.get_line_traces()

plot(traces)
