from copy import deepcopy
import random
import sys
import time
from typing import Callable, Optional
from dataclasses import dataclass, field
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

    def select_with_crossover(self) -> 'GeneticAlgorithm':
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

        self.population = new_population
        return self

    def start(self, default_max_fitness: tuple[int, int, float, int], onGeneration: Optional[Callable] = None) -> 'GeneticAlgorithm':
        elite = deepcopy(self.population.best)
        generations_not_improved = 0
        generation = 0
        best_values = [elite.get_fitness]
        best_boxes = [len(elite.result)]
        time_start = time.time()
        generations_duration = []
        generations_time = []
        time_generation = time_start
        time_end = time_start
        best_time = 0
        best_generation = 0
        # Iterar hasta que no se mejore en M generaciones o se alcance la generación N
        while (time_end - time_start) < self.MAX_DURATION and generations_not_improved < self.STOP_UNIMPROVED and generation < self.MAX_GENERATIONS:
            # print("-> Generation %d best value: %d" % (
            #      generation, elite.get_fitness))
            self.select_with_crossover()

            self.population.mutation(self.P_MUT)

            new_best = self.population.best
            if new_best > elite:  # Si el nuevo mejor es mejor que el elite, reemplazar
                elite = deepcopy(new_best)
                generations_not_improved = 0
                best_time = time.time() - time_start
                best_generation = generation
            else:
                if new_best < elite:
                    del self.population.individuals[-1]
                    new_best = deepcopy(elite)
                    self.population.replace_worst(new_best)
                generations_not_improved += 1

            best_values.append(new_best.get_fitness)
            best_boxes.append(len(new_best.result))
            # if callable(onGeneration):
            #    onGeneration(best_values, self.population)
            generation += 1
            time_end = time.time()
            generations_duration.append(time_end-time_generation)
            generations_time.append(time_end-time_start)
            time_generation = time_end
        self.stats = {
            'best_value': self.population.best.fitness,
            'problem_id': self.population.problem.id,
            'types_count': len(self.population.problem.box_types),
            'group_improvement': self.population.group_improvement.name,
            'generations': generation,
            'best': {
                'best_time': best_time,
                'best_generation': best_generation,
                'best_boxes': best_boxes,
            },
            'best_values': best_values,
            'timings': {
                'start_time': time_start,
                'end_time': time_end,
                'duration': time_end-time_start,
                'generations_duration': generations_time,
                'generations_time': generations_time,
            },
            'default_max_fitness': default_max_fitness,
            'best_solution': [(g.type.type, g.box_count, g.rotation) for g in self.population.best.genes],
        }
        return self
