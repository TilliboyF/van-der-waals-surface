import numpy as np


class Plane:
    """
    Klasse einer Ebene
    """

    def __init__(self):
        self.p: list[float] = []
        self.alpha: float = 0
        self.beta: float = 0
        self.gamma: float = 0
        self.delta: float = 0

    def set_plane(self, p: list[float], n: list[float]):
        self.p = p
        self.alpha = p[0] * n[0]
        self.beta = p[1] * n[1]
        self.gamma = p[2] * n[2]
        self.delta = p[0] * n[0] + p[1] * n[1] + p[2] * n[2]


class IntersectionPlane(Plane):
    """
    Klasse der Schnittebene
    """

    def __init__(self, s1: "Sphere", s2: "Sphere") -> None:
        super().__init__()
        self.s1: "Sphere" = s1
        self.s2: "Sphere" = s2
        self._calculate_plane(s1.center, s2.center, s1.r, s2.r)

    def _calculate_plane(
        self, c1: list[float], c2: list[float], r1: float, r2: float
    ) -> None:
        """
        Berechnet die Schnittebene
        """

        d = np.array(c2) - np.array(c1)
        length_of_d = np.linalg.norm(d)

        d1 = (r1**2 - r2**2 + length_of_d**2) / (2 * length_of_d)

        self.p = np.array(c1) + ((d1 / length_of_d) * d)

        self.alpha = d[0]
        self.beta = d[1]
        self.gamma = d[2]
        self.delta = d[0] * self.p[0] + d[1] * self.p[1] + d[2] * self.p[2]

    def calculate_intersection(self, v1: "Vertex", v2: "Vertex") -> float:
        """
        Berechnet, ob ein Kantenstück die Schnittebene schneidet:
            Wenn t >= 0 und t <= 1 -> Schnitt,
            sonst -> Kein Schnitt
        """
        v = v2.coords - v1.coords

        t = (
            self.delta
            - self.alpha * v1.coords[0]
            - self.beta * v1.coords[1]
            - self.gamma * v1.coords[2]
        )
        b = self.alpha * v[0] + self.beta * v[1] + self.gamma * v[2]

        if b == 0:
            if (
                self.alpha * v1.coords[0]
                + self.beta * v1.coords[1]
                + self.gamma * v1.coords[2]
                - self.delta
                == 0
            ):
                return v1.coords
            else:
                return 100

        return t / b

    def side_check(self, p: list[float]) -> float:
        """
        Der Seitentest der Ebene
        """
        return self.alpha * p[0] + self.beta * p[1] + self.gamma * p[2] - self.delta
