from copy import deepcopy
from dataclasses import dataclass, field
import logging
import random
from tkinter import N
from typing import Iterator, Optional

from lcp.src.problems import Problem
from .chromosome import Chromosome, Gene


@dataclass
class Population:
    problem: Problem
    individuals: list[Chromosome] = field(default_factory=list[Chromosome],
                                          init=False)

    def __iter__(self) -> Iterator[Chromosome]:
        return iter(self.individuals)

    def __getitem__(self, index: int) -> Chromosome:
        return self.individuals[index]

    def __len__(self) -> int:
        return len(self.individuals)

    def __str__(self) -> str:
        return f"Population with {len(self)} individuals best: {self.best.get_fitness}"

    @property
    def best(self) -> Chromosome:
        return max(self.individuals, key=lambda i: i.get_fitness)

    @property
    def best_fitness(self) -> float:
        return self.best.get_fitness

    def generate_random_individuals(self, count: int = 100, seed=42) -> 'Population':
        self.individuals.clear()
        # random.seed(seed)
        for _ in range(count):
            genes = [Gene(t, random.randint(t.min_count, t.max_count),
                          random.randint(0, 1)) for t in self.problem.box_types]
            random.shuffle(genes)
            self.individuals.append(Chromosome(genes, self.problem.container))

        return self

    def append(self, chromosome: Chromosome) -> 'Population':
        self.individuals.append(chromosome)
        return self

    def evaluate(self) -> 'Population':
        best_fit = 0
        for individual in self.individuals:
            if individual.get_fitness == 0:
                individual.evaluate()
            if individual.get_fitness > best_fit:
                best_fit = individual.get_fitness
        # print(f"Best fitness: {best_fit}")
        return self

    def tournament(self, TOURNAMENT_SIZE=2) -> Chromosome:
        t = random.sample(self.individuals,
                          k=TOURNAMENT_SIZE)
        max_item = max(t, key=lambda i: i.get_fitness)
        return max_item

    def mutation(self, P_MUT: float = 0.1, P_MUT_GEN=0.05) -> 'Population':
        mutate_total = [0, 0, 0]
        # print(P_MUT, P_MUT_GEN)
        for i in range(len(self.individuals)):
            if random.random() < P_MUT:
                mutate_result, c = self.individuals[i].mutate(P_MUT_GEN)
                self.individuals[i] = c
                mutate_total = [a + b for a,
                                b in zip(mutate_total, mutate_result)]

        if sum(mutate_total) > 0:
            # print(
            #    f'Se mutaron {mutate_total[0]} tipos, {mutate_total[1]} cantidades y {mutate_total[2]} rotaciones')
            self.evaluate()
        return self
