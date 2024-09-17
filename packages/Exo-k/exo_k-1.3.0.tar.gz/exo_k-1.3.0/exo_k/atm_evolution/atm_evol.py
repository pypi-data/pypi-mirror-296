# -*- coding: utf-8 -*-
"""
@author: jeremy leconte
"""
import pickle
import copy
import numpy as np
from exo_k.gas_mix import Gas_mix
from exo_k.atm import Atm
from exo_k.atm_2band import Atm_2band
from exo_k.util.cst import DAY, RGP
from .settings import Settings
from .tracers import Tracers
from .convection import turbulent_diffusion_numba, molecular_diffusion_numba, \
                convective_acceleration_numba, moist_convective_adjustment_numba, compute_condensation_numba, \
                compute_rainout_numba, moist_convective_adjustment_cloud_fraction_numba
from .condensation import Condensing_species, Condensation_Thermodynamical_Parameters 
#from .condensation_gcm import Condensing_species, Condensation_Thermodynamical_Parameters 
# The line above allows one to select the same cthermodynamics as in the LMDZ GCM. To be changed accordingly in convection.py

class Atm_evolution(object):
    """Model of atmospheric evolution.

    Uses exo_k.Atm class to compute radiative transfer
    """

    def __init__(self, bg_vmr=None, verbose=False, **kwargs):
        """Initializes atmospheric profiles.

        Most arguments are passed directly to exo_k.Atm class through **kwargs

        .. warning::
            Layers are counted from the top down (increasing pressure order).
            All methods follow the same convention.
        """
        self.settings = Settings()
        self.settings.set_parameters(**kwargs)
        self.header={'rad':0,'conv':1,'turb':2,'cond':3,'madj':4,'rain':5,'tot':6}

        # setup background gas and thermodynamical properties
        self.bg_gas = Gas_mix(bg_vmr)
        self.M_bg = self.bg_gas.molar_mass()
        self.M_bg = self.settings.use_or_set('M_bg', self.M_bg)
        self.cp = self.bg_gas.cp()
        self.cp = self.settings.pop('cp', self.cp)
        self.rcp = RGP/(self.M_bg*self.cp)
        self.rcp = self.settings.use_or_set('rcp', self.rcp)
        if (not isinstance(self.rcp, float)) or (not isinstance(self.cp, float)):
            print('None of rcp or cp should be arrays. If you provided arrays')
            print('for the background gas composition, you should also')
            print('provide the effective cp and rcp for your atmosphere.')
            raise RuntimeError('None of rcp or cp should be arrays.')
        if verbose: print('cp, M_bg, rcp:', self.cp, self.M_bg, self.rcp)

        # setup tracers
        self.tracers = Tracers(self.settings, bg_vmr = self.bg_gas.composition,
            **self.settings.parameters)
        self.initialize_condensation(**self.settings.parameters)

        self.setup_radiative_model(gas_vmr = self.tracers.gas_vmr,
            **self.settings.parameters)
        self.Nlay = self.atm.Nlay
        self.tlay = self.atm.tlay
        self.compute_hybrid_coordinates()

        if verbose: print(self.settings.parameters)
        self.evol_tau = 0.

    def set_options(self, reset_rad_model = False, check_keys = True,
            cp = None, verbose = False, **kwargs):
        """This method is used to store the global options
        in the `Settings` object.

        Arguments are all passed through **kwargs.

        Sometimes, one needs to reset the radiative model to take into
        account some modifications (like the databases). Normally, this should
        be automatic, but you can force it with `reset_rad_model=True`
        """
        if check_keys:
            for key in kwargs.keys():
                if key in self.settings._forbidden_changes:
                    print('Warning!!! ', key, ' cannot be changed by set_options.')
                    print('You should probably initialize a new Atm_evolution instance.')
                    print('Use check_keys = False to remove this warning.')
        if 'tlay' not in kwargs.keys():
            self.settings.set_parameters(tlay=self.tlay, logplay=self.atm.logplay, **kwargs)
        else:
            self.settings.set_parameters(**kwargs)
        if cp is not None:
            self.cp = cp
        if 'radiative_acceleration' in kwargs.keys():
            print("'radiative_acceleration' is deprecated. Please use acceleration_mode instead.")
            print("acceleration_mode = 1 will emulate the previous behavior but other modes exist.")
            print("In particular acceleration_mode = 4 will also accelerate convergence in convective zones")
            raise DeprecationWarning('radiative_acceleration is deprecated. Remove radiative_acceleration from the options to get rid of this message')
        
        if not set(kwargs.keys()).issubset(self.settings._non_radiative_parameters):
            reset_rad_model = True
            if verbose: print('Radiative model will be reset.')
        if reset_rad_model: self.setup_radiative_model(gas_vmr = self.tracers.gas_vmr,
                **self.settings.parameters)

    def initialize_condensation(self, condensing_species = None, **kwargs):
        """This method initializes the condensation module by
        listing all the condensing vapors and linking them to their
        condensed form. 

        For each vapor-condensate pair, a :class:`Condensible_species` object is created
        with the thermodynamical data provided. 

        Here is an example of dictionary to provide as input to include CH4 condensation
        ```
        condensing_species={'ch4':{'Latent_heat_vaporization': 5.25e5, 'cp_vap': 2.232e3, 'Mvap': 16.e-3,
            'T_ref': 90., 'Psat_ref': 0.11696e5}}
        ```
        """
        if condensing_species is None:
            condensing_species = {}
        self.condensing_pairs = list()
        self.condensing_pairs_idx = list()
        self.condensing_species_idx = dict()
        self.condensing_species_params=list()
        self.condensing_species_thermo=list()
        idx = 0
        for name in self.tracers.namelist:
            if 'type' in self.tracers.dico[name]:
                if self.tracers.dico[name]['type'] == 'vapor':
                    if 'condensed_form' not in self.tracers.dico[name]:
                        print("You should identify the 'condensed_form' of:", name)
                        raise RuntimeError()
                    elif self.tracers.dico[name]['condensed_form'] not in self.tracers.namelist:
                        print("The condensed form of a vapor should be a tracer.")
                        raise RuntimeError()
                    elif name in condensing_species.keys():
                        cond_name = self.tracers.dico[name]['condensed_form']
                        self.condensing_species_idx[name]=idx
                        self.condensing_pairs.append([name, cond_name])
                        self.condensing_pairs_idx.append(\
                            [self.tracers.idx[name], self.tracers.idx[cond_name]])
                        self.condensing_species_params.append(\
                            Condensing_species(**condensing_species[name]))
                        self.condensing_species_thermo.append(\
                            Condensation_Thermodynamical_Parameters(**condensing_species[name]))
                        idx+=1
                    else: 
                        print("The thermodynamic parameters for:", name,'were not provided')
                        print('through condensing_species = {}.')
                        raise RuntimeError()
        self.Ncond=idx
        self.total_cloud_fraction = np.ones(self.Ncond)

    def setup_radiative_model(self, k_database=None, k_database_stellar=None,
            cia_database=None, cia_database_stellar=None, gas_vmr=None, **kwargs):
        """This method initializes the exo_k.Atm object that will be used
        to carry out radiative transfer calculations. 

        This is where the radiative data used are chosen and transmitted to the 
        radiative transfer module, along with many other
        parameters including the incoming stellar flux (`flux_top_dw`), the
        blackbody temperature of the star (`Tstar`), the 

        If a `k_database_stellar` is provided, then this is this database
        that will be used to treat the scattering and absorption of incoming radiation.
        In that case, `k_database` will be used to treat the emission of the atmosphere.
        The effective cos(zenith angle) for the incoming stellar radiation can then
        be specified independently with the `mu0_stellar` keyword.

        If no `k_database_stellar` is provided, `k_database` will be used to treat
        both the atmospheric emission and the stellar radiation. Running a model
        with `k_database_stellar=k_database` yields the same results at twice the cost.
        
        Parameters
        ----------
            k_database, k_database_stellar: `exo_k.Kdatabase` objects
                radiative database for the molecules in the atmospheres.
            cia_database, cia_database_stellar: `exo_k.CIA_database` object
                radiative database for the CIA ofmolecules in the atmospheres.
        """
        if k_database is None:
            raise RuntimeError('We need at least a k_database')
        if k_database_stellar is None:
            self.atm = Atm(k_database=k_database, cia_database=cia_database, composition=gas_vmr, 
                    Mgas=self.tracers.Mgas, **kwargs)
        else:
            raise DeprecationWarning("k_database_stellar is deprecated. Proceed at your own risk.")
            self.atm = Atm_2band(k_database=k_database, cia_database=cia_database,
                k_database_stellar=k_database_stellar, cia_database_stellar=cia_database_stellar,
                composition=gas_vmr, **kwargs)
        H, net = self.atm.heating_rate(compute_kernel=True, Mgas=self.tracers.Mgas, **kwargs)

    def compute_average_fluxes(self):
        """Use the averaged heating rates to compute the various fluxes (W/m^2)
        at the level interfaces. These fluxes are positive when the energy flows
        upward.

        To be consistent with radiative fluxes, the first array value corresponds
        to the top of atmosphere and should be 0 in most cases. The last value corresponds
        to the flux between the deepest layer (considered to be the surface) and the layer just above.
        """
        self.Fnet = np.zeros((7, self.Nlay))
        self.Fnet[0] = self.Fnet_rad
        for ii in range(1,6):
            self.Fnet[ii]=np.concatenate([[0.],
                np.cumsum(self.H_ave[ii]*self.atm.dmass)[:-1]])
        self.Fnet[-1] = np.sum(self.Fnet, axis=0)


    def evolve(self, N_timestep=1, N_kernel=10000, timestep_factor=1., dT_max=100.,
            verbose=False, check_cons=False, **kwargs):
        r"""The time variable used in the model is tau=t/cp. 
        The equation we are solving in each layer is thus

        .. math::
            c_p \frac{d T}{d t}= \frac{d T}{d tau} = \sum_i H_i

        For a given timestep `dtau`, the physical time elapsed in second can be computed using `dt=dtau*cp`

        To work, the heating rates (H) must be computed in W/kg. 

        This also means that if one needs the physical rate of change of another quantity (like dq/dt)
        from the delta q over a time step,
        one needs to do `dq/dt = delta q / (timestep * cp)`

        Parameters
        ----------
            N_timestep: int
                Number of timesteps to perform.
            N_kernel: int
                Maximal number of timesteps between two computations of the radiative kernel.
            timestep_factor: float
                Multiplicative factor applied to timestep computed automatically by
                the radiative module.
                timestep_factor > 1 can lead to unstabilities.
            dT_max: float
                Maximum temperature increment in a single timestep.
            
        """
        if self.atm.k_database is None:
            print('This Atm_evolution instance is not linked to any k_database')
            print('Use self.set_options(k_database=, ...)')
            raise RuntimeError('No k_database provided.')
        self.H_ave = np.zeros((7, self.Nlay))

        self.tlay_hist = np.zeros((N_timestep,self.Nlay))
        self.Fnet_top = np.zeros((N_timestep))
        self.timestep_hist = np.zeros((N_timestep))
        if check_cons:
            self.nrj_cons = np.zeros((N_timestep,self.Nlay))
            self.nrj_cons_dry = np.zeros((N_timestep,self.Nlay))
            self.nrj_cons_cond = np.zeros((N_timestep,self.Nlay))
            self.nrj_cons_rain = np.zeros((N_timestep,self.Nlay))
            self.vapor_cons = np.zeros((N_timestep,self.Nlay))
            self.cond_cons = np.zeros((N_timestep,self.Nlay))
            self.cloud_fraction_hist = np.zeros((N_timestep))
        tau0 = self.evol_tau
        self.N_last_ker = 0
        compute_kernel = False
        dTlay_max = 2. * self.settings['dTmax_use_kernel']
        self.tracers.update_gas_composition(update_vmr=True)
        for ii in range(N_timestep):
            if np.amax(np.abs(self.tlay-self.atm.tlay_kernel)) < self.settings['dTmax_use_kernel']:
                self.N_last_ker +=1
                if verbose: print(self.N_last_ker, self.N_last_ker%N_kernel)
                compute_kernel = (self.N_last_ker%N_kernel == 0)
                if compute_kernel: self.N_last_ker = 0
            else:
                if dTlay_max < 0.5 * self.settings['dTmax_use_kernel']:
                    compute_kernel = True
                    self.N_last_ker = 0
                else:
                    compute_kernel = False
                    self.N_last_ker +=1
            if ii == N_timestep-1:
                if ii != 0:
                    compute_kernel=True
            self.H_tot=np.zeros(self.Nlay)
            if verbose: print('iter, compute_kernel:', ii, compute_kernel)
            if self.tracers.some_var_gases:
                gas_vmr_rad = self.tracers.gas_vmr
            else:
                gas_vmr_rad = None
            aer_reffs_densities = self.tracers.update_aerosol_properties(self.atm)
            self.H_rad, self.Fnet_rad = self.atm.heating_rate(compute_kernel=compute_kernel,
                rayleigh=self.settings['rayleigh'], dTmax_use_kernel=self.settings['dTmax_use_kernel'],
                gas_vmr=gas_vmr_rad, Mgas=self.tracers.Mgas, aer_reffs_densities=aer_reffs_densities, **kwargs)
