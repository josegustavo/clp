from operator import itemgetter
from copy import deepcopy


def evaluate(population, container_dimension, types):
    container_vol = container_dimension[0] * \
        container_dimension[1] * container_dimension[2]
    for key, individual in enumerate(population):
        dblf_side = [[0, 0, 0] + container_dimension +
                     [individual['types_num'][0]]]
        dblf_top = []
        dblf_front = []
        occupied_vol = 0
        number_boxes = 0
        value = 0
        result = []

        for box_counts, n_type, r in zip(individual['counts'], individual['types_num'], individual['rotations']):
            one_type = types[n_type]
            for box_number in range(box_counts):
                dblf = dblf_side + dblf_top + dblf_front
                for curr in deepcopy(dblf):
                    space_vol = curr[3] * curr[4] * \
                        curr[5]  # Volumen del espacio
                    box_vol = one_type['volume_individual']
                    box_value = one_type['value_individual']

                    # Rotación de la caja
                    if r == 0:
                        l, w, h = one_type['box_size']
                    else:
                        w, l, h = one_type['box_size']

                    if space_vol >= box_vol and curr[3] >= l and curr[4] >= w and curr[5] >= h:

                        result.append(curr[0:3] + [l, w, h, n_type])
                        occupied_vol += box_vol
                        number_boxes += 1
                        value += box_value

                        # Dividir el espacio restante
                        top_space = [curr[0], curr[1], curr[2] + h,
                                     l, curr[4], curr[5] - h, n_type] if curr[5] - h > 0 else None
                        beside_space = [curr[0], curr[1] + w, curr[2],
                                        l, curr[4] - w, h, n_type] if curr[4] - w > 0 else None
                        front_space = [curr[0] + l, curr[1], curr[2],
                                       curr[3] - l, curr[4], curr[5], n_type] if curr[3] - l > 0 else None

                        # Eliminar el espacio actual
                        if curr in dblf_side:
                            dblf_side.remove(curr)
                        elif curr in dblf_top:
                            dblf_top.remove(curr)
                        elif curr in dblf_front:
                            dblf_front.remove(curr)

                        # Añadir los nuevos espacios
                        if top_space:
                            dblf_top.append(top_space)
                            dblf_top = sorted(dblf_top, key=itemgetter(2))
                        if beside_space:
                            dblf_side.append(beside_space)
                            dblf_side = sorted(dblf_side, key=itemgetter(1))
                        if front_space:
                            dblf_front.append(front_space)
                            dblf_front = sorted(dblf_front, key=itemgetter(0))

                        # Romper el bucle para la siguiente caja
                        break

            # Para evitar colocar cajas en espacios inaccesibles, eliminar los espacio laterales y superiores
            dblf_side = []
            dblf_top = []

        fitness_value = [round((occupied_vol / container_vol * 100), 2), round((number_boxes / sum(individual['counts'])) * 100, 2),
                         value]
        population[key]['fitness'] = deepcopy(fitness_value)
        population[key]['result'] = result
    return population

# _=evaluate([the_best(population)], container_dimension, types)
# draw_anim_types(the_best(population))
