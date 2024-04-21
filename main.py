from converter import Converter
from clusterer import Clusterer

is_data_labeled = True

converter = Converter("data/iris.txt", is_data_labeled)
converter.convert()

clusterer = Clusterer(converter.observations, converter.dimensions, 3, is_data_labeled, converter.labels)
clusterer.compute()


