

import json
import logging
from os import makedirs
import os
from dataclasses import dataclass, field

from lcp.src.container import BoxType, Container
from lcp.src.problems.problem import Problem

from .problem_maker import ProblemMaker


@dataclass
class Problems:
    """
    Class representing a collection of problems.

    Attributes:
        file_path (str): The file path to the JSON file where problems are saved or loaded from (default: "problems.json").
    """

    file_path: str = field(default="problems.json")

    def generate(self, id=0, count=10, **kwargs):
        """
        Generate and save a specified number of problems to a JSON file.

        Args:
            count (int): The number of problems to generate (default: 10).
            **kwargs: Additional keyword arguments to pass to the `generate_boxes` function.

        Returns:
            None
        """

        problems = [ProblemMaker(id=(id*count)+i+1,
                                 number_problems=count,
                                 **kwargs).random_boxes for i in range(count)]
        # Make sure folder exists or create
        makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, 'w') as file:
            json.dump(problems, file, indent=4)
        logging.info(f"Problems saved to '{self.file_path}'")

    def load_problems(self) -> list[Problem]:
        # Open and read the JSON file
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        problems = []
        # Iterate over each problem in the loaded data
        for problem_data in data:
            # Convert each box type in the problem into a BoxType instance
            box_types = [BoxType(length=t['size'][0],
                                 width=t['size'][1],
                                 height=t['size'][2],
                                 type=i,
                                 min_count=0,  # t['min_count'],
                                 max_count=t['max_count'],
                                 value_individual=t['value'],
                                 weight=t['value']) for i, t in enumerate(problem_data['box_types'])]
            container = Container(length=problem_data['container'][0],
                                  width=problem_data['container'][1],
                                  height=problem_data['container'][2],
                                  )
            problem = Problem(problem_data['id'], container, box_types)
            problems.append(problem)
        logging.info("%d problems loaded from '%s'",
                     len(problems), self.file_path)

        return problems

    def load_literature_problems(self) -> list[Problem]:
        problems = []
        file_url = "https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/%s" % self.file_path
        import requests
        response = requests.get(file_url)
        lines = response.iter_lines(decode_unicode=True)
        count_problems = int(next(lines))
        problems = []
        for i in range(count_problems):
            problem_number, seed_number = map(int, next(lines).split())
            container_length, container_width, container_height = map(
                int, next(lines).split())
            box_types_count = int(next(lines))
            box_types: list[BoxType] = []
            for _ in range(box_types_count):
                box_type, box_length, box_length_indicator, box_width, box_width_indicator, box_height, box_height_indicator, box_count = map(
                    int, next(lines).split())
                box_types.append(BoxType(box_length,
                                         box_width,
                                         box_height,
                                         box_type,
                                         0,
                                         box_count,
                                         box_length*box_width*box_height,
                                         box_length*box_width*box_height))
            container = Container(length=container_length,
                                  width=container_width,
                                  height=container_height)
            problem = Problem(str(problem_number), container, box_types)
            problems.append(problem)
        return problems
