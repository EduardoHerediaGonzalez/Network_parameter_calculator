import numpy as np

# Definition of the class that represent a resistor component
class Resistor:
    # Private class attributes
    __impedance_value: complex
    __admittance_value: complex

    # Class constructors
    def __init__(self, resistance_value: float):
        self.__resistance_value = resistance_value
        self.__conductance_value = 1 / resistance_value

    # Public class methods
    def set_resistance(self, resistance_value):
        self.__resistance_value = resistance_value
        self.__conductance_value = 1 / resistance_value

    def get_resistance(self):
        return self.__resistance_value

    def get_conductance(self):
        return self.__conductance_value

    def get_impedance(self):
        reactance = 0
        self.__impedance_value = complex(self.__resistance_value, reactance)

        return  self.__impedance_value

    def get_admittance(self):
        reactance = 0
        self.__admittance_value = complex(self.__conductance_value, reactance)

        return self.__admittance_value


# Definition of the class that represent a capacitor component
class Capacitor:
    # Private class attributes
    __reactance_value: float
    __susceptance_value: float
    __impedance_value: complex
    __admittance_value: complex

    # Class constructors
    def __init__(self, capacitance_value: float):
        self.__capacitance_value = capacitance_value

    # Private class methods

    # Public class methods
    def get_reactance(self, at_frequency: int):
        self.__reactance_value = -1 / (2 * np.pi * at_frequency * self.__capacitance_value)

        return self.__reactance_value

    def get_susceptance(self, at_frequency: int):
        self.__susceptance_value = 2 * np.pi * at_frequency * self.__capacitance_value

        return self.__susceptance_value

    def get_impedance(self, at_frequency):
        resistance = 0
        reactance = self.get_reactance(at_frequency=at_frequency)

        self.__impedance_value = complex(resistance, reactance)

        return self.__impedance_value

    def get_admittance(self, at_frequency):
        conductance = 0
        susceptance = self.get_susceptance(at_frequency=at_frequency)

        self.__admittance_value = complex(conductance, susceptance)

        return self.__admittance_value


# Definition of the class that represent an inductor component
class Inductor:
    # Private class attributes
    __reactance_value: float
    __susceptance_value: float
    __impedance_value: complex
    __admittance_value: complex

    # Class constructors
    def __init__(self, inductance_value: float):
        self.__inductance_value = inductance_value

    # Private class methods

    # Public class methods
    def get_reactance(self, at_frequency: int):
        self.__reactance_value = 2 * np.pi * at_frequency * self.__inductance_value

        return self.__reactance_value

    def get_susceptance(self, at_frequency: int):
        self.__susceptance_value = -1 / (2 * np.pi * at_frequency * self.__inductance_value)

        return  self.__susceptance_value

    def get_impedance(self, at_frequency):
        resistance = 0
        reactance = self.get_reactance(at_frequency=at_frequency)

        self.__impedance_value = complex(resistance, reactance)

        return self.__impedance_value

    def get_admittance(self, at_frequency):
        conductance = 0
        susceptance = self.get_susceptance(at_frequency=at_frequency)

        self.__admittance_value = complex(conductance, susceptance)

        return self.__admittance_value


# Definition of the class that represent an impedance.
class Impedance:
    # Private class attributes
    __operation_frequency: int
    __total_impedance: complex

    # Class constructors
    def __init__(self, type_of_element: str = '', with_value: float = 1):
        self.__type_of_element = type_of_element
        self.__element_value = with_value

    # Private class methods

    # Public class methods
    def get_impedance(self, at_frequency):
        self.__operation_frequency = at_frequency

        if self.__type_of_element == 'Resistor':
            resistor = Resistor(resistance_value=self.__element_value)
            self.__total_impedance = resistor.get_impedance()

        elif self.__type_of_element == 'Capacitor':
            capacitor = Capacitor(capacitance_value=self.__element_value)
            self.__total_impedance = capacitor.get_impedance(at_frequency=self.__operation_frequency)

        elif self.__type_of_element == 'Inductor':
            inductor = Inductor(inductance_value=self.__element_value)
            self.__total_impedance = inductor.get_impedance(at_frequency=self.__operation_frequency)

        else:
            self.__total_impedance = complex(0,0)

        return self.__total_impedance


# Definition of the class that represent an admittance.
class Admittance:
    # Class attributes
    __operation_frequency: int
    __total_admittance: complex

    # Class constructors
    def __init__(self, type_of_element: str = '', with_value: float = 1):
        self.__type_of_element = type_of_element
        self.__element_value = with_value

    # Private class methods

    # Public class methods
    def get_admittance(self, at_frequency):
        self.__operation_frequency = at_frequency

        if self.__type_of_element == 'Resistor':
            resistor = Resistor(resistance_value=self.__element_value)
            self.__total_admittance = resistor.get_admittance()

        elif self.__type_of_element == 'Capacitor':
            capacitor = Capacitor(capacitance_value=self.__element_value)
            self.__total_admittance = capacitor.get_admittance(at_frequency=self.__operation_frequency)

        elif self.__type_of_element == 'Inductor':
            inductor = Inductor(inductance_value=self.__element_value)
            self.__total_admittance = inductor.get_admittance(at_frequency=self.__operation_frequency)

        else:
            self.__total_admittance = complex(0,0)

        return self.__total_admittance