from __future__ import annotations
from multiprocessing import Pool, cpu_count
from datetime import datetime

import numpy as np
from tqdm import tqdm

from tetris.ai.algorithm import Algorithm
from tetris.ai.network import Network
from tetris.ai.population import Population
from tetris.model.model import Model
from tetris.consts import Consts


class Trainer:
    def __init__(self, generations: int, pop_size: int, games_per_network: int = 10,
                 moves_per_game: int = 500, num_of_workers: int = cpu_count()) -> None:
        """
        :param generations: number of generations(epochs) to run.
        :param pop_size: the number of networks that are in the population.
        :param games_per_network: the number of games(epochs) that are used to evaluate a network.
                                  used so we know the average fitness for a network.
        :param moves_per_game: total number of tetromino pieces that the neural network gets.
                               used to limit the length of games to a fixed size.
        :param num_of_workers: the amount of processes(cores) the training will run on.
                               used to train concurrently to save time.
        """
        self.num_of_workers = num_of_workers
        self.generations = generations
        self.pop_size = pop_size
        self.games_per_network = games_per_network
        self.moves_per_game = moves_per_game

    def evaluate_network(self, network: Network) -> float:
        """
        Evaluates the network based on the number of lines cleared in self.eval_epochs games
        :param network: a neural network to evaluate
        :return: total number of lines cleared during self.eval_epochs games
        """
        model = Model()
        fitness = 0
        for _ in range(self.games_per_network):
            # initiates the model so that each game starts fresh
            model.__init__()
            # tells the model that the ai is used,
            # so that there won't be any movement cooldowns
            model.switch_use_ai()
            # runs the game for a limited number of moves
            for _ in range(self.moves_per_game):
                # if the game ended, quit
                if model.terminal:
                    break
                cells = model.board.cells
                best_move = Algorithm.best_move(cells=cells, network=network,
                                                tetromino_name=model.cur_tetromino.name)
                # if there is no held tetromino, check the next tetromino,
                # as the current one can be held
                if model.held_tetromino is None:
                    alt_best_move = Algorithm.best_move(cells=cells, network=network,
                                                        tetromino_name=model.next_tetromino)
                else:
                    alt_best_move = Algorithm.best_move(cells=cells, network=network,
                                                        tetromino_name=model.held_tetromino)

                if alt_best_move > best_move:
                    model.hold()
                    best_move = alt_best_move

                # do the best move
                for _ in range(best_move.rotation):
                    model.rotate_right()

                for _ in range(best_move.right):
                    if model.can_move_right:
                        model.move_right()

                for _ in range(best_move.left):
                    if model.can_move_left:
                        model.move_left()

                model.hard_drop()
                model.update()
            fitness += model.cleared
        return fitness

    def evaluate_networks(self, workers: Pool, networks: [list[Network]],
                          generation: int) -> list[float]:
        """
        :param workers: pool of processors that can be used to concurrently evaluate networks
        :param networks: all networks that should be evaluated
        :param generation: generation epoch
        :return: list of fitnesses of each network
        """
        # a progress bar to show the progress of the current generation
        pbar = tqdm(networks)
        pbar.set_description(f'generation {generation}')
        # runs several evaluations concurrently to save time
        return [
            workers.apply_async(func=self.evaluate_network, args=(network,)).get()
            for network in pbar
        ]

    def train(self) -> None:
        """
        Trains self.pop_size networks to get a really good network.
        Outputs the top fitness and network of each generation to a log file in
        tetris/ai/logs with a date and time stamp.
        """
        # a pool of processors that can be used to concurrently evaluate networks
        workers = Pool(self.num_of_workers)
        log_file_name = datetime.now().strftime("%d-%m-%y_%H:%M")
        log_file_path = f'{Consts.BASE_PATH}/ai/logs/{log_file_name}.txt'
        # creates the file
        open(log_file_path, 'x')
        population = None
        for gen in range(self.generations):
            if population is None:
                population = Population(size=self.pop_size)
            else:
                population = Population(old_pop=population)
            population.fitnesses = self.evaluate_networks(workers=workers,
                                                          networks=population.networks,
                                                          generation=gen)
            # outputs the best network of the current generation and its fitness to the log file
            best_network = population.networks[np.argmax(population.fitnesses)]
            log = (f'--------epoch {gen}--------\n'
                   f'top fitness={max(population.fitnesses)}\n'
                   f'top weights={best_network.weights}\n')
            open(log_file_path, 'a').write(log)


def main() -> None:
    trainer = Trainer(generations=10,
                      pop_size=200,
                      games_per_network=10,
                      moves_per_game=500)
    trainer.train()


if __name__ == '__main__':
    main()
