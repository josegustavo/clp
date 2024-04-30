

import json
import logging
from attr import dataclass, field

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

    def generate(self, count=10, **kwargs):
        """
        Generate and save a specified number of problems to a JSON file.

        Args:
            count (int): The number of problems to generate (default: 10).
            **kwargs: Additional keyword arguments to pass to the `generate_boxes` function.

        Returns:
            None
        """

        problems = [ProblemMaker(**kwargs).random_boxes for _ in range(count)]
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
                                 min_count=t['min_count'],
                                 max_count=t['max_count'],
                                 value_individual=t['value'],
                                 weight=t['value']) for i, t in enumerate(problem_data['box_types'])]
            container = Container(length=problem_data['container'][0],
                                  width=problem_data['container'][1],
                                  height=problem_data['container'][2],
                                  )
            problem = Problem(container, box_types)
            problems.append(problem)
        logging.info("%d problems loaded from '%s'",
                     len(problems), self.file_path)

        return problems
