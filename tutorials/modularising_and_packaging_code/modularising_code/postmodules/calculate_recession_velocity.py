import numpy as np
import astropy.units as apu
import astropy.constants as apc
import astropy.cosmology as acosmo

import utils

def calculate_Hubble_flow_velocity_from_cMpc(cMpc, cosmology="Planck15"):
    """
    Calculates the Hubble flow recession velocity from comoving distance

    Parameters
    ----------
    cMpc : array-like, shape (N, )
        The distance in units of comoving megaparsecs. Must be 1D or scalar.

    cosmology : string or astropy.cosmology.core.FLRW
        The cosmology to assume whilst calculating distance. Default: Planck15.

    Returns
    -------
    a : array-like, shape (N, )
        The scale factor.

    """

    cosmo = utils.get_cosmology_from_name(cosmology)
    H0 = cosmo.H0

    scale_factor = utils.calculate_scale_factor_from_cMpc(cMpc, cosmology=cosmology)

    proper_dist = cMpc * apu.Mpc / scale_factor 

    velocity = proper_dist * H0

    return velocity


if __name__ == "__main__":
    cosmology = "Planck15"

    distances = np.array([1, 10, 100, 1_000])

    velocities = calculate_Hubble_flow_velocity_from_cMpc(distances, cosmology)


    for i, (v, dist) in enumerate(zip(velocities, distances)):
        print(f"d = {dist} cMpc -> v = {v:.2f}")
