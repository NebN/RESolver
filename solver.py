from dataclasses import dataclass
from typing import List

import random

@dataclass
class RESolution:
    ok: bool
    movements: List[int]

    def length(self):
        return len(self.movements)

    def is_better_than(self, other):
        if not other:
            return True
        
        if self.ok == other.ok:
            return self.length() < other.length()
        
        return self.ok

    def __str__(self):
        return f'{"" if self.ok else "KO!!! "}{",".join(map(lambda n: str(n), self.movements))}'


class RESolver:

    goal = [True, False, True, True, False, False, False]
    max_size = len(goal)

    def __init__(self):
        self.symbols = [False] * self.max_size
        self.current_ix = 0
        self.movements = []
        self.outcome = None


    @classmethod
    def _next_movement(cls):
        if random.getrandbits(1):
            return 3
        return 4


    def _current_outcome(self):
        if (all(self.symbols)):
            return RESolution(movements=self.movements, ok=False)
        elif self.symbols == self.goal:
            return RESolution(movements=self.movements, ok=True)


    def _next(self, plus):
        self.current_ix = (self.current_ix + plus) % self.max_size
        return self.current_ix


    def _spin(self, n):
        next = self._next(n)
        self.symbols[next] = not self.symbols[next]


    def attempt_to_solve(self):
        while self.outcome is None:
            move = RESolver._next_movement()
            self.movements.append(move)
            self._spin(move)
            self.outcome = self._current_outcome()
        
        return self.outcome
        