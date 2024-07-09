import time
from Dcel import Vertex
from IntersectionManager import Intersection_Manager
from Sphere import Sphere
import plotly.graph_objects as go
from Common import plot

start_time = time.time()

triangulate_times = 8

C1 = Sphere(c=[-770,0,0], r=1700, name="Kohlenstoff1", color="black")
C1.triangulate(triangulate_times)

C2 = Sphere(c=[770,0,0], r=1700, name="Kohlenstoff2", color="black")
C2.triangulate(triangulate_times)

H1 = Sphere(c=[-1470, 930, 0], r = 1200, name="Wasserstoff1", color="blue")
H1.triangulate(triangulate_times)

H2 = Sphere(c=[-1470, -930, 0], r=1200, name="Wasserstoff2", color="blue")
H2.triangulate(triangulate_times)

H3 = Sphere(c=[1470, 930, 0], r=1200, name="Wasserstoff3", color="blue")
H3.triangulate(triangulate_times)

H4 = Sphere(c=[1470, -930, 0], r=1200, name="Wasserstoff4", color="blue")
H4.triangulate(triangulate_times)

H5 = Sphere(c=[0, 1470, 0], r=1200, name="Wasserstoff5", color="blue")
H5.triangulate(triangulate_times)

H6 = Sphere(c=[0, -1470, 0], r=1200, name="Wasserstoff6", color="blue")
H6.triangulate(triangulate_times)

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time for Sphere init: {elapsed_time} seconds")

start_time = time.time()
# C1 C2 normal intersection of 2 Spheres
manager = Intersection_Manager(C1, C2)
# H5 triple intersection with C1 C2
manager.add_Sphere2(H5)
manager.add_Sphere2(H6)
manager.spheres.append(H1)
manager.intersect_3(C1, H5, manager.circles[1], H1)
manager.spheres.append(H2)
manager.intersect_3(C1, H6, manager.circles[3], H2)
manager.spheres.append(H3)
manager.intersect_3(C2, H5, manager.circles[2], H3)
manager.spheres.append(H4)
manager.intersect_3(C2, H6, manager.circles[4], H4)

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time for Algo: {elapsed_time} seconds")

for circle in manager.circles:
  circle.color = "black"

# traces = manager.get_line_traces()

# plot(traces)
