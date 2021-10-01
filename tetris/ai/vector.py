from __future__ import annotations

import math


class Vector:
    def __init__(self, iterable: iter) -> None:
        """ Create a vector, example: v = Vector(1,2) """
        self.values = tuple(map(float, iterable))

    def magnitude(self) -> float:
        """ Returns the magnitude of the vector """
        return math.sqrt(sum(x * x for x in self))

    def normalize(self) -> Vector:
        """ normalizes a vector """
        mag = self.magnitude()
        self.values = tuple(x / mag for x in self)
        return self

    def dot(self, vector) -> float:
        """ Returns the dot product of self and another vector"""
        if not isinstance(vector, Vector):
            raise ValueError('The dot product requires another vector')
        return sum(a * b for a, b in zip(self, vector))

    def __mul__(self, other) -> Vector or float:
        """
        Returns the dot product of self and other if multiplied
        by another Vector.  If multiplied by an int or float,
        multiplies each component by other.
        """
        if isinstance(other, Vector):
            return self.dot(other)
        elif isinstance(other, (int, float)):
            return self.__class__(a * other for a in self)
        else:
            raise ValueError(f'Multiplication with type {type(other)} not supported')

    def __rmul__(self, other) -> Vector:
        return self.__mul__(other)

    def __truediv__(self, other) -> Vector:
        if isinstance(other, Vector):
            divided = tuple(self[i] / other[i] for i in range(len(self)))
        elif isinstance(other, (int, float)):
            divided = tuple(a / other for a in self)
        else:
            raise ValueError(f'Division with type {type(other)} not supported')

        return self.__class__(divided)

    def __add__(self, other) -> Vector:
        if isinstance(other, Vector):
            added = tuple(a + b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            added = tuple(a + other for a in self)
        else:
            raise ValueError(f'Addition with type {type(other)} not supported')

        return self.__class__(added)

    def __radd__(self, other) -> Vector:
        return self.__add__(other)

    def __sub__(self, other) -> Vector:
        if isinstance(other, Vector):
            subbed = tuple(a - b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            subbed = tuple(a - other for a in self)
        else:
            raise ValueError(f'Subtraction with type {type(other)} not supported')

        return self.__class__(subbed)

    def __rsub__(self, other) -> Vector:
        return self.__sub__(other)

    def __iter__(self) -> iter:
        return iter(self.values)

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, key) -> float or int:
        return self.values[key]

    def __repr__(self) -> str:
        return repr(self.values)
