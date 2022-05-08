import multiprocessing as mp
import signal

from multiprocessing.managers import BaseManager
from solver import RESolver

class BestRESolutionContainer(object):
    def __init__(self):
        self._resolution = None
        self._stopped = False

    def replace_if_better(self, resolution):
        if resolution.is_better_than(self._resolution):
            if resolution.ok:
                print(f'Found better solution {resolution}')
            self._resolution = resolution

    def stop(self):
        self._stopped = True

    def stopped(self):
        return self._stopped

    def get_best_resolution(self):
        return self._resolution


class RESolutionManager(BaseManager):
    pass


RESolutionManager.register('BestRESolutionContainer', BestRESolutionContainer)


def start_solving(solution_container):
    try:
        while not solution_container.stopped():
            solution_container.replace_if_better(RESolver().attempt_to_solve())
    except KeyboardInterrupt:
        solution_container.stop()

if __name__ == '__main__':

    custom_manager = RESolutionManager()
    custom_manager.start()
    solution_container = custom_manager.BestRESolutionContainer()

    """
    # Does not work
    def signal_manager(int, frame):
        solution_container.stop()

    def init_pool_processes():
        signal.signal(signal.SIGINT, signal_manager)
    """

    print('Starting to look for solution, interrupt with CTRL^C')

    try:
        pool = mp.Pool(processes=mp.cpu_count())
        pool.apply(func=start_solving, args=[solution_container])
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        solution_container.stop()
        print(f'\nBest solution found: {solution_container.get_best_resolution()}')
    