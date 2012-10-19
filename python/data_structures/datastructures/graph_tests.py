#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

import unittest
from graph import Vertex, Edge, Graph, MissingVertexException, MissingEdgeException

class TestVertex(unittest.TestCase):
    """
    This tests the Vertex class.
    Are these too trivial?
    """
    def setUp(self):
        self.label = "Test vertex"
        self.vertex = Vertex(self.label)
   
    def test_unhashable(self):
        # I need to be able to put a Vertex object in a setlike object
        # so we can't use an unhashable object as a label.
        self.assertRaises(TypeError,Vertex,{'alpha':1})

    def test_repr(self):
        self.assertEqual(repr(self.vertex), "Vertex %s" % self.label)
    
    def test_label(self):
        self.assertEqual(self.vertex.label,self.label) 

    def test_label_property(self):
        with self.assertRaises(AttributeError) as cm:
            self.vertex.label = "new label"

class TestEdge(unittest.TestCase):
    """
        This testss the Edge class.
    """
    def setUp(self):
        self.name = 'Vertex '
        self.vertex1 = Vertex("1")
        self.vertex2 = Vertex("2")
        self.edge = Edge(self.vertex1, self.vertex2)

    def test_repr(self):
        self.assertEquals(repr(self.edge),"Edge from Vertex 1 to Vertex 2")
    
    def test_inverse(self):
        self.assertIsInstance(self.edge.inverse, Edge)
    
    def test_vertices(self):
        self.assertEquals(self.edge.vertices, (self.vertex1, self.vertex2))

    def test_eq(self):
        self.assertEquals(self.edge.inverse, self.edge)

class TestGraph(unittest.TestCase):
    """
        This tests the Graph class.
    """

    def setUp(self):
        self.label = "test graph"
        self.extraVertex = Vertex(5)
        self.vertices = [Vertex(1), Vertex(2), Vertex(3)]
        self.extraEdge = Edge(self.extraVertex, self.vertices[0])
        self.edges = [Edge(self.vertices[2], self.vertices[0]), Edge(self.vertices[0], self.vertices[1])]
        self.graph = Graph(self.label, vertices = self.vertices, edges = self.edges) 
    
    def test_initialization(self):
        # Initialize without vertices or edges
        graph = Graph(self.label, vertices = self.vertices, edges = self.edges)
        self.assertIsInstance(graph, Graph)
        self.assertEquals(set(self.edges), graph.edges)
        self.assertEquals(set(self.vertices), graph.vertices)
       
        # Initialize with vertices but no edges
        graph = Graph('graph', vertices=self.vertices)
        self.assertIsInstance(graph, Graph)
        self.assertNotEquals(set(self.edges),set())
        self.assertEquals(set(self.vertices), set(graph.vertices))

        # Initialize with edges but no vertices (error)
        self.assertRaises(MissingVertexException, Graph, 'graph', edges = self.edges)

        # Initialize with vertices and edges that contain vertices that don't exist in the graph (also error)
        self.edges.append(self.extraEdge)
        self.assertRaises(MissingVertexException, Graph, 'graph', vertices = self.vertices, edges = self.edges)
        self.edges.remove(self.extraEdge)
        
     
    # I technically already tested the next two.
    def get_vertices(self):
        self.assertEquals(set(self.graph.vertices), self.vertices)

    def get_edges(self):
        self.assertEquals(set(graph.edges), self.edges)
   
    def test_label(self):
        self.assertEquals(self.graph.label, self.label)

    def test_add_vertex(self):
        graph = Graph("graph")
        graph.add_vertex(self.extraVertex)
        self.assertIn(self.extraVertex,graph.vertices)
        # Also make sure equality extends to attributes
        graph.add_vertex(Vertex(4))
        self.assertIn(Vertex(4),graph.vertices)

    def test_add_edge(self):
        graph = Graph("graph", vertices = self.vertices, edges = self.edges)
        graph.add_edge(Edge(self.vertices[1], self.vertices[2]))
        self.assertIn(Edge(self.vertices[1], self.vertices[2]), graph.edges)
    
    def test_add_edge_by_vertex(self):
        graph = Graph("graph", vertices = self.vertices, edges = self.edges)
        graph.add_edge_by_vertices(self.vertices[1], self.vertices[2])
        self.assertIn(Edge(self.vertices[1], self.vertices[2]), graph.edges)
    
    def test_get_edge(self):
        self.assertTrue(self.graph.get_edge(self.edges[0]))
        self.assertFalse(self.graph.get_edge(Edge(Vertex(5), self.vertices[2])))

    def test_get_edge_by_vertices(self):
        self.assertTrue(self.graph.get_edge_by_vertices(self.vertices[2], self.vertices[0]))
        self.assertFalse(self.graph.get_edge_by_vertices(self.extraVertex, self.vertices[0]))

    def test_remove_vertex(self):
        # If we remove a vertex, we should probably remove all of its edges, as well.
        # Can remove vertices from an empty graph?
        # Can we remove a vertex from a graph that has no edges associated with it?
        pass 

    def test_remove_edge(self):
        # Can we remove a regular edge that exists?
        self.graph.add_edge_by_vertices(self.vertices[1], self.vertices[2])
        self.graph.remove_edge(Edge(self.vertices[1], self.vertices[2]))
        self.assertIsNone(self.graph.get_edge_by_vertices(Vertex(1), self.vertices[2]))
        # Can we do it symmetrically?
        self.graph.add_edge_by_vertices(self.vertices[1], self.vertices[2])
        self.graph.remove_edge(Edge(self.vertices[2], self.vertices[1]))
        self.assertIsNone(self.graph.get_edge_by_vertices(self.vertices[1], self.vertices[2]))
        # What happens if we remove an edge that doesn't exist by virtue of vertex doesn't exist?
        self.assertRaises(MissingEdgeException, self.graph.remove_edge, self.extraEdge)
        # What happens if we remove an edge that doesn't exist by virtual of edge doesn't exist?
        self.graph.add_vertex(self.extraVertex)
        self.assertRaises(MissingEdgeException, self.graph.remove_edge, self.extraEdge)
        self.graph.remove_vertex(self.extraVertex)

    def test_repr(self):
        self.assertEqual(repr(self.graph), "Graph %s" % self.label)

    def test_adjacent_vertices(self):
        pass
    
    def test_connected_edges(self):
        pass

if __name__ == '__main__':
    unittest.main()
   
