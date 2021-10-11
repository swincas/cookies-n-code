import numpy as np
import astropy.units as apu
import astropy.constants as apc
import astropy.cosmology as acosmo

import utils

if __name__ == "__main__":
    cosmology = "Planck15"

    scale_factors = np.array([1, 0.75, 0.5, 0.25, 0.1, 0.05])
    distances = np.array([1, 10, 100, 1_000, 10_000])

    a_values_from_distance = utils.calculate_scale_factor_from_cMpc(distances, cosmology)
    distances_from_a_values = utils.calculate_cMpc_from_scale_factor(scale_factors, cosmology)


    for i, (a, dist) in enumerate(zip(a_values_from_distance, distances)):
        print(f"d = {dist} cMpc -> a = {a:.2f}")


    for i, (dist, a) in enumerate(zip(distances_from_a_values, scale_factors)):
        print(f"a = {a} -> d = {dist:.2f}")
