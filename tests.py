import unittest
import NetworkSim as NS
unittest.TestLoader.sortTestMethodsUsing = None

class testNetworkCreation(unittest.TestCase):
    def setUp(self):
        self.network = NS.generate_network(5, 0.2, 10, 100, 1, 10)

    def test_node_minimum(self):
        for node in NS.nx.nodes(self.network):
            self.assertGreaterEqual(self.network.nodes[node]["weight"], 10)
    
    def test_node_maximum(self):
        for node in NS.nx.nodes(self.network):
            self.assertLessEqual(self.network.nodes[node]["weight"], 100)

    def test_edge_minimum(self):
        for edge in NS.nx.edges(self.network):
            self.assertGreaterEqual(self.network.edges[edge]["weight"], 1)

    def test_edge_maximum(self):
        for edge in NS.nx.edges(self.network):
            self.assertLessEqual(self.network.edges[edge]["weight"], 10)

class testSimulationDirectoryAndSimulationCreation(unittest.TestCase):
    def setUp(self):
        NS.create_sim_directory()
        self.f = NS.create_iteration(1)

    def test_directory_creation(self):
        self.assertTrue(NS.os.path.exists("NetworkSim/"))

    def test_iteration_creation(self):
        self.assertTrue(NS.os.path.exists("NetworkSim/1/1.txt"))

    def tearDown(self):
        self.f.close()
        NS.os.remove("NetworkSim/1/1.txt")
        NS.os.rmdir("NetworkSim/1")
        NS.os.rmdir("NetworkSim")

class testPathCreation(unittest.TestCase):
    def setUp(self):
        self.network = NS.nx.Graph()
        self.network.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.network.add_edges_from([(1, 2), (1, 3), (2, 6), (3, 5), (5, 7), (6, 10), (8, 5), (9, 3), (10, 4), (10, 2)])
        self.paths = [[], [[1, 2]], [[1, 3]], [[1, 2, 6, 10, 4], [1, 2, 10, 4]], [[1, 3, 5]], [[1, 2, 6], [1, 2, 10, 6]], [[1, 3, 5, 7]], [[1, 3, 5, 8]], [[1, 3, 9]], [[1, 2, 6, 10], [1, 2, 10]], [[2, 1]], [], [[2, 1, 3]], [[2, 6, 10, 4], [2, 10, 4]], [[2, 1, 3, 5]], [[2, 6], [2, 10, 6]], [[2, 1, 3, 5, 7]], [[2, 1, 3, 5, 8]], [[2, 1, 3, 9]], [[2, 6, 10], [2, 10]], [[3, 1]], [[3, 1, 2]], [], [[3, 1, 2, 6, 10, 4], [3, 1, 2, 10, 4]], [[3, 5]], [[3, 1, 2, 6], [3, 1, 2, 10, 6]], [[3, 5, 7]], [[3, 5, 8]], [[3, 9]], [[3, 1, 2, 6, 10], [3, 1, 2, 10]], [[4, 10, 6, 2, 1], [4, 10, 2, 1]], [[4, 10, 6, 2], [4, 10, 2]], [[4, 10, 6, 2, 1, 3], [4, 10, 2, 1, 3]], [], [[4, 10, 6, 2, 1, 3, 5], [4, 10, 2, 1, 3, 5]], [[4, 10, 6], [4, 10, 2, 6]], [[4, 10, 6, 2, 1, 3, 5, 7], [4, 10, 2, 1, 3, 5, 7]], [[4, 10, 6, 2, 1, 3, 5, 8], [4, 10, 2, 1, 3, 5, 8]], [[4, 10, 6, 2, 1, 3, 9], [4, 10, 2, 1, 3, 9]], [[4, 10]], [[5, 3, 1]], [[5, 3, 1, 2]], [[5, 3]], [[5, 3, 1, 2, 6, 10, 4], [5, 3, 1, 2, 10, 4]], [], [[5, 3, 1, 2, 6], [5, 3, 1, 2, 10, 6]], [[5, 7]], [[5, 8]], [[5, 3, 9]], [[5, 3, 1, 2, 6, 10], [5, 3, 1, 2, 10]], [[6, 2, 1], [6, 10, 2, 1]], [[6, 2], [6, 10, 2]], [[6, 2, 1, 3], [6, 10, 2, 1, 3]], [[6, 2, 10, 4], [6, 10, 4]], [[6, 2, 1, 3, 5], [6, 10, 2, 1, 3, 5]], [], [[6, 2, 1, 3, 5, 7], [6, 10, 2, 1, 3, 5, 7]], [[6, 2, 1, 3, 5, 8], [6, 10, 2, 1, 3, 5, 8]], [[6, 2, 1, 3, 9], [6, 10, 2, 1, 3, 9]], [[6, 2, 10], [6, 10]], [[7, 5, 3, 1]], [[7, 5, 3, 1, 2]], [[7, 5, 3]], [[7, 5, 3, 1, 2, 6, 10, 4], [7, 5, 3, 1, 2, 10, 4]], [[7, 5]], [[7, 5, 3, 1, 2, 6], [7, 5, 3, 1, 2, 10, 6]], [], [[7, 5, 8]], [[7, 5, 3, 9]], [[7, 5, 3, 1, 2, 6, 10], [7, 5, 3, 1, 2, 10]], [[8, 5, 3, 1]], [[8, 5, 3, 1, 2]], [[8, 5, 3]], [[8, 5, 3, 1, 2, 6, 10, 4], [8, 5, 3, 1, 2, 10, 4]], [[8, 5]], [[8, 5, 3, 1, 2, 6], [8, 5, 3, 1, 2, 10, 6]], [[8, 5, 7]], [], [[8, 5, 3, 9]], [[8, 5, 3, 1, 2, 6, 10], [8, 5, 3, 1, 2, 10]], [[9, 3, 1]], [[9, 3, 1, 2]], [[9, 3]], [[9, 3, 1, 2, 6, 10, 4], [9, 3, 1, 2, 10, 4]], [[9, 3, 5]], [[9, 3, 1, 2, 6], [9, 3, 1, 2, 10, 6]], [[9, 3, 5, 7]], [[9, 3, 5, 8]], [], [[9, 3, 1, 2, 6, 10], [9, 3, 1, 2, 10]], [[10, 6, 2, 1], [10, 2, 1]], [[10, 6, 2], [10, 2]], [[10, 6, 2, 1, 3], [10, 2, 1, 3]], [[10, 4]], [[10, 6, 2, 1, 3, 5], [10, 2, 1, 3, 5]], [[10, 6], [10, 2, 6]], [[10, 6, 2, 1, 3, 5, 7], [10, 2, 1, 3, 5, 7]], [[10, 6, 2, 1, 3, 5, 8], [10, 2, 1, 3, 5, 8]], [[10, 6, 2, 1, 3, 9], [10, 2, 1, 3, 9]], []]
    
    def test_path_list_creation(self):
        generated_paths = NS.generate_paths(self.network)
        self.assertEqual(self.paths, generated_paths)

