#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

class MissingVertexException(Exception):
    pass

class MissingEdgeException(Exception):
    pass

class DuplicateEdgeException(Exception):
    pass

class InvalidVertexException(Exception):
    pass

class BadEdgesFormatException(Exception):
    pass

class Graph(object):
    """
        This class represents a basic unweighted, undirected
        graph. 
        
        There's no optimization for connectivity or anything.
        We will use the adjacency list representation.
    """
    def __has_valid_edges_arg(self, edges, vertices):
        """
            I'm using this method to determine whether the edges
            argument of the __init__ method is valid.

            Putting it here because it's ugly.

            I'll have it return True if it doesn't raise an exception.
        """
        if edges is None:
            return True

        # I guess I'll accept a list or tuple
        if isinstance(edges, list) or isinstance(edges, tuple):
            
            # I will not accept a list to represent the edges, though.
            for item in edges:
                # Every item in the edges list should be a tuple and have exactly two
                # elements. If not, this is not valid.
                
                if not ( isinstance(item, tuple) and len(item) == 2):
                    raise BadEdgesFormatException("Edges argument has an item that is not a tuple or incorrect length: %s " % (item,))
                # And for each of those items, every element should be an int or castable 
                # to int.
                for i in range(2):
                    if not isinstance(item[i], int):
                        try:
                            item[i] = int(item[i])
                        except TypeError, ValueError:
                            raise BadEdgesFormatException("Edges argument has an incorrectly formatted tuple element: %s of %s" % (element, item, ))
                    if item[i] > vertices - 1:
                        raise BadEdgesFormatException("Edges argument has an edge containing a vertex that does not exist in this graph: %s" % (item[i],))


        else:
            raise BadEdgesFormatException("Edges argument is not a list or tuple.")
        
        return True

    def __has_valid_vertices_args(self, vertex_list):
        """
        Seriously, are these vertices good?
        I find myself repeating this over and over, so I'm going to write this
        just once. 

        """

        number_vertices = len(self.adjacency_list)
        for i in range(len(vertex_list)):
            if not isinstance(vertex_list[i], int):
                try:
                    vertex_list[i] = int(vertex_list[i])
                except ValueError:
                    raise TypeError("Graph vertex arguments must be integers. Got %s." % vertex_list[i]) 
     
            if vertex_list[i] > number_vertices or vertex_list[i] < 0:
                raise InvalidVertexException("Vertex %s is not a valid vertex in this graph." % (vertex_list[i],))
        return True

    def __init__(self, label, vertices, vertex_data=None, edges=None):
        """
            Create a new graph, possibly with initial lists
            of edges and vertexes. 

            @param label: A label for the graph. 

            @param vertices: A non-negative integer representing the number of
            vertices. These vertices will be labeled 0 to vertices -1

            @param edges: A list or tuple of 2-tuples that represent the edges in this graph.
            These should be in the form (v1, v2) where v1, v2 are non-negative
            integers. Each v in each of these 2-tuples should be equal to or less than
            vertices - 1

            @vertex_data: A dictionary representing data associated with vertices.
            Keys are integers that are between 0 and vertices-1. Values are whatever you want.
            There is no error checking associated with this dictionary other than that associated with
            the construction of the dictionary, so keys in this dictionary that are not
            integers between 0 and vertices-1, they will not be accessible through this object.

            
            This method may raise any of the following exceptions:
            
            TypeError - if vertices is not an integer (or castable to integer) or
            if edges is not a list of 2 tuples of integers.

            
            BadEdgesFormatException - if edges is not a list or tuple of 2-tuples that represent
            the edges of this graph, generally because it's in the wrong format, but may also be because
            an edge contains a vertex that is not in this graph.

        """
        self.label = label
        self.adjacency_list = []
        self.vertex_data = vertex_data

        if not isinstance(vertices, int):
            try:
                vertices = int(vertices)
            except ValueError:
                raise TypeError("Graph vertices argument must be an integer. Got %s." % vertices) 
        
        self.__has_valid_edges_arg(edges, vertices) 
        
        
        # There is no limit to the number of vertices, so I will use xrange.
        # Later, there must be a way to not use an empty list for an unconnected 
        # vertex.

        for i in xrange(vertices):
            self.adjacency_list.append([])
            if edges:
                [self.adjacency_list[i].append(e[1]) for e in edges if e[0] == i]
   

    def is_adjacent(self, vertex1, vertex2):
        """
            Test to see if vertex1 is adjacent to vertex2.

            @param vertex1: A non-negative integer representing the first vertex

            @param vertex2: A non-negative integer representing the second vertex

            @returns: a boolean value indicating whether the two vertices are adjacent.

            This method may raise any of the following exceptions.
     
            InvalidVertexException - If vertex1 or vertex2 are not valid vertices. 
            
        """
        number_vertices = len(self.adjacency_list)
    
        if self.__has_valid_vertices_args([vertex1, vertex2]):
            return vertex1 in self.adjacency_list[vertex2] or vertex2 in self.adjacency_list[vertex1]


    def neighbors(self, vertex):
        """
            Return all vertices that are adjacent to vertex.

            @param vertex: A non-negative integer representing the first vertex.

            @returns: a tuple of non-negative integers representing the vertices 
            for which there are edges to vertex.

            This method may raise any of the following exceptions.

            InvalidVertexException - If vertex is not a valid vertex.
        """
        
        # TODO: Is it safe to assume that an edge from v1 to v2 is an edge from v2 to v1
        # in the adjacency list? I should probably make sure that is the case in the 
        # __init__ method. This will work as is in the case of a directed graph.
        if self.__has_valid_vertices_args([vertex]):
            return self.adjacency_list[vertex]
   
    def add_edge(self, vertex1, vertex2):
        """ 
            Add an edge to this graph.
            @param vertex1: A non-negative integer representing the first vertex.
            @param vertex2: A non-negative integer representing the second vertex.

            This method may raise any of the following exceptions.

            InvalidVertexException - if vertex1 or vertex2 are not a valid vertices.
            DuplicateEdgeException - if the edge between vertex1 and vertex2 already
                exists
        """
        if self.__has_valid_vertices_args([vertex1, vertex2]):
            self.adjacency_list[vertex1].append(vertex2)
            # Uncomment the below once we know we can depend on symmetricity.
            # self.adjacency_list[vertex2].append(vertex1)
    
    def remove_edge(self, vertex1, vertex2):
        """
            Remove an edge from this graph.
            @param vertex1: A non-negative integer representing the first vertex.
            @param vertex2: A non-negative integer representing the second vertex.

            This method may raise any of the following exceptions.

            InvalidVertexException - if vertex1 or vertex2 are not a valid vertices.
            MissingEdgeException - if the edge between vertex1 and vertex2 already
                exists

        """
        if self.__has_valid_edges_args([vertex1, vertex2]):
            try: 
                self.adjacency_list[vertex1].remove(vertex2)
            except ValueError:
                raise MissingVertexException("Cannot remove edge from %s to %s because it doesn't exist." %s (vertex1, vertex2))
    
    def get_value_at_vertex(self, vertex):
        """
            Get the value associated with the vertex vertex.
            @param vertex: A non-negative integer representing the vertex.
            
            @returns: The value corresponding to that vertex or None if there is no data.
            This method may raise InvalidVertexException if vertex is not a valid vertex.
         """
        if self.__has_valid_edges_args([vertex]):
            return self.vertex_data.get(vertex,None)
    
    def set_value_at_vertex(self, vertex, value):
        """
            Set the value associated with this vertex.
            @param vertex: A non-negative integer representing the vertex. 

            This method may raise InvalidVertexException if vertex is not a valid vertex.
        """
        if self.__has_valid_vertices_args([vertex]):
            self.vertex_data[vertex] = value

