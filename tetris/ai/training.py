from multiprocessing import Pool, cpu_count
from datetime import datetime

import numpy as np
from tqdm import tqdm

from tetris.ai.algorithm import Algorithm
from tetris.ai.network import Network
from tetris.ai.population import Population
from tetris.model.model import Model
from tetris.consts import Consts


class Training:
    workers = cpu_count()
    generations = 10
    pop_size = 200
    eval_epochs = 10
    test_moves = 500

    @staticmethod
    def evaluate_network(network: Network) -> float:
        model = Model()
        fitness = 0
        for _ in range(Training.eval_epochs):
            model.__init__()
            model.switch_use_ai()
            for _ in range(Training.test_moves):
                if model.terminal:
                    break
                cells = model.board.cells
                best_move = Algorithm.best_move(cells=cells, network=network,
                                                tetromino_name=model.cur_tetromino.name)
                if model.held_tetromino is None:
                    alt_best_move = Algorithm.best_move(cells=cells, network=network,
                                                        tetromino_name=model.next_tetromino)
                else:
                    alt_best_move = Algorithm.best_move(cells=cells, network=network,
                                                        tetromino_name=model.held_tetromino)

                if alt_best_move > best_move:
                    model.hold()
                    best_move = alt_best_move

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

    @staticmethod
    def evaluate_networks(workers: Pool, networks: [list[Network]], epoch: int) -> list[float]:
        pbar = tqdm(networks)
        pbar.set_description(f'epoch {epoch}')
        return [
            workers.apply_async(func=Training.evaluate_network, args=(network,)).get()
            for network in pbar
        ]

    @staticmethod
    def train() -> None:
        print(f'Training {Training.pop_size} networks along {Training.generations} generations, '
              f'using {Training.workers} cores')
        workers = Pool(Training.workers)
        log_file_name = datetime.now().strftime("%d-%m-%y_%H:%M")
        log_file_path = f'{Consts.BASE_PATH}/ai/logs/{log_file_name}.txt'
        open(log_file_path, 'x')
        population = None
        for i in range(Training.generations):
            if population is None:
                population = Population(size=Training.pop_size)
            else:
                population = Population(old_pop=population)
            population.fitnesses = Training.evaluate_networks(workers=workers,
                                                              networks=population.networks,
                                                              epoch=i)
            best_network = population.networks[np.argmax(population.fitnesses)]
            log = (f'--------epoch {i}--------\n'
                   f'top fitness={max(population.fitnesses)}\n'
                   f'top weights={best_network.weights}\n')
            open(log_file_path, 'a').write(log)


def main() -> None:
    Training.train()


if __name__ == '__main__':
    main()
