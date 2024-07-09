from Dcel import DCEL, Vertex, HalfEdge, Face
import numpy as np


def build(c: list[float] = [0,0,0], r: float = 1.0) -> DCEL:
    dcel = DCEL()

    vertices = _get_tetraeder_points(c,r)

    p1 = Vertex(vertices[0])
    p2 = Vertex(vertices[1])
    p3 = Vertex(vertices[2])
    p4 = Vertex(vertices[3])

    # Dreieck 1
    greenE1 = HalfEdge(p2)
    greenE2 = HalfEdge(p1)
    greenE3 = HalfEdge(p4)

    greenE1.next = greenE2
    greenE2.next = greenE3
    greenE3.next = greenE1

    # Dreieck 2
    redE1 = HalfEdge(p2)
    redE2 = HalfEdge(p4)
    redE3 = HalfEdge(p3)

    redE1.next = redE2
    redE2.next = redE3
    redE3.next = redE1

    # Dreieck 3
    blueE1 = HalfEdge(p4)
    blueE2 = HalfEdge(p1)
    blueE3 = HalfEdge(p3)

    blueE1.next = blueE2
    blueE2.next = blueE3
    blueE3.next = blueE1

    # Dreieck 4
    orangeE1 = HalfEdge(p1)
    orangeE2 = HalfEdge(p2)
    orangeE3 = HalfEdge(p3)

    orangeE1.next = orangeE2
    orangeE2.next = orangeE3
    orangeE3.next = orangeE1

    # ausgehende Kanten für Ecken und in dcel einfügen
    p1.edge = orangeE1
    p2.edge = greenE1
    p4.edge = blueE1
    p3.edge = redE3

    dcel.add_vertex(p1)
    dcel.add_vertex(p2)
    dcel.add_vertex(p3)
    dcel.add_vertex(p4)

    # twins richtig setzen
    greenE1.twin = orangeE1
    orangeE1.twin = greenE1

    greenE2.twin = blueE1
    blueE1.twin = greenE2

    greenE3.twin = redE1
    redE1.twin = greenE3

    orangeE2.twin = redE3
    redE3.twin = orangeE2

    orangeE3.twin = blueE2
    blueE2.twin = orangeE3

    redE2.twin = blueE3
    blueE3.twin = redE2

    # Alle halfedges zur dcel hinzufügen
    dcel.add_edge(greenE1)
    dcel.add_edge(greenE2)
    dcel.add_edge(greenE3)
    dcel.add_edge(orangeE1)
    dcel.add_edge(orangeE2)
    dcel.add_edge(orangeE3)
    dcel.add_edge(redE1)
    dcel.add_edge(redE2)
    dcel.add_edge(redE3)
    dcel.add_edge(blueE1)
    dcel.add_edge(blueE2)
    dcel.add_edge(blueE3)

    # Faces
    face1 = Face(orangeE1)
    face2 = Face(greenE1)
    face3 = Face(blueE1)
    face4 = Face(redE1)

    greenE1.face = face2
    greenE2.face = face2
    greenE3.face = face2

    orangeE1.face = face1
    orangeE2.face = face1
    orangeE3.face = face1

    redE1.face = face4
    redE2.face = face4
    redE3.face = face4

    blueE1.face = face3
    blueE2.face = face3
    blueE3.face = face3

    dcel.add_face(face1)
    dcel.add_face(face2)
    dcel.add_face(face3)
    dcel.add_face(face4)

    return dcel

def _get_tetraeder_points(c: list[float], r: float) -> list[list[float]]:
  a = 1  # initiale Größe
  p1 = np.array([0, 0, 0])
  p2 = np.array([a, 0, 0])
  p3 = np.array([a / 2, a * np.sqrt(3) / 2, 0])
  p4 = np.array([a / 2, a * np.sqrt(1 / 12), a * np.sqrt(2 / 3)])

  # Zentrum der Punkte
  center = (p1 + p2 + p3 + p4) / 4

  # Punkte auf 0,0,0 schieben
  adjusted_points = [p - center for p in [p1, p2, p3, p4]]
  # Punkte auf Radius der Kugel setzen
  vertices = [(np.array(c) + (r / np.linalg.norm(pt)) * pt) for pt in adjusted_points]
  return vertices
