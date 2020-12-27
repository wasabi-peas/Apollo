# -*- coding: utf-8 -*-
"""doc string"""

import abc
import datetime as dt
from typing import List, Optional, NoReturn
from src.utils import Numerical


class Barrier(metaclass=abc.ABCMeta):
    """barrier base class"""

    def __init__(self,
                 observe_dates: Optional[List[dt.date]] = None,
                 *args, **kwargs):
        """
        parameters
        ----------
        observe_dates: list of barrier observation dates
        """
        self.observe_dates = observe_dates or []
        self.triggered = False
        self.do_observe = True

    def observe(self, date: dt.date, price: Numerical) -> bool:
        """
        observe if barrier is triggered under given price

        parameters
        ----------
        date: observe date
        price: asset price or performance

        returns
        -------
        barrier is observed or not (not triggered or not)
            * for triggered status, please call barrier.triggered
        """
        if self.do_observe and date in self.observe_dates:
            self._observe_impl(date, price)
            return True
        return False

    @abc.abstractmethod
    def _observe_impl(self, date: dt.date, price: Numerical) -> NoReturn:
        pass

    def __repr__(self):
        status = ' [T]' if self.triggered else ''
        return f'<{self.__class__.__name__}{status}>'


if __name__ == '__main__':
    pass
