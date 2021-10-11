import numpy as np
import astropy.units as apu
import astropy.constants as apc
import astropy.cosmology as acosmo

def cMpc_to_z(cMpc, cosmology="Planck15"):
    """
    Convert a comoving distance with units Mpc into a redshift.
    Parameters
    ----------
    cMpc: array-like, shape (N, )
        The distance values. Must be 1D or scalar.
    cosmology: string or astropy.cosmology.core.FLRW
        The cosmology used to calculate distance. This can either be a
        string of the cosmology keyword used in astropy (e.g 'Planck13'
        or 'WMAP7') or an instance of an astropy.cosmology.
        Default: 'Planck15'
    Returns
    -------
    redshift: astropy.unit.Quantity
        The distance to a redshift in comoving Mpc.
    Examples
    --------
    """

    cosmo = get_cosmology_from_name(cosmology)

    # If the array doesn't have units, apply them for calculation later.
    if not isinstance(cMpc, apu.Quantity):
        cMpc = cMpc * apu.Mpc

    # If the comoving distance is really small the user likely wants the
    # result to be at 0.0 redshift. 1e-4 Mpc is approx 100 pc.
    distance_zero_threshold = 1e-4 * apu.Mpc

    # Check of the input distances is a list or a scalar.
    distance_is_scalar = cMpc.isscalar

    # If the distance is a scalar, perform a scalar calculation.
    if distance_is_scalar:
        if cMpc >= distance_zero_threshold:
            redshift = acosmo.z_at_value(cosmo.comoving_distance, cMpc)
        else:
            redshift = 0.0

    # If the distance is an array, perform array calculation
    else:
        # Default value is 0.0 redshift
        redshift = np.zeros_like(cMpc.value)

        for i, dist in enumerate(cMpc):
            if dist >= distance_zero_threshold:
                redshift[i] = acosmo.z_at_value(cosmo.comoving_distance, dist)

    return redshift


def get_cosmology_from_name(cosmology):
    """
    Get an astropy cosmology from a name.
    Parameters
    ----------
    cosmology: string or astropy.cosmology.core.FLRW
        The cosmology to obtain. This can either be a string of the
        cosmology keyword used in astropy (e.g 'Planck13' or 'WMAP7')
        or an instance of an astropy.cosmology.
    Returns
    -------
    cosmo: astropy.cosmology.core.FLRW
        An astropy cosmology.
    """

    # This list should be updated when astropy releases the Planck18 cosmology
    available_cosmologies = {
        "WMAP5": acosmo.WMAP5,
        "WMAP7": acosmo.WMAP7,
        "WMAP9": acosmo.WMAP9,
        "Planck13": acosmo.Planck13,
        "Planck15": acosmo.Planck15,
    }

    # If the user uses a string for the cosmology look it up in the dict.
    # If they specify a cosmology class, use that instead.
    if isinstance(cosmology, str):
        if cosmology in available_cosmologies.keys():
            cosmo = available_cosmologies[cosmology]
        else:
            msg = (f"""The cosmology '{cosmology}' is not in the list of
            available cosmologies with string keywords. The list
            if available cosmologies accessable via keyword are:
            {available_cosmologies.keys()}""")
            raise ValueError(msg)

    elif isinstance(cosmology, acosmo.core.FLRW):
        cosmo = cosmology

    return cosmo


def calculate_scale_factor_from_cMpc(cMpc, cosmology="Planck15"):
    """
    Calculates the scale factor at given comoving distances.

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
    redshift = cMpc_to_z(cMpc, cosmology=cosmology)
    a = (1 + redshift)**-1

    return a


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

    cosmo = get_cosmology_from_name(cosmology)
    H0 = cosmo.H0

    scale_factor = calculate_scale_factor_from_cMpc(cMpc, cosmology=cosmology)

    proper_dist = cMpc * apu.Mpc / scale_factor 

    velocity = proper_dist * H0

    return velocity


if __name__ == "__main__":
    cosmology = "Planck15"

    distances = np.array([1, 10, 100, 1_000])

    velocities = calculate_Hubble_flow_velocity_from_cMpc(distances, cosmology)


    for i, (v, dist) in enumerate(zip(velocities, distances)):
        print(f"d = {dist} cMpc -> v = {v:.2f}")