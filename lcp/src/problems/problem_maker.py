from math import prod
import random
import string
from dataclasses import dataclass, field

alphabet = string.ascii_lowercase + string.digits


@dataclass
class ProblemMaker:
    N_TYPES: int = 20
    CONTAINER_DIM: tuple = (12010, 2330, 2380)  # Contenedor de 40 pies
    BOX_SIDE_MIN: int = 300
    BOX_SIDE_MAX: int = 600
    id: int = field(default=0)
    number_problems: int = field(default=10)

    # def __post_init__(self):
    # self.id = ''.join(random.choices(alphabet, k=8))

    result: dict = field(init=False, repr=False)

    @property
    def random_boxes(self):
        container_volume = prod(self.CONTAINER_DIM)
        result = {
            'id': self.id,
            'container': self.CONTAINER_DIM,
            'container_volume': container_volume,
        }
        box_types = []
        min_volume, max_volume = 0, 0

        # box_sizes = [[random.randint(
        #    self.BOX_SIDE_MIN, self.BOX_SIDE_MAX) for _ in range(3)]
        #    + [random.randint(1, 100)]
        #    for _ in range(self.N_TYPES)]
        seed = (int(self.id) - 1) % self.number_problems
        random.seed(seed)
        box_sizes = []
        box_sizes_set = set()
        while len(box_sizes) < self.N_TYPES:
            box_dimensions = tuple(random.randint(self.BOX_SIDE_MIN, self.BOX_SIDE_MAX)
                                   for _ in range(3))
            if box_dimensions in box_sizes_set:
                continue
            box_sizes_set.add(box_dimensions)
            box_size = list(box_dimensions) + [random.randint(10, 100)]
            box_sizes.append(box_size)

        for i in range(self.N_TYPES):
            l, w, h, value = box_sizes[i]
            vol = l*w*h
            mean_count = int((container_volume/self.N_TYPES) // vol)
            max_count = mean_count  # + random.randint(0, mean_count//2)
            # min_count = max(0, mean_count - random.randint(0, mean_count//2))
            value = 10000 * prod([l, w, h])/container_volume
            # print(value, prod([l, w, h]), container_volume)
            box_type = {
                'type': i,
                'size': (l, w, h),
                'value': value,
                'volume': vol,
                'min_count': 0,  # min_count,
                'max_count': max_count,
            }
            # min_volume += box_type['min_count']*box_type['volume']
            max_volume += box_type['max_count']*box_type['volume']

            box_types.append(box_type)

        result['box_types'] = box_types
        result['types_count'] = len(box_types)
        self.result = result
        return result

    @ property
    def exact_boxes(self):
        """
        Generate a dictionary containing information about the generated boxes.

        Args:
            N_TYPES (int): Number of box types to generate (default: 10).
            CONTAINER_DIM (tuple): Dimensions of the container (default: (12000, 2300, 2300)).
            BOX_SIDE_MIN (int): Minimum side length of a box (default: 300).
            BOX_SIDE_MAX (int): Maximum side length of a box (default: 600).

        Returns:
            dict: A dictionary containing the following keys:
                - 'container': Dimensions of the container.
                - 'container_volume': Volume of the container.
                - 'box_types': List of dictionaries representing each box type.
                - 'types_count': Number of box types.
                - 'solution': Dictionary containing solution information.
        """
        result = {
            'container': self.CONTAINER_DIM,
            'container_volume': self.CONTAINER_DIM[0]*self.CONTAINER_DIM[1]*self.CONTAINER_DIM[2],
        }
        # Generar N cortes aleatoreos en el lado más largo del contenedor
        cuts = [self.BOX_SIDE_MIN*l for l in sorted(random.sample(
            range(1, int(self.CONTAINER_DIM[0]/self.BOX_SIDE_MIN)), self.N_TYPES-1))] + [self.CONTAINER_DIM[0]]
        # print(cuts)
        last_x = 0
        volume_total = 0
        box_types = []
        for i, c in enumerate(cuts):
            l_count, l = 0, 0
            while l > self.BOX_SIDE_MAX or l < self.BOX_SIDE_MIN:
                l_count = max(
                    1, (round((c - last_x)/random.randint(self.BOX_SIDE_MIN, self.BOX_SIDE_MAX))))
                l = (c - last_x) // l_count

            w_count, w = 0, 0
            while w > self.BOX_SIDE_MAX or w < self.BOX_SIDE_MIN:
                w_count = max(
                    1, (round(self.CONTAINER_DIM[1]/random.randint(self.BOX_SIDE_MIN, self.BOX_SIDE_MAX))))
                w = self.CONTAINER_DIM[1] // w_count

            h_count, h = 0, 0
            while h > self.BOX_SIDE_MAX or h < self.BOX_SIDE_MIN:
                h_count = max(
                    1, (round(self.CONTAINER_DIM[2]/random.randint(self.BOX_SIDE_MIN, self.BOX_SIDE_MAX))))
                h = self.CONTAINER_DIM[2] // h_count
            # print(f'{l_count}x{l}={l_count*l}, {w_count}x{w}={w_count*w}, {h_count}x{h}={h_count*h}')
            type_count = l_count*w_count*h_count
            if l > self.BOX_SIDE_MAX or w > self.BOX_SIDE_MAX or h > self.BOX_SIDE_MAX or l < self.BOX_SIDE_MIN or w < self.BOX_SIDE_MIN or h < self.BOX_SIDE_MIN:
                print(f'Box type {l}x{w}x{h} count: {type_count}')
            block_volume = (c - last_x) * \
                self.CONTAINER_DIM[1] * self.CONTAINER_DIM[2]
            size = (l, w, h)
            volume_individual = l*w*h
            if volume_individual > block_volume:
                print("Error: Box volume is greater than block volume")
            volume_total += volume_individual*type_count
            # print(f'Box type {size} count: {type_count}')
            last_x = c

            box_types.append({
                'size': size,
                'value': volume_individual,
                'volume': volume_individual,
                'min_count': round(type_count*random.uniform(0.75, 1.0)),
                'max_count': round(type_count*random.uniform(1.0, 1.25)),
                # Mantener la solución para referencia futura
                'solution': {'box_count': type_count, 'order': i},
            })
        random.shuffle(box_types)  # Desordenar los grupos
        result['box_types'] = box_types
        result['types_count'] = len(box_types)
        result['solution'] = {
            'volume_total': volume_total,
            'box_count': sum([b['solution']['box_count'] for b in box_types]),
            'value_total': sum([b['solution']['box_count']*b['value'] for b in box_types]),
        }

        # print(f'Total volume: {volume_total/1000000000} m3 de {CONTAINER_DIM[0]*CONTAINER_DIM[1]*CONTAINER_DIM[2]/1000000000} m3')
        self.result = result
        return result
