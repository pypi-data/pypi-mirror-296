import numpy
from scipy.interpolate import interp1d
from scipy.optimize import minimize
from lenstronomy.Cosmo.nfw_param import NFWParam
import astropy.units as un
from colossus.lss.bias import twoHaloTerm
from scipy.integrate import quad

class NFWParampyHalo(NFWParam):

    """Adds methods for psuedo-NFW profiles to those implemented in lenstronomy"""

    def rho0_c_pseudoNFW(self, c, z):
        """
        computes density normalization as a function of concentration parameter for an NFW-like profile
        with (1+x^2) in the denominator instead of (1+x)^2

        :param c: concentration
        :param z: redshift
        :return: density normalization in h^2/Mpc^3 (physical)
        """
        return 2 * c ** 3 * self.rhoc_z(z) * 200 / (3 * numpy.log(1+c**2))


class LensCosmo(object):

    def __init__(self, z_lens=None, z_source=None, cosmology=None):
        """

        This class performs calcuations relevant for certain halo mass profiles and lensing-related quantities for a
        given lens/source redshift and cosmology
        :param z_lens: deflector redshift
        :param z_source: source redshift
        :param cosmology: and instance of the Cosmology class (see pyhalo.Cosmology.cosmology.py)
        """
        if cosmology is None:
            from pyHalo.Cosmology.cosmology import Cosmology
            cosmology = Cosmology()

        self.cosmo = cosmology
        self._arcsec = 2 * numpy.pi / 360 / 3600
        self.h = self.cosmo.h
        # critical density of the universe in M_sun h^2 Mpc^-3
        rhoc = un.Quantity(self.cosmo.astropy.critical_density(0), unit=un.Msun / un.Mpc ** 3).value
        self.rhoc = rhoc / self.cosmo.h ** 2

        if z_lens is not None and z_source is not None:
            # critical density for lensing in units M_sun * Mpc ^ -2
            self.sigma_crit_lensing = self.get_sigma_crit_lensing(z_lens, z_source)
            # critical density for lensing in units M_sun * kpc ^ -2
            self.sigma_crit_lens_kpc = self.sigma_crit_lensing * (0.001) ** 2
            # critical density for lensing in units M_sun * arcsec ^ -2 at lens redshift
            self.sigmacrit = self.sigma_crit_lensing * (0.001) ** 2 * self.cosmo.kpc_proper_per_asec(z_lens) ** 2
            # lensing distances
            self.D_d, self.D_s, self.D_ds = self.cosmo.D_A_z(z_lens), self.cosmo.D_A_z(z_source), self.cosmo.D_A(
                z_lens, z_source)
        self._computed_zacc_pdf = False
        self._nfw_param = NFWParampyHalo(self.cosmo.astropy)
        self.z_lens = z_lens
        self.z_source = z_source
        self._z_infall_pdf = InfallDistributionGalacticus2024(z_lens)

    def z_accreted_from_zlens(self, mass, z_lens):
        """
        Returns the redshift a subhalo was accreted. Note that in the current implementation this is
        independent of infall mass
        :param mass: subhalo mass at infall
        :param z_lens: main deflector redshift
        :return: accretion redshift
        """
        return self._z_infall_pdf.z_accreted_from_zlens(z_lens)

    def two_halo_boost(self, m200, z, rmin=0.5, rmax=10):

        """
        Computes the average contribution of the two halo term in a redshift slice adjacent
        the main deflector. Returns a rescaling factor applied to the mass function normalization

        :param m200: host halo mass
        :param z: redshift
        :param rmin: lower limit of the integral, something like the virial radius ~500 kpc
        :param rmax: Upper limit of the integral, this is computed based on redshift spacing during
        the rendering of halos
        :return: scaling factor applied to the normalization of the LOS mass function
        """

        mean_boost = 2 * quad(self.twohaloterm, rmin, rmax, args=(m200, z))[0] / (rmax - rmin)
        # factor of two for symmetry in front/behind host halo

        return 1. + mean_boost

    def twohaloterm(self, r, M, z, mdef='200c'):

        """
        Computes the boost to the background density of the Universe
        from correlated structure around a host of mass M
        :param r:
        :param M:
        :param z:
        :param mdef:
        :return:
        """

        h = self.cosmo.h
        M_h = M * h
        r_h = r * h
        rho_2h = twoHaloTerm(r_h, M_h, z, mdef=mdef) / self.cosmo._colossus_cosmo.rho_m(z)
        return rho_2h

    def nfw_physical2angle(self, m, c, z, pseudo_nfw=False):
        """
        converts the physical mass and concentration parameter of an NFW profile into the lensing quantities
        updates lenstronomy implementation with arbitrary redshift

        :param m: mass enclosed 200 rho_crit in units of M_sun (physical units, meaning no little h)
        :param c: NFW concentration parameter (r200/r_s)
        :param z: redshift at which to evaluate angles from distances
        :param pseudo_nfw: specifies whether one deals with a regualr NFW profile (False) or a psuedo-NFW profile
        with (1+x^2) in the denominator rather than (1+x)^2
        :return: Rs_angle (angle at scale radius) (in units of arcsec), alpha_Rs (observed bending angle at the scale radius
        """
        rho0, Rs, _ = self.nfwParam_physical(m, c, z, pseudo_nfw)
        return self.nfw_physical2angle_fromNFWparams(rho0, Rs, z, pseudo_nfw)

    def nfw_physical2angle_fromNFWparams(self, rho0, Rs, z, pseudo_nfw=False):
        """
        computes the angular lensing properties of an NFW profile from its physical parameters
        :param rho0: central density normalization [M_sun / Mpc^3]
        :param Rs: scale radius [Mpc]
        :param z: redshift at which to evaluate angles from distances
        :param pseudo_nfw: specifies whether one deals with a regualr NFW profile (False) or a psuedo-NFW profile
        with (1+x^2) in the denominator rather than (1+x)^2
        :return: scale radius and deflection angle at the scale radius in arcsec
        """

        dd = self.cosmo.D_A_z(z)
        Rs_angle = Rs / dd / self._arcsec  # Rs in arcsec
        if pseudo_nfw:
            r2 = numpy.sqrt(2)
            alpha_Rs = rho0 * (4 * Rs ** 2 * (r2*numpy.log(1+r2) + numpy.log(1. / 2.)))
        else:
            alpha_Rs = rho0 * (4 * Rs ** 2 * (1 + numpy.log(1. / 2.)))
        sigma_crit = self.get_sigma_crit_lensing(z, self.z_source)
        return Rs_angle, alpha_Rs / sigma_crit / dd / self._arcsec

    def rN_M(self, M, z, N):
        """
        computes the radius R_N of a halo of mass M in physical mass M/h, where N is a number multiplying the critical
        density of the Universe at z

        :param M: halo mass in M_sun/h
        :param z: redshift
        :param N: number, e.g. N=200 computes r200
        :return: radius R_N in physical Mpc/h
        """
        rn_mpc_over_h = (3 * M / (4 * numpy.pi * self._nfw_param.rhoc_z(z) * N)) ** (1. / 3.)
        return rn_mpc_over_h / self.cosmo.h

    def nfwParam_physical(self, m, c, z, pseudo_nfw=False):
        """
        returns the NFW parameters in physical units
        updates lenstronomy implementation with arbitrary redshift

        :param m: physical mass in M_sun
        :param c: concentration
        :return: rho0 [Msun/Mpc^3], Rs [Mpc], r200 [Mpc]
        """
        r200 = self._nfw_param.r200_M(m * self.h, z) / self.h  # physical radius r200
        if pseudo_nfw:
            rho0 = self._nfw_param.rho0_c_pseudoNFW(c, z) * self.h ** 2 # physical density in M_sun/Mpc**3
        else:
            rho0 = self._nfw_param.rho0_c(c, z) * self.h**2  # physical density in M_sun/Mpc**3
        Rs = r200/c
        return rho0, Rs, r200

    def NFW_params_physical(self, m, c, z, pseudo_nfw=False):
        """
        returns the NFW parameters in physical units

        :param M: physical mass in M_sun
        :param c: concentration
        :param z: redshift
        :param pseudo_nfw: bool; if False, uses a regular NFW profile, if True, uses an NFW profile
        with (1+x^2) in the denominator
        :return: rho0 [Msun/kpc^3], Rs [kpc], r200 [kpc]
        """
        rho0, Rs, r200 = self.nfwParam_physical(m, c, z, pseudo_nfw)
        return rho0 * 1000 ** -3, Rs * 1000, r200 * 1000

    def sigma_crit_mass(self, z, area):

        """
        :param z: redshift
        :param area: physical area in Mpc^2
        :return: the 'critical density mass' sigma_crit * A in units M_sun
        """

        sigma_crit_mpc = self.get_sigma_crit_lensing(z, self.z_source)
        return area * sigma_crit_mpc

    @property
    def colossus(self):
        return self.cosmo.colossus

    ######################################################
    """ACCESS ROUTINES IN STRUCTURAL PARAMETERS CLASS"""
    ######################################################

    def mthermal_to_halfmode(self, m_thermal):
        """
        Convert thermal relic particle mass to half-mode mass
        :param m_thermaal:
        :return:
        """
        # too lazy for algebra
        def _func(m):
            return abs(self.halfmode_to_thermal(m)-m_thermal)/0.01
        return minimize(_func, x0=10**8, method='Nelder-Mead')['x']

    def halfmode_to_thermal(self, m_half_mode):

        """
        Converts a half mode mass in units of solar masses (no little h) to the mass of
        the corresponding thermal relic particle in keV
        :param m: half mode mass in solar masses
        :return: thermal relic particle mass in keV
        """

        omega_matter = self.cosmo.astropy.Om0
        return 2.32 * (omega_matter / 0.25)**0.4 * (self.cosmo.h/0.7)**0.8 * \
               (m_half_mode / 10 ** 9) ** (-0.3)

    def mhm_to_fsl(self, m_hm):
        """
        Converts half mode mass to free streaming length in Mpc
        See Equations 5-8 in https://arxiv.org/pdf/1112.0330.pdf
        :param m_hm: half-mode mass in units M_sun (no little h)
        :return: free streaming length in units Mpc
        """

        rhoc = self.rhoc * self.cosmo.h ** 2
        l_hm = 2 * (3 * m_hm / (4 * numpy.pi * rhoc)) ** (1. / 3)
        l_fs = l_hm / 13.93
        return l_fs

    ##################################################################################
    """ROUTINES RELATED TO LENSING STUFF"""
    ##################################################################################

    def get_sigma_crit_lensing(self, z1, z2):
        """
        Computes thee critial density for lensing in units of M_sun / Mpc^2
        :param z1: the lens redshit
        :param z2: the source redshift
        :return: the critial density for lensing
        """
        D_ds = self.cosmo.D_A(z1, z2)
        D_d = self.cosmo.D_A_z(z1)
        D_s = self.cosmo.D_A_z(z2)
        d_inv = D_s*D_ds**-1*D_d**-1
        # (Mpc ^2 / sec^2) * (Mpc^-3 M_sun^1 sec ^ 2) * Mpc ^-1 = M_sun / Mpc ^2
        epsilon_crit = (self.cosmo.c**2*(4*numpy.pi*self.cosmo.G)**-1)*d_inv
        return epsilon_crit

    def point_mass_factor_z(self, z):

        """
        Returns the cosmology-dependent factor to evaluate the Einstein radius of a point mass of mass M:

        :param z: redshift
        :return: The factor that when multiplied by sqrt(mass) gives the Einstein radius of a point mass

        R_ein = sqrt(M) * point_mass_factor_z(z)

        """
        factor = 4 * self.cosmo.G * self.cosmo.c ** -2
        dds = self.cosmo.D_A(z, self.z_source)
        dd = self.cosmo.D_A_z(z)
        ds = self.D_s
        factor *= dds / dd / ds
        return factor ** 0.5 / self.cosmo.arcsec

    def halo_dynamical_time(self, m_host, z, c_host):
        """
        This routine computes the dynamical timescale for a halo of mass M defined as
        t = 0.5427 / sqrt(G*rho)
        where G is the gravitational constant and rho is the average density
        :param m_host: host mass in M_sun
        :param z: host redshift
        :param c_host: host halo concentration
        :return: the dynamical timescale in Gyr
        """

        _, _, rvir = self.NFW_params_physical(m_host, c_host, z)
        volume = (4/3)*numpy.pi*rvir**3
        rho_average = m_host / volume
        g = 4.3e-6
        return 0.5427 / numpy.sqrt(g*rho_average)

