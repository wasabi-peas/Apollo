# -*- coding: utf-8 -*-
"""doc string"""

import abc
import datetime as dt
from typing import List, Optional
from src.utils import Numerical


class AfterTrigger:
    def __init__(self, terminate: bool, observe: bool):
        self.terminate = terminate
        self.observe = observe


class BaseBarrier(metaclass=abc.ABCMeta):
    after_trigger = AfterTrigger(terminate=False, observe=False)

    def __init__(self, observe_date: Optional[List[dt.date]]):
        self.observe_dates = observe_date
        self.triggered = False

    def register_observe_date(self, date_list: List[dt.date]):
        self.observe_dates = date_list

    @abc.abstractmethod
    def observe(self, price: Numerical) -> bool:
        return self.triggered


if __name__ == '__main__':
    pass
