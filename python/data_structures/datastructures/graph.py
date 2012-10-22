#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4


class MissingVertexException(Exception):
    pass

class MissingEdgeException(Exception):
    pass

class DuplicateEdgeException(Exception):
    pass

class DuplicateVertexException(Exception):
    pass

class Vertex(object):
    def __init__(self, label):
        """
            This label can be anything hashable.
        """
        # If this is not hashable, this is going to collapse like a
        # house of cards.
        try:
            test_hash = hash(label)
        except TypeError:
            raise TypeError("Unhashable type %s is not appropriate for a Vertex label. Value: %s"\
                    % (label.__class__.__name__, label))

        self.__label = label
    
    def __repr__(self):
        return "Vertex %s" % self.label
   
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.label)

    @property
    def label(self):
        return self.__label

class Edge(tuple):
    
    def __new__(cls, vertex1, vertex2):
        return tuple.__new__(cls, (vertex1, vertex2))
    
    def __repr__(self):
        return "Edge from %s to %s" % (repr(self[0]), repr(self[1]))
   
    def __hash__(self):
        return hash(self[0]) + hash(self[1])

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    @property
    def inverse(self):
        return Edge(self[1],self[0])

    @property
    def vertices(self):
        return self[0], self[1]

    def __eq__(self, other):
        if tuple(other) == tuple(self):
            return True
        elif tuple(other) == tuple(self.inverse):
            return True
        else: 
            return False
    
class Graph(object):
    """
        This class represents a basic unweighted graph,
        undirected graph.
    """
    def __init__(self, label, vertices=None, edges=None):
        """
            Create a new graph, possibly with initial lists
            of Edges and Vertexes. 

        """
        self.__label = label
        self.__vertices = set() 
        self.__edges = set()
   
        if vertices:
            [self.add_vertex(vertex) for vertex in vertices]
        
        if edges:
            for edge in edges:
                vertex1, vertex2 = edge.vertices
                if vertex1 in self.vertices and \
                        vertex2 in self.vertices:
                    self.add_edge(edge)
                else:
                    raise MissingVertexException("%s is not a valid Edge for this graph." % (edge,))
    @property
    def vertices(self):
        return self.__vertices

    @property
    def edges(self):
        return self.__edges

    @property
    def label(self):
        return self.__label

    def add_vertex(self, vertex):
        """
            Add a vertex to this graph. This vertex must not already exist.
        """
        if vertex not in self.vertices:
            self.__vertices.add(vertex)
        else:
            raise DuplicateVertexException("%s already exists in %s" % (vertex, self))

    def add_edge_by_vertices(self, vertex1, vertex2):
        """
            Add an edge to this graph between vertex1 and vertex2. These vertices  must
            already exist in this graph and the edge must not already exist.
        """
        new_edge = Edge(vertex1, vertex2)
        self.add_edge(new_edge)

    def add_edge(self, edge):
        """
            Add an edge to this graph. The vertices that this edge connects 
            must already exist in this graph and the edge must not already exist.
        """
        vertex1, vertex2 = edge.vertices
        if vertex1 not in self.vertices:
            raise MissingVertexException("%s is not in %s" % (vertex1, self))
        elif vertex2 not in self.vertices:
            raise MissingVertexException("%s is not in %s" % (vertex2, self))
        
        if edge not in self.edges:
            self.__edges.add(edge)
        else:
            raise DuplicateEdgeException("%s already exists in %s" % (edge, self))

    def get_edge_by_vertices(self, vertex1, vertex2):
        """
            Get the edge between vertex1 and vertex2 if it exists.
        """
        edge = Edge(vertex1, vertex2)
        return self.get_edge(edge)

    def get_edge(self, edge):
        """
            Get the named edge. This is really more useful as a test for existence.
        """
        if edge in self.edges: 
            return edge
        elif edge.inverse in self.edges:
            return edge
        else:
            raise MissingEdgeException("%s does not exist in %s" % (edge, self)) 
    
    def remove_edge(self, edge):
        """
            Use this method to remove an edge from the graph.
        """
        if edge in self.edges:
            self.__edges.remove(edge)
        elif edge.inverse in self.edges:
            self.__edges.remove(edge.inverse)
        else:
            raise MissingEdgeException("%s does not exist in %s" % (edge, self))
         
    def remove_vertex(self, vertex):
        """
            Use this method to remove a vertex from the graph.
            It will also remove all edges that reference it.
        """
        # Find all references to this vertex in this graph's edges.
        # Slow slow slow slow slow, must find different way of doing this.
        bad_edges = filter(lambda x: vertex in x.vertices, self.edges)
        [self.edges.remove(edge) for edge in bad_edges]
        
        # Remove the vertex itself.
        if  vertex in self.__vertices: 
          self.__vertices.remove(vertex)
        else:
            raise MissingVertexException("%s does not exist in %s" % (vertex, self))

    def adjacent_vertices(self, vertex):
        """
           Use this method to get a iterator yielding vertices that
           are connected to this vertex.
        """
        def get_other_vertex(edge):
            vertex1, vertex2 = edge.vertices
            return vertex1 if vertex == vertex2 else vertex2

        from itertools import imap

        return imap(get_other_vertex,self.connected_edges(vertex))
        
    def connected_edges(self, vertex):
        """
            Use this method to get an iterator yielding
            edges that are connected to this vertex.
        """
        from itertools import ifilter
       
        # Scope, don't fail me now.
        return ifilter(lambda x: vertex in x.vertices, self.edges)

    def is_connected(self):
       """
            Use this method to determine whether this graph is connected.
            A graph is connected if there's an edge from every vertex to every 
            other vertex.
       """
        # Okay. The way I wrote this, we can make some assumptions.
        # 1. Each vertex must be unique. (Labelwise, not just by memory address)
        # 2. Edges contain unique vertices are are defined by their
        # vertices, so they are also unique.
        # Thus We should be able to count the number of edges coming from
        # each vertex and determine whether or not this graph is connected.
        #
        # Hurray for avoiding BFS/DFS algorithms!
        # 
        # We can't do this with directed graphs, though :(
       pass

    def __repr__(self):
       """  
            Use this method to get a somewhat confusing textual output of vertices
            and edges connected to each vertex. 
       """
       return "Graph %s" % self.label
