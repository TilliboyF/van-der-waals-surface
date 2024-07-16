from Dcel import Vertex
from IntersectionManager import Intersection_Manager
from Sphere import Sphere
import plotly.graph_objects as go
from Common import plot


def calc_water():

    O = Sphere(c=[0, 0, 0], r=1520, name="Sauerstoff", color="red")

    H1 = Sphere(c=[-760, 580, 0], r=1200, name="Wasserstoff1", color="blue")

    H2 = Sphere(c=[760, 580, 0], r=1200, name="Wasserstoff2", color="blue")

    manager = Intersection_Manager(O, H1)
    manager.spheres.append(H2)
    manager.intersect_2(O, H2)

    for circle in manager.circles:
        circle.color = "red"

    traces = manager.get_line_traces()

    plot(traces)


if __name__ == "__main__":
    calc_water()
