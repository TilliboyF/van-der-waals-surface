import numpy as np
from Dcel import DCEL,  HalfEdge, Intersection_Data, Vertex
from IntersectionPlane import Intersection_Plane
from Common import Insert_Cases, Multi_Vertex_Edge, Position_Cases
from Sphere import Sphere
import plotly.graph_objects as go

class Intersection_Circle(DCEL):

    def __init__(self, plane: Intersection_Plane, name:str = "") -> None:
        super().__init__(center=plane.p)
        self.plane: Intersection_Plane = plane
        self.name = name

    def calc_intersection_points(self, insert: bool = True):
        s1: Sphere = self.plane.s1
        s2: Sphere = self.plane.s2

        s1_points = s1.calc_intersections(self.plane,plane_side_val=-1, insert=insert)
        s2_points = s2.calc_intersections(self.plane,plane_side_val=1, insert=insert)

        self.vertices= s1_points + s2_points

    def sort_intersection_points(self) -> None:
        if len(self.vertices) == 0:
            print("vertecies len 0")
            return
        N = [self.plane.alpha, self.plane.beta, self.plane.gamma]
        # V1 = self.plane.find_point_on_plane() - self.center
        V1 = self.vertices[0].coords - self.center
        V2 = np.cross(N, V1)

        N1 = V1 / np.linalg.norm(V1)
        N2 = V2 / np.linalg.norm(V2)

        # T = np.transpose([N1, N2])

        for p in self.vertices:
            coords_2d = [N1[0] * p.coords[0] + N1[1] * p.coords[1] + N1[2] * p.coords[2],
                        N2[0] * p.coords[0] + N2[1] * p.coords[1] + N2[2] * p.coords[2]]
            p.intersection_data.angle = np.arctan2(coords_2d[0], coords_2d[1])

        self.vertices.sort()

    def insert_circle(self) -> list[Multi_Vertex_Edge]:
        multi_edges: list[Multi_Vertex_Edge] = []

        for i in range(len(self.vertices)):
            v1 = self.vertices[i]
            last_insert = ((i+1) % len(self.vertices)) == 0
            first_insert = i == 0
            v2 = self.vertices[(i+1) % len(self.vertices)]

            e1 = HalfEdge(v1)
            e2 = HalfEdge(v2)

            e1.twin = e2
            e2.twin = e1

            insert_case: Insert_Cases = Insert_Cases.LAST if last_insert else Insert_Cases.FIRST if first_insert else Insert_Cases.NORMAL


            v1_side_value: float = self.plane.side_check(v1.edge.twin.origin.coords)
            v2_side_value: float = self.plane.side_check(v2.edge.twin.origin.coords)

            position_case: Position_Cases = None
            if v1_side_value > 0 and v2_side_value < 0:
                position_case = Position_Cases.V1_POS_V2_NEG
            elif v1_side_value < 0 and v2_side_value > 0:
                position_case = Position_Cases.V1_NEG_V2_POS
            elif v1_side_value < 0 and v2_side_value < 0:
                position_case = Position_Cases.V1_NEG_V2_NEG
            else:
                position_case = Position_Cases.V1_POS_V2_POS

            if (v1.intersection_data != None and v1.intersection_data.is_Multi) and (v2.intersection_data != None and v2.intersection_data.is_Multi):
                continue
            elif (v1.intersection_data != None and v1.intersection_data.is_Multi):
                if v1.edge.twin.next == v1.edge:
                    insert_case = Insert_Cases.FIRST
                    print("Case: First")
                else:
                    insert_case = Insert_Cases.NORMAL
                    print("Case: Normal")
                multi_edges.append(Multi_Vertex_Edge(v1,e1))
            elif (v2.intersection_data != None and v2.intersection_data.is_Multi):
                if v2.edge.twin.next == v2.edge:
                    insert_case = Insert_Cases.NORMAL
                    print("Case: Normal")
                else:
                    insert_case = Insert_Cases.LAST
                    print("Case: Last")
                multi_edges.append(Multi_Vertex_Edge(v2,e2))

            self.handle_insert_case(v1=v1, v2=v2,
                                    e1=e1, e2=e2,
                                    insert_case=insert_case,
                                    position_case=position_case)


            self.edges.append(e1)
            self.edges.append(e2)

        return multi_edges

    def handle_insert_case(self, v1: Vertex, v2: Vertex, e1: HalfEdge, e2: HalfEdge, insert_case: Insert_Cases, position_case: Position_Cases ) -> None:
        if position_case is Position_Cases.V1_POS_V2_NEG:
            if insert_case is Insert_Cases.NORMAL:
                e2.next = v1.edge.twin.next
                e1.next = v2.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next = e1
            elif insert_case is Insert_Cases.FIRST:
                e2.next = v1.edge
                e1.next = v2.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next = e1
            elif insert_case is Insert_Cases.LAST:
                e2.next = v1.edge.twin.next
                e1.next = v2.edge.twin.next
                v2.edge.twin.next = e2
                v1.edge.twin.next = e1
        elif position_case is Position_Cases.V1_NEG_V2_POS:
            if insert_case is Insert_Cases.NORMAL:
                e2.next = v1.edge
                e1.next = v2.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next.twin.next = e1
            elif insert_case is Insert_Cases.FIRST:
                e2.next = v1.edge
                e1.next = v2.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next = e1
            elif insert_case is Insert_Cases.LAST:
                e2.next = v1.edge
                e1.next = v2.edge
                v2.edge.twin.next.twin.next = e2
                v1.edge.twin.next.twin.next = e1
        elif position_case is Position_Cases.V1_NEG_V2_NEG:
            if insert_case is Insert_Cases.NORMAL:
                e1.next = v2.edge
                e2.next = v1.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next.twin.next = e1
            elif insert_case is Insert_Cases.FIRST:
                e1.next = v2.edge
                e2.next = v1.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next = e1
            elif insert_case is Insert_Cases.LAST:
                e1.next = v2.edge.twin.next
                e2.next = v1.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next.twin.next = e1
        elif position_case is Position_Cases.V1_POS_V2_POS:
            if insert_case is Insert_Cases.NORMAL:
                e2.next = v1.edge.twin.next
                e1.next = v2.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next = e1
            elif insert_case is Insert_Cases.FIRST:
                e2.next = v1.edge
                e1.next = v2.edge
                v2.edge.twin.next = e2
                v1.edge.twin.next = e1
            elif insert_case is Insert_Cases.LAST:
                e2.next = v1.edge.twin.next
                e1.next = v2.edge
                v2.edge.twin.next.twin.next = e2
                v1.edge.twin.next = e1

    def connect_normal_cases(self, v1: Vertex, v2: Vertex, e1:HalfEdge, e2: HalfEdge, first_insert:bool, last_insert:bool) -> None:
        v1_side = self.plane.side_check(v1.intersection_data.owner.center)
        v2_side = self.plane.side_check(v2.intersection_data.owner.center)

        if (v1_side > 0 and v2_side > 0) or (v1_side < 0 and v2_side < 0):  # both from same sphere
            if v1_side < 0 and v2_side < 0:  # both from s1
                if last_insert:  # last
                    e1.next = v2.edge.twin.next
                    e2.next = v1.edge
                    v2.edge.twin.next = e2
                    v1.edge.twin.next.twin.next = e1
                elif first_insert:  # first
                    e1.next = v2.edge
                    e2.next = v1.edge
                    v2.edge.twin.next = e2
                    v1.edge.twin.next = e1
                else:  # normal
                    e1.next = v2.edge
                    e2.next = v1.edge
                    v2.edge.twin.next = e2
                    v1.edge.twin.next.twin.next = e1
            else:
                if last_insert:  # last
                    e2.next = v1.edge.twin.next
                    e1.next = v2.edge
                    v2.edge.twin.next.twin.next = e2
                    v1.edge.twin.next = e1
                elif first_insert:  # first
                    e2.next = v1.edge
                    e1.next = v2.edge
                    v2.edge.twin.next = e2
                    v1.edge.twin.next = e1
                else:  # normal
                    e2.next = v1.edge.twin.next
                    e1.next = v2.edge
                    v2.edge.twin.next = e2
                    v1.edge.twin.next = e1
        else:
            if v1_side > 0 and v2_side < 0:  # v1 blue, v2 red
                if last_insert:  # last
                    e2.next = v1.edge.twin.next
                    e1.next = v2.edge.twin.next
                    v2.edge.twin.next = e2
                    v1.edge.twin.next = e1
                elif first_insert:  # first
                    e2.next = v1.edge
                    e1.next = v2.edge
                    v2.edge.twin.next = e2
                    v1.edge.twin.next = e1
                else:  # normal
                    e2.next = v1.edge.twin.next
                    e1.next = v2.edge
                    v2.edge.twin.next = e2
                    v1.edge.twin.next = e1
            else:  # v1 red, v2 blue
                if last_insert:  # last
                    e2.next = v1.edge
                    e1.next = v2.edge
                    v2.edge.twin.next.twin.next = e2
                    v1.edge.twin.next.twin.next = e1
                elif first_insert:  # first
                    e2.next = v1.edge
                    e1.next = v2.edge
                    try:
                        v2.edge.twin.next = e2
                    except AttributeError as e:
                        print(e)
                    v1.edge.twin.next = e1
                else:  # normal
                    e2.next = v1.edge
                    e1.next = v2.edge
                    v2.edge.twin.next = e2
                    v1.edge.twin.next.twin.next = e1

    def fix_circle(self) -> None:

        vertices_to_remove: list[Vertex] = []

        avg = self.get_average_distance()

        # Merge points if needed
        DELTA = avg * 0.9
        i = 0
        while (i < len(self.vertices)):

            v1 = self.vertices[i]
            v2 = self.vertices[(i+1) % len(self.vertices)]

            d = np.linalg.norm(v2.coords - v1.coords)
            if d < DELTA and v1.intersection_data.isMerged == False and v2.intersection_data.isMerged == False and v1.intersection_data.is_Multi == False and v2.intersection_data.is_Multi == False:
                self.merge(v1,v2)
                v1.intersection_data.isMerged = True
                v2.intersection_data.isMerged = True

                vertices_to_remove.append(v2) # v2 wird immer entfernt

                i += 2
            else:
                i += 1

        for p in vertices_to_remove:
            self.vertices.remove(p)

    def get_average_distance(self) -> float:
        sum = 0
        count = 0
        for i in range(len(self.vertices)):
            v1 = self.vertices[0]
            v2 = self.vertices[(i+1) % len(self.vertices)]

            if v1.intersection_data.is_Multi == True and v2.intersection_data.is_Multi == True:
                continue

            d = np.linalg.norm(v2.coords - v1.coords)
            sum += d
            count += 1

            print("Average distance: ", sum/count)
            return sum/count

    def merge(self, v1: Vertex, v2: Vertex):
        v1_side_val = self.plane.side_check(v1.edge.twin.origin.coords)
        v2_side_val = self.plane.side_check(v2.edge.twin.origin.coords)

        if (v1_side_val > 0 and v2_side_val > 0) or (v1_side_val < 0 and v2_side_val < 0):  # both from same sphere
            if v1_side_val < 0 and v2_side_val < 0:  # both from s1
                self.mergeRedRed(v1,v2)
            else: # both from s2
                self.mergeBlueBlue(v1,v2)
        else:
            if v1_side_val > 0 and v2_side_val < 0:  # v1 blue, v2 red
                self.mergeBlueRed(v1,v2)
            else:  # v1 red, v2 blue
                self.mergeRedBlue(v1,v2)

    def mergeRedRed(self, v1: Vertex, v2: Vertex):
        # find case
        if (v1.edge.next.origin == v2.edge.next.origin): # Case Dreieck

            e1 = v1.edge
            e2 = e1.next

            r_e1 = e1.twin.next.twin.next
            r_e2 = r_e1.twin

            # entferne e1 und e2
            v1.intersection_data.owner.edges.remove(e1)
            v1.intersection_data.owner.edges.remove(e2)

            # verschiebe v1
            v1.coords = (v1.coords + v2.coords)/2
            v1.edge = e2.twin

            # korrigiere next
            e1.twin.next.twin.next = r_e1.next

            # korrigiere origins
            e2.twin.origin = v1
            r_e1.next.origin = v1

            # korrigiere twins
            e1.twin.twin = e2.twin
            e2.twin.twin = e1.twin

            self.edges.remove(r_e1)
            self.edges.remove(r_e2)

        else: # Case Viereck

            e1 = v1.edge
            e2 = v2.edge

            r_e1 = e1.twin.next.twin.next
            r_e2 = r_e1.twin

            # V1 verschieben
            v1.coords = (v1.coords + v2.coords)/2
            v1.edge = e2

            # korrigiere next
            e2.twin.next = e1
            e1.twin.next.twin.next = r_e1.next

            # korrigiere origin
            e2.origin = v1
            r_e1.next.origin = v1

            self.edges.remove(r_e1)
            self.edges.remove(r_e2)

    def mergeBlueBlue(self, v1: Vertex, v2: Vertex):
        # find case
        if (v1.edge.next.origin == v2.edge.next.origin): # Case Dreieck

            e1 = v1.edge
            e2 = v2.edge

            r_e1 = e2.twin.next.twin.next
            r_e2 = r_e1.twin

            # delete e2 and e2.next
            v1.intersection_data.owner.edges.remove(e2)
            v1.intersection_data.owner.edges.remove(e2.next)

            # V1 verschieben
            v1.coords = (v1.coords + v2.coords)/2
            v1.edge = e1

            # korrigiere next
            e2.twin.next.twin.next = r_e1.next

            # korrigiere origins
            e2.twin.next.origin = v1

            # korrigiere twins
            e1.twin = e2.twin
            e2.twin.twin = e1

            self.edges.remove(r_e1)
            self.edges.remove(r_e2)

        else: # Case Viereck

            e1 = v1.edge
            e2 = v2.edge

            r_e2 = e1.twin.next
            r_e1 = r_e2.twin

            # verschiebe V1
            v1.coords = (v1.coords + v2.coords)/2

            # korrigiere next
            e1.twin.next = e2
            e2.twin.next.twin.next = r_e1.next

            # korrigiere origin
            e2.origin = v1
            e2.twin.next.origin = v1

            self.edges.remove(r_e1)
            self.edges.remove(r_e2)

    def mergeBlueRed(self, v1: Vertex, v2: Vertex):

        e1 = v1.edge
        e2 = v2.edge

        r_e1 = e2.twin.next
        r_e2 = r_e1.twin

        # v1 verschieben
        v1.coords = (v1.coords + v2.coords)/2

        # korrigiere next
        e2.twin.next = r_e1.next
        e1.twin.next = r_e2.next

        # korrigiere origin
        e2.origin = v1
        r_e2.next.origin = v1

        self.edges.remove(r_e1)
        self.edges.remove(r_e2)

        v1.intersection_data.extra_edge = e2

    def mergeRedBlue(self, v1: Vertex, v2: Vertex):
        # definiere Variablen

            e1 = v1.edge
            e2 = v2.edge

            r_e1 = e2.twin.next.twin.next
            r_e2 = r_e1.twin

            # v1 verschieben
            v1.coords = (v1.coords + v2.coords)/2

            # korrigiere next
            e1.twin.next.twin.next = e2
            e2.twin.next.twin.next = e1

            # korrigiere origin
            e2.origin = v1
            e2.twin.next.origin = v1

            self.edges.remove(r_e1)
            self.edges.remove(r_e2)

            v1.intersection_data.extra_edge = e2

    def alt_triangulate(self) -> None:
        for edge in self.edges:
            edges = self.find_all_edges(edge)
            if len(edges) > 2:
                self.triangulate_helper(edges)

    def triangulate_helper(self, edges: list[HalfEdge]) -> None:
        counter = 0
        while(edges[1].origin.intersection_data is not None):
            if counter > 10:
                print("Case rotate does not work!", edges)
                return
            first = edges.pop(0)
            edges.append(first)
            counter += 1

        # irgendwie die seite finden
        x = y = z = 0
        for edge in edges:
            x += edge.origin.coords[0]
            y += edge.origin.coords[1]
            z += edge.origin.coords[2]
        m = [x/len(edges), y/len(edges), z/len(edges)]

        m_side = self.plane.side_check(m)
        s1_side = self.plane.side_check(self.plane.s1.center)

        if (m_side < 0 and s1_side < 0) or (m_side > 0 and s1_side > 0):
            self.triangulate(edges=edges, dcel=self.plane.s1)
        else:
            self.triangulate(edges=edges, dcel=self.plane.s2)

    def find_all_edges(self, start_edge: HalfEdge) -> list[HalfEdge]:
        edges = [start_edge]
        next = start_edge.next
        MAX_ITERATIONS = 10
        counter = 0
        while next.origin is not start_edge.origin:
            if counter > MAX_ITERATIONS:
                print("maxed out finding")
                return []
            edges.append(next)
            next = next.next
            counter += 1

        # for edge in edges:
        #     if edge.origin.intersection_data is not None and edge.origin.intersection_data.is_Multi:
        #         return []

        return edges

    def triangulate(self, edges: list[HalfEdge], dcel: DCEL):
            # print("triangulate", len(edges))
            if len(edges) > 3:
                # definiere Variablen

                e_second = edges[1]
                e_first = edges.pop(0)
                e_last = edges.pop(-1)

                # neue Kanten erstellen
                h1 = HalfEdge(origin=e_second.origin)
                h2 = HalfEdge(origin=e_last.origin)

                # setze twin
                h1.twin = h2
                h2.twin = h1

                # setze next
                e_first.next = h1
                h1.next = e_last

                edges[-1].next = h2
                h2.next = e_second

                # h1 und h2 in s einfügen
                dcel.add_edge(h1)
                dcel.add_edge(h2)

                # h2 in liste setzen, damit algo rekursiv weiter laufen kann
                edges.insert(0,h2)

                self.triangulate(edges, dcel)

    def get_circle_traces(self, color: str) -> go.Scatter3d:
        return super().get_line_trace(color, self.name)

    def get_point_traces(self, color: str) -> go.Scatter3d:
        return super().get_point_trace(color, self.name)

    def remove_part(self, plane: Intersection_Plane, circle: bool = False) -> None:
        return super().remove_part(plane=plane,plane_side_val= -1 ,circle=True)

    def remove_points(self, plane: Intersection_Plane, plane_side_val: float) -> None:

        keep_points: list[Vertex] = []
        remove_points: list[Vertex] = []
        for v in self.vertices:
            if v.intersection_data != None and v.intersection_data.is_Multi:
                keep_points.append(v)
                continue
            else:
                v_val = plane.side_check(v.coords)

                if (plane_side_val < 0 and v_val < 0) or (plane_side_val > 0 and v_val > 0):
                    keep_points.append(v)
                    continue
            remove_points.append(v)
        for v in remove_points:
            v.intersection_data = None

        self.vertices = keep_points
