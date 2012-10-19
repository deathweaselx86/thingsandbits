#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4


class MissingVertexException(Exception):
    pass

class MissingEdgeException(Exception):
    pass


class Vertex(object):
    def __init__(self, label):
        """
            This label can be anything hashable.
        """
        # If this is not hashable 
        try:
            test_hash = hash(label)
        except TypeError:
            raise TypeError("Unhashable type %s is not appropriate for a Vertex label. Value: %s" % (label.__class__.__name__, label))

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
    # Does this create a tuple with new copies of the vertices?
    # TODO: Find a way to shallow copy and/or weakref the vertices
    # for this.
    def __new__(cls, vertex1, vertex2):
        return tuple.__new__(cls, (vertex1, vertex2))
    
    def __repr__(self):
        return "Edge from %s to %s" % (repr(self[0]), repr(self[1]))
    
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
        self.__vertices.add(vertex)

    def add_edge_by_vertices(self, vertex1, vertex2):
        self.__edges.add(Edge(vertex1, vertex2))

    def add_edge(self, edge):
        self.__edges.add(edge)

    def get_edge_by_vertices(self, vertex1, vertex2):
        edge = Edge(vertex1, vertex2)
        return self.get_edge(edge)

    def get_edge(self, edge):
        if edge in self.edges: 
            return edge
        elif edge.inverse in self.edges:
            return edge
        else:
            return None
   
    
    def remove_edge(self, edge):
        """
            Use this method to remove an edge from the graph.
        """
        # Should it fail silently??
        if edge in self.__edges:
            self.__edges.remove(edge)
        elif edge.inverse in self.__edges:
            self.__edges.remove(edge.inverse)
        else:
            raise MissingEdgeException("%s does not exist in graph %s" % edge, self)
         
    def remove_vertex(self, vertex):
        """
            Use this method to remove a vertex from the graph.
            It will also remove all edges that reference it.
        """
        # Find all references to this vertex in this graph's edges.
        bad_references = self.connected_edges(vertex)
        # Remove those references.
        [self.remove_edge(edge) for edge in bad_references]
        # Now remove the vertex itself.
        if  vertex in self.__vertices: 
          self.__vertices.remove(vertex)
        else:
            raise MissingVertexException("%s does not exist in graph %s" % vertex, self)

    def adjacent_vertices(self, vertex):
        """
            Use this method to get a list of vertices that
            are connected to this vertex.
        """
        associated_edges = self.connected_edges(vertex)
        # There must be a better way to do this.
        left_list = [vertex1 for vertex1, vertex2 in associated_edges.vertices if vertex2 == vertex]
        
    def connected_edges(self, vertex):
        """
            Use this method to get a list of edges that are connected
            to this vertex.
        """
        return [edge for edge in self.__edges if vertex in edge]

    def is_connected(self):
       """
            Use this method to determine whether this graph is connected.
       """
       pass

    def __repr__(self):
       """  
            Use this method to get a somewhat confusing textual output of vertices
            and edges connected to each vertex. 
       """
       return "Graph %s" % self.label
