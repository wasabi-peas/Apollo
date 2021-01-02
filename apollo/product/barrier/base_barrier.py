# -*- coding: utf-8 -*-
"""doc string"""

import abc
import datetime as dt
from typing import List, Optional, Callable, Union
from apollo.utils import Numerical


class Barrier(metaclass=abc.ABCMeta):
    """barrier base class"""

    def __init__(self, observe_dates: Optional[List[dt.date]] = None):
        """
        parameters
        ----------
        observe_dates: list of barrier observation dates
        """
        self.observe_dates = observe_dates or []

    @abc.abstractmethod
    def observe(self, date: dt.date, price: Numerical) -> bool:
        """
        observe if barrier is triggered under given price

        parameters
        ----------
        date: observe date
        price: asset price or performance

        returns
        -------
        barrier is triggered or not
        """
        pass

    @abc.abstractmethod
    def observe_func(self, date: dt.date) -> Callable:
        """
        return an observe function with price as only parameter

        parameters
        ----------
        date: observe date

        returns
        -------
        observe function takes price and return trigger or not
        """
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__}>'


if __name__ == '__main__':
    pass
