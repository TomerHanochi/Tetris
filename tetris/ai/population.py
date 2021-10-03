from __future__ import annotations
from random import random

import numpy as np

from tetris.ai.network import Network


class Population:
    def __init__(self, size: int = 500, old_pop: Population = None,
                 parent_candidates_pct: float = .1, offspring_pct: float = .3,
                 mutation_chance: float = .05, mutation_pwr: float = .2) -> None:
        """
        Represents a list of networks that can evolve over time using a genetic algorithm.
        The population starts with random networks, and each generation the fittest networks
        are combined to produce child networks.
        Afterwards the weakest networks are replaced by the children.
        :param size: the size of the initial population.
        :param old_pop: an old population on which we create a new population using the algorithm
                        described above.
        :param parent_candidates_pct: the percent of the total number of networks that we use to
                                      choose the number of parent candidates.
        :param offspring_pct: the percent of the total number of networks that we use to choose
                              the number of offspring.
        :param mutation_chance: the chance for a child to mutate.
        :param mutation_pwr: the amount the child will mutate by, random  number in the.
                             [-mutation_pwr, mutation_pwr] range.
        """
        if old_pop is None:
            self.__networks = [Network() for _ in range(size)]
            self.__fitnesses = [0 for _ in range(size)]
        else:
            self.__networks = self.crossover(networks=old_pop.networks,
                                             fitnesses=old_pop.fitnesses)
            self.__fitnesses = [0 for _ in range(len(self.networks))]

        self.offspring_pct = offspring_pct
        self.parent_candidates_pct = parent_candidates_pct
        self.mutation_chance = mutation_chance
        self.mutation_pwr = mutation_pwr

    def offspring(self, networks: list[Network], fitnesses: list[float]) -> list[Network]:
        """
        Each iteration, we pick a random percent of the total networks. The two fittest networks
        among them will become the parent networks.
        We decide the weights for the child network as:
        child_weights =  weights1 * fitness1 +  weights2 * fitness2
        It then has a chance to mutate. Mutation causes a random part of the weights to increase by
        a random number in the [-mutation_pwr, mutation_pwr] range.
        It is then normalized, resulting in a weight vector that is between the two parents, but
        closer to the fitter one.
        :param networks: a list of networks to produce offspring from.
        :param fitnesses: a list of fitnesses corresponding to the network.
        :return: a list of child networks.
        """
        num_of_offspring = int(len(networks) * self.offspring_pct)
        num_of_parent_candidates = int(len(networks) * self.parent_candidates_pct)
        offspring = list()
        for _ in range(num_of_offspring):
            # the indecies of the random parent candidates
            parent_candidates_indices = np.random.choice(len(networks), num_of_parent_candidates,
                                                         replace=False)
            # the parents and their corresponding fitnesses
            parent_candidates = np.array([networks[index] for index in parent_candidates_indices])
            parent_fitnesses = np.array([fitnesses[index] for index in parent_candidates_indices])

            # the two fittest parents
            parent_indices = np.argpartition(parent_fitnesses, -2)[-2:]
            p1, p2 = parent_candidates[parent_indices]
            f1, f2 = parent_fitnesses[parent_indices]
            child = Network(weights=p1.weights * f1 + p2.weights * f2)
            if random() < self.mutation_chance:
                child.mutate(self.mutation_pwr)
            offspring.append(child)
        return offspring

    def crossover(self, networks: list[Network], fitnesses: list[float]) -> list[Network]:
        """
        The crossover is the replacement of weak networks with possibly stronger networks.
        For each offspring we remove the weakest network, and replace it with the offspring.
        :param networks: a list of networks to produce offspring from.
        :param fitnesses: a list of fitnesses corresponding to the network.
        :return: a list of networks with the same size as networks.
        """
        offspring = self.offspring(networks, fitnesses)
        num_of_offspring = len(offspring)
        weakest_indices = np.argpartition(fitnesses, -num_of_offspring)[-num_of_offspring:]
        new_networks = [
            network for i, network in enumerate(networks) if i not in weakest_indices
        ]
        new_networks.extend(offspring)
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
