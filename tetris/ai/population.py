from __future__ import annotations

import numpy as np

from tetris.ai.network import Network


class Population:
    def __init__(self, size: int = 500, old_pop: Population = None) -> None:
        if old_pop is None:
            self.__networks = [Network() for _ in range(size)]
            self.__fitnesses = [0 for _ in range(size)]
        else:
            self.__networks = []
            self.crossover(networks=old_pop.networks, fitnesses=old_pop.fitnesses)
            self.mutate()
            self.__fitnesses = [0 for _ in range(len(self.networks))]

    def crossover(self, networks: list[Network], fitnesses: list[float]) -> None:
        sorted_networks_indecies = list(reversed(np.argsort(fitnesses)))
        elite_amount = len(sorted_networks_indecies) // 2
        elite_network_indecies = sorted_networks_indecies[:elite_amount]
        for i in elite_network_indecies:
            self.networks.append(networks[i])
        for network in self.networks.copy():
            self.networks.append(Network(weights=network.weights))

    def mutate(self) -> None:
        mutable = self.networks[len(self.networks) // 2:]
        for network in mutable:
            network.mutate(0.1)

    @property
    def networks(self) -> list[Network]:
        return self.__networks

    @property
    def fitnesses(self) -> list[float]:
        return self.__fitnesses

    @fitnesses.setter
    def fitnesses(self, fitnesses: list[float]) -> None:
        if isinstance(fitnesses, list):
            if len(fitnesses) == len(self.__fitnesses):
                self.__fitnesses = fitnesses
            else:
                raise ValueError(f'Expected len {len(self.__fitnesses)}, got len {len(fitnesses)}')
        else:
            raise TypeError(f'Expected list, got {fitnesses.__class__.__name__}')

    def __iter__(self) -> iter:
        return iter(self.networks)
