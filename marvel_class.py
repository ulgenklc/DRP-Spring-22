#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# In[2]:


class marvel_network:
    def __init__(self, pd):
        self.nx_object = self.createGraphFromDataFrame(pd)
        self.matrix = self.createAdjacencyMatrix(self.nx_object)
        self.size = self.matrix.shape[0]
        self.name = [(i,e) for i,e in enumerate(set(list(pd['source'])+list(pd['target'])))]
        self.pos = nx.random_layout(self.nx_object)
        
    def createGraphFromDataFrame(self, df):
        marvel_graph = nx.DiGraph() # this creates a directed graph object

        list_ = []

        # This loop creates the edges for the plot & appends them to a list
        for index, row in df.iterrows():
            list_.append((row["source"] , row["target"]))

        marvel_graph.add_edges_from(list_)

        return marvel_graph
    
    def createAdjacencyMatrix(self, graph):
        marvel_adj = nx.to_numpy_array(graph) # This creates the adjacency array for the digraph
        return marvel_adj
    
    def neighbors(self, node_id):
        """
        Helper function for finding the neighbors of a given node.
        
        Parameters
        -----------
        node_id: int
            ID of the node to be found the neighbors of.
            
        Return
        -----------
        neighbors: list
            list of node IDs of the neighbors of ``node_id``.
        """
        
        if node_id > self.size: 
            return('Invalid node ID')
        neighbors = []
        
        for i,e in enumerate(self.matrix[node_id]):
            if e == 1:
                neighbors.append(i)
        return(neighbors)
    
    # Number of degrees

    def degreeCentrality(self): # method is type of centrality
        return nx.degree_centrality(self.nx_object)
    def closenessCentrality(self):
        return nx.closeness_centrality(self.nx_object)
    def globalreachingCentrality(self):
        return nx.global_reaching_centrality(self.nx_object)
    def eigenvectCentrality(self):
        return nx.eigenvector_centrality(self.nx_object)
    
    # Creating edges
    def visualizeGraph(self, rankingType = 'degree'):
        new_pos = {}
        for vals in self.pos.items():
            new_pos.update({vals[0]: {"pos": list(vals[1])}})
        nx.set_node_attributes(self.nx_object, new_pos)

        edge_x = []
        edge_y = []

        for edge in self.nx_object.edges():
            x0, y0 = self.nx_object.nodes[edge[0]]['pos']
            x1, y1 = self.nx_object.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in self.nx_object.nodes():
            x, y = self.nx_object.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)

        node_text = []
        for node in self.nx_object.nodes:
            node_text.append(node)


        colorList = []
        if rankingType == 'degree':
            centralities = self.degreeCentrality()
        elif rankingType == 'closeness':
            centralities = self.closenessCentrality()
        elif rankingType == 'globalreach':
            centralities = self.globalreachingCentrality()
        elif rankingType == 'eigenvector':
            centralities = self.eigenvectCentrality()
        
        for i in self.nx_object.nodes:
            colorList.append(centralities[i])

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color= colorList,
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))
        node_trace.text = node_text


        # Creating Viz
        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title='<br>Marvel Character Representation',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        return fig


# In[ ]:




