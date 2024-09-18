#   #!/usr/bin/env python
#   -*- coding: utf-8 -*-
#   ******************************************************************************
#     Copyright (c) 2024.
#     Developed by Yifei Lu
#     Last change on 8/7/24, 2:20 PM
#     Last change by yifei
#    *****************************************************************************
from collections import OrderedDict
import logging
from scipy.constants import atm, zero_Celsius

# from .thermo.thermo import Mixture
# from thermo import Mixture
from .GERG2008.gerg2008 import *
from .GERG2008.gerg2008_constants import *
from .GERG2008.gerg2008 import convert_to_gerg2008_composition
# from .heating_value import calc_heating_value


class GasMixture:
    """
    Class for gas mixture properties
    """
    def __init__(self, pressure, temperature, composition: OrderedDict, method='GERG-2008'):
        """

        :param pressure:
        :param temperature:
        :param composition:
        :param method:
        """
        self.pressure = pressure
        self.temperature = temperature
        self.composition = composition
        self.method = method
        self.convert_composition_format()
        self.update_gas_mixture()

    def convert_composition_format(self):
        if self.method == "GERG-2008":
            self.eos_composition = convert_to_gerg2008_composition(self.composition)
            self.eos_composition_tmp = convert_to_gerg2008_composition(self.composition)
        elif self.method == "PREOS":
            self.eos_composition = self.composition
            self.eos_composition_tmp = self.composition

    def convert_eos_composition_to_dictionary(self):
        if self.method == "GERG-2008":
            self.composition = convert_gerg2008_to_dictionary(self.eos_composition)
        return None

    def update_gas_mixture(self):
        if self.method == "GERG-2008":
            self.gerg2008_mixture = GasMixtureGERG2008(P_Pa=self.pressure,
                                                       T_K=self.temperature,
                                                       composition=self.eos_composition_tmp)
        elif self.method == "PREOS":
            self.thermo_mixture = Mixture(P=self.pressure,
                                          T=self.temperature,
                                          zs=self.eos_composition_tmp)

    @property
    def compressibility(self):
        if self.method == "PREOS":
            if self.thermo_mixture.Z is not None:
                z = self.thermo_mixture.Z
            else:
                logging.warning("Compressibility is not available, using the Z for gas!")
                z = self.thermo_mixture.Zg
            return self.thermo_mixture.Z
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.Z

    @property
    def specific_gravity(self):
        if self.method == "PREOS":
            if self.thermo_mixture.SG is not None:
                specific_gravity = self.thermo_mixture.SG
            else:
                logging.warning("Specific gravity is not available, using the SG for gas!")
                specific_gravity = self.thermo_mixture.SGg
            return specific_gravity
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.SG

    @property
    def molar_mass(self):
        if self.method == "PREOS":
            return self.thermo_mixture.MW
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.MolarMass

    @property
    def density(self):
        if self.method == "PREOS":
            return self.thermo_mixture.rho
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.rho

    @property
    def standard_density(self):
        if self.method == "PREOS":
            return Mixture(P=1*atm,
                           T=15+zero_Celsius,
                           zs=self.composition).rho

        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.standard_density

    @property
    def joule_thomson_coefficient(self):
        if self.method == "PREOS":
            return self.thermo_mixture.JT
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.JT

    @property
    def viscosity(self):
        if self.method == "PREOS":
            return self.thermo_mixture.mu
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.viscosity

    @property
    def heat_capacity_constant_pressure(self):
        if self.method == "PREOS":
            return self.thermo_mixture.Cp
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.Cp

    @property
    def R_specific(self):
        if self.method == "PREOS":
            return self.thermo_mixture.R_specific
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.R_specific

    @property
    def HHV_J_per_m3(self):
        if self.method == "PREOS":
            return None
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.HHV_J_per_m3

    @property
    def HHV_J_per_sm3(self):
        if self.method == "PREOS":
            return None
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.HHV_J_per_sm3

    @property
    def HHV_J_per_kg(self):
        if self.method == "PREOS":
            return None
        elif self.method == "GERG-2008":
            return self.gerg2008_mixture.HHV_J_per_kg
