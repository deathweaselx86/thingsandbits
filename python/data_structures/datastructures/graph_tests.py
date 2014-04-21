# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

import unittest
from graph import Graph, MissingVertexException,\
        MissingEdgeException, DuplicateEdgeException

# These need to be rewritten... later.
"""
class TestGraph(unittest.TestCase):
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
        self.failUnless(isinstance(graph, Graph))
        self.assertEquals(set(self.edges), graph.edges)
        self.assertEquals(set(self.vertices), graph.vertices)

        # Initialize with vertices but no edges
        graph = Graph('graph', vertices=self.vertices)
        self.assertTrue(isinstance(graph, Graph))
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
        self.failUnless(self.extraVertex in graph.vertices)
        # Also make sure equality extends to attributes
        graph.add_vertex(Vertex(4))
        self.failUnless(Vertex(4) in graph.vertices)

    def test_add_edge(self):
        edge = Edge(self.vertices[1], self.vertices[2])
        loop = Edge(self.vertices[1], self.vertices[1])
        graph = Graph("graph", vertices = self.vertices, edges = self.edges)
        graph.add_edge(edge)
        self.failUnless(edge in graph.edges)
        # Can we add a loop?
        graph.add_edge(loop)
        self.assertTrue(loop in graph.edges)

    def test_add_edge_by_vertex(self):
        graph = Graph("graph", vertices = self.vertices, edges = self.edges)
        graph.add_edge_by_vertices(self.vertices[1], self.vertices[2])
        thisEdge = Edge(self.vertices[1], self.vertices[2])
        self.failUnless(thisEdge in graph.edges)

    def test_vertex_uniqueness(self):
        self.assertRaises(DuplicateVertexException, self.graph.add_vertex, self.vertices[0])

    def test_edge_uniqueness(self):
        self.assertRaises(DuplicateEdgeException, self.graph.add_edge,\
                Edge(self.vertices[2], self.vertices[0]))

    def test_get_edge(self):
        bad_edge = Edge(self.extraVertex, self.vertices[2])
        loop = Edge(self.vertices[0], self.vertices[0])
        self.assertTrue(self.graph.get_edge(self.edges[0]))
        self.assertRaises(MissingEdgeException, self.graph.get_edge, bad_edge)
        # What happens if we try to get a loop that doesn't exist?
        self.assertRaises(MissingEdgeException, self.graph.get_edge, loop)

    def test_get_edge_by_vertices(self):
        self.assertTrue(self.graph.get_edge_by_vertices(self.vertices[2], self.vertices[0]))
        self.assertRaises(MissingEdgeException, self.graph.get_edge_by_vertices, self.extraVertex, self.vertices[0])

    def test_remove_vertex(self):
        # If we remove a vertex, we should probably remove all of its edges, as well.
        graph = Graph("graph", vertices=self.vertices, edges=self.edges)
        self.failUnless(graph.remove_vertex(self.vertices[0]) is None)
        self.assertRaises(MissingEdgeException, graph.get_edge, Edge(self.vertices[0], self.vertices[2]))
        # Can remove vertices from an empty graph?
        graph = Graph("graph")
        self.assertRaises(MissingVertexException, graph.remove_vertex, self.extraVertex)
        # Can we remove a vertex from a graph that has no edges associated with it?
        graph = Graph("graph", vertices=[self.extraVertex])
        self.failUnless(graph.remove_vertex(self.extraVertex) is None)
"""

if __name__ == '__main__':
    unittest.main()
