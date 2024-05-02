from copy import copy
from dataclasses import dataclass, field
from enum import Enum
import logging
import random
from types import NoneType

from lcp.src.location import Position
from lcp.src.container import Box, Container, FreeSpace
from .gene import Gene
from .dblf import DBLF

Improvement = Enum('Improvement', ['none', 'during', 'late'])


@dataclass
class Chromosome(list):
    genes: list[Gene]
    container: Container
    fitness: tuple[float, int, int] = field(init=False)
    result: list[Box] = field(init=False)
    improved: bool = field(default=False, init=False)
    dblf: DBLF = field(init=False)
    evaluated: bool = field(default=False, init=False)

    @property
    def get_fitness(self):
        if not self.evaluated:
            raise ValueError("Fitness no calculado")
        return self.fitness[2]

    def __post_init__(self):
        super().__init__(self.genes)
        self.fitness = (0, 0, 0)
        self.result = []
        self.dblf = DBLF(
            side=[FreeSpace(Position(0, 0, 0), self.container, 'side')])

    def __str__(self) -> str:
        return f"""Chromosome with {len(self.genes)} genes
{"\n".join([str(g) for g in self.genes])}
Fitness: {self.fitness}"""

    def evaluate(self, improvement: Improvement = Improvement.none, is_improving_late=False) -> 'Chromosome':
        if self.evaluated:
            return self

        max_volume = self.container.volume

        occupied_vol = self.container.volume * \
            self.fitness[0] if is_improving_late else 0
        number_boxes = self.fitness[1] if is_improving_late else 0
        value = self.fitness[2] if is_improving_late else 0
        result: list[Box] = self.result

        while len(self.dblf):
            for g_i, gene in enumerate(self.genes):
                min_pos = Position(99999, 99999, 99999)
                max_pos = Position(-99999, -99999, -99999)
                one_type = gene.type
                box_number = gene.box_count if is_improving_late else 0
                # logging.debug("Comenzó el tipo %d %s" % (one_type.type, gene.size))
                while box_number < gene.box_count:
                    box_number += 1
                    available = self.dblf.first_available(gene.size,
                                                          one_type.type if is_improving_late else None)
                    if available:
                        min_pos = Position(min(min_pos.x, available.position.x),
                                           min(min_pos.y, available.position.y),
                                           min(min_pos.z, available.position.z))

                        max_pos = Position(max(max_pos.x, available.position.x + gene.size.length),
                                           max(max_pos.y, available.position.y +
                                               gene.size.width),
                                           max(max_pos.z, available.position.z + gene.size.height))

                        new_box = Box(available.position,
                                      gene.size, one_type.type)
                        # logging.debug("\nnew box (%d): %s" % (box_number, new_box))
                        occupied_vol += gene.size.volume
                        number_boxes += 1
                        value += one_type.value_individual
                        if value > max_volume:
                            raise ValueError(
                                "Se excedió el volumen del contenedor %s" % self)

                        result.append(new_box)

                        # Eliminar el espacio usado
                        self.dblf.remove(available)
                        # Añadir los nuevos espacios generados
                        side, top, front = available.split(
                            gene.size, one_type.type)
                        self.dblf += DBLF(side=side, top=top, front=front)
                        self.dblf.compact()
                    else:
                        # logging.debug("No hay espacio disponible para la caja %d %s" %
                        #              (box_number, gene.size))
                        box_number -= 1
                        break

                    # Mejorar
                    # Si se ha llegado al límite de cajas, intentar aumentar el límite de cajas si queda espacio al lado o encima
                    if improvement.name == 'during' and box_number == gene.box_count and one_type.max_count > box_number:
                        self.improved = True
                        available = DBLF(side=self.dblf.side, top=self.dblf.top).first_available(gene.size,
                                                                                                 one_type.type if is_improving_late else None)  # No buscar en el frente
                        if available:  # Si hay espacio disponible seguir añadiendo cajas
                            # logging.debug(
                            #    "Se llegó al número de cajas definido %d, se añadirá una caja más" % box_number)
                            gene.box_count += 1

                gene.box_count = box_number  # Actualizar el número de cajas realmente añadidas

                # logging.debug("Terminó el tipo %d con %d cajas" %
                #              (one_type.type, box_number))
                # Usar solo espacios frontales
                # if dblf.front:
                #    dblf = DBLF(side=[dblf.front[0]], top=[], front=[])
                if box_number > 0:
                    # Eliminar espacios al fondo que quedaron no accesibles
                    max_depth = self.genes[g_i+1].size.length if g_i + \
                        1 < len(self.genes) else 0
                    self.dblf.remove_unreachable(min_pos, max_pos, max_depth)

            if improvement.name == 'late' and not is_improving_late and len(self.dblf.unused) > 0:
                self.improved = True
                is_improving_late = True
                # print(dblf.unused)
                top_group = list(
                    filter(lambda x: x.group == 'top', self.dblf.unused))
                side_group = list(
                    filter(lambda x: x.group == 'side', self.dblf.unused))
                front_group = list(
                    filter(lambda x: x.group == 'front', self.dblf.unused))
                self.dblf = DBLF(side=side_group,
                                 top=top_group,
                                 front=front_group)
            else:
                break
        # Activar para visualizar los espacios disponibles
        # for d in dblf.side:
        #     result.append(Box(d.position, d.size, 20))
        # for d in dblf.top:
        #     result.append(Box(d.position, d.size, 21))
        # for d in dblf.front:
        #     result.append(Box(d.position, d.size, 22))

        self.fitness = (round((occupied_vol / self.container.volume), 2),
                        number_boxes,
                        value)
        self.result = result
        self.evaluated = True

        return self

    def get_dblf_unused(self) -> DBLF:
        top_group = list(
            filter(lambda x: x.group == 'top', self.dblf.unused))
        side_group = list(
            filter(lambda x: x.group == 'side', self.dblf.unused))
        front_group = list(
            filter(lambda x: x.group == 'front', self.dblf.unused))
        dblf = DBLF(side=side_group,
                    top=top_group,
                    front=front_group)
        return dblf

    def evaluate_with_improvement_late(self) -> 'Chromosome':
        if not self.evaluated:
            raise ValueError("No se puede mejorar un cromosoma no evaluado")

        if len(self.dblf.unused) > 0:
            self.dblf = self.get_dblf_unused()
            self.evaluated = False
            self.evaluate(is_improving_late=True)
            self.improved = True

        return self

    def __matmul__(self, other: 'Chromosome') -> tuple['Chromosome', 'Chromosome']:
        return self.crossover(other)

    def crossover_one_point(self, other: 'Chromosome', point) -> 'Chromosome':
        genes = [copy(g) for g in self.genes[:point]]
        current_types = [g.type.type for g in genes]
        for o in other.genes:
            if o.type.type not in current_types:
                genes.append(copy(o))
        if (len(genes) != len(self.genes)):
            raise ValueError("Error en el conteo de genes en el crossover")
        return Chromosome(genes, self.container)

    def crossover(self, other: 'Chromosome') -> tuple['Chromosome', 'Chromosome']:
        crossover_point = random.randint(1, len(self.genes) - 1)
        child_1 = self.crossover_one_point(other, crossover_point)
        child_2 = other.crossover_one_point(self, crossover_point)
        # child_1.evaluate()
        # child_2.evaluate()
        return child_1, child_2

    def mutate(self, P_MUT_GEN=0.05) -> tuple[list[int], 'Chromosome']:
        mutated = [0, 0, 0]
        new_genes = [copy(g) for g in self.genes]
        type_mutation = random.choice(['interchange', 'count', 'rotation'])
        if type_mutation == 'interchange':
            # Intercambiar dos genes
            i, j = random.sample(range(len(new_genes)), k=2)
            new_genes[i], new_genes[j] = new_genes[j], new_genes[i]
            mutated[0] += 1
        elif type_mutation == 'count':
            gene = random.choice(new_genes)
            gene.mutate_quantity(0.1)
            mutated[1] += 1
        elif type_mutation == 'rotation':
            gene = random.choice(new_genes)
            gene.mutate_rotation()
            mutated[2] += 1

        # if random.random() < P_MUT_GEN:  # Intercambiar el tipo de caja con otro
        #     i, j = random.sample(range(len(new_genes)), k=2)
        #     # Intercambiar dos genes
        #     new_genes[i], new_genes[j] = new_genes[j], new_genes[i]
        #     mutated[0] += 1

        # # Recorrer los genes y mutar la cantidad y la rotación
        # for gene in new_genes:
        #     if random.random() < P_MUT_GEN:  # Incrementar o decrementar el número de cajas en un porcentaje
        #         # Incrementar o decrementar hasta un 10%
        #         gene.mutate_quantity(0.1)
        #         mutated[1] += 1
        #     if random.random() < P_MUT_GEN:  # Mutación not de la rotación
        #         gene.mutate_rotation()
        #         mutated[2] += 1

        # Verificar si todos los tipos están presentes
        if len(set([g.type.type for g in new_genes])) != len(new_genes):
            # print("%s %s" % (gene, other))
            raise ValueError("Error en la mutación de cromosoma")

        # Si se mutó, reiniciar el fitness para recalcularlo
        if sum(mutated) > 0:
            return mutated, Chromosome(new_genes, self.container)
        else:
            return mutated, self
