class Cluster:

    def __init__(self, name, coordinates):
        # Name of a cluster, so they can be distinguished from each other
        self.name = name
        # Coordinates of the cluster in space
        self.coordinates = coordinates
        # List of assigned observations
        self.observations = []

    def update(self, coordinates):
        self.coordinates = coordinates

    def assign_observation(self, observation):
        self.observations.append(observation)

    def reset_observations_assignment(self):
        self.observations = []
