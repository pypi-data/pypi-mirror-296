# -*- coding: utf-8 -*-
"""
@author: jeremy leconte

A module to handle ouputs rebinning and plotting
"""
from __future__ import annotations

from typing import Optional

import astropy.units as u
import h5py
import numpy as np

from exo_k.util.interp import rebin
from exo_k.util.spectral_object import Spectral_object
from exo_k.util.cst import PLANCK, C_LUM

planckovclum = PLANCK * 100. * C_LUM  #100 is a conversion factor from cm^-1 to m^-1

class Spectrum(Spectral_object):
    """A class defining a Spectrum object to plot and manipulate.
    """

    def __init__(self, value = None, wns = None, wnedges = None, input_spectral_unit='cm^-1', spectral_unit='cm^-1',
            filename = None, spectral_radiance = False, 
            from_taurex = False, dataset = 'native_spectrum', **kwargs):
        """Instanciate with a value, bin centers, and bin edges.
        Can also load a Taurex spectrum if filename is provided.

        Parameters
        ----------
            value: Array
                spectrum values
            wns: Array
                Spectral grid (can be wavenumbers or wavelengths)
            wnedges: Array
                Bin edges grid (can be wavenumbers or wavelengths)
            input_spectral_unit: str
                Unit of the input spectral grid
            spectral_unit: str
                desired output unit for the spectral grid
            filename: str
                Name of a file where the spectrum is stored. 
                If a filename is given, there is no need to provide
                values, wns, ...
            spectral_radiance: bool
                If True, the spectrum is assumed to be a flux in units of
                inverse spectral units (for example W/micron if the spectral unit is microns)
                If False, the spectrum is considered as monochromatic values (like Rp/Rs**2)
        """
        super().__init__()
        self.value = value
        self.wns = wns
        self.wnedges = wnedges
        self.spec_unit = input_spectral_unit
        self.spectral_radiance = spectral_radiance

        if filename is not None:
            if from_taurex:
                self.load_taurex(filename, dataset)
            elif filename.lower().endswith(('.hdf5', '.h5')):
                self.read_hdf5(filename)
            elif filename.lower().endswith(('.dat', '.txt')):
                self.read_ascii(filename, **kwargs)

        if (self.wnedges is None) and (self.wns is not None):
            self.wnedges = np.concatenate(([self.wns[0]],
                (self.wns[:-1]+self.wns[1:])*0.5,[self.wns[-1]]))

        self.convert_spectral_units(input_spectral_unit=input_spectral_unit,
                                    spectral_unit=spectral_unit, spectral_radiance=spectral_radiance)

        if self.wnedges is not None:
            self.dwnedges = np.diff(self.wnedges)
        else:
            self.dwnedges = None

    def convert_spectral_units(self, input_spectral_unit='cm^-1', spectral_unit='cm^-1',
                               spectral_radiance: Optional[bool] = None):
        if spectral_unit != input_spectral_unit:
            wns_tmp = (self.wns*u.Unit(input_spectral_unit)).to(u.Unit(spectral_unit), equivalencies=u.spectral()).value
            wnedges_tmp = (self.wnedges*u.Unit(input_spectral_unit)).to(u.Unit(spectral_unit), equivalencies=u.spectral()).value

            if spectral_radiance is not None:
                self.spectral_radiance = spectral_radiance

            if self.spectral_radiance:
                dwnedges = np.diff(self.wnedges)
                dwnedges_tmp = np.diff(wnedges_tmp)
                self.value = self.value * np.abs(dwnedges / dwnedges_tmp)
                # assumes that the wavelength unit
                # is the same as the spectral unit (for example F in W/nm if wl in nm).

            if wnedges_tmp[-1] > wnedges_tmp[0]:
                self.wns = wns_tmp
                self.wnedges = wnedges_tmp
            else:
                self.wns = np.copy(wns_tmp[::-1])
                self.wnedges = np.copy(wnedges_tmp[::-1])
                self.value = np.copy(self.value[::-1])

    def normalize(self, bolometric_flux: float):
        """Normalize the spectrum to a specified bolometric flux

        Parameters
        ----------
            bolometric_flux: float
                Integral of the flux over the total bandpass after normalization. 
        """
        factor = bolometric_flux / self.total
        self.value *= factor

    def photonize(self):
        """Translate to photon count in each bin
        """
        self.value /= self.wns * planckovclum

    def dephotonize(self):
        """Translate back to energy
        """
        self.value *= self.wns * planckovclum

    def integrate_per_bin(self):
        """integrate energy in each bin
        """
        self.value *= self.dwnedges

    def copy(self):
        """Deep copy of the spectrum.
        """
        return Spectrum(self.value.copy(), self.wns.copy(), self.wnedges.copy(),
                        input_spectral_unit=self.spec_unit, spectral_unit=self.spec_unit)

    def plot_spectrum(self, ax, per_wavenumber=True, x_axis='wls',
                      xscale=None, yscale=None, **kwarg):
        """Plot the spectrum
        
        Parameters
        ----------
            ax : :class:`pyplot.Axes`
                A pyplot axes instance where to put the plot.
            per_wavenumber: bool, optional
                Defines the units of spectral flux density.
                False converts to per wavelength units.
            x_axis: str, optional
                If 'wls', x axis is wavelength. Wavenumber otherwise.
            xscale, yscale: str, optional
                If 'log' log axes are used.
        """
        if per_wavenumber:
            toplot=self.value
        else:
            toplot=self.value/self.wls**2*1.e4
        if x_axis == 'wls':
            ax.plot(self.wls,toplot,**kwarg)
            ax.set_xlabel('Wavelength (micron)')
        else:
            ax.plot(self.wns,toplot,**kwarg)
            ax.set_xlabel('Wavenumber (cm$^{-1}$)')
        ax.set_ylabel('Flux')
        if xscale is not None: ax.set_xscale(xscale)
        if yscale is not None: ax.set_yscale(yscale)

    def bin_down(self, wnedges):
        """Bins down the spectrum to a new grid of wnedges by conserving area.
        
        Parameters
        ----------
            wnedges: array, np.ndarray
                Wavenumbers of the bin edges to be used
        """
        wnedges=np.array(wnedges)
        self.value=rebin(self.value,self.wnedges,wnedges)
        self.wnedges=wnedges
        self.dwnedges = np.diff(self.wnedges)
        self.wns=0.5*(self.wnedges[:-1]+self.wnedges[1:])

    def bin_down_cp(self, wnedges):
        """Returns a new binned down spectrum to a grid of wnedges by conserving area.
        
        Parameters
        ----------
            wnedges: array, np.ndarray
                Wavenumbers of the bin edges to be used

        Returns
        -------
            :class:`Spectrum`
                Binned down spectrum
        """
        res=self.copy()
        res.bin_down(wnedges)
        return res

    def clip_spectral_range(self, wn_range=None, wl_range=None):
        """Limits the data to the provided spectral range (inplace):

           * Wavenumber in cm^-1 if using wn_range argument
           * Wavelength in micron if using wl_range
        """
        iw_min, iw_max = self.select_spectral_range(wn_range, wl_range)
        self.value = self.value[iw_min:iw_max]

    def randomize(self, uncertainty: float = 0.):
        """Adds random noise with a given uncertainty.
        """
        rng = np.random.default_rng()

        self.noise = uncertainty * rng.standard_normal(self.value.size)
        self.value += self.noise

    def __add__(self, other):
        """Defines addition
        """
        if isinstance(other, (float, int, np.ndarray)):
            return Spectrum(self.value + other, self.wns, self.wnedges)

        if (self.wns.size == other.wns.size) and np.array_equal(self.wns, other.wns):
            val = self.value + other.value
            return Spectrum(val, self.wns, self.wnedges)
        else:
            raise RuntimeError('The two spectra do not have the same spectral sampling.')

    def __radd__(self, other):
        """Use commutativity v + S == S + v"""

        return self.__add__(other)

    def __sub__(self, other):
        """Defines subtraction
        """
        if isinstance(other, (float, int, np.ndarray)):
            return Spectrum(self.value - other, self.wns, self.wnedges)

        if (self.wns.size == other.wns.size) and np.array_equal(self.wns, other.wns):
            val = self.value - other.value
            return Spectrum(val, self.wns, self.wnedges)
        else:
            raise RuntimeError('The two spectra do not have the same spectral sampling.')

    def __mul__(self, other):
        """Defines multiplication
        """
        if isinstance(other, (float, int, np.ndarray)):
            return Spectrum(self.value * other, self.wns, self.wnedges)

        if (self.wns.size == other.wns.size) and np.array_equal(self.wns, other.wns):
            val = self.value * other.value
            return Spectrum(val, self.wns, self.wnedges)
        else:
            raise RuntimeError('The two spectra do not have the same spectral sampling.')

    def __rmul__(self, other):
        """Use commutativity v * S == S * v"""

        return self.__mul__(other)

    def __truediv__(self, other):
        """Defines division
        """
        if isinstance(other, (float, int, np.ndarray)):
            return Spectrum(self.value / other, self.wns, self.wnedges)

        if (self.wns.size == other.wns.size) and np.array_equal(self.wns, other.wns):
            val = self.value / other.value
            return Spectrum(val, self.wns, self.wnedges)
        else:
            raise RuntimeError('The two spectra do not have the same spectral sampling.')

    def __rtruediv__(self, other):
        """Defines division
        """
        if isinstance(other, (float, int, np.ndarray)):
            return Spectrum(other / self.value, self.wns, self.wnedges)

        if (self.wns.size == other.wns.size) and np.array_equal(self.wns, other.wns):
            val = other.value / self.value
            return Spectrum(val, self.wns, self.wnedges)
        else:
            raise RuntimeError('The two spectra do not have the same spectral sampling.')

    def std(self):
        """Defines standard deviation
        """
        return self.value.std()

    def abs(self):
        """Defines absolute value
        """
        return Spectrum(np.abs(self.value),self.wns,self.wnedges)

    def log10(self):
        """Defines Log 10
        """
        return Spectrum(np.log10(self.value),self.wns,self.wnedges)

    @property
    def total(self):
        """Defines the weighted sum over the spectrum
        """
        return np.dot(self.value,self.dwnedges)

    def read_hdf5(self, filename=None):
        """Reads data in a hdf5 file

        Parameters
        ----------
            filename: str
                Name of the file to be created and saved
        """
        if (filename is None or not filename.lower().endswith(('.hdf5', '.h5'))):
            raise RuntimeError("You should provide an input hdf5 file")
        with h5py.File(filename, 'r') as f:
            self.wns=f['bin_centers'][...]
            self.wnedges=f['bin_edges'][...]
            if 'units' in f['bin_edges'].attrs:
                self.spec_unit=f['bin_edges'].attrs['units']
            else:
                if 'units' in f['bin_centers'].attrs:
                    self.spec_unit=f['bin_centers'].attrs['units']
            self.value=f['spectrum'][...]

    def write_hdf5(self, filename):
        """Saves data in a hdf5 format

        Parameters
        ----------
            filename: str
                Name of the file to be created and saved
        """
        fullfilename=filename
        if not filename.lower().endswith(('.hdf5', '.h5')):
            fullfilename=filename+'.h5'
        compression="gzip"
        with h5py.File(fullfilename, 'w') as f:
            f.create_dataset("spectrum", data=self.value, compression=compression)
            f.create_dataset("bin_edges", data=self.wnedges, compression=compression)
            f["bin_edges"].attrs["units"] = 'cm^-1'
            f.create_dataset("bin_centers", data=self.wns, compression=compression)
            f["bin_centers"].attrs["units"] = 'cm^-1'

    def read_ascii(self, filename, usecols = (0,1), skip_header=0):
        """Saves data in a ascii format

        Parameters
        ----------
            filename: str
                Name of the file to be read
            spec_axis: str
                Whether the spectral axis in the file is
                wavenumber in cm^-1 ('wns') or wavelength in microns ('wls')
            skip_header: int
                Number of lines to skip
        """
        raw=np.genfromtxt(filename, skip_header = skip_header,
            usecols = usecols, names=('spec_axis','value'))
        self.wns = raw['spec_axis']
        self.value = raw['value']

    def write_ascii(self, filename, fmt='%.18e', spec_axis='wns', header=None, per_wavenumber=True):
        """Saves data in a ascii format

        Parameters
        ----------
            filename: str
                Name of the file to be created and saved
        """
        fullfilename=filename
        if not filename.lower().endswith(('.dat', '.txt')):
            fullfilename=filename+'.dat'
        head=header
        if per_wavenumber:
            towrite = self.value
        else:
            towrite = self.value/self.wls**2*1.e4

        if spec_axis=='wns':
            if head is None: head='wavenumber(cm^-1)     spectrum'
            np.savetxt(fullfilename, np.array([self.wns,towrite]).transpose(),
                fmt=fmt, header=head)
        else:    
            if head is None: head='wavelength(micron)    spectrum'
            np.savetxt(fullfilename, np.array([self.wls[::-1],towrite[::-1]]).transpose(),
                fmt=fmt, header=head)

    def load_taurex(self, filename,dataset='native_spectrum'):
        """Loads a taurex file

        Parameters
        ----------
            filename: str
                Full name (path) of the hdf5 file to load
            dataset: str
                Name of the hdf5 dataset to load
        """
        with h5py.File(filename, 'r') as f:
            self.wns = f['Output/Spectra/native_wngrid'][...]
            self.value = f['Output/Spectra/'+dataset][...]

        self.wnedges=np.concatenate(([self.wns[0]],(self.wns[:-1]+self.wns[1:])*0.5,[self.wns[-1]]))

    def __repr__(self):
        """Method to output header
        """
        output="""
        value        : {val}
        wl (microns) : {wl}
        """.format(val=self.value,wl=self.wls)
        return output

