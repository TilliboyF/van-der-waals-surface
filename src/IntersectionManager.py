from IntersectionPlane import IntersectionPlane
from IntersectionCircle import IntersectionCircle
from Sphere import Sphere
import plotly.graph_objects as go
import numpy as np


class Intersection_Manager:

    def __init__(self, s1: Sphere, s2: Sphere):
        self.circles: list[IntersectionCircle] = []
        self.spheres: list[Sphere] = []

        self.spheres.append(s1)
        self.spheres.append(s2)

        self.intersect_2(s1, s2)

    def intersect_2(self, s1: Sphere, s2: Sphere):
        """
        Schnitt zweier Kugeln
        """
        # Kapitel 5.2.1
        plane = IntersectionPlane(s1=s1, s2=s2)
        circle = IntersectionCircle(plane=plane, name=s1.name + "_" + s2.name)

        self.circles.append(circle)

        # Kapitel 5.2.2
        circle.calc_intersection_points()
        # kapitel 5.2.4
        circle.sort_intersection_points()

        # Kapitel 5.2.3
        s1.remove_part(plane=plane, plane_side_val=-1)
        s2.remove_part(plane=plane, plane_side_val=1)

        # Kapitel 5.2.5
        circle.insert_circle()

        # Kapitel 5.2.7
        circle.fix_circle()

        # Kapitel 5.2.6
        circle.restore_triangulation()

        # reset (relevant für weitere Schnitte)
        for edge in circle.edges:
            edge.origin.intersection_data = None
        for edge in s1.edges:
            edge.origin.intersection_data = None
        for edge in s2.edges:
            edge.origin.intersection_data = None

    def add_Sphere(self, s: Sphere):
        """
        Der missglückte Versuch eine universelle Lösung zu implementieren, mithilfe der neue Kugeln hinzugefügt werden können...
        """

        intersections: list[Sphere] = []

        for sphere in self.spheres:
            d = np.linalg.norm(np.array(s.center) - np.array(sphere.center))
            if d < (s.r + sphere.r):
                intersections.append(sphere)

        self.spheres.append(s)

        for circle in self.circles:
            s1: Sphere = circle.plane.s1
            s2: Sphere = circle.plane.s2
            if s1 in intersections and s2 in intersections:
                self.intersect_3(s1, s2, circle, s)
                intersections.remove(s1)
                intersections.remove(s2)

        for sphere in intersections:
            self.intersect_2(sphere, s)

    def intersect_3(
        self,
        s1: Sphere,
        s2: Sphere,
        s1_s2_circle: IntersectionCircle,
        new_Sphere: Sphere,
    ):
        """
        Schnitt dreier Kugeln
        """

        c0 = s1_s2_circle
        c1 = self.part_intersect(s1, new_Sphere)

        c0.remove_points(plane=c1.plane, plane_side_val=1)

        multi_points = c0.calc_intersections(
            plane=c1.plane, plane_side_val=-1, multi=True
        )  # Schnitt mit ebene von c1

        c0.remove_part(plane=c1.plane, circle=True)

        c1.add_vertices(multi_points)
        c1.sort_intersection_points()
        c1.remove_points(plane=c0.plane, plane_side_val=-1)

        c2 = self.part_intersect(s1=s2, s2=new_Sphere)
        c2.add_vertices(list=multi_points)
        c2.sort_intersection_points()
        c2.remove_points(plane=c0.plane, plane_side_val=1)

        c1.insert_circle()  # einfügen Schnittkreis
        c2.insert_circle()  # einfügen Schnittkreis

        c1.fix_circle()  # verschmelzen der Schnittpunkte
        c2.fix_circle()  # verschmelzen der Schnittpunkte

        c1.restore_triangulation()  # wiederherstellung der Triangulierung
        c2.restore_triangulation()  # wiederherstellung der Trianguliering

        # reset (relevant für weitere Schnitte)
        for edge in c1.edges:
            edge.origin.intersection_data = None
        for edge in c2.edges:
            edge.origin.intersection_data = None
        for edge in s1.edges:
            edge.origin.intersection_data = None
        for edge in s2.edges:
            edge.origin.intersection_data = None
        for edge in new_Sphere.edges:
            edge.origin.intersection_data = None

    def part_intersect(self, s1: Sphere, s2: Sphere) -> IntersectionCircle:
        """
        Hilfsmethode für den Schnitt dreier Kugeln,
        um die Schnittebene zu ermitteln,
        die Schnittpunkte der beiden Kugeln
        und entfernt die Kugelteile
        """
        plane = IntersectionPlane(s1=s1, s2=s2)
        circle = IntersectionCircle(plane=plane, name=s1.name + "_" + s2.name)

        self.circles.append(circle)

        circle.calc_intersection_points(insert=True)

        s1.remove_part(plane=plane, plane_side_val=-1)
        s2.remove_part(plane=plane, plane_side_val=1)

        return circle

    def get_line_traces(self) -> list[go.Scatter3d]:
        """
        Hilfsmethode um die gesamte Oberfläche zu plotten
        """
        color = [
            "red",
            "blue",
            "green",
            "purple",
            "orange",
            "cyan",
            "yellow",
            "pink",
            "magenta",
            "lime",
            "maroon",
            "navy",
            "olive",
            "teal",
            "aqua",
            "fuchsia",
            "silver",
            "gray",
            "black",
            "white",
            "brown",
            "gold",
            "salmon",
            "indigo",
            "violet",
            "turquoise",
            "coral",
            "crimson",
            "khaki",
            "lavender",
            "orchid",
            "plum",
            "sienna",
            "tan",
            "thistle",
            "tomato",
            "wheat",
            "azure",
            "beige",
            "chocolate",
            "ivory",
            "mintcream",
            "peachpuff",
            "seashell",
            "snow",
            "lightblue",
            "lightgreen",
            "lightpink",
            "lightsalmon",
            "lightcoral",
            "lightcyan",
            "lightgoldenrodyellow",
            "lightgray",
            "lightseagreen",
            "lightskyblue",
            "lightslategray",
            "lightsteelblue",
            "lightyellow",
        ]

        color_index = 0

        res = []
        for s in self.spheres:
            res.append(s.get_line_trace(color=color[color_index]))
            color_index += 1
            color_index = color_index % len(color)

        for c in self.circles:
            res.append(c.get_circle_traces(color=color[color_index]))
            # res.append(c.get_point_trace(color=color[color_index]))
            color_index += 1
            color_index = color_index % len(color)

        return res
