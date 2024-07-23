import numpy as np
from IntersectionPlane import IntersectionPlane
import plotly.graph_objects as go


class Vertex:
    """
    Ecke einer DCEL
    """

    def __init__(self, coords: list[float], edge: "HalfEdge" = None):
        self.coords: list[float] = coords
        self.edge: "HalfEdge" = edge
        self.done: bool = False
        self.intersection_data: Intersection_Data = None

    def __eq__(self, value: object) -> bool:
        """
        Methode zum prüfen auf Gleichheit
        """
        return (
            self.coords[0] == value.coords[0]
            and self.coords[1] == value.coords[1]
            and self.coords[2] == value.coords[2]
        )

    def __lt__(self, value: object) -> bool:
        """
        Methode dient dazu, Schnittpunkte zu sortieren in Abhängigkeit ihres Winkels
        """
        return self.intersection_data.__lt__(value.intersection_data)

    def __str__(self) -> str:
        return "Coords: % s, intersectionpoint: % s" % (
            self.coords,
            self.intersection_data != None,
        )


class Intersection_Data:
    """
    Speichert alle benötigten Daten für einen Schnittpunkt ab
    """

    def __init__(self, owner: "DCEL"):
        self.angle: float = 0
        self.owner: "DCEL" = owner
        self.angle: float = 0.0
        self.isMerged: bool = False
        self.extra_edge: "HalfEdge" = None
        self.is_Multi: bool = False

    def __lt__(self, other) -> bool:
        return self.angle < other.angle


class HalfEdge:
    """
    Halbkante einer DCEL
    """

    _id_counter = 0  # dient dazu den Halbkanten eine ID eindeutige ID zu geben um auf Gleichheit testen zu können

    def __init__(
        self,
        origin: Vertex,
        next: "HalfEdge" = None,
        twin: "HalfEdge" = None,
        face: "Face" = None,
    ):
        self.origin: Vertex = origin
        self.next: HalfEdge = next
        self.twin: HalfEdge = twin
        self.face: Face = face
        self.done: bool = False
        self.ID: int = HalfEdge._id_counter
        HalfEdge._id_counter += 1

    def __str__(self) -> str:
        return "origin: % s" % (self.origin)

    def __eq__(self, value: object) -> bool:
        """
        Ermöglicht das Vergleichen von Halbkanten
        """
        if not isinstance(value, HalfEdge):
            return False
        return self.ID == value.ID


class Face:
    """
    Fläche einer DCEL
    """

    def __init__(self, outer_component: HalfEdge):
        self.outer_component = outer_component
        self.do_not_triangulate = False


