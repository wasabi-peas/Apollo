# -*- coding: utf-8 -*-
"""doc string"""

import numpy as np
from typing import Union
from apollo.utils.typing import Numerical


class NumberCompare:
    """compare number based on given precision"""

    def __init__(self, abs_tol=1E-8):
        """
        parameters
        ----------
        abs_tol: absolute tolerance
        """
        self._abs_tol = abs_tol

    def equal(self, num1: Union[Numerical, np.array],
              num2: Union[Numerical, np.array]) -> Union[bool, np.array]:
        """check if num1 == num2"""
        return np.isclose(num1, num2, rtol=0, atol=self._abs_tol)

    def greater(self, num1: Union[Numerical, np.array],
                num2: Union[Numerical, np.array]) -> Union[bool, np.array]:
        """check if num1 > num2"""
        return np.greater(num1, num2) & (~self.equal(num1, num2))

    def less(self, num1: Union[Numerical, np.array],
             num2: Union[Numerical, np.array]) -> Union[bool, np.array]:
        """check if num1 < num2"""
        return np.less(num1, num2) & (~self.equal(num1, num2))

    def greater_equal(self, num1: Union[Numerical, np.array],
                      num2: Union[Numerical, np.array]) -> Union[bool, np.array]:
        """check if num1 <= num2"""
        return np.greater(num1, num2) | self.equal(num1, num2)

    def less_equal(self, num1: Union[Numerical, np.array],
                   num2: Union[Numerical, np.array]) -> Union[bool, np.array]:
        """check if num1 >= num2"""
        return np.less(num1, num2) | self.equal(num1, num2)


precision_2 = NumberCompare(1E-2)
precision_4 = NumberCompare(1E-4)
precision_8 = NumberCompare(1E-8)


if __name__ == '__main__':
    pass
