from random import uniform
from math import exp

from tetris.ai.vector import Vector
from tetris.ai.heuristics import Heuristics


class Network:
    def __init__(self, size: int = Heuristics.size, weights: Vector = None,
                 activation_func: str = 'sigmoid') -> None:
        if weights is None:
            self.__weights = Vector(uniform(-1, 1) for _ in range(size))
        else:
            self.__weights = weights
        self.weights.normalize()
        self.activation = getattr(Network, activation_func)

    def activate(self, x: Vector) -> float:
        return self.activation(self.weights.dot(x))

    def mutate(self, power: float) -> None:
        self.__weights -= Vector(uniform(-power, power) for _ in range(len(self.__weights)))
        self.__weights.normalize()

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
