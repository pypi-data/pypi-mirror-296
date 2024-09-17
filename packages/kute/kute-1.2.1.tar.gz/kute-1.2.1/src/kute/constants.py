# Copyright (c) 2024 The KUTE contributors

# Constants (in S.I. units)
NA = 6.02214076e23 # Avogadro's number
KB = 1.380649e-23 # Boltzmann constant in J/K
EPSILON_0 = 8.8541878128e-12 # Vacuum permittivity in F/m
ELEMENTARY_CHARGE = 1.602176634e-19 # Elementary charge in Coulombs

# Transformations
KG_TO_AMU = 1 / 1.66053906660e-27 # Kilograms to atomic mass units
J_TO_KCAL = 1 / 4184 # Joules to kilocalories
J_TO_ERGS = 1e7 # Joules to ergs
J_TO_EV = 1 / 1.602176634e-19 # Joules to electron volts
METERS_TO_NANOMETERS = 1e9 # Meters to nanometers
METERS_TO_ANGSTROMS = 1e10 # Meters to angstroms
SEC_TO_PS = 1e12 # Seconds to picoseconds
SEC_TO_FS = 1e15 # Seconds to femtoseconds
PAS_TO_POISE = 1e1 # Pascal-seconds to poise
NEWTONS_TO_DYNES = 1e5 # Newtons to dynes
PA_TO_PSI = 0.000145038 # Pascals to pounds per square inch

# Atomic masses (in atomic mass units)
ATOMIC_MASSES = {
    "H": 1.00784,
    "He": 4.0026,
    "Li": 6.9410,
    "Be": 9.0121831,
    "B": 10.811,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Ne": 20.180,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "Si": 28.086,
    "P": 30.974,
    "S": 32.065,
    "Cl": 35.453,
    "Ar": 39.948,
    "K": 39.098,
    "Ca": 40.078,
    "Sc": 44.956,
    "Se": 78.960,
    "Ti": 47.867,
    "Br": 79.904,
    "Ag": 107.87,
    "Au": 196.967,
    "Hg": 200.59,
    "Rn": 222.0,
}