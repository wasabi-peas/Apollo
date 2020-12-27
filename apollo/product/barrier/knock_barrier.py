# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
from typing import NoReturn
from apollo.product.barrier.position_barrier import PositionBarrier
from apollo.utils import Numerical


class _KnockBarrier(PositionBarrier):
    """stop observe once triggered"""
    def _observe_impl(self, date: dt.date, price: Numerical) -> NoReturn:
        super()._observe_impl(date, price)
        if self.triggered:
            self.do_observe = False


class KnockOutBarrier(_KnockBarrier):
    """
    knock-out barrier
    terminate contract and post a different payoff immediately
    """
    pass


class KnockInBarrier(PositionBarrier):
    """
    knock-in barrier
    switch product future payoff, non-reversible
        typically from a constant payoff to an option payoff
    """
    pass


if __name__ == '__main__':
    pass