class InfallDistributionGalacticus2024(object):
    """ACCRETION REDSHIFT PDF FROM GALACTICUS USING THE VERSION OF GALACTICUS AS OF FEB 2024 AND SELECTING ON
    SUBHALOS WITH A BOUND MASS > 10^6"""

    def __init__(self, z_lens):
        self.z_lens = z_lens
        self._counts = numpy.array([ 50,  93, 125, 180, 175, 144, 120, 117,  97,  82,  52,  51,  35,
        20,   9,   4,   4,   0,   1,   1])
        self._z_infall = numpy.array([ 0.53836189,  1.37376234,  2.2091628 ,  3.04456325,  3.87996371,
        4.71536416,  5.55076461,  6.38616507,  7.22156552,  8.05696598,
        8.89236643,  9.72776689, 10.56316734, 11.39856779, 12.23396825,
       13.0693687 , 13.90476916, 14.74016961, 15.57557007, 16.41097052]) - 0.5
        cdf = numpy.cumsum(self._counts)
        self._cdf = cdf / numpy.max(cdf)
        self._cdf_min = numpy.min(self._cdf)
        self._cdf_max = numpy.max(self._cdf)
        self._interp = interp1d(self._cdf, self._z_infall)

    def z_accreted_from_zlens(self, z_lens):
        u = numpy.random.uniform(self._cdf_min, self._cdf_max)
        z_infall = z_lens + self._interp(u)
        return z_infall


