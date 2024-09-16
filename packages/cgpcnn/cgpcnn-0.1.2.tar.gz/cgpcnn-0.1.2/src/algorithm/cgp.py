import time
import numpy as np
import math
import matplotlib.pyplot as plt
from src.algorithm.individual import Individual
import os


class CGP:
    def __init__(self, net_info, eval_func, lambda_offspring, imgSize, verbose, logger, result_folder_path, IndividualClass=Individual):
        self.lambda_offspring = lambda_offspring
        self.pop = [IndividualClass(net_info) for _ in range(1 + self.lambda_offspring)]
        self.eval_func = eval_func
        self.num_gen = 0
        self.num_eval = 0
        self.max_pool_num = float('inf') if imgSize is None else int(math.log2(imgSize) - 2)
        self.logger = logger
        self.best_accuracy = -float('inf')
        self.verbose = verbose
        self.result_folder_path = result_folder_path
        self.history = []
        self.best_individuals = []

        os.makedirs(self.result_folder_path, exist_ok=True)

    def _evaluation(self, pop, eval_flag):
        net_lists = [pop[i].active_net_list() for i in np.where(eval_flag)[0]]
        fp = self.eval_func(net_lists)
        for i, j in enumerate(np.where(eval_flag)[0]):
            pop[j].eval = fp[i]
        return np.array([ind.eval for ind in pop])

    def evolution(self, max_eval, mutation_rate):
        start_time = time.time()
        eval_flag = np.empty(self.lambda_offspring)
        active_num = self.pop[0].count_active_node()
        _, pool_num = self.pop[0].check_pool()

        while active_num < self.pop[0].net_info.min_active_num or pool_num > self.max_pool_num:
            self.pop[0].mutation(1.0)
            active_num = self.pop[0].count_active_node()
            _, pool_num = self.pop[0].check_pool()

        evaluations = self._evaluation([self.pop[0]], np.array([True]))
        self.history.append(evaluations[evaluations.argmax()])
        self.best_individuals.append(self.pop[0])

        while self.num_gen < max_eval:
            self.num_gen += 1
            for i in range(self.lambda_offspring):
                eval_flag[i] = False
                self.pop[i + 1].copy(self.pop[0])
                active_num = self.pop[i + 1].count_active_node()
                _, pool_num = self.pop[i + 1].check_pool()
                while not eval_flag[i] or active_num < self.pop[i + 1].net_info.min_active_num or pool_num > self.max_pool_num:
                    self.pop[i + 1].copy(self.pop[0])
                    eval_flag[i] = self.pop[i + 1].mutation(mutation_rate)
                    active_num = self.pop[i + 1].count_active_node()
                    _, pool_num = self.pop[i + 1].check_pool()

            evaluations = self._evaluation(self.pop[1:], eval_flag=eval_flag)
            best_arg = evaluations.argmax()
            best_accuracy = evaluations[best_arg]

            if best_accuracy > self.best_accuracy:
                self.best_accuracy = best_accuracy
                self.best_model = self.pop[best_arg + 1]

            if best_accuracy > self.pop[0].eval:
                self.pop[0].copy(self.pop[best_arg + 1])
            else:
                self.pop[0].neutral_mutation(mutation_rate)

            self.history.append(self.best_accuracy)
            self.best_individuals.append(self.best_model)
            self.logger.info(f'Generation {self.num_gen}: Best Model Accuracy = {best_accuracy:.4f} History: {self.history}')

            if self.verbose:
                plt.plot(self.history)
                plt.xlabel('Generations')
                plt.ylabel('Best Fitness')
                plt.savefig(os.path.join(self.result_folder_path, 'generation_fitness_plot.png'))

        total_time = time.time() - start_time
        self.logger.info(f'Total Evolution Time: {total_time:.2f} seconds')

        self.logger.info(f"Final Test Accuracy: {best_accuracy * 100:.2f}%")
        self.logger.info(f"Best Model: {self.history}")

        return self.best_model, self.best_accuracy, self.history
