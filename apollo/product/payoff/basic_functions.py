import numpy as np
from abc import ABCMeta, abstractmethod
from apollo.utils import Numerical


class FunctionBase(metaclass=ABCMeta):
    """base class for 2D functions"""
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def formula(self, *args, **kwargs):
        pass


class Constant(FunctionBase):
    """constant function"""
    def __init__(self, level: Numerical = 1, *args, **kwargs):
        """
        init
        :param level: constant value
        """
        self.level = level
        super().__init__(*args, **kwargs)

    def formula(self, *args, **kwargs):
        return self.level


class Linear(FunctionBase):
    """linear function"""
    def __init__(self, slope: Numerical = 1, origin: Numerical = 0, *args, **kwargs):
        """
        init
        :param slope: slope of the linear function
        :param origin: shift in x-axis
        """
        self.slope = slope
        self.origin = origin
        super().__init__(*args, **kwargs)

    def formula(self, x: Numerical):
        return self.slope * (x - self.origin)


class Step(FunctionBase):
    """step function"""
    def __init__(self,
                 level: Numerical = 1,
                 origin: Numerical = 0,
                 sign: int = 1,
                 inclusive: bool = True,
                 *args,
                 **kwargs):
        """
        init
        :param level: constant value
        :param origin: shift in x-axis
        :param sign: flip the function about the origin
        :param inclusive: constant value in the origin
        """
        self.level = level
        self.origin = origin
        self.sign = sign
        self.inclusive = inclusive
        super().__init__(*args, **kwargs)

    def formula(self, x: Numerical):
        return np.piecewise(x,
                            [x * self.sign < self.origin * self.sign,
                             x == self.origin,
                             x * self.sign > self.origin * self.sign],
                            [0.0,
                             self.level if self.inclusive else 0.0,
                             self.level])


class Ramp(FunctionBase):
    """ramp function"""
    def __init__(self,
                 slope: Numerical = 1,
                 origin: Numerical = 0,
                 sign: int = 1,
                 *args, **kwargs):
        """
        init
        :param slope: the slope of the ramp function
        :param origin: shift in x-axis
        :param sign: flip the function about the origin
        """
        self.slope = slope
        self.origin = origin
        self.sign = sign
        super().__init__(*args, **kwargs)

    def formula(self, x: Numerical):
        return max(self.sign * (x - self.origin), 0) * self.slope


if __name__ == '__main__':
    s = Step(origin=1, sign=-1, level=2.3, inclusive=False)
    print(s.formula(0.5))

    r = Ramp(slope=1.2, sign=-1, origin=1)
    print(r.formula(0.8))

    s1 = Step(origin=1, sign=1, level=1, inclusive=False)
    s2 = Step(origin=1, sign=-1, level=-1, inclusive=False)
    s3 = Step(origin=2, sign=1, level=-1, inclusive=False)

    def combine(_x):
        return s1.formula(_x) + s2.formula(_x) + s3.formula(_x)
    print(combine(0.5))


