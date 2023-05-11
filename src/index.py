import numpy as np


class SearchSpaceIndex():

    vector: np.array
    listObjects: list

    def __init__(self, listObjects: list):

        self.listObjects = listObjects
        self.vector = None

    def load_vector(self, vector_fp: str):

        self.vector = np.load(vector_fp)
        print("Loaded vector has shape: ", self.vector.shape)

    def create_vector(self, listObjects: list):

        self.vector = np.array([obj.info_vector for obj in listObjects])
        print("Created vector has shape: ", self.vector.shape)

    def save_vector(self, vector_fp: str):

        np.save(vector_fp, self.vector)
        print("Saved vector")
