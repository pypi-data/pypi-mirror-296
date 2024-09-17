# -*- coding: utf-8 -*-
"""
@author: jeremy leconte

This module contain classes to handle the radiative properties of atmospheres.
This allows us to compute the transmission and emission spectra
of those atmospheres.

Physical properties of the atmosphere are handled in atm_profile.py.

The nomenclature for layers, levels, etc, is as follows (example with 4 layers; Nlay=4):

::

    -------------------  Model top or first level (plev[0])
    - - - - - - - - - -  First atmospheric layer (play[0]=plev[0], tlay[0], xlay[0])

    -------------------  plev[1]

    - - - - - - - - - -  play[1], tlay[1], xlay[1]

    -------------------  plev[2]

    - - - - - - - - - - play[2], tlay[2], xlay[2]

    -------------------  plev[3]

    - - - - - - - - - -  bottom layer (play[Nlay-1]=psurf, tlay[3], xlay[3])
    ------------------- Surface (plev[Nlev-1=Nlay]=psurf)
    ///////////////////

.. image:: /images/atm_schema.png


Temperatures (`tlay`) and volume mixing ratios (`xlay`) are provided at the
*mid layer* point (`play`) (Note that this does not mean
that this point is the middle of the layer, in general, it is not).

If pressure levels are not specified by the user with `logplevel`,
they are at the mid point between
the pressure of the layers directly above and below. The pressure of the
top and bottom levels are confounded with the pressure of the
top and bottom mid layer points.

For radiative calculations, the source function (temperature) needs to be known at
the boundaries of the *radiative* layers but the opacity needs to be known
inside the *radiative* layer.
For this reason, there are `Nlay-1` radiative layers and they are offset
with respect to atmospheric layers.
Opacities are computed at the center of those radiative layers, i.e. at the pressure levels.
The temperature is interpolated at these levels with an arithmetic average.
Volume mixing ratios are interpolated using a geometric average. 

"""
import functools
import numbers
import warnings
from typing import Callable, Literal, Optional, Tuple, Union

import numpy as np

from .adatabase import Adatabase
from .atm_profile import Atm_profile
from .ciadatabase import CIAdatabase
from .kdatabase import Kdatabase
from .two_stream import two_stream_toon as toon  # noqa; noqa
from .util.cst import PI
from .util.interp import gauss_legendre
from .util.radiation import (Bnu, Bnu_integral_array, Bnu_integral_num, path_integral_corrk, path_integral_xsec,
                             rad_prop_corrk, rad_prop_xsec, )
from .util.spectrum import Spectrum


