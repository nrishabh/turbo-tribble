import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import cdist
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.neighbors import KDTree
import time
import faiss
from annoy import AnnoyIndex
from sklearn.neighbors import BallTree


def search_tree(tree, query_vector, data_matrix, k=1):
    if tree.is_leaf():
        return [tree.id]

    left_child = tree.get_left()
    right_child = tree.get_right()

    left_centroid = np.mean(data_matrix[left_child.pre_order()], axis=0)
    right_centroid = np.mean(data_matrix[right_child.pre_order()], axis=0)

    dist_left = np.linalg.norm(query_vector - left_centroid)
    dist_right = np.linalg.norm(query_vector - right_centroid)

    if dist_left < dist_right:
        closest_ids = search_tree(left_child, query_vector, data_matrix, k)
        if len(closest_ids) < k:
            closest_ids += search_tree(right_child, query_vector, data_matrix, k - len(closest_ids))
    else:
        closest_ids = search_tree(right_child, query_vector, data_matrix, k)
        if len(closest_ids) < k:
            closest_ids += search_tree(left_child, query_vector, data_matrix, k - len(closest_ids))

    return closest_ids


def hierarchical_search(data_matrix, xq, k, linked):

    # linked = linkage(data_matrix, method='ward')

    tree = to_tree(linked)

    closest_ids = search_tree(tree, xq, data_matrix, k)

    distances = cdist(xq, data_matrix[closest_ids], metric='euclidean')

    sorted_indices = np.argsort(distances)
    closest_ids = np.array(closest_ids)[sorted_indices]

    return closest_ids[0]

def linear_search(data_matrix, xq, k=5):
    # Time linear_search
    # start_time = time.time()

    distances = cdist(xq.reshape(1, -1), data_matrix, metric='euclidean')

    # print("Linear search time: {:.6f} seconds".format(time.time() - start_time))

    sorted_indices = np.argsort(distances)
    closest_ids = sorted_indices[:, :k]
    
    return closest_ids[0]

def kd_tree_search(data_matrix, xq, k,tree):

    distances, indices = tree.query(xq.reshape(1, -1), k=k)

    return indices[0]

def ball_tree_search(data_matrix, xq, k,tree):

    distances, indices = tree.query(xq.reshape(1, -1), k=k)

    return indices[0]


def annoy_search(data_matrix, xq, k,tree):

    indices = tree.get_nns_by_vector(xq.flatten(), k)

    return indices

def faiss_search(data_matrix, xq, k,index):
    distances, indices = index.search(xq.astype(np.float32), k)

    return indices[0]