class DCEL:
    """
    Die DCEL, welche die Ecken-, Halbkanten- und Flächenstruktur hält
    """

    def __init__(
        self,
        color: str = "",
        center: list[float] = [],
    ):
        self.vertices: list[Vertex] = []
        self.edges: list[HalfEdge] = []
        self.faces: list[Face] = []
        self.center: list[float] = center
        self.color: str = color

    def add_vertex(self, vertex: Vertex):
        """Fügt eine Ecke hinzu"""
        self.vertices.append(vertex)

    def add_vertices(self, list: list[Vertex]):
        """Fügt mehrere Ecken hinzu"""
        for v in list:
            self.add_vertex(v)

    def add_edge(self, edge: HalfEdge):
        """Fügt eine Halbkante hinzu"""
        self.edges.append(edge)

    def add_edges(self, list: list[HalfEdge]):
        """Fügt mehrere Halbkanten hinzu"""
        for e in list:
            self.add_edge(e)

    def add_face(self, face: Face):
        """Fügt Fläche hinzu"""
        self.faces = np.append(self.faces, face)

    def add_faces(self, list: list[Face]):
        """Fügt mehrere Flächen hinzu"""
        self.faces = np.append(self.faces, list)

    def reset_edges(self):
        """Setzt den Erledigt-Indikator der Halbkanten auf False"""
        for edge in self.edges:
            edge.done = False

    def calc_intersections(
        self,
        plane: IntersectionPlane,
        plane_side_val: float,
        insert: bool = True,
        multi: bool = False,
    ) -> list[Vertex]:
        """
        Diese Methode berechnet die Schnittpunkte der Halbkanten mit der Schnittebene
        wie in Kapitel 5.2.2 spezifiziert
        """
        intersection_points: list[Vertex] = []
        existing_p: list[Vertex] = []

        for e in self.edges:
            if not e.done:
                e.done = True
                e.twin.done = True

                p1 = e.origin
                p2 = e.twin.origin

                t = plane.calculate_intersection(v1=p1, v2=p2)

                if not insert:
                    if t > 0 and t < 1:
                        v = Vertex(coords=(p1.coords + t * (p2.coords - p1.coords)))
                        v.intersection_data = Intersection_Data(owner=self)
                        intersection_points.append(v)
                    elif t == 0 or t == 1:
                        existing_p.append(p1 if t == 0 else p2)

                else:
                    if (
                        t == 0
                    ):  # momentane Lösung für bestehende Punkte als Schnittpunkte
                        t = 0.05
                        existing_p.append(p1)

                    if (
                        t == 1
                    ):  # momentane Lösung für bestehende Punkte als Schnittpunkte
                        t = 0.95
                        existing_p.append(p1)

                    if t > 0 and t < 1:
                        v = self.insert_intersection_point(
                            coords=(p1.coords + t * (p2.coords - p1.coords)),
                            e1=e,
                            e2=e.twin,
                            plane=plane,
                            plane_side_val=plane_side_val,
                        )
                        if multi:
                            v.intersection_data.is_Multi = True
                        intersection_points.append(v)

        print("existing points length: ", len(existing_p))
        self.reset_edges()
        return intersection_points

    def insert_intersection_point(
        self,
        coords: list[float],
        e1: HalfEdge,
        e2: HalfEdge,
        plane: IntersectionPlane,
        plane_side_val: float,
        insert: bool = True,
    ) -> Vertex:
        """
        Fügt einen Schnittpunkt ein, wie auf Seite definiert
        """

        val_e1 = plane.side_check(p=e1.origin.coords)

        new_vertex = Vertex(coords=coords)

        new_vertex.intersection_data = Intersection_Data(owner=self)

        if insert:
            self.add_vertex(vertex=new_vertex)

        if (val_e1 > 0 and plane_side_val > 0) or (
            val_e1 < 0 and plane_side_val < 0
        ):  # v1 is on right side
            # print("Case v1 on right side, side % s, v1 % s" % (side_val, val_v1))
            e2.origin = new_vertex
            e1.next = e2
            new_vertex.edge = e2
        else:  # v2 is on right side
            # print("Case v2 on right side, side % s, v1 % s" % (side_val, val_v1))
            e1.origin = new_vertex
            e2.next = e1
            new_vertex.edge = e1

        return new_vertex

    def remove_part(
        self, plane: IntersectionPlane, plane_side_val: float, circle: bool = False
    ) -> None:
        """
        Entfernt den Teil der DCEL, welcher ein anderes Vorzeichen hat, als plane_side_val
        """
        keep_edges: list[HalfEdge] = []

        self.reset_edges()

        for edge in self.edges:
            if not edge.done:
                edge.done = True
                edge.twin.done = True

                if circle:
                    if (
                        edge.origin.intersection_data != None
                        and edge.origin.intersection_data.is_Multi
                    ) or (
                        edge.twin.origin.intersection_data != None
                        and edge.twin.origin.intersection_data.is_Multi
                    ):
                        keep_edges.append(edge)
                        keep_edges.append(edge.twin)
                        continue
                else:
                    if (
                        edge.origin.intersection_data != None
                        or edge.twin.origin.intersection_data != None
                    ):
                        keep_edges.append(edge)
                        keep_edges.append(edge.twin)
                        continue

                edge_side_val = plane.side_check(p=edge.origin.coords)
                edge_twin_side_val = plane.side_check(p=edge.twin.origin.coords)
                if (
                    (plane_side_val < 0 and edge_side_val < 0)
                    or (plane_side_val > 0 and edge_side_val > 0)
                ) and (
                    (plane_side_val < 0 and edge_twin_side_val < 0)
                    or (plane_side_val > 0 and edge_twin_side_val > 0)
                ):
                    keep_edges.append(edge)
                    keep_edges.append(edge.twin)

        self.edges = keep_edges
        self.reset_edges()

    def get_line_trace(self, color: str, name: str = "") -> go.Scatter3d:
        """
        Hilfsmethode um die Halbkanten der DCEL zu plotten
        """

        x_lines = []
        y_lines = []
        z_lines = []

        for e in self.edges:
            start = e.origin.coords
            end = e.next.origin.coords

            x_lines.extend([start[0], end[0], None])
            y_lines.extend([start[1], end[1], None])
            z_lines.extend([start[2], end[2], None])

        return go.Scatter3d(
            x=x_lines,
            y=y_lines,
            z=z_lines,
            mode="lines",
            line=dict(color=self.color if self.color != "" else color, width=2),
            name=name,
        )

    def get_point_trace(self, color: str, name: str = "") -> go.Scatter3d:
        """Hilfsmethode um die Ecken der DCEL zu plotten"""
        x = []
        y = []
        z = []

        for e in self.vertices:
            x.append(e.coords[0])
            y.append(e.coords[1])
            z.append(e.coords[2])

        return go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            marker=dict(color=self.color if self.color != "" else color, size=4),
            name=name,
        )
