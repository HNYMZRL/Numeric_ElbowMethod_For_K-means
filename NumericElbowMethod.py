def ElbowMethod(array, max_cluster_number, min_cluster_number=1, 
                init = 'k-means++', max_iter = 300, n_init = 50, 
                random_state = None, remark=True):
    """
    The methods computes a possible optimal number of clusters by computing . 
    It case such number does not exists we still get a number, but different 
    runs with different random_state values produced different outcomes. 
    
    Parameters
    ----------
    array:  a numpy array of data. Must be of shape (n_clusters, n_features).
    
    max_cluster_number:  int
        The maximal number of clusters for which you want to compute 
        squared distances of samples to their closest cluster center measure.
    
    min_cluster_number: int, default=1
        The minimal number of clusters you want to calculate squared 
        distances of samples to their closest cluster center measure.
    
    init: {'k-means++', 'random', ndarray, callable}, default='k-means++'
        Method for initialization, see K-means documentation.
    
    max_iter: int, default=300
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia. The greater is the number, 
        the longer will be the run and your numbers will be more stable if an 
        optimal number exists. 
    
    random_state: int
        Random state value. Note that it will be uses for each K-means run, 
        for all cluster numbers.
    remark: boolean, default = True
        For printing out a warning that the method may not be reliable for some
        cases.

    """
    import numpy as np
    from sklearn.cluster import KMeans
    wcss = np.zeros(max_cluster_number) #within_cluster_sum_squares
    
    for i in range(max_cluster_number):
        n = i+1 # we are to start with at least 1 cluster
        kmeans = KMeans(n_clusters = n, init=init, max_iter=max_iter, 
                        n_init=n_init, random_state=random_state)
        kmeans.fit(array)
        wcss[i] = kmeans.inertia_
    
    cosines = -1 * np.ones(max_cluster_number-2)# the angles of interes are 
    # between cluster numbers, so the 1st and last does not count
    
    for i in range(max_cluster_number-2):
    # check if the point is below a segment midpoint connecting its neighbors
        if (wcss[i+1] < (wcss[i+2]+wcss[i])/2 ):
            cosines[i]= (-1+(wcss[i]-wcss[i+1])*(wcss[i+2]-wcss[i+1]))/ \
            ((1+(wcss[i]-wcss[i+1])**2)*(1+ (wcss[i+2]-wcss[i+1])**2))**.5
    
    if remark:
        print("""Remark:\n\t Remember that the Kmeans is randomized and may 
        yield different results for different runs. If each time repeated 
        applications of the method(with different random_state parameters)
        yield different values for the optimal number then Elbow method with 
        K-means does not work well on the array. The method produces roundish 
        clusters and they may be not suitalbe for your objective.""")
    
    return (np.flip(np.argsort(cosines[1:-1]))+2+min_cluster_number)[0]
