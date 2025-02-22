# -*- coding: utf-8 -*-
import random
import json
from Code.src.problems.problems import Problems
from Code.src.algorithm import Population, GeneticAlgorithm
from Code.src.algorithm.population import GroupImprovement
from concurrent.futures import ProcessPoolExecutor

types_count = [5, 10, 20, 30, 40, 50]

for i, n in enumerate(types_count):
    random.seed(100)
    Problems(file_path='problems/types_%d.json' % n)\
        .generate(id=i, count=25, N_TYPES=n, BOX_SIDE_MIN=250, BOX_SIDE_MAX=750)

improvements = [GroupImprovement.none,
                GroupImprovement.during,
                GroupImprovement.late_all,
                GroupImprovement.late_some,
                GroupImprovement.late_best,
                ]

MAX_DURATION = 600

random.seed(42)


def solve(args):
    problem, imp, num_types = args
    random.seed(problem.id)  # usar la misma semilla para cada problema

    population = Population(problem)
    individuals = population.generate_random_individuals(100)
    population.individuals = individuals
    population.evaluate()
    first_best_fitness = population.best.fitness

    if imp != GroupImprovement.none:
        population = Population(problem, imp)
        population.individuals = individuals
        population.evaluate()

    ga = GeneticAlgorithm(population=population,
                          MAX_DURATION=MAX_DURATION,
                          P_MUT_GEN=1/num_types,
                          )
    ga.start(first_best_fitness)
    return ga.stats


def main():
    with ProcessPoolExecutor(max_workers=8) as executor:
        args = []
        for i in types_count:
            # if i in [40, 50]:
            problems = Problems(file_path='problems/types_%d.json' %
                                i).load_problems()
            for problem in problems:
                num_types = len(problem.box_types)
                args += [(problem, imp, num_types) for imp in improvements]
        # print("Cantidad de problemas a resolver: %s" % len(args))
        results = executor.map(solve, args)

        for result in results:
            with open('results.txt', 'a') as outfile:
                json.dump(result, outfile)
                outfile.write('\n')
            print("\rProblema resuelto: %s" % result['problem_id'])


if __name__ == "__main__":
    main()
