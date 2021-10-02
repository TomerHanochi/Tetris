from __future__ import annotations
from random import random

import numpy as np

from tetris.ai.network import Network


class Population:
    subpool_size = .1
    offspring_size = .3
    mutation_chance = .05
    mutation_pwr = .2

    def __init__(self, size: int = 500, old_pop: Population = None) -> None:
        if old_pop is None:
            self.__networks = [Network() for _ in range(size)]
            self.__fitnesses = [0 for _ in range(size)]
        else:
            self.__networks = Population.crossover(networks=old_pop.networks,
                                                   fitnesses=old_pop.fitnesses)
            self.__fitnesses = [0 for _ in range(len(self.networks))]

    @staticmethod
    def offspring(networks: list[Network], fitnesses: list[float]) -> list[Network]:
        offsprings = list()
        num_of_offspring = int(len(networks) * Population.offspring_size)
        num_of_parent_candidates = int(len(networks) * Population.subpool_size)
        for _ in range(num_of_offspring):
            parent_candidates_indices = np.random.choice(len(networks), num_of_parent_candidates,
                                                         replace=False)
            parent_candidates = np.array([networks[index] for index in parent_candidates_indices])
            parent_fitnesses = np.array([fitnesses[index] for index in parent_candidates_indices])

            parent_indices = np.argpartition(parent_fitnesses, -2)[-2:]
            parent1, parent2 = parent_candidates[parent_indices]
            fitness1, fitness2 = parent_fitnesses[parent_indices]
            offspring = Network(weights=parent1.weights * int(fitness1 + 1) +
                                        parent2.weights * int(fitness2 + 1))
            if random() < Population.mutation_chance:
                offspring.mutate(Population.mutation_pwr)
            offsprings.append(offspring)
        return offsprings

    @staticmethod
    def crossover(networks: list[Network], fitnesses: list[float]) -> list[Network]:
        num_of_offspring = int(len(networks) * Population.offspring_size)
        weakest_indices = np.argpartition(fitnesses, -num_of_offspring)[-num_of_offspring:]
        new_networks = [
            network for i, network in enumerate(networks) if i not in weakest_indices
        ]
        new_networks.extend(Population.offspring(networks, fitnesses))
        return new_networks

    @property
    def networks(self) -> list[Network]:
        return self.__networks

    @property
    def fitnesses(self) -> list[float]:
        return self.__fitnesses

    @fitnesses.setter
    def fitnesses(self, fitnesses: list[float]) -> None:
        if isinstance(fitnesses, list):
            if len(fitnesses) == len(self.fitnesses):
                self.__fitnesses = fitnesses
            else:
                raise ValueError(f'Expected len {len(self.__fitnesses)}, got len {len(fitnesses)}')
        else:
            raise TypeError(f'Expected list, got {fitnesses.__class__.__name__}')

    def __iter__(self) -> iter:
        return iter(self.networks)
