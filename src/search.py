
import numpy as np
import time
from pynndescent import NNDescent
from src.hc import *

class SearchModule():

    searchspace: object  # SearchSpaceIndex object
    nndescent: object  # NNDescent object

    def __init__(self, searchspace):
        self.searchspace = searchspace

    def nndescent_fit(self):

        self.nndescent = NNDescent(self.searchspace.vector, metric='cosine')
        tic = time.time()
        self.nndescent.prepare()
        toc = time.time()
        print("Time taken to build index: ", toc - tic)

    def nndescent_lookup(self, xq, k: int = 5):

        tic = time.time()
        indices, distances = self.nndescent.query(xq, k)
        toc = time.time()
        print("Time taken to query: ", toc - tic)

        return indices, distances

    def nndescent_search(self, listQueries: list, k: int = 5):

        xq = np.array([q.info_vector for q in listQueries])
        listIndices, distances = self.nndescent_lookup(xq, k)

        for i, q in enumerate(list(listIndices)):
            print("Query: ", listQueries[i].text)
            for j, index in enumerate(q):
                print("\t Result ", j + 1, ": ", str(self.searchspace.listObjects[index].text))
                print("\t Distance: ", distances[i][j])
            print("\n")

    def hierarchical_search(self, listQueries: list, k: int = 5):
        tic = time.time()
        listIndices = list()
        linked = linkage(self.searchspace.vector, method='ward')
        toc = time.time()
        print(f"Time taken for building index {toc - tic}")

        for i in range(len(listQueries)):
            tic = time.time()
            resulting_indices = hierarchical_search(self.searchspace.vector,np.array([listQueries[i].info_vector]), k, linked)
            toc = time.time()
            print(f"Time taken for this query {i+1}: {toc - tic}")
            listIndices.append(resulting_indices)

        for i, q in enumerate(listIndices):
            print("Query: ", listQueries[i].text)
            for j, index in enumerate(q):
                print("\t Result ", j + 1, ": ", str(self.searchspace.listObjects[index].text))
                # print("\t Distance: ", distances[i][j])
            print("\n")

    def linear_search(self, listQueries: list, k: int = 5):

        listIndices = list()
        for i in range(len(listQueries)):
            tic = time.time()
            resulting_indices = linear_search(self.searchspace.vector, np.array([listQueries[i].info_vector]), k)
            toc = time.time()
            print(f"Time taken for query {i+1}: {toc - tic}")
            listIndices.append(resulting_indices)

        for i, q in enumerate(listIndices):
            print("Query: ", listQueries[i].text)
            for j, index in enumerate(q):
                print("\t Result ", j + 1, ": ", str(self.searchspace.listObjects[index].text))
                # print("\t Distance: ", distances[i][j])
            print("\n")

    def kd_tree_search(self, listQueries: list, k: int = 5):
        tic = time.time()
        tree = KDTree(self.searchspace.vector)
        listIndices = list()
        toc = time.time()
        print(f"Time taken for building index {toc - tic}")
        for i in range(len(listQueries)):
            tic = time.time()
            resulting_indices = kd_tree_search(self.searchspace.vector,np.array([listQueries[i].info_vector]), k, tree)
            toc = time.time()
            print(f"Time taken for this query {i+1}: {toc - tic}")
            listIndices.append(resulting_indices)

        for i, q in enumerate(listIndices):
            print("Query: ", listQueries[i].text)
            for j, index in enumerate(q):
                print("\t Result ", j + 1, ": ", str(self.searchspace.listObjects[index].text))
                # print("\t Distance: ", distances[i][j])
            print("\n")

    def ball_tree_search(self, listQueries: list, k: int = 5):
        tic = time.time()
        tree = BallTree(self.searchspace.vector)
        listIndices = list()
        toc = time.time()
        print(f"Time taken for building index {toc - tic}")
        for i in range(len(listQueries)):
            tic = time.time()
            resulting_indices = ball_tree_search(self.searchspace.vector,np.array([listQueries[i].info_vector]), k, tree)
            toc = time.time()
            print(f"Time taken for this query {i+1}: {toc - tic}")
            listIndices.append(resulting_indices)

        for i, q in enumerate(listIndices):
            print("Query: ", listQueries[i].text)
            for j, index in enumerate(q):
                print("\t Result ", j + 1, ": ", str(self.searchspace.listObjects[index].text))
                # print("\t Distance: ", distances[i][j])
            print("\n")

    def annoy_search(self, listQueries: list, k: int = 5):
        tic = time.time()
        dim = self.searchspace.vector.shape[1]
        tree = AnnoyIndex(dim, 'euclidean')
        for i, vec in enumerate(self.searchspace.vector):
            tree.add_item(i, vec)

        tree.build(10)  # Number of trees to build, higher values provide better search accuracy
        toc = time.time()
        print(f"Time taken for building index {toc - tic}")
        listIndices = list()
        for i in range(len(listQueries)):
            tic = time.time()
            resulting_indices = annoy_search(self.searchspace.vector,np.array([listQueries[i].info_vector]), k, tree)
            toc = time.time()
            print(f"Time taken for this query {i+1}: {toc - tic}")
            listIndices.append(resulting_indices)

        for i, q in enumerate(listIndices):
            print("Query: ", listQueries[i].text)
            for j, index in enumerate(q):
                print("\t Result ", j + 1, ": ", str(self.searchspace.listObjects[index].text))
                # print("\t Distance: ", distances[i][j])
            print("\n")

    def faiss_search(self, listQueries: list, k: int = 5):
        tic = time.time()
        dim = self.searchspace.vector.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(self.searchspace.vector.astype(np.float32))
        toc = time.time()
        print(f"Time taken for building index {toc - tic}")
        listIndices = list()
        for i in range(len(listQueries)):
            tic = time.time()
            resulting_indices = faiss_search(self.searchspace.vector,np.array([listQueries[i].info_vector]), k, index)
            toc = time.time()
            print(f"Time taken for this query {i+1}: {toc - tic}")
            listIndices.append(resulting_indices)

        for i, q in enumerate(listIndices):
            print("Query: ", listQueries[i].text)
            for j, index in enumerate(q):
                print("\t Result ", j + 1, ": ", str(self.searchspace.listObjects[index].text))
                # print("\t Distance: ", distances[i][j])
            print("\n")