# class InfallDistributionGalacticus2024(object):
#     """ACCRETION REDSHIFT PDF FROM GALACTICUS USING THE VERSION OF GALACTICUS AS OF FEB 2024"""
#
#     def __init__(self, z_lens):
#         self.z_lens = z_lens
#         self._counts = numpy.array([ 74, 111, 138, 225, 281, 394, 396, 492, 603, 665, 626, 738, 714,
#         725, 744, 712, 679, 600, 556, 524, 478, 442, 347, 322, 283, 198,
#         189, 148, 137,  98,  77,  44,  32,  32,  26,  18,  15,   6,   5,
#         4,   0,   2,   0,   0])
#         self._z_infall = numpy.array([ 0.25,  0.75,  1.25,  1.75,  2.25,  2.75,  3.25,  3.75,  4.25,
#         4.75,  5.25,  5.75,  6.25,  6.75,  7.25,  7.75,  8.25,  8.75,
#         9.25,  9.75, 10.25, 10.75, 11.25, 11.75, 12.25, 12.75, 13.25,
#         13.75, 14.25, 14.75, 15.25, 15.75, 16.25, 16.75, 17.25, 17.75,
#         18.25, 18.75, 19.25, 19.75, 20.25, 20.75, 21.25, 21.75])
#         cdf = numpy.cumsum(self._counts)
#         self._cdf = cdf / numpy.max(cdf)
#         self._cdf_min = numpy.min(self._cdf)
#         self._cdf_max = numpy.max(self._cdf)
#         self._interp = interp1d(self._cdf, self._z_infall)
#
#     def z_accreted_from_zlens(self, z_lens):
#         u = numpy.random.uniform(self._cdf_min, self._cdf_max)
#         z_infall = z_lens + self._interp(u)
#         return z_infall
#
# class InfallDistributionGalacticus2020(object):
#     """ACCRETION REDSHIFT PDF FROM GALACTICUS USING THE VERSION OF GALACTICUS PUBLISHED IN 2020 WITH
#     WARM DARK MATTER CHILLS OUT"""
#     def __init__(self, z_lens):
#         self.z_lens = z_lens
#
#     @property
#     def _subhalo_accretion_pdfs(self):
#
#         if self._computed_zacc_pdf is False:
#             self._computed_zacc_pdf = True
#             self._mlist, self._dzvals, self._cdfs = self._Msub_cdfs(self.z_lens)
#
#         return self._mlist, self._dzvals, self._cdfs
#
#     def z_accreted_from_zlens(self, msub, zlens):
#
#         mlist, dzvals, cdfs = self._subhalo_accretion_pdfs
#
#         idx = self._mass_index(msub, mlist)
#
#         z_accreted = zlens + self._sample_cdf_single(cdfs[idx])
#
#         return z_accreted
#
#     def _cdf_numerical(self, m, z_lens, delta_z_values):
#
#         c_d_f = []
#
#         prob = 0
#         for zi in delta_z_values:
#             prob += self._P_fit_diff_M_sub(z_lens + zi, z_lens, m)
#             c_d_f.append(prob)
#         return numpy.array(c_d_f) / c_d_f[-1]
#
#     def _Msub_cdfs(self, z_lens):
#
#         M_sub_exp = numpy.arange(6.0, 10.2, 0.2)
#         M_sub_list = 10 ** M_sub_exp
#         delta_z = numpy.linspace(0., 6, 8000)
#         funcs = []
#
#         for mi in M_sub_list:
#             # cdfi = P_fit_diff_M_sub_cumulative(z_lens+delta_z, z_lens, mi)
#             cdfi = self._cdf_numerical(mi, z_lens, delta_z)
#
#             funcs.append(interp1d(cdfi, delta_z))
#
#         return M_sub_list, delta_z, funcs
#
#     def z_decay_mass_dependence(self, M_sub):
#         # Mass dependence of z_decay.
#         a = 3.21509397
#         b = 1.04659814e-03
#
#         return a - b * numpy.log(M_sub / 1.0e6) ** 3
#
#     def z_decay_exp_mass_dependence(self, M_sub):
#         # Mass dependence of z_decay_exp.
#
#         a = 0.30335749
#         b = 3.2777e-4
#
#         return a - b * numpy.log(M_sub / 1.0e6) ** 3
#
#     def _P_fit_diff_M_sub(self, z, z_lens, M_sub):
#         # Given the redhsift of the lens, z_lens, and the subhalo mass, M_sub, return the
#         # posibility that the subhlao has an accretion redhisft of z.
#
#         z_decay = self.z_decay_mass_dependence(M_sub)
#         z_decay_exp = self.z_decay_exp_mass_dependence(M_sub)
#
#         normalization = 2.0 / numpy.sqrt(2.0 * numpy.pi) / z_decay \
#                         / numpy.exp(0.5 * z_decay ** 2 * z_decay_exp ** 2) \
#                         / erfc(z_decay * z_decay_exp / numpy.sqrt(2.0))
#         return normalization * numpy.exp(-0.5 * ((z - z_lens) / z_decay) ** 2) \
#                * numpy.exp(-z_decay_exp * (z - z_lens))
#
#     def _sample_cdf_single(self, cdf_interp):
#
#         u = numpy.random.uniform(0, 1)
#
#         try:
#             output = float(cdf_interp(u))
#             if numpy.isnan(output):
#                 output = 0
#
#         except:
#             output = 0
#
#         return output
#
#     def _mass_index(self, subhalo_mass, mass_array):
#
#         idx = numpy.argmin(numpy.absolute(subhalo_mass - mass_array))
#         return idx

