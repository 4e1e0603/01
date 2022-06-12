# -*- coding: utf-8 -*-

"""
Marked Petri net.

Terminologie:
- Place
- Transition
"""

from dataclasses import dataclass


@dataclass
class Place:
    holding: int  # The number of tokens this place holds.


@dataclass
class Arc:
    place: Place
    amount: int  # The ammount of tokens to remove on fire (default = 1).


@dataclass
class Outgoing(Arc):
    def trigger(self) -> None:
        self.place.holding -= self.amount

    def not_blocking(self) -> bool:
        return self.place.holding >= self.amount


@dataclass
class Ingoing(Arc):
    def trigger(self) -> None:
        pass


class Transition:
    def __init__(self, ingoing_arcs, outgoing_arcs):
        self.outgoing_arcs = set(outgoing_arcs)
        self.arcs = self.union(ingoing_arcs)

    def fire():
        ...


class PetriNet:
    def __init__(self, transitions: list[Transition]) -> None:
        self.transitions = transitions

    def execute():
        print("--START--")

        print("--FINISH--")


def parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--firings", type=int)
    parser.add_argument("--marking", type=int, nargs="+")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # places
    ps = 
    
    # transitions
    ts = dict(
        t1 = Transition(None, None),
        t2 = Transition(None, None), 
    )

    # firing_sequence: deterministic example
    fs = ["t1", "t1", "t2", "t1"] 

    petri_net.run(fs, ps)