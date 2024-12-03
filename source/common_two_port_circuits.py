from numpy.matrixlib.defmatrix import matrix
from source.passive_components import *

# Definition of the class that represents a series impedance circuit
class SeriesImpedanceCircuit:
    # Private class attributes
    __parameter_a = 1
    __parameter_b: complex
    __parameter_c = 0
    __parameter_d = 1
    __matrix_abcd: matrix
    __impedance: Impedance

    # Class constructors
    def __init__(self, type_of_element : str = '', element_value : float = 0):
        self.__impedance = Impedance(type_of_element=type_of_element, with_value=element_value)

    # Public class methods
    def get_ABCD_matrix(self, at_frequency):
        self.__matrix_abcd = np.matrix([[self.__parameter_a, self.__impedance.get_impedance(at_frequency=at_frequency)], [self.__parameter_c, self.__parameter_d]])

        return self.__matrix_abcd

# Definition of the class that represents a shunt impedance circuit
class ShuntImpedanceCircuit:
    # Private class attributes
    __parameter_a = 1
    __parameter_b = 0
    __parameter_c: complex
    __parameter_d = 1
    __matrix_abcd: matrix
    __admittance: Admittance

    # Class constructors
    def __init__(self, type_of_element : str = '', element_value : float = 0):
        self.__admittance = Admittance(type_of_element=type_of_element, with_value=element_value)

    # Public class methods
    def get_ABCD_matrix(self, at_frequency):
        self.__matrix_abcd = np.matrix([[self.__parameter_a, self.__parameter_b], [self.__admittance.get_admittance(at_frequency=at_frequency), self.__parameter_d]])

        return self.__matrix_abcd

# Definition of the class that represents a T circuit
class TCircuit:
    # Private class attributes
    __parameter_a: complex
    __parameter_b: complex
    __parameter_c: complex
    __parameter_d: complex
    __matrix_abcd: matrix
    __impedance_a: Impedance
    __impedance_b: Impedance
    __impedance_c: Impedance

    # Class constructors
    def __init__(self, type_of_element_a : str = '', element_a_value : float = 0,
                 type_of_element_b : str = '', element_b_value : float = 0,
                 type_of_element_c : str = '', element_c_value : float = 0):
        self.__impedance_a = Impedance(type_of_element=type_of_element_a, with_value=element_a_value)
        self.__impedance_b = Impedance(type_of_element=type_of_element_b, with_value=element_b_value)
        self.__impedance_c = Impedance(type_of_element=type_of_element_c, with_value=element_c_value)

    # Private class methods
    def __get_parameter_a(self, at_frequency):
        impedance_z_a = self.__impedance_a.get_impedance(at_frequency=at_frequency)
        impedance_z_c = self.__impedance_c.get_impedance(at_frequency=at_frequency)

        self.__parameter_a = 1 + (impedance_z_a / impedance_z_c)

        return self.__parameter_a

    def __get_parameter_b(self, at_frequency):
        impedance_z_a = self.__impedance_a.get_impedance(at_frequency=at_frequency)
        impedance_z_b = self.__impedance_b.get_impedance(at_frequency=at_frequency)
        impedance_z_c = self.__impedance_c.get_impedance(at_frequency=at_frequency)

        self.__parameter_b = impedance_z_a + impedance_z_b + ((impedance_z_a * impedance_z_b) / impedance_z_c)

        return self.__parameter_b

    def __get_parameter_c(self, at_frequency):
        impedance_z_c = self.__impedance_c.get_impedance(at_frequency=at_frequency)

        self.__parameter_c = 1 / impedance_z_c

        return self.__parameter_c

    def __get_parameter_d(self, at_frequency):
        impedance_z_b = self.__impedance_b.get_impedance(at_frequency=at_frequency)
        impedance_z_c = self.__impedance_c.get_impedance(at_frequency=at_frequency)

        self.__parameter_d = 1 + (impedance_z_b / impedance_z_c)

        return self.__parameter_d

    # Public class methods
    def get_ABCD_matrix(self, at_frequency):
        parameter_a = self.__get_parameter_a(at_frequency=at_frequency)
        parameter_b = self.__get_parameter_b(at_frequency=at_frequency)
        parameter_c = self.__get_parameter_c(at_frequency=at_frequency)
        parameter_d = self.__get_parameter_d(at_frequency=at_frequency)

        self.__matrix_abcd = np.matrix([[parameter_a, parameter_b],[parameter_c, parameter_d]])

        return self.__matrix_abcd

