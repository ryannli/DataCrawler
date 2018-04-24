import igraph as ig
import json
import urllib.request as urllib2
import random
import math
from controller.graph_lib import construct_graph
from model.utils import get_readable_string_from_int
import plotly.plotly as py
import plotly
from plotly.graph_objs import *

# This script build 3d plot for actor and movie data by using igraph and plotly
# Tutorial from https://plot.ly/python/3d-network-graph/

ACTOR_FILE_PATH = '../data/actors_small.json'
MOVIE_FILE_PATH = '../data/movies_small.json'
with open(ACTOR_FILE_PATH, encoding='utf-8') as data_file:
    actor_data = json.load(data_file)
with open(MOVIE_FILE_PATH, encoding='utf-8') as data_file:
    movie_data = json.load(data_file)

# Step 1: Construct graph and collect useful information for plot
graph = construct_graph(actor_data, movie_data)
vertices = graph.get_all_vertices()
vertices_list = list(vertices.keys())
edges = graph.get_edges()
sources = [vertices_list.index(e[0]) for e in edges]
targets = [vertices_list.index(e[1]) for e in edges]

N = len(vertices)
# Gets edges paired list for igraph
ig_edges = [(sources[i], targets[i]) for i in range(len(edges))]
# Build graph from edges
G = ig.Graph(ig_edges, directed=False)
layt = G.layout('kk', dim=3)

# Collects useful information for plot
labels = [] # The text information about a vertex
group = []  # The group number for future coloring
sizes = []  # The size of the vertex for visualization
for node in vertices_list:
    if "age" in vertices[node].get_content():
        group.append(random.randint(0, 10))
        labels.append(node
                      + " -- " + "Age: " + str((vertices[node].get_content())['age']))
        sizes.append((vertices[node].get_content())['age']/2.5)
    else:
        group.append(random.randint(20, 30))
        labels.append(node
                      + " -- " + "Grossing: " + get_readable_string_from_int((vertices[node].get_content())['gross']))
        sizes.append(math.log(vertices[node].get_content()['gross']/1000000, 1.1) * 0.6)


# Step 2: Construct 3d plot
Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
Yn = [layt[k][1] for k in range(N)]  # y-coordinates of nodes
Zn = [layt[k][2] for k in range(N)]  # z-coordinates of nodes
Xe = []
Ye = []
Ze = []
for e in ig_edges:
    Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
    Ye += [layt[e[0]][1], layt[e[1]][1], None]  # y-coordinates of edge ends
    Ze += [layt[e[0]][2], layt[e[1]][2], None]  # z-coordinates of edge ends

# For edges
trace1 = Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=Line(color='rgb(125,125,125)', width=2),
                   )

# For vertices
trace2 = Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode='markers',
                   name='actors',
                   marker=Marker(symbol='dot',
                                 size=sizes,
                                 color=group,
                                 colorscale='Viridis',
                                 line=Line(color='rgb(50,50,50)', width=0.5)
                                 ),
                   text=labels,
                   hoverinfo='text'
                   )

axis = dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )

layout = Layout(
    title="Network of Actors and Movies Crawler Data <br> (3D visualization)",
    width=800,
    height=800,
    showlegend=False,
    scene=Scene(
        xaxis=XAxis(axis, showspikes=False),
        yaxis=YAxis(axis, showspikes=False),
        zaxis=ZAxis(axis, showspikes=False),
    ),
    margin=Margin(
        t=100
    ),
    hovermode='closest', )

# Combine edges and vertices
data = Data([trace1, trace2])

# Plot and save
plotly.offline.plot({
    "data": data,
    "layout": layout
})
