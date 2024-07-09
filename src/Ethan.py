import time
from Common import plot
from IntersectionManager import Intersection_Manager
from Sphere import Sphere


def calc_ethan():

    start_time = time.time()

    triangulate_times = 4

    C1 = Sphere(c=[-770, 0, 0], r=1700, name="Kohlenstoff1", color="black")
    C1.triangulate(triangulate_times)

    C2 = Sphere(c=[770, 0, 0], r=1700, name="Kohlenstoff2", color="black")
    C2.triangulate(triangulate_times)

    H1 = Sphere(c=[-1470, 930, 0], r=1200, name="Wasserstoff1", color="blue")
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

    manager = Intersection_Manager(s1=C1, s2=C2)

    manager.spheres.append(H5)
    manager.intersect_3(s1=C1, s2=C2, new_Sphere=H5, s1_s2_circle=manager.circles[0])

    manager.spheres.append(H6)
    manager.intersect_3(s1=C1, s2=C2, new_Sphere=H6, s1_s2_circle=manager.circles[0])

    manager.spheres.append(H1)
    manager.intersect_3(s1=C1, s2=H5, s1_s2_circle=manager.circles[1], new_Sphere=H1)

    manager.spheres.append(H2)
    manager.intersect_3(s1=C1, s2=H6, s1_s2_circle=manager.circles[3], new_Sphere=H2)

    manager.spheres.append(H3)
    manager.intersect_3(s1=C2, s2=H5, s1_s2_circle=manager.circles[2], new_Sphere=H3)

    manager.spheres.append(H4)
    manager.intersect_3(s1=C2, s2=H6, s1_s2_circle=manager.circles[4], new_Sphere=H4)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time for Algo: {elapsed_time} seconds")

    for circle in manager.circles:
        circle.color = "black"

    traces = manager.get_line_traces()

    plot(traces)


if __name__ == "__main__":
    calc_ethan()
