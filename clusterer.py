import math
import random

from cluster import Cluster


def is_still_running(cluster_old_observations):

    # Check if any cluster's list of assigned observations changed
    for cluster in cluster_old_observations:
        for observation in cluster.observations:
            if observation not in cluster_old_observations[cluster]:
                return True

    # If cluster observation assignment stays the same, we should end model creation - break out from the loop
    return False


class Clusterer:

    def __init__(self, observations, dimensions, k, is_data_labeled=False, labels=None):
        # List of observations
        self.observations = observations
        # Dimensionality of observations
        self.dimensions = dimensions
        # K - number of clusters
        self.k = k
        # Is the cluster working on labeled data : should it print purity information
        self.is_data_labeled = is_data_labeled
        # In case of labeled observations, store list of label names
        self.labels = labels
        # List of clusters
        self.clusters = []

    def compute(self):

        # Shuffle observations data
        random.shuffle(self.observations)

        # As initial step we need to somehow chose initial locations for clusters' centroids
        # Clusterer class comes with several methods for choosing initial clusters' centroids
        self.random_location_for_centroids()

        # Dictionary maps cluster with old (previous iteration) observations assigned to cluster
        # This dictionary is used in stop property of a loop which is responsible for model creation
        cluster_old_observations = dict()
        # Fill dictionary with initial data
        for cluster in self.clusters:
            cluster_old_observations[cluster] = None

        # Store iteration count
        iteration = 0

        # Update centroids coordinates and observations cluster assignment
        # until no change in centroids coordinates occurs
        while iteration == 0 or is_still_running(cluster_old_observations):

            iteration += 1

            # Update old assigned observations dictionary
            for cluster in self.clusters:
                cluster_old_observations[cluster] = cluster.observations

            # Reset cluster's observation assignment
            for cluster in self.clusters:
                cluster.reset_observations_assignment()

            # Dictionary that maps clusters with sum of distances per dimension between their
            # centroids and assigned observations
            cluster_sum_of_distances_map = dict()
            # Dictionary that maps clusters with number of observations assigned to it
            cluster_number_of_observations = dict()
            for cluster in self.clusters:
                cluster_sum_of_distances_map[cluster] = [0 for _ in range(0, self.dimensions)]
                cluster_number_of_observations[cluster] = 0

            # Assign nearest cluster to each observation
            self.assign_clusters(cluster_sum_of_distances_map, cluster_number_of_observations)

            # Reposition clusters' centroids
            self.reposition_clusters(cluster_sum_of_distances_map, cluster_number_of_observations)

            # If observations data is labeled, inform about purity of clusters
            if self.is_data_labeled:
                print("Purity level: " + str(self.compute_purity()))

            # TMP TEST
            self.test(iteration)

    def location_of_centroids_based_on_random_observations(self):

        # Chose location of centroids based on coordinates of randomly chosen observations
        for c in range(0, self.k):
            coordinates_of_cluster = self.observations[c].coordinates
            self.clusters.append(Cluster("cluster " + str(c), coordinates_of_cluster))

    def random_location_for_centroids(self):
        # As an initial step assign random coordinates for cluster's centroids
        # Random coordinates have to be bounded my minimal and maximal values in each dimension of observations
        # Min/Max values list stores Min/Max values of observations in respect of each dimension
        min_values = [val for val in self.observations[0].coordinates]
        max_values = [val for val in self.observations[0].coordinates]

        for observation in self.observations:
            for i in range(0, self.dimensions):
                if observation.coordinates[i] < min_values[i]:
                    min_values[i] = observation.coordinates[i]
                elif observation.coordinates[i] > max_values[i]:
                    max_values[i] = observation.coordinates[i]

        # Create clusters' centroids with sensibly constraint coordinates
        for c in range(0, self.k):
            coordinates = []
            for i in range(0, self.dimensions):
                coordinates.append(random.uniform(min_values[i], max_values[i]))
            self.clusters.append(Cluster("cluster " + str(c), coordinates))

    def assign_clusters(self, cluster_sum_of_distances_map, cluster_number_of_observations):

        # Find nearest centroid for each observation based on Euclidean distance
        for observation in self.observations:
            # Store smallest distance to compare centroids, and chose the closes one
            smallest_distance = None
            # Store nearest centroid
            nearest_cluster = None
            # Valuable for centroid's reposition
            # store distance from observation to centroid in respect of each dimension
            smallest_distances_per_dimension = []
            # Iterate over each cluster
            for cluster in self.clusters:
                distance = 0
                distances_per_dimension = []
                for a, b in zip(observation.coordinates, cluster.coordinates):
                    # Increment sum of Euclidean distances
                    distance += pow((a - b), 2)
                    # Update list of distances per each dimension
                    distances_per_dimension.append(math.fabs(a - b))
                # Compute square root of sum to make it a Euclidean distance
                distance = math.sqrt(distance)
                # Compare this distance with the smallest distance recorded for this observation
                if smallest_distance is None or distance < smallest_distance:
                    smallest_distance = distance
                    nearest_cluster = cluster
                    smallest_distances_per_dimension = distances_per_dimension
            # Finally we can assign cluster for observation
            observation.assign(nearest_cluster)
            # And assign this observation to cluster
            nearest_cluster.assign_observation(observation)
            # Also we update two dictionaries which will be utilized in further step
            cluster_number_of_observations[nearest_cluster] += 1
            # We need to store sum of distances per each dimension in order to reposition centroid
            updated_sum_of_distances = []
            for summed_distances, new_distance in \
                    (zip(cluster_sum_of_distances_map[nearest_cluster], smallest_distances_per_dimension)):
                updated_sum_of_distances.append(summed_distances + new_distance)
            # Update sum of distances per dimension of this centroid
            cluster_sum_of_distances_map[nearest_cluster] = updated_sum_of_distances

    def reposition_clusters(self, cluster_sum_of_distance_map, cluster_number_of_observations):

        # Reposition each clusters' centroid
        for cluster in self.clusters:
            # Number of assigned observations
            num_of_o = cluster_number_of_observations[cluster]
            summed_coordinates = cluster_sum_of_distance_map[cluster]
            # If no observations are assigned to this cluster, don't modify its coordinates
            # in order to avoid division by 0
            if num_of_o != 0:
                new_coordinates = [val / num_of_o for val in summed_coordinates]
                # Update cluster's coordinates
                cluster.update(new_coordinates)

    def compute_purity(self):
        pass

    def test(self, i):

        print("Iteration ",i)

        print("Clusters : ")
        for cluster in self.clusters:
            print("name -", cluster.name, "coordinates -", cluster.coordinates, "num of assigned observations -",
                  len(cluster.observations))
        #
        # print("Observations : ")
        # for observation in self.observations:
        #     print("label -", observation.label, "cluster -", observation.cluster.name)