class testPathGraphicCreation(unittest.TestCase):
    def setUp(self):
        self.network = NS.nx.Graph()
        self.network.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.network.add_edges_from([(1, 2), (1, 3), (2, 6), (3, 5), (5, 7), (6, 10), (8, 5), (9, 3), (10, 4), (10, 2)])
        NS.create_sim_directory()
        self.f = NS.create_iteration(1)

    def test_path_png_creation(self):
        NS.generateGraph(self.network, "NetworkSim/1", 1)
        self.assertTrue(NS.os.path.exists("NetworkSim/1/1.png"))

    def tearDown(self):
        self.f.close()
        NS.os.remove("NetworkSim/1/1.txt")
        NS.os.remove("NetworkSim/1/1.png")
        NS.os.rmdir("NetworkSim/1")
        NS.os.rmdir("NetworkSim")

class TestSimulationCreation(unittest.TestCase):
    def setUp(self):
        NS.create_sim_directory()
        NS.run_sim(3, 10, 0.2, 10, 100, 1, 10)
    
    def test_sim_directory_final_creation(self):
        flag = True
        for directory in NS.os.listdir("NetworkSim"):
            if not NS.os.path.exists("NetworkSim/{}".format(directory)):
                flag = False
            if not NS.os.path.exists("NetworkSim/{}/{}.txt".format(directory, directory)):
                flag = False
            if not NS.os.path.exists("NetworkSim/{}/{}.png".format(directory, directory)):
                flag = False
        
        self.assertTrue(flag)

    def tearDown(self):
        for directory in NS.os.listdir("NetworkSim"):
            NS.os.remove("NetworkSim/{}/{}.txt".format(directory, directory))
            NS.os.remove("NetworkSim/{}/{}.png".format(directory, directory))
            NS.os.rmdir("NetworkSim/{}".format(directory))
        NS.os.rmdir("NetworkSim")


if __name__ == '__main__':
    unittest.main()
    