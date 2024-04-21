from observation import Observation


class Converter:

    def __init__(self, directory, is_data_labelled=False):
        # Path to data file
        self.directory = directory
        # Depending on the presence of labels converter changes behaviour
        self.is_data_labelled = is_data_labelled
        # Labels tuple
        self.labels = None
        # Observations tuple
        self.observations = None
        # Convert raw data into observations objects and list of labels
        self.convert()

    def convert(self):

        # Fill observations list and labels list
        # Open file with  data
        with open(self.directory, "r", encoding="UTF-8") as file:
            for line in file:

                if self.is_data_labelled:
                    attributes = [float(val) for val in line.split(",")[0:-1]]
                    label = line.split(",")[-1].strip("\n")

                    # Add label to labels list if it's not already there
                    if label not in self.labels:
                        self.labels.append(label)

                else:
                    attributes = [float(val) for val in line.split(",")[:]]
                    label = None

                observation = Observation(coordinates=attributes, label=label)
                self.observations.append(observation)