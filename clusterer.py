class Clusterer:

    def __init__(self, observations, k, is_data_labeled=False, labels=None):
        # List of observations
        self.observations = observations
        # K - number of clusters
        self.k = k
        # Is the cluster working on labeled data : should it print purity information
        self.is_data_labeled = is_data_labeled
        # In case of labeled observations, store list of label names
        self.labels = labels
        #
