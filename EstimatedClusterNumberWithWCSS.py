# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 20:11:42 2021

@author: mathemilda
"""

"""
    The methods estimates a possible good enough number of clusters under
    given conditions using numeric version of Elbow method.
    In case such number does not exists we still get a number, but a
    warning will be issued that the clustering was not reliable.

    Parameters
    ----------
    array:  a numpy array of data. Must be of shape (n_points, n_features).

    start: int, default=1
        The minimal number of clusters to consider.

    end:  int, default=11
        The maximal number of clusters to consider.

    threshold: float, default=0.67
        The minimal proportion of cluster number frequency among all runs
        for the clustering to be consider as a reasonable choice under
        given conditions.

    init: {'k-means++', 'random', ndarray, callable}, default='k-means++'
        Method for initialization, see K-means documentation.

    subset: float, default=0.997
        A random subset of provided array to cluster for a each run. It
        is a way to regularise the procedure.

    metric: str, default="elbow"
        A metric for measuring goodness of clustering. There are plans to
        add "silhouette" to this, by popular requests.

    n_init: int, default=3
        Must be a positive interger. It defines how many times the algorithm
        will be repeated and how many possible optimal numbers you will get.

    kmeans_n_init: int, default=50
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia.

    max_iter: int, default=300
        Number of times the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia. The greater is the number,
        the longer will be the run and your numbers will be more stable if an
        optimal number exists.

    random_state: int
        Random state value. Note that it will be uses for each K-means run,
        for all cluster numbers.


    Attributes
    ----------
    estimated_: numpy_array
        A one-dimensional array of optimal cluster numbers.

    cluster_frequencies_
        A dictionary with cluster numbers and their corresponding
        frequences which were calculated by the method as good ones.
        It is sorted by frequences in descending order.

"""

from sklearn.base import BaseEstimator


class NumericElbowMethod(BaseEstimator):
    def __init__(
        self,
        start=2,
        end=11,
        n_init=51,
        threshold=0.67,
        subset=0.997,
        # K-means parameters
        kmeans_n_init=30,
        max_iter=300,
        init="k-means++",
        random_state=None,
        **kwargs):
        self.start = start
        self.end = end
        self.n_init = n_init
        self.threshold = threshold
        self.subset = subset
        # K-means parameters
        self.kmeans_n_init = kmeans_n_init
        self.max_iter = max_iter
        self.init = init
        self.random_state = random_state
    
    def fit(self, array, y=None):
        import numpy as np
        # from tqdm import trange
        from sklearn.cluster import KMeans

        estimated_ = [0] * self.n_init
        arr_size = int(array.shape[0] * self.subset)
        # end points should be evaluated for clustering, too
        start = max([1, self.start - 1])
        end = self.end + 1
        # for j in trange(self.n_init):
        for j in range(self.n_init):
            indx = end - start + 1
            wcss = np.zeros(indx)  # placehodler for within_cluster_sum_squares
            subarray = array[np.random.choice(array.shape[0], size=arr_size), :]
            for i in range(indx):
                kmeans = KMeans(
                    n_clusters=i + start,
                    init=self.init,
                    max_iter=self.max_iter,
                    n_init=self.kmeans_n_init,
                    random_state=self.random_state)
                kmeans.fit(subarray)
                wcss[i] = kmeans.inertia_
            
            cosines = -1 * np.ones(indx - 2)  # the angles of interes are
                # between cluster numbers, so the 1st and last clusters
                # do not contribute any angles.
            for i in range(indx - 2):
                # check if the point is below a midpoint of segment 
                # connecting its neighbors
                if wcss[i + 1] < (wcss[i + 2] + wcss[i]) / 2:
                    cosines[i] = (
                        (-1 + (wcss[i] - wcss[i + 1]) *
                        (wcss[i + 2] - wcss[i + 1]))
                        / (
                            (1 + (wcss[i] - wcss[i + 1]) ** 2)
                            * (1 + (wcss[i + 2] - wcss[i + 1]) ** 2)
                        )
                        ** 0.5
                        )
            
            estimated_[j] = np.flip(np.argsort(cosines))[0] + start + 1

        count_dict = dict()
        most_frequent = estimated_[0]
        for nu in estimated_:
            if nu in count_dict:
                count_dict[nu] += 1
            else:
                count_dict[nu] = 1
        
            if count_dict[most_frequent] < count_dict[nu]:
                most_frequent = nu
        
        if count_dict[most_frequent] < self.threshold * self.n_init + 1:
            print(
                """\nWarning:\t The clustering did not produce a
                      reliable result, although it can suffice for
                      your business/research objective. It might 
                      be improved with other parameters or methods."""
                )
        sorted_counts_dict = {}
        sorted_counts = sorted(count_dict, reverse=True, key=count_dict.get)
        
        for w in sorted_counts:
            sorted_counts_dict[w] = count_dict[w]
        
        self.estimated_n_ = most_frequent
        self.cluster_frequencies_ = sorted_counts_dict
        return self
