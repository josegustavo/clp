from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Iterator, Optional


from lcp.src.problems import Problem
from .chromosome import Chromosome, Gene, Improvement

GroupImprovement = Enum(
    'GroupImprovement', ['none', 'during', 'late_all', 'late_some', 'late_best'])


@dataclass
class Population:
    problem: Problem
    individuals: list[Chromosome] = field(default_factory=list[Chromosome],
                                          init=False)
    group_improvement: GroupImprovement = field(default=GroupImprovement.none)
    evaluated: bool = field(default=False, init=False)

    def __iter__(self) -> Iterator[Chromosome]:
        return iter(self.individuals)

    def __getitem__(self, index: int) -> Chromosome:
        return self.individuals[index]

    def __len__(self) -> int:
        return len(self.individuals)

    def __str__(self) -> str:
        return f"Population with {len(self)} individuals best: {self.best.get_fitness}"

    def replace_worst(self, chromosome: Chromosome) -> 'Population':
        self.individuals.insert(0, chromosome)
        del self.individuals[-1]
        return self

    @property
    def default_max(self) -> Optional[Chromosome]:
        filtered = list(filter(lambda t: t.isMaxInitial, self.individuals))
        return filtered[0] if filtered else None

    @property
    def best(self) -> Chromosome:
        if not self.evaluated:
            self.evaluate()

        return self.individuals[0]

    @property
    def best_fitness(self) -> float:
        return self.best.get_fitness

    def generate_random_individuals(self, count: int = 100) -> list[Chromosome]:
        individuals: list[Chromosome] = []
        # Generar dos soluciones iniciales usando los valores mínimos y máximos propuestos

        genes = [Gene(t, t.max_count, 0) for t in self.problem.box_types]
        random.shuffle(genes)
        individuals.append(Chromosome(
            genes, self.problem.container, True))

        genes = [Gene(t, t.min_count, 0) for t in self.problem.box_types]
        random.shuffle(genes)
        individuals.append(Chromosome(genes, self.problem.container))

        for _ in range(count-2):  # Generar 2 menos
            genes = [Gene(t, random.randint(t.min_count, t.max_count),
                          random.randint(0, 1)) for t in self.problem.box_types]
            random.shuffle(genes)
            individuals.append(Chromosome(genes, self.problem.container))

        return individuals

    def append(self, chromosome: Chromosome) -> 'Population':
        self.individuals.append(chromosome)
        return self

    def evaluate(self) -> 'Population':
        # for individual in self.individuals:
        #    if individual.get_fitness == 0:
        #        individual.evaluate(
        #            )
        #    if individual.get_fitness > best_fit:
        #        best_fit = individual.get_fitness
        if self.group_improvement == GroupImprovement.none:
            self.individuals.sort(key=lambda i: i.evaluate().
                                  get_fitness,
                                  reverse=True)
        elif self.group_improvement == GroupImprovement.during:
            self.individuals.sort(key=lambda i: i.evaluate(Improvement.during).
                                  get_fitness,
                                  reverse=True)
        elif self.group_improvement == GroupImprovement.late_all:
            self.individuals.sort(key=lambda i: i.evaluate().
                                  evaluate_with_improvement_late(),
                                  reverse=True)
        else:
            self.individuals.sort(
                key=lambda i: i.evaluate().get_fitness, reverse=True)
            if self.group_improvement == GroupImprovement.late_some:
                for i in self.individuals[:5]:
                    i.evaluate_with_improvement_late()
            elif self.group_improvement == GroupImprovement.late_best:
                self.individuals[0].evaluate_with_improvement_late()
            self.individuals.sort(
                key=lambda i: i.get_fitness, reverse=True)
        # print(f"Best fitness: {best_fit}")
        self.evaluated = True
        return self

    def tournament(self, TOURNAMENT_SIZE=2) -> Chromosome:
        t = random.sample(self.individuals,
                          k=TOURNAMENT_SIZE)
        max_item = max(t, key=lambda i: i.get_fitness)
        return max_item

    def mutation(self, P_MUT: float = 0.05) -> 'Population':
        mutate_total = [0, 0, 0]

        for i in range(len(self.individuals)):
            if random.random() < P_MUT:
                mutate_result, c = self.individuals[i].mutate()
                self.individuals[i] = c
                mutate_total = [a + b for a,
                                b in zip(mutate_total, mutate_result)]

        if sum(mutate_total) > 0:
            # print(
            #    f'Se mutaron {mutate_total[0]} tipos, {mutate_total[1]} cantidades y {mutate_total[2]} rotaciones')
            self.evaluate()
        return self
