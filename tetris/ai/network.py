from random import uniform, choice
from math import exp

from tetris.ai.vector import Vector
from tetris.ai.heuristics import Heuristics


class Network:
    def __init__(self, size: int = Heuristics.size, weights: iter = None,
                 activation_func: str = 'sigmoid') -> None:
        """
        A neural network with no hidden layers.
        :param size: the number of inputs
        :param weights: vector of weights to be used
        :param activation_func: the activation function to be used, relu or sigmoid
        """
        if weights is None:
            # if there are no weights to use create a random network
            self.__weights = Vector(uniform(-1, 1) for _ in range(size))
        else:
            self.__weights = Vector(weight for weight in weights)
        self.__weights = self.weights.normalized()
        self.activation = getattr(Network, activation_func)

    def activate(self, x: Vector) -> float:
        return self.activation(self.weights.dot(x))

    def mutate(self, power: float) -> None:
        """
        Mutates a random weight of the network by a random amount
        :param power: the range of possible values to mutate by, [-power, power]
        """
        mutation = choice(range(len(self.weights)))
        self.__weights += Vector(
            uniform(-power, power) if i == mutation else 0 for i in range(len(self.weights))
        )
        self.__weights = self.weights.normalized()

    @property
    def weights(self) -> Vector:
        return self.__weights

    @staticmethod
    def relu(x) -> float:
        return x if x > 0 else 0

    @staticmethod
    def sigmoid(x) -> float:
        return 1 / (1 + exp(-x))

    def __repr__(self) -> str:
        return (f'Network(size={len(self.weights)}, weights={repr(self.weights)}, activation_func='
                f'{self.activation.__name__})')
