from enum import Enum
from Dcel import HalfEdge, Vertex
import plotly.graph_objects as go
import numpy as np

class Multi_Vertex_Edge:
    def __init__(self, vertex: Vertex, edge: HalfEdge):
        self.vertex = vertex
        self.edge = edge


def plot(data: list[go.Scatter3d]) -> None:
    fig = go.Figure(data=data)

    fig.update_layout(
    paper_bgcolor='rgb(255,255,255)',
    plot_bgcolor='rgb(0,0,0)',
    scene=dict(
        xaxis=dict(showbackground=True, showticklabels=True, visible=False),
        yaxis=dict(showbackground=True, showticklabels=True, visible=False),
        zaxis=dict(showbackground=True, showticklabels=True, visible=False), ))

    fig.show(renderer="browser")

def get_vector(edge: HalfEdge) -> list[float]:
    v1 = edge.origin.coords
    v2 = edge.next.origin.coords
    return v2 - v1

def get_angle(e1: list[float], e2: list[float]) -> float:
    return np.arccos((np.dot(e1, e2))/(np.linalg.norm(e1) * np.linalg.norm(e2)))

class Insert_Cases(Enum):
    NORMAL = 0
    FIRST = 1
    LAST = 2

class Position_Cases(Enum):
    V1_POS_V2_NEG = 0
    V1_NEG_V2_POS = 1
    V1_NEG_V2_NEG = 2
    V1_POS_V2_POS = 3