class Atm(Atm_profile):
    """Class based on Atm_profile that handles radiative transfer calculations.

    Radiative data are accessed through the :any:`gas_mix.Gas_mix` class.
    """

    def __init__(self, k_database=None, cia_database=None, a_database=None,
                 wn_range=None, wl_range=None, internal_flux: float = 0., rayleigh: bool = False,
                 flux_top_dw: float = 0., Tstar: Optional[float] = 5570,
                 albedo_surf: float = 0., wn_albedo_cutoff=5000.,
                 **kwargs):
        """Initialization method that calls Atm_Profile().__init__(**kwargs) and links
        to Kdatabase and other radiative data. 
        """
        super().__init__(**kwargs)
        self.known_spectral_axis = False

        # Track number of call.
        # INFO: Clean them up
        self.number_computation_albedo_surf_nu: int = 0
        self.number_computation_flux_top_dw_nu: int = 0

        self.set_k_database(k_database)
        self.set_cia_database(cia_database)
        self.set_a_database(a_database)
        self.set_spectral_range(wn_range=wn_range, wl_range=wl_range)
        self.set_internal_flux(internal_flux)

        self.compute_flux_top_dw_nu = True
        self.Tstar: Optional[float] = None
        self.stellar_spectrum: Optional[Spectrum] = None

        self.set_incoming_stellar_flux(flux_top_dw=flux_top_dw, Tstar=Tstar, **kwargs)

        self.compute_albedo_surf_nu = True
        self.set_surface_albedo(albedo_surf=albedo_surf,
                                wn_albedo_cutoff=wn_albedo_cutoff)
        self.set_rayleigh(rayleigh=rayleigh)
        self.flux_net_nu = None
        self.kernel = None

    def set_k_database(self, k_database: Optional[Kdatabase] = None):
        """Change the radiative database used by the
        :class:`Gas_mix` object handling opacities inside
        :class:`Atm`.

        See :any:`gas_mix.Gas_mix.set_k_database` for details.

        Parameters
        ----------
            k_database: :class:`Kdatabase` object
                New Kdatabase to use.
        """
        self.gas_mix.set_k_database(k_database=k_database)
        self.k_database = self.gas_mix.k_database
        self.Ng = self.gas_mix.Ng
        # to know whether we are dealing with corr-k or not and access some attributes. 

        if self.k_database is not None:
            # self.Nw = self.k_database.Nw
            # self.wnedges = self.k_database.wnedges
            # self.wns = self.k_database.wns
            # self.dwnedges = np.diff(self.wnedges)
            self.compute_albedo_surf_nu = True
            self.number_computation_albedo_surf_nu = 0
            self.compute_flux_top_dw_nu = True
            self.number_computation_flux_top_dw_nu = 0
            self.known_spectral_axis = False

    def set_cia_database(self, cia_database: Optional[CIAdatabase] = None):
        """Change the CIA database used by the
        :class:`Gas_mix` object handling opacities inside
        :class:`Atm`.

        See :any:`gas_mix.Gas_mix.set_cia_database` for details.

        Parameters
        ----------
            cia_database: :class:`CIAdatabase` object
                New CIAdatabase to use.
        """
        self.gas_mix.set_cia_database(cia_database=cia_database)

    def set_a_database(self, a_database: Optional[Adatabase] = None):
        """Change the Aerosol database used by the
        :class:`Aerosols` object handling aerosol optical properties.

        See :any:`aerosols.Aerosols.set_a_database` for details.

        Parameters
        ----------
            a_database: :class:`Adatabase` object
                New Adatabase to use.
        """
        self.aerosols.set_a_database(a_database=a_database)

    def set_spectral_range(self,
                           wn_range: Optional[Tuple[float, float]] = None,
                           wl_range: Optional[Tuple[float, float]] = None):
        """Sets the spectral range in which computations will be done by specifying
        either the wavenumber (in cm^-1) or the wavelength (in micron) range.

        See :any:`gas_mix.Gas_mix.set_spectral_range` for details.
        """
        self.gas_mix.set_spectral_range(wn_range=wn_range, wl_range=wl_range)
        self.compute_albedo_surf_nu = True
        self.compute_flux_top_dw_nu = True
        self.known_spectral_axis = False

    def set_incoming_stellar_flux(self, flux_top_dw: Optional[float] = None, Tstar: Optional[float] = None,
                                  stellar_spectrum: Optional[Spectrum] = None, **kwargs):
        """Sets the stellar incoming flux integrated in each wavenumber
        channel.

        .. important::
            The normalization is such that the flux input is exactly
            flux_top_dw whatever the spectral range used.

        Parameters
        ----------
            flux_top_dw:
                Bolometric Incoming flux (in W/m^2).
            Tstar:
                Stellar temperature (in K) used to compute the spectral distribution
                of incoming flux using a blackbody.
            stellar_spectrum:
                Spectrum of the star in units of per wavenumber. The specific units do not matter as
                the overall flux will be renormalized.
        """
        if flux_top_dw is not None:
            self.flux_top_dw = flux_top_dw
            self.compute_flux_top_dw_nu = True

        if (Tstar is not None) and (stellar_spectrum is not None):
            raise ValueError('`Tstar` and `stellar_spectrum` are both used to set the incoming flux. Choose one!')

        # If `Tstar` xor `stellar_spectrum` is set, set the value, erasing the other.
        # If `Tstar` and `stellar_spectrum` are  both `None`, we use the value already store in the object.
        if Tstar is not None:
            self.Tstar = Tstar
            self.stellar_spectrum = None
            self.compute_flux_top_dw_nu = True

        if stellar_spectrum is not None:
            self.stellar_spectrum = stellar_spectrum
            self.Tstar = None
            self.compute_flux_top_dw_nu = True

        # If we are able to compute the spectrum, compute it.
        if self.compute_flux_top_dw_nu is True and self.known_spectral_axis is True:
            if self.stellar_spectrum is not None:
                binned_spec = self.stellar_spectrum.bin_down_cp(self.wnedges)
                self.flux_top_dw_nu = binned_spec.value
                factor = self.flux_top_dw / binned_spec.total
            elif self.Tstar is not None:
                self.flux_top_dw_nu = Bnu_integral_num(self.wnedges, self.Tstar)
                factor = self.flux_top_dw / (np.sum(self.flux_top_dw_nu) * self.dwnedges)
            else:
                raise RuntimeError('Something went wrong, Tstar and stellar_spectrum cannot be both None')

            self.flux_top_dw_nu = self.flux_top_dw_nu * factor
            self.compute_flux_top_dw_nu = False
            self.number_computation_flux_top_dw_nu += 1

    @property
    def spectral_incoming_flux(self):
        """Returns a :class:`Spectrum` object with the value of the incoming stellar flux at the top
        of atmosphere. 
        """
        return Spectrum(value=self.flux_top_dw_nu, wns=self.wns, wnedges=self.wnedges)

    def set_internal_flux(self, internal_flux: float) -> None:
        """Sets internal flux from the subsurface in W/m^2
        """
        self.internal_flux: float = internal_flux

    def set_surface_albedo(self, albedo_surf: Union[float, np.ndarray, None] = None,
                           wn_albedo_cutoff: Optional[float] = None,
                           **kwargs):
        """Sets the value of the mean surface albedo using an heaviside filter.
        
        Parameters
        ----------
            albedo_surf:
                Effective visible surface albedo.
                If `albedo_surf` is an array, we suppose that the albedo is already in the form for `albedo_surf_nu`.

            wn_albedo_cutoff :
                wavenumber value in cm-1 dividing the visible range from the IR range, 
                where the albedo goes from a given value 'albedo_surf' to 0.
        """
        if albedo_surf is not None:
            self.albedo_surf = albedo_surf
            self.compute_albedo_surf_nu = True

        if wn_albedo_cutoff is not None:
            self.wn_albedo_cutoff = wn_albedo_cutoff
            self.compute_albedo_surf_nu = True

        if self.compute_albedo_surf_nu is True and self.known_spectral_axis is True:
            self._setup_albedo_surf_nu()
            self.compute_albedo_surf_nu = False
            self.number_computation_albedo_surf_nu += 1

    def _setup_albedo_surf_nu(self):
        """Compute the value of the mean surface albedo for each wavenumber in an array.
        If the albedo value is modified, this method needs to be called again.
        For now, only available with wavenumbers
        """

        if isinstance(self.albedo_surf, numbers.Number):
            self.albedo_surf_nu = np.where(self.wns >= self.wn_albedo_cutoff, self.albedo_surf, 0.)
        elif isinstance(self.albedo_surf, np.ndarray):
            if self.wns.shape != self.albedo_surf.shape:
                raise ValueError('Mismatching shape.')
            self.albedo_surf_nu = self.albedo_surf
        else:
            raise ValueError

    def set_rayleigh(self, rayleigh:bool = False):
        """Sets whether or not Rayleigh scattering is included."""
        self.rayleigh: bool = rayleigh

    def spectral_integration(self, spectral_var: np.ndarray) -> np.ndarray:
        """Spectrally integrate an array, taking care of whether
        we are dealing with corr-k or xsec data.

        Parameters
        ----------
            spectral_var:
                array to integrate

        Returns
        -------
            var: np.ndarray
                array integrated over wavenumber (and g-space if relevant)
        """

        return np.sum(self.g_integration(spectral_var) * self.dwnedges, axis=-1)
    
    def interpolate_atm_profile(self, logplay, Mgas=None, gas_vmr=None, **kwargs):
        """Re interpolates the current profile on a new log pressure grid.
        Recomputes the radiative kernel on the new grid. 

        See Atm_profile.interpolate_profile for details and options

        Parameters
        ----------
            logplay: array
                New log pressure grid
        """
        self.interpolate_profile(logplay, **kwargs) 
        H, net = self.heating_rate(compute_kernel=True, Mgas=Mgas,
                gas_vmr=gas_vmr, **kwargs)        

    def g_integration(self, spectral_var):
        """Integrate an array along the g direction (only for corrk)

        Parameters
        ----------
            spectral_var:
                array to integrate

        Returns
        -------
            var: array, np.ndarray
                array integrated over g-space if relevant
        """
        if self.Ng is None or spectral_var.shape[-1] != self.Ng:
            # INFO: Should var be a copy, like the second case
            var = spectral_var
        else:
            var = np.sum(spectral_var * self.k_database.weights, axis=-1)

        return var

    def opacity(self, rayleigh: Optional[bool] = None, compute_all_opt_prop: bool = False,
                wn_range: Optional[Tuple[float, float]] = None, wl_range: Optional[Tuple[float, float]] = None,
                **kwargs):
        """Computes the opacity of each of the radiative layers (m^2/molecule).

        Parameters
        ----------
            rayleigh:
                If true, the rayleigh cross section is computed in
                self.kdata_scat and added to kdata(total extinction cross section)
                If None, the global attribute self.rayleigh is used.
            compute_all_opt_prop:
            wn_range, wl_range:

        See :any:`gas_mix.Gas_mix.cross_section` for details.
        """
        if rayleigh is None:
            local_rayleigh = self.rayleigh
        else:
            local_rayleigh = rayleigh

        self.kdata = self.gas_mix.cross_section(rayleigh=local_rayleigh,
                                                wn_range=wn_range, wl_range=wl_range, **kwargs)
        shape = self.kdata.shape

        if (wn_range is not None) or (wl_range is not None):
            self.compute_albedo_surf_nu = True
            self.compute_flux_top_dw_nu = True
            self.known_spectral_axis = False

        if self.aerosols.adatabase is not None:
            [kdata_aer, k_scat_aer, g_aer] = self.aerosols.optical_properties(
                    compute_all_opt_prop=compute_all_opt_prop,
                    wn_range=wn_range, wl_range=wl_range, **kwargs)
            if self.Ng is None:
                self.kdata += kdata_aer
            else:
                self.kdata += kdata_aer[:, :, None]
        if compute_all_opt_prop:
            if local_rayleigh:
                kdata_scat_tot = self.gas_mix.kdata_scat
            else:
                kdata_scat_tot = np.zeros(shape[0:2], dtype=float)

            if self.aerosols.adatabase is not None:
                kdata_scat_tot += k_scat_aer
                self.asym_param = np.where(kdata_scat_tot<=0., 0., k_scat_aer * g_aer / kdata_scat_tot)
                #JL23 the line above can be replaced by the lines below to avoid a warning message about
                # division by zero as np.where evaluates both values no matter what
                # this however can lea to some dimensions issues with rayleigh
                #mask = (kdata_scat_tot<=0.)
                #print(mask.shape, k_scat_aer.shape, g_aer.shape, kdata_scat_tot.shape)
                #self.asym_param = np.empty_like(kdata_scat_tot)
                #self.asym_param[mask] = 0.
                #self.asym_param[~mask] = k_scat_aer[~mask] * g_aer[~mask] / kdata_scat_tot[~mask]
            else:
                self.asym_param = np.zeros(shape[0:2], dtype=float)

            if self.Ng is None:
                self.single_scat_albedo = kdata_scat_tot / self.kdata
            else:
                self.single_scat_albedo = kdata_scat_tot[:, :, None] / self.kdata
                self.asym_param = self.asym_param[:, :, None] * np.ones(self.Ng)
                # JL21 the line above could be removed as asym param does not seem to change
                # with g point, but then the dimensions should be change in 2stream routines.

            self.single_scat_albedo=np.core.umath.minimum(self.single_scat_albedo,0.9999999999)

        self.Nw = self.gas_mix.Nw
        self.wns = self.gas_mix.wns
        self.wnedges = self.gas_mix.wnedges
        self.dwnedges = self.gas_mix.dwnedges
        self.known_spectral_axis = True

    def source_function(self, integral: bool = True, source: bool = True) -> np.ndarray:
        r"""
        Compute the blackbody source function (Pi*Bnu) for each layer of the atmosphere.

        Parameters
        ----------
            integral:
                * If true, the black body is integrated within each wavenumber bin.
                * If not, only the central value is used.
                  False is faster and should be ok for small bins,
                  but True is the correct version. 
            source:
                If False, the source function is put to 0 (for solar absorption calculations)
        Returns
        -------
        $\pi B_\nu$ : np.ndarray
            Blackbody source function.

        """
        if source is False:
            return np.zeros((self.Nlay, self.Nw))

        if integral is False:
            return PI * Bnu(self.wns[None, :], self.tlay[:, None])

        # JL2020 What is below is slightly faster for very large resolutions
        # piBatm=np.empty((self.Nlay,self.Nw))
        # for ii in range(self.Nlay):
        #    piBatm[ii]=PI*Bnu_integral_num(self.wnedges,self.tlay[ii])/dw
        # JL2020 What is below is much faster for moderate to low resolutions

        return PI * Bnu_integral_array(self.wnedges, self.tlay, self.Nw, self.Nlay) / self.dwnedges

    def setup_emission_caculation(self, mu_eff: float = 0.5, rayleigh: Optional[bool] = None, integral: bool = True,
                                  source: bool = True, gas_vmr=None, Mgas=None, aer_reffs_densities=None, **kwargs):
        """Computes all necessary quantities for emission calculations
        (opacity, source, etc.)
        """
        if gas_vmr is not None:
            self.set_gas(gas_vmr, Mgas=Mgas)

        if aer_reffs_densities is not None:
            self.aerosols.set_aer_reffs_densities(aer_reffs_densities=aer_reffs_densities)

        self.opacity(rayleigh=rayleigh, **kwargs)
        self.set_surface_albedo(**kwargs)
        self.set_incoming_stellar_flux(**kwargs)
        self.piBatm = self.source_function(integral=integral, source=source)
        self.compute_layer_col_density()

        if self.Ng is None:
            self.tau, self.dtau = rad_prop_xsec(self.dcol_density_rad,
                                                self.kdata, mu_eff)
        else:
            self.tau, self.dtau = rad_prop_corrk(self.dcol_density_rad,
                                                 self.kdata, mu_eff)
            self.weights = self.k_database.weights

    def emission_spectrum(self, integral=True, mu0=0.5, mu_quad_order=None,
                          dtau_min=1.e-13, **kwargs):
        """Returns the emission flux at the top of the atmosphere (in W/m^2/cm^-1)

        Parameters
        ----------
            integral: boolean, optional
                * If true, the black body is integrated within each wavenumber bin.
                * If not, only the central value is used.
                  False is faster and should be ok for small bins,
                  but True is the correct version. 

        Other Parameters
        ----------------
            mu0: float
                Cosine of the quadrature angle use to compute output flux
            mu_quad_order: int
                If an integer is given, the emission intensity is computed
                for a number of angles and integrated following a gauss legendre
                quadrature rule of order `mu_quad_order`.
            dtau_min: float
                If the optical depth in a layer is smaller than dtau_min,
                dtau_min is used in that layer instead. Important as too
                transparent layers can cause important numerical rounding errors.

        Returns
        -------
            Spectrum object 
                A spectrum with the Spectral flux at the top of the atmosphere (in W/m^2/cm^-1)
        """
        if mu_quad_order is not None:
            # if we want quadrature, use the more general method.
            return self.emission_spectrum_quad(integral=integral,
                                               mu_quad_order=mu_quad_order, dtau_min=dtau_min, **kwargs)

        try:
            self.setup_emission_caculation(mu_eff=mu0, rayleigh=False, integral=integral, **kwargs)
        except TypeError:
            raise RuntimeError("""
            Cannot use rayleigh option with emission_spectrum.
            If you meant to include scattering, you should use emission_spectrum_2stream.
            """)
        # self.tau and self.dtau include the 1/mu0 factor.
        expdtau = np.exp(-self.dtau)
        expdtauminone = np.where(self.dtau < dtau_min, -self.dtau, expdtau - 1.)
        # careful: due to numerical limitations, 
        # the limited development of Exp(-dtau)-1 needs to be used for small values of dtau
        exptau = np.exp(-self.tau)
        if self.Ng is None:
            timesBatmTop = (1. + expdtauminone / self.dtau) * exptau[:-1]
            timesBatmBottom = (-expdtau - expdtauminone / self.dtau) * exptau[:-1]
            timesBatmBottom[-1] += exptau[-1]
        else:
            timesBatmTop = np.sum((1. + expdtauminone / self.dtau) * exptau[:-1] * self.weights, axis=-1)
            timesBatmBottom = np.sum((-expdtau - expdtauminone / self.dtau) * exptau[:-1] \
                                     * self.weights, axis=-1)
            timesBatmBottom[-1] += np.sum(exptau[-1] * self.weights, axis=-1)
        IpTop = np.sum(self.piBatm[:-1] * timesBatmTop + self.piBatm[1:] * timesBatmBottom, axis=0)

        return Spectrum(IpTop, self.wns, self.wnedges)

    def emission_spectrum_quad(self, integral=True, mu_quad_order=3, dtau_min=1.e-13, **kwargs):
        """Returns the emission flux at the top of the atmosphere (in W/m^2/cm^-1)
        using gauss legendre qudrature of order `mu_quad_order`

        Parameters
        ----------
            integral: boolean, optional
                * If true, the black body is integrated within each wavenumber bin.
                * If not, only the central value is used.
                  False is faster and should be ok for small bins,
                  but True is the correct version. 
            dtau_min: float
                If the optical depth in a layer is smaller than dtau_min,
                dtau_min is used in that layer instead. Important as too
                transparent layers can cause important numerical rounding errors.
                  
        Returns
        -------
            Spectrum object 
                A spectrum with the Spectral flux at the top of the atmosphere (in W/m^2/cm^-1)
        """
        self.setup_emission_caculation(mu_eff=1., rayleigh=False, integral=integral, **kwargs)
        # angle effect dealt with later

        IpTop = np.zeros(self.kdata.shape[1])
        mu_w, mu_a, _ = gauss_legendre(mu_quad_order)
        mu_w = mu_w * mu_a * 2.  # takes care of the mu factor in last integral => int(mu I d mu)
        # Factor 2 takes care of the fact that the source function is pi*Batm
        # but we want 2*Pi*Batm
        for ii, mu0 in enumerate(mu_a):
            tau = self.tau / mu0
            dtau = self.dtau / mu0
            expdtau = np.exp(-dtau)
            expdtauminone = np.where(dtau < dtau_min, -dtau, expdtau - 1.)
            exptau = np.exp(-tau)
            if self.Ng is None:
                timesBatmTop = (1. + expdtauminone / dtau) * exptau[:-1]
                timesBatmBottom = (-expdtau - expdtauminone / dtau) * exptau[:-1]
                timesBatmBottom[-1] += exptau[-1]
            else:
                timesBatmTop = np.sum((1. + expdtauminone / dtau) * exptau[:-1] \
                                      * self.weights, axis=-1)
                timesBatmBottom = np.sum((-expdtau - expdtauminone / dtau) * exptau[:-1] \
                                         * self.weights, axis=-1)
                timesBatmBottom[-1] += np.sum(exptau[-1] * self.weights, axis=-1)
            IpTop += np.sum(self.piBatm[:-1] * timesBatmTop + self.piBatm[1:] * timesBatmBottom, axis=0) \
                     * mu_w[ii]

        return Spectrum(IpTop, self.wns, self.wnedges)

    def emission_spectrum_2stream(self, integral: bool = True, mu0: float = 0.5,
                                  method: Literal['toon'] = 'toon',
                                  dtau_min: float = 1.e-10, flux_at_level: bool = False,
                                  rayleigh: Optional[bool] = None, source: bool = True, compute_kernel: bool = False,
                                  flux_top_dw: Optional[float] = None, mu_star: Optional[float] = None,
                                  stellar_mode: Literal['diffusive', 'collimated'] = 'diffusive',
                                  **kwargs) -> Spectrum:
        r"""
        Returns the emission flux at the top of the atmosphere (in W/m^2/cm^-1)

        Parameters
        ----------
            integral :
                * If True, the source function (black body)
                  is integrated within each wavenumber bin.
                * If False, only the central value is used.
                  False is faster and should be ok for small bins
                  (e.g. used with `Xtable`),
                  but True is the most accurate mode. 
            rayleigh :
                Whether to account for rayleigh scattering or not. 
                If None, the global attribute self.rayleigh is used.

        Other Parameters
        ----------------
        mu0:
            Cosine of the quadrature angle used to compute output flux
        flux_top_dw:
            (W/m^2) allows you to specify the stellar flux impinging on the top of the atmosphere.
            (Used to rescale the stellar spectrum).
        stellar_mode:
            When `flux_top_dw` is provided, set the method to be used to take it into account.

            - ``diffusive``: Incoming diffuse flux at the upper boundary.
            - ``collimated``: Incoming diffuse flux is treated as a source term.
        mu_star:
            $\mu_*$ is the incident direction of the solar beam. Used when the incoming diffuse flux is treated as a
            source term.
        dtau_min:
            If the optical depth in a layer is smaller than dtau_min,
            dtau_min is used in that layer instead. Important as too
            transparent layers can cause important numerical rounding errors.
        flux_at_level:
            Whether the fluxes are computed at the levels (True) or
            in the middle of the layers (False). e.g. this needs to
            be True to be able to use the kernel with the evolution model.
        source:
            Whether to include the self emission of the gas in the computation.
        compute_kernel:
            Whether we want to recompute the kernel of the heating rates along
            with the fluxes.
        method:
            What method to use to compute the 2 stream fluxes.

            - 'toon' (default) uses Toon et al. (1989).

        Returns
        -------
            Spectrum object :
                A spectrum with the Spectral flux at the top of the atmosphere (in W/m^2/cm^-1)
        """

        self.setup_emission_caculation(mu_eff=1., rayleigh=rayleigh, integral=integral,
                                       source=source, flux_top_dw=flux_top_dw, compute_all_opt_prop=True, **kwargs)
        # mu_eff=1. because the mu effect is taken into account in solve_2stream_nu
        # we must compute the vertical optical depth here.
        # JL21: shouldn't we remove flux_top_dw, it seems not to be used.

        # Enforce `dtau_min`.
        self.single_scat_albedo = np.where(self.dtau < dtau_min, 0., self.single_scat_albedo)
        self.dtau = np.clip(self.dtau, dtau_min, None, out=self.dtau)  # Clipping is done inplace using `out=self.dtau`.
        self.tau[1:] = np.cumsum(self.dtau, axis=0,
                                 out=self.tau[1:])  # Cumsum is done inplace using `out=self.tau[1:]`.

        module_to_use = globals()[method]
        # globals()[method] converts the method string into a module name
        #  if the module has been loaded

        if self.Ng is None:
            solve_2stream_nu = module_to_use.solve_2stream_nu_xsec
        else:
            solve_2stream_nu = module_to_use.solve_2stream_nu_corrk

        if stellar_mode == 'diffusive' and mu_star is not None:
            warnings.warn(f'{mu_star=:.2f} not valid when {stellar_mode=}. (should be `None`)', UserWarning)

        # When in collimated mode, ensure that if `flux_top_dw` is not None, `mu_star` is valid.
        # If `flux_top_dw` is `None`, no need to be that strict.
        if stellar_mode == 'collimated' and (mu_star is None or not 0. < mu_star <= 1.):
            raise ValueError(f'{mu_star=} is not valid when {stellar_mode=}.')

        # We need to call `solve_2stream_nu` in this function but also in `_compute_kernel`.
        # `_compute_kernel` make change  only to the parameter `source_nu`.
        # To tie better both function, the following allow us to instantiate a temporary
        # function named `solve_2stream_specialized` depending only on `source_nu`.
        # Callable[ [np.ndarray], tuple[...]]: this is a typehint of what `solve_2stream` is.
        # Something that we can call, ie a `Callable` with the following input-output: [< input  > , < output >].
        #
        # Next the use of `functools.partial` allow to set some of the parameters of `solve_2stream_nu`.
        solve_2stream_specialized: Callable[[np.ndarray], tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = \
            functools.partial(solve_2stream_nu, tau_nu=self.tau, dtau_nu=self.dtau,
                              omega0_nu=self.single_scat_albedo, g_asym_nu=self.asym_param,
                              flux_top_dw_nu=self.flux_top_dw_nu, alb_surf_nu=self.albedo_surf_nu,
                              mu0=mu0, flux_at_level=flux_at_level,
                              mu_star=mu_star, stellar_mode=stellar_mode)

        # Solve 2-stream and expand values.
        self.flux_up_nu, self.flux_down_nu, self.flux_net_nu, self.J4pi = solve_2stream_specialized(self.piBatm)

        if compute_kernel is True:
            self._compute_kernel(solve_2stream_specialized, per_unit_mass=True, integral=True, **kwargs)

        if self.Ng is None:
            return Spectrum(self.flux_up_nu[0], self.wns, self.wnedges)
        else:
            return Spectrum(np.sum(self.flux_up_nu[0] * self.weights, axis=1), self.wns, self.wnedges)

    def _compute_kernel(self,
                        solve_2stream_specialized: Callable[
                            [np.ndarray], Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]],
                        epsilon: float = 0.01, per_unit_mass: bool = True, integral: bool = True,
                        **kwargs):
        """Computes the Jacobian matrix d Heating[lay=i] / d T[lay=j]

        The user should not call this method directly.
        To recompute the kernel, call `emission_spectrum_2stream` with the option `compute_kernel=True`.

        After the computation, the kernel is stored in `self.kernel` and the temperature array at which the kernel
        has been computed in `self.tlay_kernel`.

        Parameters
        ----------
            solve_2stream_specialized:
                Name of the function that will be used to compute the fluxes.
                `emission_spectrum_2stream` will create a lambda function that take care of specifying all arguments
                leaving `source_nu` to be specified.
            epsilon:
                The temperature increment used to compute the derivative will be `epsilon*self.tlay`
            per_unit_mass:
                Whether the heating rates will be normalized per unit of mass (i.e. the kernel values will have units
                of W/kg/K).
                If False, kernel in W/layer/K.
            integral:
                Whether the integral mode is used in flux computations. e.g. this needs to be `True` to be able to
                use the kernel with the evolution model.
        """

        net = self.spectral_integration(self.flux_net_nu)
        self.kernel = np.empty((self.Nlay, self.Nlay))

        self.piBatm = self.source_function(integral=integral)
        tlay = self.tlay

        dT = epsilon * tlay
        self.tlay = tlay + dT
        newpiBatm = self.source_function(integral=integral)

        pibatm = np.copy(self.piBatm)
        for ilay in range(self.Nlay):
            # Update the temperature one layer at a time.
            pibatm[ilay] = newpiBatm[ilay]  # Update current layer

            _, _, flux_net_tmp, _ = solve_2stream_specialized(pibatm)

            net_tmp = self.spectral_integration(flux_net_tmp)
            self.kernel[ilay] = (net - net_tmp) / dT[ilay]

            pibatm[ilay] = self.piBatm[ilay]  # Restore the actual temperature

        # Ensure temperature have been restored
        assert np.allclose(pibatm, self.piBatm)

        self.kernel[:, :-1] -= self.kernel[:, 1:]
        self.tlay = tlay
        self.tlay_kernel = self.tlay

        if per_unit_mass:
            self.kernel *= self.inv_dmass

    def flux_divergence(self, per_unit_mass: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """Computes the divergence of the net flux in the layers
        (used to compute heating rates).

        :func:`emission_spectrum_2stream` needs to be run first.

        Parameters
        ----------
            per_unit_mass:
                If True, the heating rates are normalized by the
                mass of each layer (result in W/kg).

        Returns
        -------
            H: np.ndarray
                Heating rate in each layer (Difference of the net fluxes). Positive means heating.
                The last value is the net flux impinging on the surface + the internal flux.
            net: np.ndarray
                Net fluxes at level surfaces
        """
        if self.flux_net_nu is None:
            raise RuntimeError('Should have ran `emission_spectrum_2stream`.')

        net = self.spectral_integration(self.flux_net_nu)

        H = -np.copy(net)
        H[:-1] -= H[1:]

        # Take into account the internal flux.
        H[-1] += self.internal_flux

        if per_unit_mass is True:
            H *= self.inv_dmass

        return H, net

    def bolometric_fluxes(self, per_unit_mass: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Computes the bolometric fluxes at levels and the divergence of the net flux in the layers
        (used to compute heating rates).

        :func:`emission_spectrum_2stream` needs to be run first.

        Parameters
        ----------
            per_unit_mass:
                If True, the heating rates are normalized by the
                mass of each layer (result in W/kg).

        Returns
        -------
            up: np.ndarray
                Upward fluxes at level surfaces
            dw: np.ndarray
                Downward fluxes at level surfaces
            net: np.ndarray
                Net fluxes at level surfaces
            H: np.ndarray
                Heating rate in each layer (Difference of the net fluxes). Positive means heating.
                The last value is the net flux impinging on the surface + the internal flux.
        """
        H, net = self.flux_divergence(per_unit_mass=per_unit_mass)

        up = self.spectral_integration(self.flux_up_nu)
        dw = self.spectral_integration(self.flux_down_nu)

        return up, dw, net, H

    def heating_rate(self, compute_kernel: bool = False, per_unit_mass: bool = True,
                     dTmax_use_kernel: Optional[float] = None, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """Computes the heating rates and net fluxes in the atmosphere.

        Parameters
        ----------
            compute_kernel:
                If True, the kernel (jacobian of the heat rates) is recomputed
            per_unit_mass:
                If True, the heating rates are normalized by the
                mass of each layer (result in W/kg).
            dTmax_use_kernel:
                Maximum temperature difference between the current temperature
                and the temperature of the last kernel computation before
                a new kernel is recomputed.
            kwargs:
                Arguments to use when calling `emission_spectrum_2stream`.

        Returns
        -------
            H: np.ndarray
                Heating rate in each layer (Difference of the net fluxes). Positive means heating.
                The last value is the net flux impinging on the surface + the internal flux.
            net: np.ndarray
                Net fluxes at level surfaces
        """

        if compute_kernel is False and dTmax_use_kernel is not None:
            dT = self.tlay - self.tlay_kernel

            if np.amax(np.abs(dT)) < dTmax_use_kernel:
                try:
                    H = self.H_kernel + np.dot(dT, self.kernel)
                    net = self.internal_flux - np.cumsum((H * self.dmass)[::-1])[::-1]
                except:
                    raise RuntimeError("Kernel has not been precomputed")

                return H, net

        _ = self.emission_spectrum_2stream(compute_kernel=compute_kernel, flux_at_level=True, **kwargs)

        H, net = self.flux_divergence(per_unit_mass=per_unit_mass)

        if compute_kernel is True:
            self.H_kernel = H
            self.tau_rads = 1. / np.abs(self.kernel.diagonal())
            self.tau_rad = np.amin(self.tau_rads)

        return H, net

    def bolometric_fluxes_2band(self, flux_top_dw=None, per_unit_mass: bool = True, **kwargs):
        """Computes the bolometric fluxes at levels and heating rates using `bolometric_fluxes`.

        However, the (up, down, net) fluxes are separated in two contributions:
          - the part emitted directly by the atmosphere (_emis).
          - the part due to the incoming stellar light (_stell),
            that can be used to compute the absorbed stellar radiation and the bond_albedo.

        We also provide the associated heating rates (H in W/kg)
        """
        save_stellar_flux = np.copy(self.flux_top_dw_nu)
        self.flux_top_dw_nu = self.flux_top_dw_nu * 0.
        _ = self.emission_spectrum_2stream(flux_at_level=True, integral=True, **kwargs)
        Fup_emis, Fdw_emis, Fnet_emis, H_emis = self.bolometric_fluxes(per_unit_mass=per_unit_mass)
        self.flux_top_dw_nu = save_stellar_flux

        save_internal_flux = np.copy(self.internal_flux)
        _ = self.emission_spectrum_2stream(flux_at_level=True, integral=True,
                                           flux_top_dw=flux_top_dw, source=False, **kwargs)
        Fup_stel, Fdw_stel, Fnet_stel, H_stel = self.bolometric_fluxes(per_unit_mass=per_unit_mass)
        self.internal_flux = save_internal_flux

        return Fup_emis, Fdw_emis, Fnet_emis, H_emis, Fup_stel, Fdw_stel, Fnet_stel, H_stel

    def spectral_fluxes_2band(self, **kwargs):
        """Computes the spectral fluxes at levels.

        The (up, down, net) fluxes are separated in two contributions:
          - the part emitted directly by the atmosphere (_emis).
          - the part due to the incoming stellar light (_stell),
            that can be used to compute the absorbed stellar radiation and the bond_albedo.
        """
        save_stellar_flux = np.copy(self.flux_top_dw_nu)
        self.flux_top_dw_nu = self.flux_top_dw_nu * 0.
        _ = self.emission_spectrum_2stream(flux_at_level=True, integral=True, **kwargs)
        Fup_emis = self.g_integration(self.flux_up_nu)
        Fdw_emis = self.g_integration(self.flux_down_nu)
        Fnet_emis = self.g_integration(self.flux_net_nu)
        self.flux_top_dw_nu = save_stellar_flux

        _ = self.emission_spectrum_2stream(flux_at_level=True, integral=True, source=False, **kwargs)
        Fup_stel = self.g_integration(self.flux_up_nu)
        Fdw_stel = self.g_integration(self.flux_down_nu)
        Fnet_stel = self.g_integration(self.flux_net_nu)

        return Fup_emis, Fdw_emis, Fnet_emis, Fup_stel, Fdw_stel, Fnet_stel

    def transmittance_profile(self, **kwargs):
        """Computes the transmittance profile of an atmosphere,
        i.e. Exp(-tau) for each layer of the model.
        Real work done in the numbafied function path_integral_corrk/xsec
        depending on the type of data.
        """
        self.opacity(**kwargs)
        self.compute_tangent_path()
        self.compute_number_density()

        if self.Ng is not None:
            self.weights = self.k_database.weights
            transmittance = path_integral_corrk(
                    self.Nlay - 1, self.Nw, self.Ng, self.tangent_path, self.n_density, self.kdata, self.weights)
        else:
            transmittance = path_integral_xsec(
                    self.Nlay - 1, self.Nw, self.tangent_path, self.n_density, self.kdata)

        return transmittance

    def transmission_spectrum(self, normalized=False, Rstar=None, **kwargs):
        r"""Computes the transmission spectrum of the atmosphere.
        In general (see options below), the code returns the transit depth:

        .. math::
            \delta_\nu=(\pi R_p^2+\alpha_\nu)/(\pi R_{star}^2),

        where

        .. math::
          \alpha_\nu=2 \pi \int_0^{z_{max}} (R_p+z)*(1-e^{-\tau_\nu(z)) d z.
        
        Parameters
        ----------
            Rstar: float or astropy.unit object, optional
                Radius of the host star. If a float is specified, meters are assumed.
                Does not need to be given here if
                it has already been specified as an attribute of the :class:`Atm` object.
                If specified, the result is the transit depth:

                .. math::
                  \delta_\nu=(\pi R_p^2+\alpha_\nu)/(\pi R_{star}^2).

            normalized: boolean, optional
                Used only if self.Rstar and Rstar are None:

                * If True,
                  the result is normalized to the planetary radius:

                  .. math::
                    \delta_\nu=1+\frac{\alpha_\nu}{\pi R_p^2}.
                * If False,
                                    
                  .. math::
                    \delta_\nu=\pi R_p^2+\alpha_\nu.

        Returns
        -------
            array
                The transit spectrum (see above for normalization options).
        """
        if Rstar is not None:
            self.set_Rstar(Rstar)
        transmittance = self.transmittance_profile(**kwargs)
        self.compute_area()
        res = Spectrum((np.dot(self.area, (1. - transmittance))), self.wns, self.wnedges)
        if self.Rstar is not None:
            return (res + (PI * self.Rp ** 2)) / (PI * self.Rstar ** 2)
        elif normalized:
            return res / (PI * self.Rp ** 2) + 1
        else:
            return res + (PI * self.Rp ** 2)

    def __repr__(self):
        """Method to output header
        """
        output = super().__repr__()
        output += """
    k_database      :
        {kdatab}
    cia_database    :
        {cdatab}""".format(kdatab=self.k_database, cdatab=self.gas_mix.cia_database)
        if self.gas_mix._wn_range is not None:
            output += '    wn range        : ' + self.gas_mix._wn_range + '\n'

        return output

    def exp_minus_tau(self):
        """Sums Exp(-tau) over gauss points
        """
        weights = self.k_database.weights
        return np.sum(np.exp(-self.tau[1:]) * weights, axis=2)

    def exp_minus_tau_g(self, g_index):
        """Sums Exp(-tau) over gauss point
        """
        return np.exp(-self.tau[1:, :, g_index])

    def blackbody(self, layer_idx: int = -1, integral: bool = True) -> Spectrum:
        """Computes the surface black body flux (in W/m^2/cm^-1) for the temperature
        of layer `layer_idx`.

        Parameters
        ----------
            layer_idx:
                Index of layer used for the temperature.
            integral:
                * If true, the black body is integrated within each wavenumber bin.
                * If not, only the central value is used.
                  False is faster and should be ok for small bins,
                  but True is the correct version. 
        Returns
        -------
            Spectrum object
                Spectral flux in W/m^2/cm^-1
        """
        if not self.known_spectral_axis:
            self.opacity(integral=integral)

        if integral:
            piBatm = PI * Bnu_integral_num(self.wnedges, self.tlay[layer_idx]) / self.dwnedges
        else:
            piBatm = PI * Bnu(self.wns[:], self.tlay[layer_idx])

        return Spectrum(piBatm, self.wns, self.wnedges)

    def surf_bb(self, **kwargs) -> Spectrum:
        """Computes the surface black body flux (in W/m^2/cm^-1).

        See :any:`blackbody` for options.

        Returns
        -------
            Spectrum object
                Spectral flux of a bb at the surface (in W/m^2/cm^-1)
        """
        return self.blackbody(layer_idx=-1, **kwargs)

    def top_bb(self, **kwargs) -> Spectrum:
        """Computes the top of atmosphere black body flux (in W/m^2/cm^-1).

        See :any:`blackbody` for options.

        Returns
        -------
            Spectrum object
                Spectral flux of a bb at the temperature at the top of atmosphere (in W/m^2/cm^-1)
        """
        return self.blackbody(layer_idx=0, **kwargs)

    def contribution_function(self) -> np.ndarray:
        r"""
        Compute the contribution function $Cf(P,\lambda) = B(T,\lambda) \frac{d e^\tau}{d \log P}$.

        $\tau$ and $\log P$ are taken at the mid-layers, the temperature needs to be taken at the level surfaces.
        For that, we use the computed temperature `t_opac`.

        The result is not normalized to allow comparison.
        Returns
        -------
        np.ndarray
            Contribution function [W/m^2/str/cm-1].
            Shape: **(Nlay - 1, Nw)**.

        """
        B = Bnu_integral_array(self.wnedges, self.t_opac, self.Nw,
                               self.t_opac.shape[0]) / self.dwnedges
        dlogP = np.diff(self.logplay)
        detau = np.diff(self.g_integration(np.exp(-self.tau)), axis=0)

        return - ((B * detau).T / dlogP).T
