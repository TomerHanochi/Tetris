from random import uniform

from tetris.ai.vector import Vector


class Network:
    def __init__(self, size: int = 4, weights: Vector = None, activate_func: str = 'relu') -> None:
        if weights is None:
            self.__weights = Vector(*(uniform(-1, 1) for _ in range(size)))
        else:
            self.__weights = weights
        self.weights.normalize()
        self.activation = getattr(Network, activate_func)

    def activate(self, x: Vector) -> float:
        return self.activation(self.weights.dot(x))

    def mutate(self, power: float) -> None:
        self.__weights -= Vector(*(uniform(-power, power) for _ in range(len(self.__weights))))
        self.__weights.normalize()

    @property
    def weights(self) -> Vector:
        return self.__weights

    @staticmethod
    def relu(x) -> float:
        return x if x > 0 else 0
