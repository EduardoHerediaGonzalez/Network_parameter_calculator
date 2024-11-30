import numpy as np

# Definition of the class that represent a resistor component
class Resistor:
    # Private class attributes
    __resistance: float = 0
    __conductance: float = 0

    # Class constructors
    def __init__(self, resistance: float = 0):
        self.__resistance = resistance
        try:
            self.__conductance = 1 / resistance
        except:
            self.__conductance = 0

    # Public class methods
    def set_resistance(self, to_value: float):
        self.__resistance = to_value
        self.__conductance = 1 / to_value

    def get_resistance(self):
        return self.__resistance

    def get_conductance(self):
        return self.__conductance


# Definition of the class that represent a capacitor component
class Capacitor:
    # Private class attributes
    __capacitance: float = 0
    __reactance: float = 0
    __susceptance: float = 0

    # Class constructors
    def __init__(self, capacitance: float = 0):
        self.__capacitance = capacitance

    # Public class methods
    def set_capacitance(self, to_value: float):
        self.__capacitance = to_value

    def get_capacitance(self):
        return self.__capacitance

    def get_reactance(self, at_frequency: float):
        try:
            self.__reactance = -1 / (2 * np.pi * at_frequency * self.__capacitance)
        except:
            self.__reactance = float(0)

        return self.__reactance

    def get_susceptance(self, at_frequency: float):
        self.__susceptance = 2 * np.pi * at_frequency * self.__capacitance

        return self.__susceptance


# Definition of the class that represent an inductor component
class Inductor:
    # Private class attributes
    __inductance: float = 0
    __reactance: float = 0
    __susceptance: float = 0

    # Class constructors
    def __init__(self, inductance: float = 0):
        self.__inductance = inductance

    # Public class methods
    def set_inductance(self, to_value):
        self.__inductance = to_value

    def get_inductance(self):
        return self.__inductance

    def get_reactance(self, at_frequency: float):
        self.__reactance = 2 * np.pi * at_frequency * self.__inductance

        return self.__reactance

    def get_susceptance(self, at_frequency: float):
        try:
            self.__susceptance = -1 / (2 * np.pi * at_frequency * self.__inductance)
        except:
            self.__susceptance = float(0)

        return  self.__susceptance


# Definition of the class that represent an impedance.
class Impedance:
    # Private class attributes
    __total_impedance: complex
    __type_of_element: str = ''
    __element_value: float = 0
    __resistance: float = 0
    __reactance: float = 0
    __impedance: complex = complex(0,0)

    # Class constructors
    def __init__(self, type_of_element: str = '', with_value: float = 0):
        self.__type_of_element = type_of_element
        self.__element_value = with_value

    # Public class methods
    def get_impedance(self, at_frequency):
        if self.__type_of_element == 'Resistor':
            self.__resistance = Resistor(resistance=self.__element_value).get_resistance()
            self.__reactance = float(0)

        elif self.__type_of_element == 'Capacitor':
            self.__resistance = float(0)
            self.__reactance = Capacitor(capacitance=self.__element_value).get_reactance(at_frequency=at_frequency)

        elif self.__type_of_element == 'Inductor':
            self.__resistance = float(0)
            self.__reactance = Inductor(inductance=self.__element_value).get_reactance(at_frequency=at_frequency)

        elif self.__type_of_element == 'Transmission line length (l)':
            self.__resistance = float(0)
            self.__reactance = PhaseConstant(length=self.__element_value).get_reactance(at_frequency=at_frequency)

        elif self.__type_of_element == 'Characteristic impedance (Zo)':
            self.__resistance = CharacteristicImpedance(characteristic_impedance=self.__element_value).get_characteristic_impedance()
            self.__reactance = float(0)
        else:
            self.__impedance = complex(0,0)

        self.__impedance = complex(self.__resistance, self.__reactance)

        return self.__impedance


# Definition of the class that represent an admittance.
class Admittance:
    # Class attributes
    __total_impedance: complex
    __type_of_element: str = ''
    __element_value: float = 0
    __conductance: float = 0
    __susceptance: float = 0
    __admittance: complex = complex(0,0)

    # Class constructors
    def __init__(self, type_of_element: str = '', with_value: float = 0):
        self.__type_of_element = type_of_element
        self.__element_value = with_value

    # Public class methods
    def get_admittance(self, at_frequency):
        if self.__type_of_element == 'Resistor':
            self.__conductance = Resistor(resistance=self.__element_value).get_conductance()
            self.__susceptance = float(0)

        elif self.__type_of_element == 'Capacitor':
            self.__conductance = float(0)
            self.__susceptance = Capacitor(capacitance=self.__element_value).get_susceptance(at_frequency=at_frequency)

        elif self.__type_of_element == 'Inductor':
            self.__conductance = float(0)
            self.__susceptance = Inductor(inductance=self.__element_value).get_susceptance(at_frequency=at_frequency)

        else:
            self.__admittance = complex(0,0)

        self.__admittance = complex(self.__conductance, self.__susceptance)

        return self.__admittance


# Definition of the class that represent an Open circuit Beta*length.
class PhaseConstant:
    # Private class attributes
    __length: float = 0
    __reactance: float = 0

    def __init__(self, length: float = 0):
        self.__length = length

    # Public class methods
    def set_length(self, to_value: float):
        self.__length = to_value

    def get_length(self):
        return self.__length

    def get_reactance(self, at_frequency: float):
        self.__reactance = (2 * np.pi * at_frequency * self.__length) / 2.998e8
        print(self.__reactance)
        return self.__reactance


class CharacteristicImpedance:
    # Private class attributes
    __characteristic_impedance: float = 0

    # Class constructors
    def __init__(self, characteristic_impedance: float = 0):
        self.__characteristic_impedance = characteristic_impedance
    # Public class methods
    def set_characteristic_impedance(self, to_value: float):
        self.__characteristic_impedance = to_value

    def get_characteristic_impedance(self):
        return self.__characteristic_impedance