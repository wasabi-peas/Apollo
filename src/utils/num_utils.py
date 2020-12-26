# -*- coding: utf-8 -*-
"""doc string"""

from src.utils.typing import Numerical


class NumberCompare:
    """compare number based on given precision"""

    def __init__(self, digit: int = -8):
        """
        parameters
        ----------
        digit: precision digit (1Ex)
            e.x. digit = -3, then precision = 0.001
            e.x. digit = 2, then precision = 100
        """
        self._precision = 10 ** digit

    def equal(self, num1: Numerical, num2: Numerical) -> bool:
        """check if num1 == num2"""
        return abs(num1 - num2) < self._precision

    def greater(self, num1: Numerical, num2: Numerical) -> bool:
        """check if num1 > num2"""
        return (num1 > num2) and (not self.equal(num1, num2))

    def smaller(self, num1: Numerical, num2: Numerical) -> bool:
        """check if num1 < num2"""
        return (num1 < num2) and (not self.equal(num1, num2))

    def not_greater(self, num1: Numerical, num2: Numerical) -> bool:
        """check if num1 <= num2"""
        return (num1 < num2) or self.equal(num1, num2)

    def not_smaller(self, num1: Numerical, num2: Numerical) -> bool:
        """check if num1 >= num2"""
        return (num1 > num2) or self.equal(num1, num2)


precision_2 = NumberCompare(-2)
precision_4 = NumberCompare(-4)
precision_8 = NumberCompare(-8)


if __name__ == '__main__':
    pass
