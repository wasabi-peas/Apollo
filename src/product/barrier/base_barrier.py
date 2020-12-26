# -*- coding: utf-8 -*-
"""doc string"""

import abc
import datetime as dt
from typing import List, Optional, NoReturn
from src.utils import Numerical


class AfterTrigger:
    """performance record after barrier is triggered"""
    def __init__(self, terminate: bool, observe: bool):
        self.terminate = terminate
        self.observe = observe

    def __repr__(self):
        terminate = 'terminate' if self.terminate else 'no-terminate'
        observe = 'observe' if self.terminate else 'no-observe'
        return f'<AfterTrigger {terminate}&{observe}>'


class BaseBarrier(metaclass=abc.ABCMeta):
    """barrier base class"""
    after_trigger = AfterTrigger(terminate=False, observe=True)

    def __init__(self, observe_dates: Optional[List[dt.date]] = None,
                 *args, **kwargs):
        """
        parameters
        ----------
        observe_dates: list of barrier observation dates
        """
        self.observe_dates = observe_dates or []
        self.triggered = False

    def register_observe_date(self, date_list: List[dt.date]) -> NoReturn:
        self.observe_dates = date_list

    def observe(self, price: Numerical) -> bool:
        """
        observe if barrier is triggered under given price

        parameters
        ----------
        price: asset price or performance

        returns
        -------
        barrier is triggered or not
        """
        if self.triggered and not self.after_trigger.observe:
            return self.triggered
        return self._observe_impl(price)

    @abc.abstractmethod
    def _observe_impl(self, price: Numerical) -> bool:
        return self.triggered

    def __repr__(self):
        status = 'trigger' if self.triggered else 'no-trigger'
        return f'<{self.__class__.__name__} {status}>'


if __name__ == '__main__':
    pass
