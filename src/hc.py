import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import cdist


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


def hierarchical_search(data_matrix, xq, k):

    linked = linkage(data_matrix, method='ward')

    tree = to_tree(linked)

    closest_ids = search_tree(tree, xq, data_matrix, k)

    distances = cdist(xq, data_matrix[closest_ids], metric='euclidean')

    sorted_indices = np.argsort(distances)
    closest_ids = np.array(closest_ids)[sorted_indices]

    # Assuming you have the 'linked' variable from the previous code snippet

    # Create a dendrogram
    # plt.figure(figsize=(10, 7))
    # dendrogram(linked, truncate_mode='level', p=5)
    # plt.title("Hierarchical Clustering Dendrogram")
    # plt.xlabel("Vector Index")
    # plt.ylabel("Distance")
    # plt.show()
    print("Closest IDs: ", closest_ids)
    return closest_ids[0]
