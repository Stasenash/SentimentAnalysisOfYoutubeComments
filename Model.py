from abc import abstractmethod, ABCMeta


class Model:
    __metaclass__ = ABCMeta
    """Abstract class that represents model of neuron network"""

    @abstractmethod
    def _read_data(self):
        """some ways to read data"""

    @abstractmethod
    def _prepare_train_data(self, data):
        """some ways to prepare data for neuron network training"""

    @abstractmethod
    def _create_model_layers(self):
        """creating model and add layers to it"""

    @abstractmethod
    def _train_model(self, model):
        """train neuron network on prepared data set"""

    @abstractmethod
    def _execute_teaching(self, model):
        """create neuron network model and train it"""

    @abstractmethod
    def get_prediction(self, texts):
        """getting a results of neuron work"""
