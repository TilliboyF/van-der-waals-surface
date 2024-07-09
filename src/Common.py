from enum import Enum
import plotly.graph_objects as go


def plot(data: list[go.Scatter3d]) -> None:
    """
    Hilsmethode, die einen Plot erstellt
    """
    fig = go.Figure(data=data)

    fig.update_layout(
        paper_bgcolor="rgb(255,255,255)",
        plot_bgcolor="rgb(0,0,0)",
        scene=dict(
            xaxis=dict(showbackground=True, showticklabels=True, visible=False),
            yaxis=dict(showbackground=True, showticklabels=True, visible=False),
            zaxis=dict(showbackground=True, showticklabels=True, visible=False),
        ),
    )

    fig.show(renderer="browser")


class Insert_Cases(Enum):
    NORMAL = 0
    FIRST = 1
    LAST = 2


class Position_Cases(Enum):
    V1_POS_V2_NEG = 0
    V1_NEG_V2_POS = 1
    V1_NEG_V2_NEG = 2
    V1_POS_V2_POS = 3