# Definition of the class that represents a Pi circuit
class PiCircuit:
    # Private class attributes
    __parameter_a: complex
    __parameter_b: complex
    __parameter_c: complex
    __parameter_d: complex
    __matrix_abcd: matrix
    __admittance_a: Admittance
    __admittance_b: Admittance
    __admittance_c: Admittance

    # Class constructors
    def __init__(self, type_of_element_a : str = '', element_a_value : float = 0,
                 type_of_element_b : str = '', element_b_value : float = 0,
                 type_of_element_c : str = '', element_c_value : float = 0):
        self.__admittance_a = Admittance(type_of_element=type_of_element_a, with_value=element_a_value)
        self.__admittance_b = Admittance(type_of_element=type_of_element_b, with_value=element_b_value)
        self.__admittance_c = Admittance(type_of_element=type_of_element_c, with_value=element_c_value)

    # Private class methods
    def __get_parameter_a(self, at_frequency):
        admittance_y_b = self.__admittance_b.get_admittance(at_frequency=at_frequency)
        admittance_y_c = self.__admittance_c.get_admittance(at_frequency=at_frequency)

        self.__parameter_a = 1 + (admittance_y_b / admittance_y_c)

        return self.__parameter_a

    def __get_parameter_b(self, at_frequency):
        admittance_y_c = self.__admittance_c.get_admittance(at_frequency=at_frequency)

        self.__parameter_b = 1 / admittance_y_c

        return self.__parameter_b

    def __get_parameter_c(self, at_frequency):
        admittance_y_a = self.__admittance_a.get_admittance(at_frequency=at_frequency)
        admittance_y_b = self.__admittance_b.get_admittance(at_frequency=at_frequency)
        admittance_y_c = self.__admittance_c.get_admittance(at_frequency=at_frequency)

        self.__parameter_c = admittance_y_a + admittance_y_b + ((admittance_y_a * admittance_y_b) / admittance_y_c)

        return self.__parameter_c

    def __get_parameter_d(self, at_frequency):
        admittance_y_a = self.__admittance_a.get_admittance(at_frequency=at_frequency)
        admittance_y_c = self.__admittance_c.get_admittance(at_frequency=at_frequency)

        self.__parameter_d = 1 + (admittance_y_a / admittance_y_c)

        return self.__parameter_d

    # Public class methods
    def get_ABCD_matrix(self, at_frequency):
        self.__matrix_abcd = np.matrix(
            [[self.__get_parameter_a(at_frequency=at_frequency), self.__get_parameter_b(at_frequency=at_frequency)],
             [self.__get_parameter_c(at_frequency=at_frequency), self.__get_parameter_d(at_frequency=at_frequency)]],
            dtype=complex)

        return self.__matrix_abcd