#            if verbose and compute_kernel: print('H_rad', self.H_rad)
            self.H_tot += self.H_rad
            self.timestep = timestep_factor * self.atm.tau_rad
            #if verbose: print('tau_rad, dt:', self.atm.tau_rad, self.timestep)
            self.evol_tau += self.timestep
            if self.settings['convection']:
                self.H_conv = self.tracers.dry_convective_adjustment(self.timestep, self.H_tot, self.atm, verbose = verbose)
                self.H_tot += self.H_conv
                if check_cons:
                    self.nrj_cons_dry[ii] += self.H_conv * self.atm.dmass
            else:
                self.H_conv = np.zeros(self.Nlay)
            if self.settings['diffusion']:
                if check_cons:
                    self.vapor_cons[ii] -= self.tracers['H2O'] * self.atm.dmass
                    self.cond_cons[ii] -= self.tracers['H2O_liq'] * self.atm.dmass
                self.H_turb = self.turbulent_diffusion(self.timestep, self.H_tot, self.atm, self.cp,
                                        index_dry_convective_top=self.tracers.index_dry_convective_top, 
                                        Kzz_pressure_factor=self.settings['Kzz_pressure_factor'],
                                        verbose=verbose
                                        )
                self.H_tot += self.H_turb
                if check_cons:
                    self.nrj_cons_dry[ii] += self.H_turb * self.atm.dmass
                    self.vapor_cons[ii] += self.tracers['H2O'] * self.atm.dmass
                    self.cond_cons[ii] += self.tracers['H2O_liq'] * self.atm.dmass
                self.tracers.update_gas_composition(update_vmr=False)
            else:
                self.H_turb = np.zeros(self.Nlay)
            if self.settings['molecular_diffusion']:
                self.H_diff = self.molecular_diffusion(self.timestep,
                    self.H_tot, self.atm, self.cp)
                self.H_tot += self.H_diff
            qarray_before_condensation = np.copy(self.tracers.qarray)
            if self.settings['moist_convection']:
                #if check_cons:
                #    self.vapor_cons[ii] -= self.tracers['H2O'] * self.atm.dmass
                #    self.cond_cons[ii] -= self.tracers['H2O_liq'] * self.atm.dmass
                self.H_madj = self.moist_convective_adjustment(self.timestep, self.H_tot,
                                    moist_inhibition=self.settings['moist_inhibition'], verbose = verbose)                
                self.H_tot += self.H_madj
                if check_cons:
                    if np.sum(self.H_madj * self.atm.dmass)<0.:
                        print('madj<0:',self.H_madj, self.total_cloud_fraction[0])
                    self.nrj_cons[ii] += self.H_madj * self.atm.dmass
                    #self.vapor_cons[ii] += self.tracers['H2O'] * self.atm.dmass
                    #self.cond_cons[ii] += self.tracers['H2O_liq'] * self.atm.dmass
                    self.cloud_fraction_hist[ii] = self.total_cloud_fraction[0]
                    self.total_cloud_fraction[0] = 1.
            else:
                self.H_madj = np.zeros(self.Nlay)
            if self.settings['condensation']:
                #if check_cons:
                #    self.vapor_cons[ii] -= self.tracers['H2O'] * self.atm.dmass
                #    self.cond_cons[ii] -= self.tracers['H2O_liq'] * self.atm.dmass
                self.H_cond = self.condensation(self.timestep, self.H_tot, verbose = verbose)
                self.H_tot += self.H_cond
                if check_cons:
                    self.nrj_cons_cond[ii] += self.H_cond * self.atm.dmass
                    #self.vapor_cons[ii] += self.tracers['H2O'] * self.atm.dmass
                    #self.cond_cons[ii] += self.tracers['H2O_liq'] * self.atm.dmass
            else:
                self.H_cond = np.zeros(self.Nlay)
            if self.settings['rain']:
                if check_cons:
                    self.vapor_cons[ii] -= self.tracers['H2O'] * self.atm.dmass
                    self.cond_cons[ii] -= self.tracers['H2O_liq'] * self.atm.dmass
                self.H_rain = self.rainout(self.timestep, self.H_tot, verbose = verbose)
                self.H_tot += self.H_rain
                if check_cons:
                    self.nrj_cons_rain[ii] += self.H_rain * self.atm.dmass
                    self.vapor_cons[ii] += self.tracers['H2O'] * self.atm.dmass
                    self.cond_cons[ii] += self.tracers['H2O_liq'] * self.atm.dmass
            else:
                self.H_rain = np.zeros(self.Nlay)
            if self.settings['mass_redistribution']:
                self.mass_redistribution(qarray_before_condensation)
            if self.settings['surface_reservoir']:
                self.tracers.update_surface_reservoir(condensing_pairs_idx = self.condensing_pairs_idx,
                    surf_layer_mass = self.atm.dmass[-1])
            if self.settings['acceleration_mode'] > 0:
                self.radiative_acceleration(timestep = self.timestep, \
                    acceleration_mode = self.settings['acceleration_mode'],
                    acceleration_top_pressure = self.settings['acceleration_top_pressure'], 
                    verbose = verbose)
                #self.H_tot *= self.acceleration_factor
            dTlay= self.H_tot * self.timestep
            dTlay_max = np.amax(np.abs(dTlay))
            if dTlay_max > dT_max:
                print('dT > dTmax:',dTlay_max,' at k=',np.argmax(np.abs(dTlay))) 
            if verbose:
                print('heat rates (rad, dry conv), dTmax:', 
                    np.sum(self.H_rad*self.atm.dmass), np.sum(self.H_conv*self.atm.dmass),
                    dTlay_max)
            dTlay=np.clip(dTlay,-dT_max,dT_max)
            self.tlay = self.tlay + dTlay
            self.tlay_hist[ii] = self.tlay
            for jj, H in enumerate([self.H_rad, self.H_conv, self.H_turb, self.H_cond, self.H_madj,
                  self.H_rain, self.H_tot]):
                self.H_ave[jj] += H * self.timestep
            self.Fnet_top[ii] = self.Fnet_rad[0]
            self.timestep_hist[ii] = self.timestep
            self.atm.set_T_profile(self.tlay)
            self.tracers.update_gas_composition(update_vmr=True)
        inv_delta_t = 1./(self.evol_tau-tau0)
        self.H_ave *= inv_delta_t
        self.compute_average_fluxes()

    def equilibrate(self, Fnet_tolerance = None, N_iter_max = 10,
        N_timestep_ini = 100, N_timestep_max = 1000000, verbose = False, **kwargs):
        """Evolves an atmosphere until it is at equilibrium.
        
        Equilibrium is assumed to be reached when the net top of atmosphere
        flux remains within +-Fnet_tolerance of the internal flux
        for a whole evolution step.

        The number of timesteps per evolution step in multiplied by two 
        at each iteration, starting from N_timestep_ini, until the limit of
        N_timestep_max is reached.

        Parameters
        ----------
            Fnet_tolerance: float
                Tolerance on net flux in W/m^2 to identify convergence.
            N_iter_max: int
                Max number of successive calls to evolve
            N_timestep_ini: int
                Initial number of timesteps in a single evolution step
            N_timestep_max: int
                Max number of timesteps in a single evolution step
        """
        iter=1
        if Fnet_tolerance is None:
            raise RuntimeError('You should provide the maximum tolerance on the net flux: Fnet_tolerance (in W/m^2)') 
        N_timestep = N_timestep_ini
        while iter <= N_iter_max:
            time_init = self.evol_tau
            self.evolve(N_timestep = N_timestep, **kwargs)
            net = self.Fnet_top - self.atm.internal_flux
            if verbose:
                print('iter: {iter}, N_timestep: {Nt}'.format(iter = iter, Nt = N_timestep))
                print('Fnet mean: {fme:.3g} W/m^2, (min:{fmi:.3g}, max:{fma:.3g})'.format( \
                    fme = net.mean(), fmi = net.min(), fma = net.max()))   
                print('timestep: {ts1:.3g} d | {ts2:.3g} s, total time: {ev_t:.3g} yr'.format( \
                    ts1 = self.timestep*self.cp/(DAY), ts2 = self.timestep*self.cp,
                    ev_t = (self.evol_tau-time_init)*self.cp/(DAY*365.)))   
                #print('timestep:',self.timestep*self.cp/(DAY),'days, ',
                #    self.timestep*self.cp,'s, evol_time(yr):',(self.evol_tau-time_init)*self.cp/(DAY*365.))
            if np.all(np.abs(net) < Fnet_tolerance): break
            N_timestep = min( N_timestep * 2, N_timestep_max)
            iter += 1
            
    def moist_convective_adjustment(self, timestep, Htot, moist_inhibition = True,
            verbose = False):
        """This method computes the vapor and temperature tendencies do to
        moist convectoin in saturated layers.

        The tracer array in modified in place.

        Parameters
        ----------
            timestep: float
                physical timestep of the current step (in s/cp).
            Htot: array, np.ndarray
                Total heating rate (in W/kg) of all physical processes
                already computed

        Return
        ------
            H_madj: array, np.ndarray
                Heating rate due to large scale condensation (W/kg)
        """
        new_t = self.atm.tlay + timestep * Htot
        H_madj = np.zeros(self.Nlay)
        for i_cond in range(self.Ncond): #careful i_cond is the index of the condensing pair
            # in the list of condensing species, idx_cond is the position of the
            # condensate linked to i_cond in the tracers array.
            idx_vap, idx_cond = self.condensing_pairs_idx[i_cond]
            thermo_parameters = self.condensing_species_thermo[i_cond].th_params
            if self.settings['humidity_distribution_width']<0.:
                H, qarray, new_t, self.total_cloud_fraction[i_cond] = moist_convective_adjustment_numba(timestep, self.Nlay,
                    new_t, self.atm.play, self.atm.dmass, self.cp, self.tracers.Mgas, self.tracers.qarray, idx_vap, idx_cond,
                    thermo_parameters,
                    moist_inhibition = moist_inhibition,
                    verbose = verbose)
            else:
                H, qarray, new_t, self.total_cloud_fraction[i_cond] = moist_convective_adjustment_cloud_fraction_numba(timestep, self.Nlay,
                    new_t, self.atm.play, self.atm.dmass, self.cp, self.tracers.Mgas, self.tracers.qarray, idx_vap, idx_cond,
                    thermo_parameters,
                    moist_inhibition = moist_inhibition,
                    humidity_distribution_width = self.settings['humidity_distribution_width'],
                    verbose = verbose)
            #print('t after madj:', new_t)
            H_madj += H
            self.tracers.qarray = qarray
            if verbose: print(qarray[idx_cond])
        return H_madj

    def turbulent_diffusion(self, timestep, Htot, atm, cp, index_dry_convective_top=None,
                            Kzz_pressure_factor=-1., verbose=False):
        """Mixes tracers following a diffusion equation
        with a constant Kzz parameter (self.Kzz in m^2/s).

        Parameters
        ----------
            timestep: float
                physical timestep of the current step (in s/cp).
                (needs to be converted before it is sent to `turbulent diffusion`)
            Htot: array
                Total heating rate (in W/kg) of all physical processes
                already computed
            atm: :class:`Atm` object
                The Atm object used in the radiative transfer which
                contains many state variables. 
        """
        new_t = atm.tlay + timestep * Htot
        if self.settings['moist_inhibition']:
            Mgas_tmp = self.tracers.Mgas
        else:
            Mgas_tmp = np.mean(self.tracers.Mgas)
            Mgas_tmp = np.full_like(self.tracers.Mgas, Mgas_tmp)
        if Kzz_pressure_factor > 0.:
            p0 = self.atm.play[index_dry_convective_top]
            self.Kzz = self.settings['Kzz'] * np.where(self.atm.play>p0, 1., (self.atm.play/p0)**Kzz_pressure_factor)
            self.Kzz = np.core.umath.maximum(self.Kzz,self.settings['Kzz_min'])
            if verbose: print('Kzz=',self.Kzz)
        else:
            self.Kzz = np.ones(self.Nlay) * self.settings['Kzz']
        H_turb, self.tracers.qarray = turbulent_diffusion_numba(timestep*cp, self.Nlay,
                    atm.play, atm.plev,
                    atm.dmass, new_t, atm.exner, new_t/Mgas_tmp,
                    atm.grav, self.Kzz, self.tracers.qarray, cp, mix_potential_temp=self.settings['mix_potential_temp'])
        return H_turb

    def molecular_diffusion(self, timestep, Htot, atm, cp):
        """Mixes energy following a diffusion equation
        with a constant Dmol parameter (self.Dmol in m^2/s).

        Parameters
        ----------
            timestep: float
                physical timestep of the current step (in s/cp).
                (needs to be converted before it is sent to `turbulent diffusion)
            Htot: array, np.ndarray
                Total heating rate (in W/kg) of all physical processes
                already computed
            atm: :class:`Atm` object
                The Atm object used in the radiative transfer which
                contains many state variables. 
        """
        new_t = atm.tlay + timestep * Htot
        H_diff = molecular_diffusion_numba(timestep*cp, self.Nlay,
                    atm.play, atm.plev,
                    atm.dmass, new_t, self.tracers.Mgas,
                    atm.grav, self.tracers.Dmol)
        return H_diff

    def condensation(self, timestep, Htot, verbose = False):
        """This method computes the vapor and temperature tendencies do to
        large scale condensation in saturated layers.

        The tracer array in modified in place.

        Parameters
        ----------
            timestep: float
                physical timestep of the current step (in s/cp).
            Htot: array, np.ndarray
                Total heating rate (in W/kg) of all physical processes
                already computed

        Return
        ------
            H_cond: array, np.ndarray
                Heating rate due to large scale condensation (W/kg)
        """
        new_t = self.atm.tlay + timestep * Htot
        H_cond = np.zeros(self.Nlay)
        for i_cond in range(self.Ncond): #careful i_cond is a dumy loop index, idx_cond is position of species i_cond in tracers array.
            idx_vap, idx_cond = self.condensing_pairs_idx[i_cond]
            thermo_parameters = self.condensing_species_thermo[i_cond].th_params
            H_cond += compute_condensation_numba(timestep, self.Nlay, new_t, self.atm.play,
                self.cp, self.tracers.Mgas, self.tracers.qarray,
                idx_vap, idx_cond, thermo_parameters,
                latent_heating = self.settings['latent_heating'],
                condensation_timestep_reducer = self.settings['condensation_timestep_reducer'],
                verbose = verbose)
        return H_cond

    def rainout(self, timestep, Htot, verbose = False):
        """This method computes rainout.

        Condensates are carried down and reevaporated whenever there is
        "room" in an unsaturated layer. 

        The option `evap_coeff` acts has an efficiency factor. `evap_coeff=1`
        is the efficient evaporation limit. When `evap_coeff<1` the maximum amount of
        condensates that can be reevaporated in a single layer is multiplied by
        `evap_coeff`

        All condensates are finaly evaporated in the last layer or when T > Tboil.

        The tracer array is modified in place.

        Parameters
        ----------
            timestep: float
                physical timestep of the current step (in s/cp).
            Htot: array, np.ndarray
                Total heating rate (in W/kg) of all physical processes
                already computed

        Return
        ------
            H_rain: array, np.ndarray
                Heating rate due to re evaporation (W/kg)
        """
        new_t = self.atm.tlay + timestep * Htot
        H_rain=np.zeros(self.Nlay)
        for i_cond in range(self.Ncond):
            idx_vap, idx_cond = self.condensing_pairs_idx[i_cond]
            thermo_parameters = self.condensing_species_thermo[i_cond].th_params
            H_rain += compute_rainout_numba(timestep, self.Nlay, new_t, self.atm.play,
                self.atm.dmass, self.cp, self.tracers.Mgas, self.tracers.qarray,
                idx_vap, idx_cond, thermo_parameters,
                self.settings['evap_coeff'], self.tracers.qdeep[idx_vap],
                q_cloud=self.settings['q_cloud'],
                latent_heating = self.settings['latent_heating'],
                total_cloud_fraction = self.total_cloud_fraction[i_cond],
                humidity_distribution_width = self.settings['humidity_distribution_width'],
                verbose = verbose)

        return H_rain

    def compute_hybrid_coordinates(self):
        """Compute hybrid coordinates as in GCM.

        This will be used when surface pressure changes.
        
        Convention : sigma = (p-ptop)/(psurf-ptop)
        For each layer/level, the pressure is p = sigma * psurf + gamma
        """
        psurf = self.atm.plev[-1]
        ptop = self.atm.plev[0]
        self.sigma_lay = (self.atm.play-ptop)/(psurf-ptop)
        self.gamma_lay = (1.-self.sigma_lay)*ptop
        self.sigma_lev = (self.atm.plev-ptop)/(psurf-ptop)
        self.gamma_lev = (1.-self.sigma_lev)*ptop
        self.dsigma_lev = np.diff(self.sigma_lev)

    def compute_mass_flux(self, dvapor_mass, sum_dvapor_mass):
        """Computes the mass flux through the hybrid coordinate interfaces (kg/s/m^2; positive upward).
        (see Methods in Leconte et al. (2013))

        W[k] is the mass flux between layer k-1 et k.

        Parameters
        ----------
            sum_dvapor_mass: float
                Total mass of vapor added to the atmosphere
                in the last timestep.
            dvapor_mass: array, np.ndarray
                mass of vapor added to each layer.

        For the moment, W[0] = W[Nlay]
        """
        W = np.zeros(self.Nlay+1)
        #W[0] = 0. #No mass flux between the top of the atm and space
        W[1:] = np.cumsum(self.dsigma_lev * sum_dvapor_mass - dvapor_mass) 
        W[-1] = 0. #No mass flux between the surface and the atm
        return W

    def mass_redistribution(self, qarray_before_condensation):
        """Update new mass and new pressure of a layer due to the evaporation and condensation of a given species, 
        for more details see Methods, Leconte et al., 2013 (Nature)
     
        Parameters
        ----------

        """
        if self.Ncond > 1:
            raise NotImplementedError('Mass redistribution limited to one condensing species')
        #Pour juste l'eau 
        for i_cond in range(self.Ncond):
            idx_vap, idx_cond = self.condensing_pairs_idx[i_cond]
 
        dq_mass_redist = np.zeros_like(qarray_before_condensation)

        variation_qarray = self.tracers.qarray - qarray_before_condensation #Evolution of qarray before and after condensation/rain/moist_convection steps
        
        dvapor_mass = self.atm.dmass*variation_qarray[idx_vap] #Need to use idx_vap because dvapor_mass
        sum_dvapor_mass = np.sum(dvapor_mass)
        dcond_mass = self.atm.dmass*variation_qarray[idx_cond]
        self.dpsurf = sum_dvapor_mass*self.atm.grav
        dgas_mass = self.dsigma_lev*self.dpsurf/self.atm.grav
            
        if self.settings['compute_mass_fluxes']:
            self.W = self.compute_mass_flux(dvapor_mass, sum_dvapor_mass)
            for indice, q in enumerate(self.tracers.qarray):
                if indice == idx_vap: #Condensible gas in vapor form
                    epsilon = dvapor_mass
                elif indice == idx_cond: #Condensible gas in condensed form
                    epsilon = dcond_mass 
                else: #Other tracers
                    epsilon = 0.
                qarray_lev = np.zeros(self.Nlay+1)
                qarray_lev[1:-1] = (q[1:] + q[:-1]) / 2 #We choose the arithmetic mean value of the qarray as the value of the qarray at the middle of the levels ie q_(k+1/2)
                qarray_transport_through_sigma_lev = (qarray_lev[1:]-qarray_before_condensation[indice])*self.W[1:] \
                    - (qarray_lev[:-1]-qarray_before_condensation[indice])*self.W[:-1] #Attention si W à la surface est non nulnp.diff(self.qarray_lev*self.W)
                dq_mass_redist[indice] = (1./(self.atm.dmass+dgas_mass))* \
                    (qarray_transport_through_sigma_lev+epsilon-qarray_before_condensation[indice]*dvapor_mass)
                self.tracers.qarray[indice] = np.abs(qarray_before_condensation[indice] + dq_mass_redist[indice]) # carefull abs should be removed
        else:
            self.W = np.zeros(self.Nlay+1)
            for indice, q in enumerate(qarray_before_condensation):
                if indice==idx_vap: #Condensible gas in vapor form
                    epsilon = dvapor_mass
                elif indice==idx_cond: #Condensible gas in condensed form
                    epsilon = dcond_mass
                else: #Other tracer
                    epsilon = 0.
                dq_mass_redist[indice] = (1./(self.atm.dmass+dgas_mass))*(epsilon-q*dgas_mass)
                self.tracers.qarray[indice] = qarray_before_condensation[indice] + dq_mass_redist[indice]
                
        plev = self.sigma_lev*(self.atm.psurf+self.dpsurf)+self.gamma_lev
        play = self.sigma_lay*(self.atm.psurf+self.dpsurf)+self.gamma_lay
        self.atm.update_pressure_profile(play = play, plev = plev)

    def radiative_acceleration(self, timestep = 0., acceleration_mode = 0, acceleration_top_pressure = None,
                               verbose = False, **kwargs):
        """"Computes an acceleration factor and a new heating rate to speed up convergence

        Parameters
        ----------
            acceleration_mode: int
                0: no acceleration
                1 or 3: acceleration limited to radiative zones.
                2 or 4: acceleration in convective zones as well. 

        * 1: acceleration limited to radiative zones. 
          The largest radiative timescale in non-radiative zones is 
          used as reference radiative timsescale to compute acceleration.
        * 2: Same as mode 1 + acceleration in convective zones
        * 3 acceleration limited to radiative zones.
          The smallest radiative timescale in radiative zones is 
          used as reference radiative timsescale to compute acceleration.
        * 4: Same as mode 3 + acceleration in convective zones
        """
        self.acceleration_factor = np.ones_like(self.H_tot)
        rad_layers =  np.isclose(self.H_tot, self.H_rad, atol=0.e0, rtol=1.e-10)
        rad_layers_for_convection =  np.copy(rad_layers)
        if acceleration_top_pressure is not None:
            rad_layers[np.where(self.atm.play < acceleration_top_pressure)[0]] = False
            rad_layers_for_convection[np.where(self.atm.play < acceleration_top_pressure)[0]] = True
        # determines which layer is purely radiative
        if verbose: 
            print('in acc rad_layers, H_tot, H_rad')
            print(rad_layers)
            print(np.transpose([rad_layers, self.H_tot,self.H_rad]))
        if (np.all(rad_layers)) or (not(np.any(rad_layers))):
            self.base_timescale = self.atm.tau_rad
            # we do not use timestep to avoid including the timestep_factor
        else:
            if acceleration_mode <= 2:
                self.base_timescale = np.amax(self.atm.tau_rads[np.logical_not(rad_layers)])
            elif acceleration_mode <= 4:
                self.base_timescale = np.amin(self.atm.tau_rads[rad_layers])
            else:
                raise NotImplementedError('Only acceleration_mode <= 4 is supported for the moment')

        self.acceleration_factor[rad_layers] = np.core.umath.maximum(
            self.atm.tau_rads[rad_layers] \
            / self.base_timescale * self.settings['radiative_acceleration_factor'],
            1.)

        if (acceleration_mode == 2) or (acceleration_mode == 4):
            self.H_acc = convective_acceleration_numba(timestep, self.Nlay, self.H_rad,
                    rad_layers_for_convection, self.atm.tau_rad, self.atm.tau_rads, self.atm.dmass,
                    convective_acceleration_mode = self.settings['convective_acceleration_mode'],
                    convective_acceleration_factor = self.settings['convective_acceleration_factor'],
                    verbose = verbose)
        else:
            self.H_acc = np.zeros(self.Nlay)
        
        if verbose: 
            print('in acc acceleration_factor, H_tot, H_acc')
            print(np.transpose([self.acceleration_factor, self.H_tot, self.H_acc]))
        self.H_tot = self.H_tot * self.acceleration_factor + self.H_acc

    @property
    def time(self):
        """Yields current time in seconds
        """
        return self.evol_tau * self.cp

    @property
    def time_hist(self):
        """Yields the array of the times for the last call to evolve (in seconds)
        """
        return np.cumsum(self.timestep_hist) * self.cp
    
    def heating_rate(self, physical_process):
        """Returns heating rates in W/kg per layer averaged over last call to evolve.
        Possible physical_processes are rad, cond, conv, rain, madj, tot"""
        return self.H_ave[self.header[physical_process]]

    def net_flux(self, physical_process):
        """Returns net_flux in W/m^2 averaged over last call to evolve.
        Possible physical_processes are rad, cond, conv, rain, madj, tot"""
        return self.Fnet[self.header[physical_process]]
    
    def qsat(self, mol):
        """Returns the saturation specific concentration of molecule mol (kg/kg)"""
        cond_species_param = self.condensing_species_params[self.condensing_species_idx[mol]]
        psat = cond_species_param.Psat(self.atm.tlay)
        qsat = cond_species_param.qsat(psat, self.atm.play,
                            cond_species_param.Mvap/self.tracers.Mgas)
        return qsat
    
    def interpolate_profile(self, logplay, adiabatic_extrapolation=True, **kwargs):
        """Re interpolates the current atmosphere on a new log pressure grid.

        Extrapolation is isothermal at the top and can be adiabatic at the bottom

        Parameters
        ----------
            logplay: array
                New log pressure grid
            adiabatic_extrapolation: bool
                Whether or not to extrapolate using the adiabat below the bottom
        """
        self.tracers.interpolate_tracers_profile(logplay, self.atm.logplay)
        self.atm.interpolate_atm_profile(logplay, adiabatic_extrapolation=adiabatic_extrapolation,
                            Mgas=self.tracers.Mgas,gas_vmr=self.tracers.gas_vmr, **kwargs)
        self.tlay = self.atm.tlay
        self.Nlay = self.atm.Nlay
        self.settings.set_parameters(logplay=logplay, tlay=self.tlay)

    def write_pickle(self, filename, data_reduction_level = 1):
        """Saves the instance in a pickle file

        Parameters
        ----------
            filename: str
                Path to pickle file
            data_reduction_level: int
                Level of data to delete.
                0: keep everything (results in big files).
                1: removes some arrays, should not affect subsequent evolution.
                2: removes the k and cia databases. The radiative model will need to be reset.
                This can be done with
                `set_options(k_database=, cia_database=, reset_rad_model=True)` after
                re-loading the `Atm_evolution` instance.
        """
        other = copy.deepcopy(self)
        if data_reduction_level >=1 :
            other.tlay_hist = None
            other.atm.asym_param = None
            other.atm.kdata = None
            other.atm.tau = None
            other.atm.dtau = None
            other.atm.flux_down_nu = None
            other.atm.flux_net_nu = None
            other.atm.flux_up_nu = None
            other.atm.piBatm = None
            other.atm.single_scat_albedo = None
            other.atm.gas_mix.kdata_scat = None
        if data_reduction_level >=2 :
            other.settings['k_database'] = None
            other.settings['cia_database'] = None
            other.atm.k_database = None
            other.atm.gas_mix.k_database = None
            other.atm.gas_mix.cia_database = None
            other.atm.kernel = None
            other.atm.tlay_kernel = None
            other.atm.H_kernel = None
        with open(filename, 'wb') as filehandler:
            pickle.dump(other, filehandler)
