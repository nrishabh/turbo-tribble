
import numpy as np
import time
from pynndescent import NNDescent
from src.hc import hierarchical_search


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

        listIndices = list()
        for i in range(len(listQueries)):
            tic = time.time()
            resulting_indices = hierarchical_search(self.searchspace.vector, np.array([listQueries[i].info_vector]), k)
            toc = time.time()
            print(f"Time taken for query {i+1}: {toc - tic}")
            listIndices.append(resulting_indices)

        for i, q in enumerate(listIndices):
            print("Query: ", listQueries[i].text)
            for j, index in enumerate(q):
                print("\t Result ", j + 1, ": ", str(self.searchspace.listObjects[index].text))
                # print("\t Distance: ", distances[i][j])
            print("\n")