# Definition of the class that represents a Transmission line circuit
class TransmissionLineCircuit:
    # Private class attributes
    __parameter_a: complex
    __parameter_b: complex
    __parameter_c: complex
    __parameter_d: complex
    __matrix_abcd: matrix
    __line_length: float
    __characteristic_impedance: float
    __phase_constant: float

    # Class constructors
    def __init__(self, line_length: float = 0, characteristic_impedance: float = 50):
        self.__line_length = line_length
        self.__characteristic_impedance = characteristic_impedance

    # Private class methods
    def __get_phase_constant(self, at_frequency):
        self.__phase_constant = (2 * np.pi * at_frequency) / 3e8

        return self.__phase_constant

    def __get_electrical_length(self, at_frequency):
        electrical_length = self.__get_phase_constant(at_frequency=at_frequency) * self.__line_length

        return electrical_length

    def __get_parameter_a(self, at_frequency):
        self.__parameter_a = complex(np.cos(self.__get_electrical_length(at_frequency=at_frequency)), 0)

        return self.__parameter_a

    def __get_parameter_b(self, at_frequency):
        self.__parameter_b = complex(0, (self.__characteristic_impedance * np.sin(self.__get_electrical_length(at_frequency=at_frequency))))

        return self.__parameter_b

    def __get_parameter_c(self, at_frequency):
        self.__parameter_c = complex(0, (np.sin(self.__get_electrical_length(at_frequency=at_frequency)) / self.__characteristic_impedance))

        return self.__parameter_c

    def __get_parameter_d(self, at_frequency):
        self.__parameter_d = complex(np.cos(self.__get_electrical_length(at_frequency=at_frequency)), 0)

        return self.__parameter_d

    # Public class methods
    def get_ABCD_matrix(self, at_frequency):
        self.__matrix_abcd = np.matrix(
            [[self.__get_parameter_a(at_frequency=at_frequency), self.__get_parameter_b(at_frequency=at_frequency)],
             [self.__get_parameter_c(at_frequency=at_frequency), self.__get_parameter_d(at_frequency=at_frequency)]],
            dtype=complex)

        return self.__matrix_abcd

# Definition of the class that represents an Open stub circuit
class OpenStubCircuit:
    # Private class attributes
    __parameter_a = 1
    __parameter_b = 0
    __parameter_c: complex
    __parameter_d = 1
    __matrix_abcd: matrix
    __line_length: float
    __characteristic_impedance: float
    __phase_constant: float

    # Class constructors
    def __init__(self, line_length: float = 0, characteristic_impedance: float = 50):
        self.__line_length = line_length
        self.__characteristic_impedance = characteristic_impedance

    # Private class methods
    def __get_phase_constant(self, at_frequency):
        self.__phase_constant = (2 * np.pi * at_frequency) / 3e8

        return self.__phase_constant

    def __get_electrical_length(self, at_frequency):
        electrical_length = self.__get_phase_constant(at_frequency=at_frequency) * self.__line_length

        return electrical_length

    def __get_parameter_c(self, at_frequency):
        self.__parameter_c = complex(0, (1 / (self.__characteristic_impedance * (1 / np.tan(self.__get_electrical_length(at_frequency=at_frequency))))))

        return self.__parameter_c

    # Public class methods
    def get_ABCD_matrix(self, at_frequency):
        self.__matrix_abcd = np.matrix([[self.__parameter_a, self.__parameter_b], [self.__get_parameter_c(at_frequency=at_frequency), self.__parameter_d]])

        return self.__matrix_abcd

# Definition of the class that represents a Short stub circuit
class ShortStubCircuit:
    # Private class attributes
    __parameter_a = 1
    __parameter_b = 0
    __parameter_c: complex
    __parameter_d = 1
    __matrix_abcd: matrix
    __line_length: float
    __characteristic_impedance: float
    __phase_constant: float

    # Class constructors
    def __init__(self, line_length: float = 0, characteristic_impedance: float = 50):
        self.__line_length = line_length
        self.__characteristic_impedance = characteristic_impedance

    # Private class methods
    def __get_phase_constant(self, at_frequency):
        self.__phase_constant = (2 * np.pi * at_frequency) / 3e8

        return self.__phase_constant

    def __get_electrical_length(self, at_frequency):
        electrical_length = self.__get_phase_constant(at_frequency=at_frequency) * self.__line_length

        return electrical_length

    def __get_parameter_c(self, at_frequency):
        self.__parameter_c = complex(0, (-1 / (self.__characteristic_impedance * np.tan(self.__get_electrical_length(at_frequency=at_frequency)))))
        return self.__parameter_c

    # Public class methods
    def get_ABCD_matrix(self, at_frequency):
        self.__matrix_abcd = np.matrix([[self.__parameter_a, self.__parameter_b], [self.__get_parameter_c(at_frequency=at_frequency), self.__parameter_d]])

        return self.__matrix_abcd