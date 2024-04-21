class Cluster:

    def __init__(self, name, coordinates):
        # Name of a cluster, so they can be distinguished from each other
        self.name = name
        # Coordinates of the cluster in space
        self.coordinates = coordinates

    def update(self, coordinates):
        self.coordinates = coordinates
