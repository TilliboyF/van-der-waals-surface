from Dcel import DCEL, Face, HalfEdge, Vertex
import numpy as np
import Tetraeder as tetraeder
import plotly.graph_objects as go


class Sphere(DCEL):

    def __init__(
        self,
        c: list[float] = [0, 0, 0],
        r: float = 1.0,
        name: str = "",
        color: str = "",
        triangulate: bool = True,
    ) -> None:
        super().__init__(center=c, color=color)
        self.r = r
        dcel = tetraeder.build(c, r)
        self.edges = dcel.edges
        self.faces = dcel.faces
        self.vertices = dcel.vertices
        self.name = name
        if triangulate:
            self.triangulate()

    def __eq__(self, value: object) -> bool:
        return self.name == value.name

    # Die Hauptmethode, die vollständig für das triangulieren zuständig ist und dafür sorgt, wie oft trianguliert werden soll.
    def triangulate(self, n: int = 4):
        for i in range(n - 1):
            self._stepTriangulte(i == 0)

    # die Methode, welche einmal trianguliert
    def _stepTriangulte(self, isFirst: bool):
        newEdges = []
        for h in self.edges:
            if not h.done:
                h.done = True
                h.twin.done = True
                # Berechnung des Mittelpunktes
                middlePoint = (h.twin.origin.coords + h.origin.coords) / 2
                newVertex = Vertex(middlePoint)

                # verschieben der neuen Ecke auf den Kugelradius
                newVertex.coords = self._move_on_Sphere(newVertex.coords)
                self.add_vertex(newVertex)

                # Erzeugen der neuen Halbkanten
                newEdge1, newEdge2 = self._create_new_half_edges(
                    newVertex=newVertex, h=h
                )
                newEdges.extend([newEdge1, newEdge2])

        self._reset_edges()
        self.add_edges(newEdges)
        self._update_faces(isFirst)

    # Die Methode bringt einen neu erzeugten Punkt auf den Kugel Radius
    def _move_on_Sphere(self, coords: list[float]) -> list[float]:
        offset = coords - self.center
        normalized_offset = offset / np.linalg.norm(offset)
        return self.center + self.r * normalized_offset

    # Methode um die Halbkanten zu resetten
    def _reset_edges(self):
        for h in self.edges:
            h.done = False

    # Diese Methode fügt die neue Ecke in der Mitte von 2 Ecken ein und verbindet die Halbkanten korrekt und erzeugt 2 neue Halbkanten
    def _create_new_half_edges(
        self, newVertex: Vertex, h: HalfEdge
    ) -> tuple[HalfEdge, HalfEdge]:
        newEdge1 = HalfEdge(newVertex)
        newEdge1.done = True
        newEdge1.next = h.next
        h.next = newEdge1
        newEdge1.face = h.face
        h.twin.twin = newEdge1
        newEdge1.twin = h.twin

        newEdge2 = HalfEdge(newVertex)
        newEdge2.done = True
        newEdge2.next = h.twin.next
        h.twin.next = newEdge2
        newEdge2.face = h.twin.face
        h.twin = newEdge2
        newEdge2.twin = h

        return newEdge1, newEdge2

    # In diesem Schritt werden die Flächen durchlaufen und die 3 neuen Dreicke eingefügt
    def _update_faces(self, isFirst: bool):
        newFaces = []
        for f in self.faces:
            h1 = f.outer_component
            h2 = h1.next
            h3 = h2.next
            h4 = h3.next
            h5 = h4.next
            h6 = h5.next

            v1 = h1.origin
            v2 = h2.origin
            v3 = h3.origin
            v4 = h4.origin
            v5 = h5.origin
            v6 = h6.origin

            nh1 = HalfEdge(v2)
            nh2 = HalfEdge(v6)
            nh3 = HalfEdge(v4)
            nh4 = HalfEdge(v2)
            nh5 = HalfEdge(v6)
            nh6 = HalfEdge(v4)
            self.add_edges([nh1, nh2, nh3, nh4, nh5, nh6])

            nf1 = Face(h2)
            nf2 = Face(h4)
            nf3 = Face(nh2)
            newFaces.extend([nf1, nf2, nf3])
            # Dreieck/Fläche f
            nh1.face = f
            nh1.twin = nh2
            nh1.next = h6

            h1.next = nh1

            # Dreieck/Fläche nf1
            h3.next = nh3
            nh3.next = h2
            h2.face = nf1
            h3.face = nf1
            nh3.face = nf1
            nh3.twin = nh4

            # Dreieck/Fläche nf2
            h5.next = nh5
            nh5.next = h4

            h4.face = nf2
            h5.face = nf2
            nh5.face = nf2

            nh5.twin = nh6

            # Dreieck/Fläche nf3
            nh2.next = nh4
            nh4.next = nh6
            nh6.next = nh2

            nh2.twin = nh1
            nh4.twin = nh3
            nh6.twin = nh5

            nh2.face = nf3
            nh4.face = nf3
            nh6.face = nf3

            # first round extra step:
            if isFirst:
                m1 = Vertex((v2.coords + v4.coords) / 2)
                m2 = Vertex((v4.coords + v6.coords) / 2)
                m3 = Vertex((v6.coords + v2.coords) / 2)

                m1.coords = self._move_on_Sphere(m1.coords)
                m2.coords = self._move_on_Sphere(m2.coords)
                m3.coords = self._move_on_Sphere(m3.coords)

                self.add_vertices([m1, m2, m3])

                u1 = HalfEdge(m1)
                u2 = HalfEdge(m1)

                nh3.next = u1
                nh4.next = u2
                u2.next = nh6
                u1.next = h2

                u1.twin = nh4
                nh4.twin = u1

                u2.twin = nh3
                nh3.twin = u2

                u3 = HalfEdge(m2)
                u4 = HalfEdge(m2)

                nh6.next = u4
                nh5.next = u3
                u4.next = nh2
                u3.next = h4

                u3.twin = nh6
                nh6.twin = u3

                u4.twin = nh5
                nh5.twin = u4

                u5 = HalfEdge(m3)
                u6 = HalfEdge(m3)

                nh2.next = u6
                nh1.next = u5
                u6.next = nh4
                u5.next = h6

                u5.twin = nh2
                nh2.twin = u5

                u6.twin = nh1
                nh1.twin = u6

                self.add_edges([u1, u2, u3, u4, u5, u6])

                n1 = HalfEdge(m1)
                n2 = HalfEdge(m3)
                n3 = HalfEdge(m2)
                n4 = HalfEdge(m1)
                n5 = HalfEdge(m3)
                n6 = HalfEdge(m2)

                self.add_edges([n1, n2, n3, n4, n5, n6])

                n1.twin = n2
                n2.twin = n1
                n3.twin = n4
                n4.twin = n3
                n5.twin = n6
                n6.twin = n5

                n2.next = n4
                n4.next = n6
                n6.next = n2

                n1.next = u6
                nh4.next = n1

                n3.next = u2
                nh6.next = n3

                n5.next = u4
                nh2.next = n5

                w1 = HalfEdge(v1)
                w2 = HalfEdge(m3)
                w3 = HalfEdge(v3)
                w4 = HalfEdge(m1)
                w5 = HalfEdge(v5)
                w6 = HalfEdge(m2)

                self.add_edges([w1, w2, w3, w4, w5, w6])

                w1.twin = w2
                w2.twin = w1
                w3.twin = w4
                w4.twin = w3
                w5.twin = w6
                w6.twin = w5

                w1.next = u5
                h6.next = w1

                w2.next = h1
                nh1.next = w2

                w3.next = u1
                h2.next = w3

                w4.next = h3
                nh3.next = w4

                w5.next = u3
                h4.next = w5

                w6.next = h5
                nh5.next = w6

                nh1.face = f
                w2.face = f

                w3.face = nf1
                u1.face = nf1

                w5.face = nf2
                u3.face = nf2

                n5.face = nf3
                u4.face = nf3

                t1 = Face(w1)
                w1.face = t1
                u5.face = t1
                h6.face = t1

                t2 = Face(u6)
                u6.face = t2
                nh4.face = t2
                n1.face = t2

                t3 = Face(w4)
                w4.face = t3
                h3.face = t3
                nh3.face = t3

                t4 = Face(n2)
                n2.face = t4
                n4.face = t4
                n6.face = t4

                t5 = Face(u2)
                u2.face = t5
                nh6.face = t5
                n3.face = t5

                t6 = Face(w6)
                w6.face = t6
                h5.face = t6
                nh5.face = t6

                newFaces.extend([t1, t2, t3, t4, t5, t6])

        self.add_faces(newFaces)

    def get_line_trace(self, color: str) -> go.Scatter3d:
        return super().get_line_trace(color=color, name=self.name)
