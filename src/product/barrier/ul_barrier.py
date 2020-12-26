# -*- coding: utf-8 -*-
"""doc string"""

from typing import Callable
from src.product.barrier.base_barrier import BaseBarrier
from src.utils import Numerical, precision_8


class _PositionBarrier(BaseBarrier):
    _check_func = (Callable, Callable)

    def __init__(self, position: Numerical, inclusive: bool = True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = position
        self.inclusive = inclusive

    def observe(self, price: Numerical) -> bool:
        if self.inclusive:
            check_func = self._check_func[0]
        else:
            check_func = self._check_func[1]
        if check_func(price, self.position):
            self.triggered = True
        return self.triggered


class UpperBarrier(_PositionBarrier):
    _check_func = (precision_8.not_smaller, precision_8.greater)


class LowerBarrier(_PositionBarrier):
    _check_func = (precision_8.not_greater, precision_8.smaller)


if __name__ == '__main__':
    pass
