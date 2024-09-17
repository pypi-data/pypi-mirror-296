# -*- coding: utf-8 -*-
"""
Created in Jan 2021.

@author: jeremy leconte
"""

from typing import Literal, Optional, Tuple  # noqa

import numba
import numpy as np

# Bug: Sphinx should replace `StellarMode` with the following content. Does not actually work.
# StellarMode: TypeAlias = Literal['diffusive', 'collimated']
"""Alias for the supported modes to treat the stellar flux."""


##-- Solve the 2-stream equations --##
@numba.jit(nopython=True, fastmath=True, cache=True)
def solve_2stream_nu_xsec(source_nu: np.ndarray, tau_nu: np.ndarray, dtau_nu: np.ndarray,
                          omega0_nu: np.ndarray, g_asym_nu: np.ndarray,
                          flux_top_dw_nu: np.ndarray, alb_surf_nu: np.ndarray,
                          mu0: float = 0.5, flux_at_level: bool = False,
                          mu_star: Optional[float] = None,
                          stellar_mode: Literal['diffusive', 'collimated'] = 'diffusive',
                          planck_correction_factor: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""
    Deals with the spectral axis.

    Parameters
    ----------
    source_nu :
        $\pi B(T)$ (Planck function) at each of the Nlay+1 level interfaces.
        Shape: **(Nlev+1, Nw)**.
    tau_nu :
        Cumulative optical depth of the previous levels, start at 0.
        The last value tau[-1] is equals to the optical depth of the column.
        Shape: **(Nlev+1, Nw)**.
    dtau_nu :
        Optical depth of each level, for each band.
        Shape: **(Nlev, Nw)**.
    omega0_nu :
        Single scattering albedo of each level for each band.
        Shape: **(Nlev, Nw)**.
    g_asym_nu :
        Asymmetry factor.
        Shape: **(Nlev, Nw)**.
    flux_top_dw_nu :
        Top down flux, either diffusive or collimated.
        Shape: **(Nw,)**.
    alb_surf_nu :
        Surface albedo. Emissivity is assumed to be 1.-alb_surf. Shape: **(Nw,)**.
    mu0 :
        $\mu_0$ is the incident direction of the observer. It is used as an effective angle.

        - $\frac{1}{2}$ yields the hemispheric mean approximation.
        - $\frac{1}{\sqrt(3)}$ yields the quadrature approximation
    flux_at_level :
        - If ``flux_at_level`` is ``True``, fluxes are calculated at the **level surfaces**.
        - If ``False``, fluxes are computed at the **middle of the layers**.

        The top of atmosphere flux is always computed at the top of the uppermost layer (1st level).
    mu_star :
        $\mu_*$ is the incident direction of the solar beam. Used when the incoming diffuse flux is treated as a
        source term.
    stellar_mode :
        When `flux_top_dw_nu` is provided, set the method to be used to take it into account.

        - ``diffusive``: Incoming diffuse flux at the upper boundary.
        - ``collimated``: Incoming diffuse flux is treated as a source term.
    planck_correction_factor :
        Allow setting the epsilon used to rewrite the equations , from Chaverot et al. (2022).

    Returns
    -------
    flux_up : np.ndarray
        Shape: **(Nlev, Nw)**.
    flux_dw : np.ndarray
        Shape: **(Nlev, Nw)**.
    flux_net: np.ndarray
        Shape: **(Nlev, Nw)**.
    J4pi: np.ndarray
        Shape: **(Nlev, Nw, Ng)**.
    """
    NLEV, NW = source_nu.shape

    flux_up: np.ndarray = np.zeros((NLEV, NW))
    flux_dw: np.ndarray = np.zeros((NLEV, NW))
    flux_net: np.ndarray = np.zeros((NLEV, NW))
    J4pi: np.ndarray = np.zeros((NLEV, NW))

    for iW in range(NW):
        flux_up[:, iW], flux_dw[:, iW], flux_net[:, iW], J4pi[:, iW] = \
            solve_2stream(source_nu[:, iW], tau_nu[:, iW], dtau_nu[:, iW],
                          omega0_nu[:, iW], g_asym_nu[:, iW],
                          flux_top_dw_nu[iW], alb_surf_nu[iW],
                          mu0, flux_at_level,
                          mu_star, stellar_mode,
                          planck_correction_factor)

    return flux_up, flux_dw, flux_net, J4pi


@numba.jit(nopython=True, fastmath=True, cache=True)
def solve_2stream_nu_corrk(source_nu: np.ndarray, tau_nu: np.ndarray, dtau_nu: np.ndarray,
                           omega0_nu: np.ndarray, g_asym_nu: np.ndarray,
                           flux_top_dw_nu: np.ndarray, alb_surf_nu: np.ndarray,
                           mu0: float = 0.5, flux_at_level: bool = False,
                           mu_star: Optional[float] = None,
                           stellar_mode: Literal['diffusive', 'collimated'] = 'diffusive',
                           planck_correction_factor: Optional[float] = None
                           ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""
    Deals with the spectral axis.

    Parameters
    ----------
    source_nu :
        $\pi B(T)$ (Planck function) at each of the Nlay+1 level interfaces.
        Shape: **(Nlev+1, Nw)**.
    tau_nu :
        Cumulative optical depth of the previous levels, start at 0.
        The last value tau[-1] is equals to the optical depth of the column.
        Shape: **(Nlev+1, Nw, Ng)**.
    dtau_nu :
        Optical depth of each level, for each band.
        Shape: **(Nlev, Nw, Ng)**.
    omega0_nu :
        Single scattering albedo of each level, for each band.
        Shape: **(Nlev, Nw, Ng)**.
    g_asym_nu :
        Asymmetry factor.
        Shape: **(Nlev, Nw, Ng)**.
    flux_top_dw_nu :
        Top down flux, either diffusive or collimated.
        Shape: **(Nw,)**.
    alb_surf_nu :
        Surface albedo. Emissivity is assumed to be 1.-alb_surf. Shape: **(Nw,)**.
    mu0 :
        $\mu_0$ is the incident direction of the observer.  It is used as an effective angle.

        - $\frac{1}{2}$ yields the hemispheric mean approximation.
        - $\frac{1}{\sqrt(3)}$ yields the quadrature approximation
    flux_at_level :
        - If ``flux_at_level`` is ``True``, fluxes are calculated at the **level surfaces**.
        - If ``False``, fluxes are computed at the **middle of the layers**.

        The top of atmosphere flux is always computed at the top of the uppermost layer (1st level).
    mu_star :
        $\mu_*$ is the incident direction of the solar beam. Used when the incoming diffuse flux is treated as a
        source term.
    stellar_mode :
        Dictate how `flux_top_dw_nu` is taken it into account.
        - ``diffusive``: Incoming diffuse flux at the upper boundary.
        - ``collimated``: Incoming diffuse flux is treated as a source term.
    planck_correction_factor :
        Allow setting the epsilon used to rewrite the equations , from Chaverot et al. (2022).

    Returns
    -------
    flux_up : np.ndarray
        Shape: **(Nlev, Nw, Ng)**.
    flux_dw : np.ndarray
        Shape: **(Nlev, Nw, Ng)**.
    flux_net: np.ndarray
        Shape: **(Nlev, Nw, Ng)**.
    J4pi: np.ndarray
        Shape: **(Nlev, Nw, Ng)**.
    """
    NLEV, NW = source_nu.shape
    NG = dtau_nu.shape[-1]

    flux_up: np.ndarray = np.zeros((NLEV, NW, NG))
    flux_dw: np.ndarray = np.zeros((NLEV, NW, NG))
    flux_net: np.ndarray = np.zeros((NLEV, NW, NG))
    J4pi: np.ndarray = np.zeros((NLEV, NW, NG))

    for iW in range(NW):
        for iG in range(NG):
            (flux_up[:, iW, iG],
             flux_dw[:, iW, iG],
             flux_net[:, iW, iG],
             J4pi[:, iW, iG]) = solve_2stream(source=source_nu[:, iW], tau=tau_nu[:, iW, iG], dtau=dtau_nu[:, iW, iG],
                                              omega0=omega0_nu[:, iW, iG], g_asym=g_asym_nu[:, iW, iG],
                                              flux_top_dw=flux_top_dw_nu[iW], alb_surf=alb_surf_nu[iW],
                                              mu0=mu0, flux_at_level=flux_at_level,
                                              mu_star=mu_star, stellar_mode=stellar_mode,
                                              planck_correction_factor=planck_correction_factor)

    return flux_up, flux_dw, flux_net, J4pi


@numba.jit(nopython=True, fastmath=True, cache=True)
def solve_2stream(source: np.ndarray, tau: np.ndarray, dtau: np.ndarray,
                  omega0: np.ndarray, g_asym: np.ndarray,
                  flux_top_dw: float, alb_surf: float,
                  mu0: float, flux_at_level: bool,
                  mu_star: Optional[float],
                  stellar_mode: Literal['diffusive', 'collimated'],
                  planck_correction_factor: Optional[float]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""
    Solve the 2-stream equations over a bin.

    After Toon et al. (JGR, 1989). Equation numbers refer to this article.

    ``alb_surf`` = $R_{sfc}$,
    ``emis_surf`` = $\varepsilon$ = ``1 - alb_surf`` = $1 - R_{sfc}$,

    Parameters
    ----------
    source:
        Shape: **(Nlev+1,)**.
    tau:
        Shape: **(Nlev+1,)**.
    dtau:
        Shape: **(Nlev,)**.
    omega0:
        Shape: **(Nlev,)**.
    g_asym:
        Shape: **(Nlev,)**.
    mu0:
    flux_top_dw:
    alb_surf:
    flux_at_level:
    mu_star:
    stellar_mode :
    planck_correction_factor :
        Allow setting the epsilon used to rewrite the equations , from Chaverot et al. (2022).

    Returns
    -------
    flux_up : np.ndarray
        Shape: **(Nlev+1,)**.
    flux_dw : np.ndarray
        Shape: **(Nlev+1,)**.
    flux_net: np.ndarray
        Shape: **(Nlev+1,)**.
    J4pi: np.ndarray
        Shape: **(Nlev+1,)**.
    """
    Nlev = dtau.size

    r"""This factor ensure that the emissivity will not be greater than $1.$, when $\mu_0\neq .5$
    , from Chaverot et al. (2022)
    When  $\mu_0 = .5$, we retrieve the hemispheric mean method, 
    while for $\mu_0 = 1/\sqrt{3}$, we retrieve the quadrature method, from Toon et al. (1989)
    """
    planck_correction_factor: float = planck_correction_factor or 2. * mu0

    flux_diffuse_top_dw = flux_top_dw if stellar_mode == 'diffusive' else 0.
    # To skip the compute intensive part, if collimated flux is not used set to `None` and not `0`.
    # Moreover, when collimated flux is used but the column is not exposed to it,
    # setting `mu_star` to `None` allow to skip the computation of a source term null.
    flux_collimated_top_dw = flux_top_dw if stellar_mode == 'collimated' and mu_star is not None else None

    """
    Due to the fact that numba is typed, if we type `mu_star` as `Optional[float]`, 
    the fact that "`stellar_mode == 'collimated'` => `mu_star` is not `None`" is not 
    obvious to numba. 
    So, the code-branch `if flux_collimated_top_dw is not None: ...` where `mu_star` is used as a float
    will result on a compilation error. It's because numba do not know that in this case, `mu_star` is a float.
    There are 2 solutions: 
        - use `if flux_collimated_top_dw is not None and isinstance(mu_star, float)`
        - set `mu_star` to `0.` knowing that it will not be used.
    We use the second solution to simplify the code.
    """
    mu_star: float = mu_star if mu_star is not None else 0.

    gamma_1, gamma_2, gamma_3, gamma_4 = _gammas_toon(omega0=omega0, g_asym=g_asym,
                                                      mu0=mu0, mu_star=mu_star, planck_correction_factor=planck_correction_factor,  # 1. / np.sqrt(3.)
                                                      stellar_mode=stellar_mode)

    flux_up, flux_dw, flux_net, J4pi = matrix_toon_tridiag(Nlev=Nlev, taucum=tau, dtau=dtau, omega_0=omega0,
                                                           gamma_1=gamma_1, gamma_2=gamma_2,
                                                           gamma_3=gamma_3, gamma_4=gamma_4,
                                                           source=source, mu0=mu0, mu_star=mu_star,
                                                           flux_diffuse_top_dw=flux_diffuse_top_dw,
                                                           flux_collimated_top_dw=flux_collimated_top_dw,
                                                           alb_surf=alb_surf, flux_at_level=flux_at_level)

    return flux_up, flux_dw, flux_net, J4pi


##-- $C^{+}(0), C^{-}(0),C^{+}(\tau)$ and $C^{-}(\tau)$ --##
@numba.jit(nopython=True, fastmath=True, cache=True)
def c_planck(source: np.ndarray, dtau: np.ndarray,
             gamma_1: np.ndarray, gamma_2: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""
    c_up/dw is for c+/- without direct beam scattering.

    _top is for tau equal 0 (top of the layer)
    _bot is for tau=dtau (bottom of the layer)
    removed a pi factor because source is pi*B
    Parameters
    ----------
    source :
        Shape: **(Nlev+1,)**
    dtau :
        Shape: **(Nlev,)**
    gamma_1 :
        Shape: **(Nlev,)**
    gamma_2 :
        Shape: **(Nlev,)**

    Returns
    -------
    c_up_top : np.ndarray
        Shape: **(Nlev,)**
    c_dw_top : np.ndarray
        Shape: **(Nlev,)**
    c_up_bot : np.ndarray
        Shape: **(Nlev,)**
    c_dw_bot : np.ndarray
        Shape: **(Nlev,)**
    """
    # cst=2*mu0
    # cst=1. # this factor seems to avoid emissivity greater than one.
    # but what is the analytical basis for this ???
    # print(gamma_1+gamma_2)

    inv_dtaugam = 1. / (dtau * (gamma_1 + gamma_2))

    c_up_top = (source[:-1] * (1. - inv_dtaugam) + source[1:] * inv_dtaugam)  # *cst
    c_dw_top = (source[:-1] * (1. + inv_dtaugam) - source[1:] * inv_dtaugam)  # *cst

    c_up_bot = (-source[:-1] * inv_dtaugam + source[1:] * (1. + inv_dtaugam))  # *cst
    c_dw_bot = (source[:-1] * inv_dtaugam + source[1:] * (1. - inv_dtaugam))  # *cst

    return c_up_top, c_dw_top, c_up_bot, c_dw_bot


@numba.jit(nopython=True, fastmath=True, cache=True)
def _c_star_denominator(l: np.ndarray, mu_star: float, eps_frac: float = 1.e-12) -> np.ndarray:
    r"""
    Compute the denominator for equations (23) and (24).
    We use the following reference: https://github.com/NCAR/iCESM1.2/blob/355f7b2c77f1b49004145f6b975617c0917d18ce/models/atm/cam/src/chemistry/mozart/mo_ps2str.F90#L236C1-L238C47
    This allow to properly implement "In practice, if the equality happens to occur, this problem can be eliminated
    by simply choosing a slightly different value of mu0" (Toon & al 1989)

    Parameters
    ----------
    l :
        lambda_toon value
    mu_star :
        $\mu_{*}$
    eps_frac:
    """
    #
    #
    # Naively compute the denominator
    frac: np.ndarray = l * l - 1. / (mu_star * mu_star)

    temp = np.maximum(eps_frac * np.ones_like(frac), np.abs(frac))

    # Return the proper denominator
    return np.copysign(temp, frac)


@numba.jit(nopython=True, fastmath=True, cache=True)
def c_star(flux_collimated_top_down: float, taucum: np.ndarray, dtau: np.ndarray,
           gamma_1: np.ndarray, gamma_2: np.ndarray, gamma_3: np.ndarray, gamma_4: np.ndarray,
           omega_0: np.ndarray, mu_star: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""
    Compute the values of $C^{+}(0), C^{-}(0),C^{+}(\tau)$ and $C^{-}(\tau)$ for the solar radiation part.

    Follow the equations (23) and (24).

    Parameters
    ----------
    flux_collimated_top_down :
    taucum :
        Shape: **(Nlev+1,)**.
    dtau :
        Shape: **(Nlev,)**.
    gamma_1 :
        $\gamma_{1}$
        Shape: **(Nlev,)**.
    gamma_2 :
        $\gamma_{2}$
        Shape: **(Nlev,)**.
    gamma_3 :
        $\gamma_{3}$
        Shape: **(Nlev,)**.
    gamma_4 :
        $\gamma_{3}$
        Shape: **(Nlev,)**.
    omega_0 :
        $\omega_{0}$
        Shape: **(Nlev,)**.
    mu_star :
        $\mu_{*}$

    Returns
    -------
    $C^{+}(0)$ :
        Shape: **(Nlev,)**.
    $C^{-}(0)$ :
        Shape: **(Nlev,)**.
    $C^{+}(\tau)$ :
        Shape: **(Nlev,)**.
    $C^{-}(\tau)$ :
        Shape: **(Nlev,)**.
    """
    r"""From `Table 1` of Toon et al., `\lambda_4 = 1 - \lambda_3`"""

    r"""
    If $\lambda=\frac{1}{\mu_*}, we get a divide by zero.
    naive implementation
    .. code:
        frac: float = lambda_toon2(gamma_1, gamma_2) - 1. / mu_star ** 2
    """
    l: np.ndarray = lambda_toon(gamma_1, gamma_2)

    frac = _c_star_denominator(l, mu_star)

    # Replace `source` with `flux_collimated_top_down / mu_star` to get the stellar flux along the ray.
    common_part = omega_0 * flux_collimated_top_down / mu_star
    inv_mu_star = 1. / mu_star

    fac_up = (gamma_1 - inv_mu_star) * gamma_3 + gamma_4 * gamma_2
    fac_dw = (gamma_1 + inv_mu_star) * gamma_4 + gamma_2 * gamma_3

    # For the level n, \dtau = 0
    c_up_top: np.ndarray = common_part * np.exp(- taucum[:-1] / mu_star) * fac_up / frac
    c_dw_top: np.ndarray = common_part * np.exp(- taucum[:-1] / mu_star) * fac_dw / frac

    # For the level n, \dtau = \dtau_n
    c_up_bot: np.ndarray = common_part * np.exp(- taucum[1:] / mu_star) * fac_up / frac
    c_dw_bot: np.ndarray = common_part * np.exp(- taucum[1:] / mu_star) * fac_dw / frac

    return c_up_top, c_dw_top, c_up_bot, c_dw_bot


##-- C^{+}(\frac{\tau}{2})$ and $C^{-}(\frac{\tau}{2})$ --##
@numba.jit(nopython=True, fastmath=True, cache=True)
def c_planck_mid(source: np.ndarray, dtau: np.ndarray,
                 gamma_1: np.ndarray, gamma_2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Compute $C^\pm$ at the middle of the layer, i.e. at tau=dtau/2, ie $C^\pm(\frac{\tau}{2})$.

    c_up/dw is for c+/- without direct beam scattering.

    Parameters
    ----------
    source :
        Shape: **(Nlev+1,)**.
    dtau :
        Shape: **(Nlev,)**.
    gamma_1 :
        $\gamma_1$
        Shape: **(Nlev,)**.
    gamma_2 :
        $\gamma_2$
        Shape: **(Nlev,)**.

    Returns
    -------
    $C^{+}(\frac{\tau}{2})$ :
        Shape: **(Nlev,)**.
    $C^{-}(\frac{\tau}{2})$ :
        Shape: **(Nlev,)**.
    """
    inv_dtaugam = 1. / (dtau * (gamma_1 + gamma_2))

    c_up_mid = (source[:-1] * (.5 - inv_dtaugam) + source[1:] * (0.5 + inv_dtaugam))
    c_dw_mid = (source[:-1] * (.5 + inv_dtaugam) + source[1:] * (0.5 - inv_dtaugam))

    return c_up_mid, c_dw_mid


@numba.jit(nopython=True, fastmath=True, cache=True)
def c_star_mid(flux_collimated_top_down: float, taucum: np.ndarray, dtau: np.ndarray,
               gamma_1: np.ndarray, gamma_2: np.ndarray, gamma_3: np.ndarray, gamma_4: np.ndarray,
               omega_0: np.ndarray, mu_star: float) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Compute $C^\pm$ at the middle of the layer, i.e. at tau=dtau/2, ie $C^\pm(\frac{\tau}{2})$.

    Parameters
    ----------
    flux_collimated_top_down :
    taucum :
        Shape: **(Nlev+1,)**.
    dtau :
        Shape: **(Nlev,)**.
    gamma_1 :
        $\gamma_1$
        Shape: **(Nlev,)**.
    gamma_2 :
        $\gamma_2$
        Shape: **(Nlev,)**.
    gamma_3 :
        $\gamma_3$
        Shape: **(Nlev,)**.
    gamma_4 :
        $\gamma_{3}$
        Shape: **(Nlev,)**.
    omega_0 :
        $\omega_0$
        Shape: **(Nlev,)**.
    mu_star :
        $\mu_*$

    Returns
    -------
    $C^{+}(\frac{\tau}{2})$ :
        Shape: **(Nlev,)**.
    $C^{-}(\frac{\tau}{2})$ :
        Shape: **(Nlev,)**.
    """

    l: np.ndarray = lambda_toon(gamma_1, gamma_2)

    frac: np.ndarray = _c_star_denominator(l, mu_star)

    # Replace `source` with ` source / mu_star` to get the stellar flux along the ray.
    common_part = omega_0 * flux_collimated_top_down / mu_star
    inv_mu_star = 1. / mu_star

    fac_up = (gamma_1 - inv_mu_star) * gamma_3 + gamma_4 * gamma_2
    fac_dw = (gamma_1 + inv_mu_star) * gamma_4 + gamma_2 * gamma_3

    c_up_mid: np.ndarray = common_part * np.exp(- (taucum[:-1] + .5 * dtau) / mu_star) * fac_up / frac
    c_dw_mid: np.ndarray = common_part * np.exp(- (taucum[:-1] + .5 * dtau) / mu_star) * fac_dw / frac

    return c_up_mid, c_dw_mid


@numba.jit(nopython=True, fastmath=True, cache=True)
def mid_factor_toon(dtau: np.ndarray, gamma_1: np.ndarray, gamma_2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Factors to recover the flux at mid layer.

    Parameters
    ----------
    dtau :
        Shape: **(Nlev,)**.
    gamma_1 :
        $\gamma_1$
        Shape: **(Nlev,)**.
    gamma_2 :
        $\gamma_2$
        Shape: **(Nlev,)**.

    Returns
    -------
    $\text{factor}_{1,\frac{1}{2}}$ : np.ndarray
    $\text{factor}_{2,\frac{1}{2}}$ : np.ndarray
    """
    lamb, GAMMA = lambda_GAMMA(gamma_1, gamma_2)

    expdtaumid = np.exp(-lamb * dtau * 0.5)

    mid_fac1 = 2. * (1. + GAMMA) * expdtaumid
    mid_fac2 = 2. * (1. - GAMMA) * expdtaumid

    return mid_fac1, mid_fac2


##-- $S^\pm$ --##
@numba.jit(nopython=True, fastmath=True, cache=True)
def s_planck(omega0: np.ndarray, bb_source: np.ndarray, planck_correction_factor: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Implement equation (15).

    Parameters
    ----------
    omega0 :
        Shape: **(Nlev,)**.
    bb_source :
        Shape: **(Nlev,)**.
    planck_correction_factor:

    Returns
    -------
    $S^+$ : np.ndarray
        Shape: **(Nlev,)**.
    $S^-$ : np.ndarray
        Shape: **(Nlev,)**.

    """
    s = 2. * (1. - omega0) * bb_source[:-1] / planck_correction_factor

    return s, s


@numba.jit(nopython=True, fastmath=True, cache=True)
def s_star(omega0: np.ndarray, gamma_3: np.ndarray, gamma_4: np.ndarray, taucum: np.ndarray,
           flux_collimated_top_down: float, mu_star: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Implement equations (13) and (14).

    Parameters
    ----------
    omega0 :
        Shape: **(Nlev,)**.
    gamma_3 :
        Shape: **(Nlev,)**.
    gamma_4 :
        Shape: **(Nlev,)**.
    taucum :
        Shape: **(Nlev+1,)**.
    flux_collimated_top_down :
    mu_star :

    Returns
    -------
    $S^+$ : np.ndarray
        Shape: **(Nlev,)**.
    $S^-$ : np.ndarray
        Shape: **(Nlev,)**.

    """
    sp = gamma_3 * flux_collimated_top_down / mu_star * omega0 * np.exp(-taucum[:-1] / mu_star)
    sm = gamma_4 * flux_collimated_top_down / mu_star * omega0 * np.exp(-taucum[:-1] / mu_star)

    return sp, sm


@numba.jit(nopython=True, fastmath=True, cache=True)
def _gamma_planck(omega0: np.ndarray, g_asym: np.ndarray,
                  mu0: float, planck_correction_factor: float) -> Tuple[np.ndarray, np.ndarray]:
    r"""
        Compute the value for $\gamma_1$ and $\gamma_2$ using Table 1.

    Parameters
    ----------
        omega0:
            Shape: **(Nlev,)**
        g_asym:
            Shape: **(Nlev,)**
        mu0:
        planck_correction_factor:
    Returns
    -------
        $\gamma_1$ : np.ndarray
            Shape: **(Nlev,)**

        $\gamma_2$ : np.ndarray
            Shape: **(Nlev,)**
    """

    gamma_1 = (2. - omega0 * (1. + g_asym)) / planck_correction_factor
    gamma_2 = omega0 * (1. - g_asym) / planck_correction_factor

    return gamma_1, gamma_2


##-- $\gamma_i, e_i$, \lambda. \Gamma$ --##
@numba.jit(nopython=True, fastmath=True, cache=True)
def _gamma_star(g_asym: np.ndarray, mu0: float, mu_star: float) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Compute the value of $\gamma_{3,4}$, following Toon et al.

    At this moment, we made the choice to use the value for the quadrature method
    and identifying the factor $\sqrt{3}$ to $\frac{1}{mu0}$ in our code.
    Moreover, these factor are not subject to the `planck_correction_factor`.

    Notes
    -----
    For this function, $\mu_0$ should have the same meaning as $\mu_1$ in the article.

    Parameters
    ----------
    g_asym :
         Shape: **(Nlev,)**.
    mu0 :
    mu_star :

    Returns
    -------
    $\gamma_3$: np.ndarray
        Shape: **(Nlev,)**.
    $\gamma_4$: np.ndarray
        Shape: **(Nlev,)**.
    """
    gamma_3 = (1 - g_asym * mu_star/mu0)/2
    gamma_4 = 1. - gamma_3

    return gamma_3, gamma_4


@numba.jit(nopython=True, fastmath=True, cache=True)
def _gammas_toon(omega0: np.ndarray, g_asym: np.ndarray,
                 mu0: float, mu_star: float, planck_correction_factor: float,
                 stellar_mode: Literal['diffusive', 'collimated']) -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""
    Compute the value for $\gamma_1$, $\gamma_2$, $\gamma_3$ and $\gamma_4$.

    Parameters
    ----------
        omega0 :
            Shape: **(Nlev,)**
        g_asym :
            Shape: **(Nlev,)**
        mu0 :
        mu_star :
        planck_correction_factor:
        stellar_mode:
    Returns
    -------
        $\gamma_1$ : np.ndarray
            Shape: **(Nlev,)**

        $\gamma_2$ : np.ndarray
            Shape: **(Nlev,)**

        $\gamma_3$ : np.ndarray
            Shape: **(Nlev,)**

        $\gamma_4$ : np.ndarray
            Shape: **(Nlev,)**
    """
    gamma_1, gamma_2 = _gamma_planck(omega0, g_asym, mu0, planck_correction_factor)
    gamma_3, gamma_4 = np.empty_like(gamma_1), np.empty_like(gamma_1)

    if stellar_mode == 'collimated':
        gamma_3, gamma_4 = _gamma_star(g_asym, mu0, mu_star)

    return gamma_1, gamma_2, gamma_3, gamma_4


@numba.jit(nopython=True, fastmath=True, cache=True)
def lambda_toon2(gamma_1: np.ndarray, gamma_2: np.ndarray) -> np.ndarray:
    r"""
    Compute $\lambda^2$ from eq 21 of Toon et al.

    Parameters
    ----------
    gamma_1 :
        $\gamma_1$, Shape: **(Nlev,)**.
    gamma_2 :
        $\gamma_2$, Shape: **(Nlev,)**.

    Returns
    -------
    $\left( \gamma_1^2 - \gamma_2^2 \right)$ : np.ndarray
        Shape: **(Nlev,)**.
    """
    return gamma_1 * gamma_1 - gamma_2 * gamma_2


@numba.jit(nopython=True, fastmath=True, cache=True)
def lambda_toon(gamma_1: np.ndarray, gamma_2: np.ndarray) -> np.ndarray:
    r"""
    Compute $\lambda$ from eq 21 of Toon et al.

    Parameters
    ----------
    gamma_1 :
        $\gamma_1$
        Shape: **(Nlev,)**.
    gamma_2 :
        $\gamma_2$
        Shape: **(Nlev,)**.

    Returns
    -------
    $\left( \gamma_1^2 - \gamma_2^2 \right)^\frac{1}{2}$ : np.ndarray
        Shape: **(Nlev,)**.
    """
    return np.sqrt(lambda_toon2(gamma_1, gamma_2))


@numba.jit(nopython=True, fastmath=True, cache=True)
def lambda_GAMMA(gamma_1, gamma_2) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Compute $\lambda$ and $\Gamma$ from eq 21 and 22 of Toon et al.

    Notes
    -----
        Toon and al. provide two formulas for $\Gamma$ at equation (22):

        - $\frac{\gamma_2}{\gamma_1 + \lambda}$
        - $\frac{\gamma_1 - \lambda}{\gamma_2}$

        We choose two use the first one.

    Parameters
    ----------
    gamma_1 :
        $\gamma_1$
        Shape: **(Nlev,)**
    gamma_2 :
        $\gamma_2$
        Shape: **(Nlev,)**

    Returns
    -------
    $\lambda$ : np.ndarray
        Shape: **(Nlev,)**
    $\Gamma$ : np.ndarray
        Shape: **(Nlev,)**
    """
    lamb = lambda_toon(gamma_1, gamma_2)

    GAMMA = gamma_2 / (lamb + gamma_1)
    # GAMMA=(gamma_1-lamb)/(gamma_2)

    return lamb, GAMMA


@numba.jit(nopython=True, fastmath=True, cache=True)
def e_i_toon(dtau: np.ndarray,
             gamma_1: np.ndarray, gamma_2: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""
    $e_i$ factors defined in eq 44.

    Parameters
    ----------
    dtau :
        Shape: **(Nlev,)**
    gamma_1 :
        $\gamma_1$
        Shape: **(Nlev,)**
    gamma_2 :
        $\gamma_2$
        Shape: **(Nlev,)**

    Returns
    -------
    $e_{1}$ : np.ndarray
        Shape: **(Nlev,)**
    $e_{2}$ : np.ndarray
        Shape: **(Nlev,)**
    $e_{3}$ : np.ndarray
        Shape: **(Nlev,)**
    $e_{4}$ : np.ndarray
        Shape: **(Nlev,)**

    """
    lamb, GAMMA = lambda_GAMMA(gamma_1, gamma_2)

    expdtau = np.exp(-lamb * dtau)

    e_1 = 1. + GAMMA * expdtau
    e_2 = 1. - GAMMA * expdtau
    e_3 = GAMMA + expdtau
    e_4 = GAMMA - expdtau

    return e_1, e_2, e_3, e_4


##-- Solver --##
@numba.jit(nopython=True, fastmath=True, cache=True)
def matrix_toon_tridiag(Nlev: int,
                        taucum: np.ndarray, dtau: np.ndarray, omega_0: np.ndarray,
                        gamma_1: np.ndarray, gamma_2: np.ndarray, gamma_3: np.ndarray, gamma_4: np.ndarray,
                        source: np.ndarray,
                        mu0: float, mu_star: float,
                        flux_diffuse_top_dw: float, flux_collimated_top_dw: Optional[float],
                        alb_surf: float, flux_at_level: bool) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""
    Compute the up/dw/net fluxes and J4pi.

    Parameters
    ----------
    Nlev:
        Number of levels.
    taucum:
        Shape: **(Nlev+1,)=(Nlay,)**.
    dtau:
        Shape: **(Nlev,)**.
    omega_0:
        Shape: **(Nlev,)**.
    source:
        Shape: **(Nlev,)**.
    gamma_1:
        Shape: **(Nlev,)**.
    gamma_2:
        Shape: **(Nlev,)**.
    gamma_3:
        Shape: **(Nlev,)**.
        Required in `collimated` mode.
    gamma_4:
        Shape: **(Nlev,)**.
        Required in `collimated` mode.
    mu0:
    mu_star:
    flux_diffuse_top_dw:
        Top downward flux to be treated as a diffusive flux (ie, boundary condition).
    flux_collimated_top_dw:
        Top downward flux to be treated as a collimated flux. Can be seen as $\mu_0\pi Fs$ in toon.
    alb_surf:
        Shape: **(Nlev,)**.
    flux_at_level:

    Returns
    -------

        $F_{up}$: np.ndarray
            Upper flux at the bottom of the Nlay layers.
            Shape: **(Nlev+1,)=(Nlay,)**.

        $F_{dw}$: np.ndarray
            Down flux at the bottom of the Nlay layers.
            Shape: **(Nlev+1,)=(Nlay,)**.

        $F_{net}$: np.ndarray
            Net flux at the bottom of the Nlay layers.
            Shape: **(Nlev+1,)=(Nlay,)**.

        $4\pi J_n$: np.ndarray
            J4pi at the bottom of the Nlay layers.
            Take into account the contribution from the incident flux.
            Shape: **(Nlev+1,)=(Nlay,)**.
    """
    e_1, e_2, e_3, e_4 = e_i_toon(dtau, gamma_1, gamma_2)

    c_up_top = np.zeros_like(dtau)
    c_dw_top = np.zeros_like(dtau)
    c_up_bot = np.zeros_like(dtau)
    c_dw_bot = np.zeros_like(dtau)

    c_up_top_planck, c_dw_top_planck, c_up_bot_planck, c_dw_bot_planck = c_planck(source, dtau, gamma_1, gamma_2)

    # Take into account the bb source term
    c_up_top += c_up_top_planck
    c_dw_top += c_dw_top_planck
    c_up_bot += c_up_bot_planck
    c_dw_bot += c_dw_bot_planck

    source_surface = (1. - alb_surf) * source[-1]
    r"""
        $S_{sfc}$, where $S_{sfc}$ is `alb_surf` and $\varepsilon$ is `1 - alb_surf`.
    """

    # We now add the contribution from the stellar source.
    if flux_collimated_top_dw is not None:
        c_up_top_star, c_dw_top_star, c_up_bot_star, c_dw_bot_star = c_star(flux_collimated_top_dw, taucum, dtau,
                                                                            gamma_1, gamma_2, gamma_3, gamma_4, omega_0,
                                                                            mu_star)
        # Take into account the stellar flux as a source term
        c_up_top += c_up_top_star
        c_dw_top += c_dw_top_star
        c_up_bot += c_up_bot_star
        c_dw_bot += c_dw_bot_star

        # Update source_surface to take into account the stellar flux
        source_surface += alb_surf * flux_collimated_top_dw * np.exp(- taucum[-1] / mu_star)

    A = np.zeros((2 * Nlev))
    B = np.zeros((2 * Nlev))
    D = np.zeros((2 * Nlev))
    E = np.zeros((2 * Nlev))

    # upper boundary
    A[0] = 0.
    B[0] = e_1[0]
    D[0] = -e_2[0]
    E[0] = flux_diffuse_top_dw - c_dw_top[0]

    # even in Toon indexing. (remember python arrays start at 0.)
    A[1:-1:2] = e_1[:-1] * e_2[1:] - e_3[:-1] * e_4[1:]
    B[1:-1:2] = e_2[:-1] * e_2[1:] - e_4[:-1] * e_4[1:]
    D[1:-1:2] = e_1[1:] * e_4[1:] - e_2[1:] * e_3[1:]
    E[1:-1:2] = (c_up_top[1:] - c_up_bot[:-1]) * e_2[1:] - (c_dw_top[1:] - c_dw_bot[:-1]) * e_4[1:]

    # the middle sign above is different in my calculations and toon (+ in Toon)
    # odd
    A[2:-1:2] = e_2[:-1] * e_3[:-1] - e_4[:-1] * e_1[:-1]
    B[2:-1:2] = e_1[:-1] * e_1[1:] - e_3[:-1] * e_3[1:]
    D[2:-1:2] = e_3[:-1] * e_4[1:] - e_1[:-1] * e_2[1:]
    E[2:-1:2] = (c_up_top[1:] - c_up_bot[:-1]) * e_3[:-1] - (c_dw_top[1:] - c_dw_bot[:-1]) * e_1[:-1]

    # surface
    A[-1] = e_1[-1] - alb_surf * e_3[-1]
    B[-1] = e_2[-1] - alb_surf * e_4[-1]
    D[-1] = 0
    E[-1] = source_surface - c_up_bot[-1] + alb_surf * c_dw_bot[-1]

    Y = DTRIDGL(2 * Nlev, A, B, D, E)

    flux_net = np.zeros((Nlev + 1))
    J4pimu = np.zeros((Nlev + 1))

    if flux_at_level is True:
        c_up_mid, c_dw_mid = c_planck_mid(source, dtau, gamma_1, gamma_2)

        # Recompute the stellar source term at mid layer
        if flux_collimated_top_dw is not None:
            c_up_mid_star, c_dw_mid_star = c_star_mid(flux_collimated_top_dw, taucum, dtau, gamma_1, gamma_2, gamma_3,
                                                      gamma_4, omega_0, mu_star)

            c_up_mid += c_up_mid_star
            c_dw_mid += c_dw_mid_star

        mid_factor1, mid_factor2 = mid_factor_toon(dtau, gamma_1, gamma_2)

        flux_net[1:] = Y[1::2] * mid_factor2 + c_up_mid - c_dw_mid
        J4pimu[1:] = Y[::2] * mid_factor1 + c_up_mid + c_dw_mid

        # flux_net[-1] = Y[-2]*(e_1[-1]-e_3[-1])+Y[-1]*(e_2[-1]-e_4[-1])+c_up_bot[-1]-c_dw_bot[-1]
        # J4pimu[-1]   = Y[-2]*(e_1[-1]+e_3[-1])+Y[-1]*(e_2[-1]+e_4[-1])+c_up_bot[-1]+c_dw_bot[-1]
    else:
        flux_net[1:] = Y[::2] * (e_1 - e_3) + Y[1::2] * (e_2 - e_4) + c_up_bot - c_dw_bot
        J4pimu[1:] = Y[::2] * (e_1 + e_3) + Y[1::2] * (e_2 + e_4) + c_up_bot + c_dw_bot

    # ?
    flux_net_top = Y[0] * e_3[0] - Y[1] * e_4[0] + c_up_top[0]
    J4pimu[0] = flux_net_top + flux_diffuse_top_dw
    flux_net[0] = flux_net_top - flux_diffuse_top_dw

    # We compute the `stellar_source` contribution.
    direct = np.zeros_like(taucum)

    if flux_collimated_top_dw is not None:
        if flux_at_level is True:
            direct[0] = flux_collimated_top_dw
            direct[1:-1] = flux_collimated_top_dw * np.exp(- (taucum[0:-2] + .5 * dtau[:-1]) / mu_star)
            direct[-1] = flux_collimated_top_dw * np.exp(- (taucum[-1]) / mu_star)
        else:
            direct: np.ndarray = flux_collimated_top_dw * np.exp(- taucum / mu_star)

    # Compute the up/down fluxes without taking account the `stellar_source` contribution.
    # This match the default behavior.

    flux_up = .5 * (J4pimu + flux_net)
    flux_dw = .5 * (J4pimu - flux_net)
    J4pi = J4pimu / mu0

    if flux_collimated_top_dw is not None:
        J4pi += direct / mu_star
        flux_net -= direct

        flux_dw += direct

    return flux_up, flux_dw, flux_net, J4pi


@numba.jit(nopython=True, fastmath=True, cache=True)
def DTRIDGL(L: int, AF: np.ndarray, BF: np.ndarray, CF: np.ndarray, DF: np.ndarray) -> np.ndarray:
    """
    DIMENSION AF(L),BF(L),CF(L),DF(L),XK(L).

    DIMENSION AS(2*L),DS(2*L)

    !*    THIS SUBROUTINE SOLVES A SYSTEM OF TRIDIAGIONAL MATRIX
    !*    EQUATIONS. THE FORM OF THE EQUATIONS ARE:
    !*    A(I)*X(I-1) + B(I)*X(I) + C(I)*X(I+1) = D(I)
    !======================================================================!

    Parameters
    ----------
    L :
    AF :
        Shape: **(L,)**.
    BF :
        Shape: **(L,)**.
    CF :
        Shape: **(L,)**.
    DF :
        Shape: **(L,)**.

    Returns
    -------
        Y: np.ndarray
    """
    AS = np.zeros_like(AF)
    DS = np.zeros_like(AF)
    XK = np.zeros_like(AF)

    AS[-1] = AF[-1] / BF[-1]
    DS[-1] = DF[-1] / BF[-1]

    for I in range(1, L):
        X = 1. / (BF[L + 1 - I - 2] - CF[L + 1 - I - 2] * AS[L + 2 - I - 2])
        AS[L + 1 - I - 2] = AF[L + 1 - I - 2] * X
        DS[L + 1 - I - 2] = (DF[L + 1 - I - 2] - CF[L + 1 - I - 2] * DS[L + 2 - I - 2]) * X

    XK[0] = DS[0]
    for I in range(1, L):
        XKB = XK[I - 1]
        XK[I] = DS[I] - AS[I] * XKB

    return XK
