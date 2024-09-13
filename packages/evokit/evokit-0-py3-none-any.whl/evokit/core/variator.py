from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from typing import Sequence
    from typing import Tuple
    from typing import Self
    from typing import Type
    from typing import Any

from abc import abstractmethod
from abc import ABC
from typing import Generic, TypeVar

from .population import Individual, Population
from typing import override

D = TypeVar("D", bound=Individual)


class Variator(ABC, Generic[D]):
    def __new__(cls: Type[Self], *args: Any, **kwargs: Any) -> Self:
        """Machinery. Implement managed attributes.

        :meta private:
        """
        instance: Self = super().__new__(cls)
        instance.arity = None
        instance.coarity = None
        return instance

    def __init__(self: Self) -> None:
        self.arity: Optional[int]
        self.coarity: Optional[int]

    @abstractmethod
    def vary(self, parents: Sequence[D]) -> Tuple[D, ...]:
        """Apply the variator to a tuple of parents

        Produce a tuple of individuals from a tuple of individuals.
        The input and output tuple sizes should match the arity and coarity of
        this selector, respectively.

        Note:
            If the result could have a different
            :attr:`fitness .Individual.reset_fitness`
            than the original individual, call :meth:`.Individual.reset_fitness`
            to clear its fitness.
        """
        pass

    def _group_to_parents(self,
                          population: Population[D])\
            -> Sequence[Sequence[D]]:
        """Machinery.
        """
        # Tuple magic. Zipping an iterable with itself extracts a tuple of
        #   that size. The "discarding" behaviour is implemented this way.
        parent_groups: Sequence[Sequence[D]]
        if self.arity is None:
            raise TypeError("Variator does not specify arity,"
                            "cannot create parent groups")
        else:
            parent_groups = tuple(zip(*(iter(population),) * self.arity))
        return parent_groups

    def vary_population(self: Self, population: Population[D]) -> Population[D]:
        """Vary the population.

        Separate ``population`` into groups of size `.arity`. For each group,
        call `.vary` with that group as argument, then collect the result.

        At the end, return a :class:`.Population` of collected results.
        """
        next_population = Population[D]()
        parent_groups: Sequence[Sequence[D]] =\
            self._group_to_parents(population)
        for group in parent_groups:
            results = self.vary(group)
            for individual in results:
                next_population.append(individual)
        return next_population


class NullVariator(Variator[D]):
    """Variator that does not change anything
    """
    def __init__(self) -> None:
        self.arity = 1
        self.coarity = 1

    @override
    def vary(self, parents: Sequence[D]) -> Tuple[D, ...]:
        return tuple(parents)
