class Observation:
    def __init__(self, coordinates, label=None):
        # Attribute values interpreted as coordinates in space
        self.coordinates = coordinates
        # Assigned cluster
        self.cluster = None
        # Label - only in case of labelled data
        self.label = label

    def assign(self, cluster):
        self.cluster = cluster
