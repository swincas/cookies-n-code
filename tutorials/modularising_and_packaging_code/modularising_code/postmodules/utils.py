import numpy as np
import astropy.units as apu
import astropy.constants as apc
import astropy.cosmology as acosmo


def z_to_cMpc(redshift, cosmology='Planck15'):
    """
    Convert a redshift into a comoving distance with units of Mpc.
    Parameters
    ----------
    redshift: array-like, shape (N, )
        The redshift values. Must be 1D or scalar.
    cosmology: string or astropy.cosmology.core.FLRW
        The cosmology used to calculate distance. This can either be a
        string of the cosmology keyword used in astropy (e.g 'Planck13'
        or 'WMAP7') or an instance of an astropy.cosmology.
        Default: 'Planck15'
    Returns
    -------
    distance: astropy.unit.quantity.Quantity
        The distance to a redshift in comoving Mpc.
    Examples
    --------
    >>> cosmology.z_to_cMpc(2)
    <Quantity 5311.53878858 Mpc>
    >>> cosmology.z_to_cMpc(2, cosmology="WMAP7")
    <Quantity 5279.26488146 Mpc>
    >>> import astropy.cosmology as acosmo
    >>> P13 = acosmo.Planck13
    >>> cosmology.z_to_cMpc(2, cosmology=Planck13)
    <Quantity 5310.8891027 Mpc>
    >>> cosmology.z_to_cMpc(2, cosmology="WMAP7")
    <Quantity 5279.26488146 Mpc>
    >>> redshifts = np.array([0, 1, 2, 3])
    >>> cosmology.z_to_cMpc(redshifts)
    <Quantity [0. , 3395.90541667, 5311.53878858, 6509.79588814] Mpc>
    """

    cosmo = get_cosmology_from_name(cosmology)

    distance = cosmo.comoving_distance(redshift)

    # If the redshift is really small the user likely wants the result
    # to be at 0.0 Mpc. 1e-4 Mpc is 100 pc.
    distance_zero_threshold = 1e-4 * apu.Mpc

    distance[distance < distance_zero_threshold] = 0

    return distance


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


def calculate_cMpc_from_scale_factor(a, cosmology="Planck15"):
    """
    Calculates the comoving distance to specified scale factors.

    Parameters
    ----------
    a : array-like, shape (N, )
        The scale factors.

    cosmology : string or astropy.cosmology.core.FLRW
        The cosmology to assume whilst calculating distance. Default: Planck15.

    Returns
    -------
    cMpc : array-like, shape (N, )
        The distances in units of comoving megaparsecs.

    """

    redshift = -1 + a**-1
    cMpc = z_to_cMpc(redshift, cosmology=cosmology)

    return cMpc


