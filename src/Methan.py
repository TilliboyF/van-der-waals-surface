from IntersectionManager import Intersection_Manager
from Sphere import Sphere
import plotly.graph_objects as go
from Common import plot


def calc_methan():
    C = Sphere(c=[0, 0, 0], r=1700, name="Kohlenstoff", color="black")

    H1 = Sphere(c=[630, 630, 630], r=1200, name="Wasserstoff1", color="blue")

    H2 = Sphere(c=[-630, -630, 630], r=1200, name="Wasserstoff2", color="blue")

    H3 = Sphere(c=[-630, 630, -630], r=1200, name="Wasserstoff3", color="blue")

    H4 = Sphere(c=[630, -630, -630], r=1200, name="Wasserstoff4", color="blue")

    manager = Intersection_Manager(C, H1)
    manager.spheres.append(H2)
    manager.spheres.append(H3)
    manager.spheres.append(H4)
    manager.intersect_2(C, H2)
    manager.intersect_2(C, H3)
    manager.intersect_2(C, H4)

    for circle in manager.circles:
        circle.color = "black"

    traces = manager.get_line_traces()

    plot(traces)


if __name__ == "__main__":
    calc_methan()
