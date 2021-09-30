from numpy import argmax

from multiprocessing import Pool

from tetris.ai.algorithm import Algorithm
from tetris.ai.network import Network
from tetris.ai.population import Population
from tetris.model.model import Model


class Training:
    workers = 6
    generations = 20
    pop_size = 200
    eval_epochs = 3
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
        return fitness / Training.eval_epochs

    @staticmethod
    def evaluate_networks(workers: Pool, networks: [list[Network]]) -> list[float]:
        return [
            workers.apply_async(func=Training.evaluate_network, args=(network,)).get()
            for network in networks
        ]

    @staticmethod
    def train() -> None:
        workers = Pool(Training.workers)
        population = Population(size=Training.pop_size)
        population.fitnesses = Training.evaluate_networks(workers=workers,
                                                          networks=population.networks)
        print(f'epoch: {0}, fitnesses={sorted(population.fitnesses)[-10:]}')
        for i in range(1, Training.generations):
            population = Population(old_pop=population)
            population.fitnesses = Training.evaluate_networks(workers=workers,
                                                              networks=population.networks)
            print(f'epoch: {i}, fitnesses={sorted(population.fitnesses)[-10:]}')
        best_network = population.networks[argmax(population.fitnesses)]
        print(best_network.weights)
        print(best_network)


def main() -> None:
    Training.train()


if __name__ == '__main__':
    main()
