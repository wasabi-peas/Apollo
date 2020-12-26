# -*- coding: utf-8 -*-
"""doc string"""

from typing import Type, Union
from src.product.barrier.base_barrier import BaseBarrier, AfterTrigger


class _BarrierMixin:
    """barrier mixin base class"""
    after_trigger = AfterTrigger(terminate=False, observe=True)

    def __repr__(self):
        return repr(self.after_trigger).replace(
            '<', f'<{self.__class__.__name__} ')


class KnockOutMixin(_BarrierMixin):
    """
    knock-out barrier mixin
    terminate contract and post a different payoff immediately
    """
    after_trigger = AfterTrigger(terminate=True, observe=False)


class KnockInMixin:
    """
    knock-in barrier mixin
    switch product future payoff, non-reversible
        typically from a constant payoff to an option payoff
    """
    after_trigger = AfterTrigger(terminate=False, observe=False)


class LizardMixin:
    """
    lizard barrier mixin
    terminate contract for protective purpose
        typically post a conservative payoff than knock-out
    """
    after_trigger = AfterTrigger(terminate=True, observe=False)


class AccrualMixin:
    """
    accrual barrier mixin
    no effect to contract term and observe regularly
        payoff-accumulating barrier
    """
    after_trigger = AfterTrigger(terminate=False, observe=True)


def make_barrier(base_barrier: Type[BaseBarrier],
                 barrier_mixin: Type[_BarrierMixin],
                 ) -> Type[Union[BaseBarrier, _BarrierMixin]]:
    """
    add barrier mixin into base barrier

    parameters
    ----------
    base_barrier: base barrier class to be mixed to
    barrier_mixin: barrier mixin to be mixed

    returns
    -------
    mixed barrier class

    examples
    --------
    >>> from src.product.barrier import UpperBarrier
    >>> Barrier = make_barrier(UpperBarrier, KnockOutMixin)
    >>> print(Barrier.__name__)
    KnockOutUpperBarrier
    >>> print(Barrier.after_trigger)
    <AfterTrigger terminate&observe>
    >>> barrier = Barrier(position=1.2)
    >>> print(barrier)
    <KnockOutUpperBarrier @1.2 no-triggered>
    """
    mixin_name = barrier_mixin.__name__.replace('Mixin', '')
    barrier_name = f'{mixin_name}{base_barrier.__name__}'
    namespace = {'base_barrier': base_barrier, 'barrier_mixin': barrier_mixin}
    statement = f'class {barrier_name}(barrier_mixin, base_barrier): pass'
    exec(statement, namespace)
    return namespace[barrier_name]


if __name__ == '__main__':
    pass
