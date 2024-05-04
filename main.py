# -*- coding: utf-8 -*-
import random
import json
from lcp.src.problems.problems import Problems
from lcp.src.algorithm import Population, GeneticAlgorithm
from lcp.src.algorithm.population import GroupImprovement
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import multiprocessing

random.seed(42)

types_count = [5, 10, 15, 20]

for i in types_count:
    Problems(file_path='problems/types_%d.json' % i)\
        .generate(25, N_TYPES=i, BOX_SIDE_MIN=250, BOX_SIDE_MAX=750)

improvements = [GroupImprovement.none,
                GroupImprovement.during,
                GroupImprovement.late_all,
                GroupImprovement.late_best,
                GroupImprovement.late_some]


def solve(args):
    problem, imp, num_types = args
    random.seed(100)
    population = Population(problem, imp)\
        .generate_random_individuals(100).evaluate()
    ga = GeneticAlgorithm(population=population,
                          MAX_DURATION=300,
                          P_MUT_GEN=1/num_types,
                          )
    ga.start()
    return ga.stats


def main():
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()-1) as executor:
        args = []
        for i in types_count:
            problems = Problems(file_path='problems/types_%d.json' %
                                i).load_problems()
            for problem in problems:
                num_types = len(problem.box_types)
                args += [(problem, imp, num_types) for imp in improvements]
        # print("Cantidad de problemas a resolver: %s" % len(args))
        results = executor.map(solve, args)

        with tqdm(total=len(args)) as pbar:
            for result in results:
                with open('results.txt', 'a') as outfile:
                    json.dump(result, outfile)
                    outfile.write('\n')
                pbar.update()


if __name__ == "__main__":
    main()
