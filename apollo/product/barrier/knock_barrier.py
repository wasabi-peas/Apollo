# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
from typing import NoReturn
from apollo.product.barrier.position_barrier import PositionBarrier
from apollo.utils import Numerical


class _KnockBarrier(PositionBarrier):
    """stop observe once triggered"""
    pass


class KnockOutBarrier(_KnockBarrier):
    """
    knock-out barrier
    terminate contract and post a different payoff immediately
    """
    pass


class KnockInBarrier(_KnockBarrier):
    """
    knock-in barrier
    switch product future payoff, non-reversible
        typically from a constant payoff to an option payoff
    """
    pass


if __name__ == '__main__':
    pass
