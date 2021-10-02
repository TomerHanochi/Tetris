from __future__ import annotations
import math


class Vector(tuple):
    def __new__(cls, iterable: iter) -> Vector:
        """ An immutable vector based on a tuple. """
        return super().__new__(cls, iterable)

    def magnitude(self) -> float:
        """ Returns the magnitude/length of the vector. """
        return math.sqrt(sum(x * x for x in self))

    def normalized(self) -> Vector:
        """ Returns a new vector that is equal to normalized self. """
        mag = self.magnitude()
        return self.__class__(x / mag for x in self)

    def dot(self, vector: Vector) -> float:
        """ Returns the dot product of self and another vector. """
        if not isinstance(vector, Vector):
            raise ValueError('The dot product requires another vector')
        return sum(a * b for a, b in zip(self, vector))

    def __mul__(self, other: Vector | int | float) -> Vector | float:
        """
        :param other: a vector, or a scalar.
        :return: if other is a vector, return self and other's dot product.
                 if other is a scalar, return a new vector with each value of self multiplied
                 by other.
        """
        if isinstance(other, Vector):
            return self.dot(other)
        elif isinstance(other, (int, float)):
            return self.__class__(a * other for a in self)
        else:
            raise ValueError(f'Multiplication with type {other.__class__.__name__} not supported')

    def __rmul__(self, other: Vector | int | float) -> Vector | float:
        return self.__mul__(other)

    def __truediv__(self, other: Vector | int | float) -> Vector:
        """
        :param other: a vector, or a scalar
        :return: if other is a vector, return a new vector with each value of self divided by the
                 respective value of other
                 if other is a scalar, return a new vector with each value of self divided
                 by other
        """
        if isinstance(other, Vector):
            divided = (a / b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            divided = (a / other for a in self)
        else:
            raise ValueError(f'Division with type {other.__class__.__name__} not supported')

        return self.__class__(divided)

    def __add__(self, other) -> Vector:
        """
        :param other: a vector, or a scalar.
        :return: if other is a vector, return a new vector with each value of self added with the
                 respective value of other.
                 if other is a scalar, return a new vector with each value of self added with
                 other.
        """
        if isinstance(other, Vector):
            added = (a + b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            added = (a + other for a in self)
        else:
            raise ValueError(f'Addition with type {type(other)} not supported')

        return self.__class__(added)

    def __radd__(self, other) -> Vector:
        return self.__add__(other)

    def __sub__(self, other) -> Vector:
        """
        :param other: a vector, or a scalar.
        :return: if other is a vector, return a new vector with each value of self subbed with the
                 respective value of other.
                 if other is a scalar, return a new vector with each value of self subbed with
                 other.
        """
        if isinstance(other, Vector):
            subbed = (a - b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            subbed = (a - other for a in self)
        else:
            raise ValueError(f'Subtraction with type {type(other)} not supported')

        return self.__class__(subbed)

    def __rsub__(self, other) -> Vector:
        return self.__sub__(other)

    def __repr__(self) -> str:
        return f'Vector{tuple(a for a in self)!r}'
