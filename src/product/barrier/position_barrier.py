# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
from typing import List, Union, NoReturn
from src.product.barrier.base_barrier import Barrier
from src.utils import Numerical, precision_8


class PositionBarrier(Barrier):
    """
    most common barrier to compare asset price and barrier position
    to decide if barrier should be triggered or not
    """
    _all_compare_func = {
        'upper': (precision_8.greater, precision_8.not_smaller),
        'lower': (precision_8.smaller, precision_8.not_greater)
    }

    def __init__(self,
                 position: Union[Numerical, List[Numerical]],
                 observe_dates: Union[List[dt.date]],
                 direction: str = 'upper',
                 inclusive: bool = True,
                 *args, **kwargs):
        """
        parameters
        ----------
        position: barrier position in price or performance to compare asset price with
            when position is given as list, dimension should match the dimension of observation dates
        observe_dates: list of barrier observation dates
        direction: upper barrier or lower barrier
        inclusive: trigger or not when asset price equals to barrier position
        """
        super().__init__(observe_dates, *args, **kwargs)
        assert direction in ['upper', 'lower'], \
            f"direction should be either 'upper' or 'lower', " \
            f"got '{direction}'"
        self.direction = direction
        if isinstance(position, list):
            assert len(position) == len(self.observe_dates), \
                f'position dimension ({len(position)}) != ' \
                f'date dimension ({len(self.observe_dates)})'
            self.position = {date: pos for date, pos in
                             zip(self.observe_dates, position)}
        else:
            self.position = position
        self.inclusive = inclusive

    @property
    def _compare_func(self):
        """function to compare price and position"""
        return self._all_compare_func[self.direction][int(self.inclusive)]

    def _observe_impl(self, date: dt.date, price: Numerical) -> NoReturn:
        if isinstance(self.position, dict):
            position = self.position[date]
        else:
            position = self.position
        self.triggered = self._compare_func(price, position)

    def __repr__(self):
        status = ' [T]' if self.triggered else ''
        description = f'{self.direction}@{self.position}'
        return f'<{self.__class__.__name__} {description}{status}>'


if __name__ == '__main__':
    pass
