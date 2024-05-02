from copy import deepcopy
from enum import Enum
from hmac import new
import random
import sys
import time
from tracemalloc import stop
from typing import Callable, Optional
from dataclasses import dataclass, field
from lcp.src.algorithm.chromosome import Chromosome
from .population import Population

inf = sys.maxsize


@dataclass
class GeneticAlgorithm:
    population: Population

    TOURNAMENT_SIZE: int = field(default=2)

    P_CROSSOVER: float = field(default=0.8)
    P_MUT: float = field(default=0.05)
    P_MUT_GEN: float = field(default=0.05)

    MAX_GENERATIONS: int = field(default=inf)
    STOP_UNIMPROVED: int = field(default=inf)
    MAX_DURATION: int = field(default=inf)

    stats: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        if self.MAX_GENERATIONS == inf and self.STOP_UNIMPROVED == inf and self.MAX_DURATION == inf:
            raise ValueError(
                "At least one of MAX_GENERATIONS, STOP_UNIMPROVED or MAX_TIME must be set")

    def select_with_crossover(self, elite) -> 'GeneticAlgorithm':
        new_population = Population(
            self.population.problem, self.population.group_improvement)

        while len(new_population) < len(self.population):
            # Selección aleatoria de 2 individuos eligiendo el mejor
            parent_1 = self.population.tournament(self.TOURNAMENT_SIZE)
            # Selección aleatoria de 2 individuos eligiendo el mejor
            parent_2 = self.population.tournament(self.TOURNAMENT_SIZE)
            if (parent_1 is parent_2):  # Si ambos padres son iguales, ignorar
                continue
            # ¿Se deben cruzar los padres?
            if random.random() < self.P_CROSSOVER:
                # Cruzar los padres
                child_1, child_2 = parent_1 @ parent_2
                new_population.append(child_1)
                new_population.append(child_2)
            else:
                # Si no se cruzan, se añaden los padres
                new_population.append(deepcopy(parent_1))
                new_population.append(deepcopy(parent_2))

        new_best = new_population.best
        # Si el mejor individuo de la elite sigue siendo el mejor, se reemplaza por el peor de los seleccionados
        # print(elite['fitness'][2], best_of_selected['fitness'][2])
        if elite.get_fitness > new_best.get_fitness:
            min_item = min(new_population, key=lambda i: i.get_fitness)
            min_item_index = new_population.individuals.index(min_item)
            new_population.individuals[min_item_index] = deepcopy(elite)

        new_population.evaluate()
        self.population = new_population
        return self

    def start(self, onGeneration: Optional[Callable] = None) -> 'GeneticAlgorithm':
        elite = deepcopy(self.population.best)
        elite_fitness = elite.get_fitness
        # print(elite)
        generations_not_improved = 0
        generation = 0
        best_values = [elite.get_fitness]
        time_start = int(time.time())
        time_end = time_start
        # Iterar hasta que no se mejore en M generaciones o se alcance la generación N
        while (time_end-time_start) < self.MAX_DURATION and generations_not_improved < self.STOP_UNIMPROVED and generation < self.MAX_GENERATIONS:
            # print("-> Generation %d best value: %d" % (
            #      generation, elite.get_fitness))
            self.select_with_crossover(elite)

            # P_MUT = self.P_MUT + (generations_not_improved/1000)
            # P_MUT_GEN = self.P_MUT_GEN + (generations_not_improved/2000)
            self.population.mutation(self.P_MUT, self.P_MUT_GEN)

            new_best = self.population.best
            if new_best.get_fitness > elite_fitness:
                # print("New elite: ", new_best.get_fitness,
                #      "Old elite: ", elite_fitness)
                elite = deepcopy(new_best)
                elite_fitness = elite.get_fitness
                generations_not_improved = 0
            # Si en la mutación se perdió el individuo de la elite, reemplazar el peor de la población
            elif new_best.get_fitness < elite_fitness:
                # print("El nuevo mejor individuo %d es peor que el elite %d" % (
                #    new_best.get_fitness, elite_fitness))
                min_item = min(self.population.individuals,
                               key=lambda i: i.get_fitness)
                min_item_index = self.population.individuals.index(min_item)
                self.population.individuals[min_item_index] = deepcopy(elite)
                # print("Se ha perdido el elite, reemplazado al peor de la población")
                generations_not_improved += 1
            else:
                generations_not_improved += 1
            # print(self.population.best)
            best_values.append(self.population.best.get_fitness)
            generation += 1
            if callable(onGeneration):
                onGeneration(best_values, self.population)
            time_end = int(time.time())
        self.stats = {
            'best_value': self.population.best.fitness,
            'time_start': time_start,
            'types_count': len(self.population.problem.box_types),
            'generations': generation,
            'best_values': best_values,
            'start_time': time_start,
            'end_time': time_end,
            'duration': time_end-time_start,
        }
        return self
