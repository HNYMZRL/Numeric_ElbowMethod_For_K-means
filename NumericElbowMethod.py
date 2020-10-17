def ElbowMethod(array, max_cluster_number, min_cluster_number=1, init = 'k-means++', max_iter = 300, n_init = 50, random_state = None, remark=True):
    import numpy as np
    from sklearn.cluster import KMeans
    wcss = np.zeros(max_cluster_number) #within_cluster_sum_squares
    
    for i in range(max_cluster_number):
        n = i+1 # we are to start with at least 1 cluster
        kmeans = KMeans(n_clusters = n, init=init, max_iter=max_iter, n_init=n_init, random_state=random_state)
        kmeans.fit(array)
        wcss[i] = kmeans.inertia_
    
    cosines = -1 * np.ones(max_cluster_number-2)# the agles are between cluster numbers, so the 1st and last does not count
    
    for i in range(max_cluster_number-2):
    # check if the point is below a segment midpoint connecting its neighbors
        if (wcss[i+1] < (wcss[i+2]+wcss[i])/2 ):
            cosines[i]= (-1+(wcss[i]-wcss[i+1])*(wcss[i+2]-wcss[i+1]))/ \
            ((1+(wcss[i]-wcss[i+1])**2)*(1+ (wcss[i+2]-wcss[i+1])**2))**.5
    
    if remark:
        print("""Remark:\n\t Remember that the Kmeans is randomized and may yield different results for different runs.
        If each time repeated applications of the method(with different random_state parameters)yield  
        different values for the optimal number then Elbow method with K-means does not work well 
        on the array. The method produces roundish clusters and they may be not suitalbe for 
        your objective.""")
    
    return (np.flip(np.argsort(cosines[1:-1]))+2+min_cluster_number)[0]
