from numpy.matrixlib.defmatrix import matrix
from source.passive_components import *

# Definition of the class that represents the series impedance circuit of a two-port network
class SeriesImpedanceCircuit:
    # Private class attributes
    __parameter_a = 1
    __parameter_b: complex
    __parameter_c = 0
    __parameter_d = 1
    __delta_abcd: complex
    __matrix_abcd: matrix
    __impedance: Impedance

    # Class constructors
    def __init__(self, type_of_element : str = '', element_value : float = 0):
        self.__impedance = Impedance(type_of_element=type_of_element, with_value=element_value)

    # Public class methods
    def get_delta_abcd(self, at_frequency):
        self.__delta_abcd = (self.__parameter_a * self.__parameter_d) - (self.__impedance.get_impedance(at_frequency=at_frequency) * self.__parameter_c)

        return  int(self.__delta_abcd.real)

    def get_matrix_abcd(self, at_frequency):
        self.__matrix_abcd = np.matrix([[self.__parameter_a, self.__impedance.get_impedance(at_frequency=at_frequency)], [self.__parameter_c, self.__parameter_d]])

        return self.__matrix_abcd

# Definition of the class that represents the shunt impedance circuit of a two-port network
class ShuntImpedanceCircuit:
    # Private class attributes
    __parameter_a = 1
    __parameter_b = 0
    __parameter_c: complex
    __parameter_d = 1
    __delta_abcd: complex
    __matrix_abcd: matrix
    __admittance: Admittance

    # Class constructors
    def __init__(self, type_of_element : str = '', element_value : float = 0):
        self.__admittance = Admittance(type_of_element=type_of_element, with_value=element_value)

    # Public class methods
    def get_delta_abcd(self, at_frequency):
        self.__delta_abcd = (self.__parameter_a * self.__parameter_d) - (self.__parameter_b * self.__admittance.get_admittance(at_frequency=at_frequency))

        return  int(self.__delta_abcd.real)

    def get_matrix_abcd(self, at_frequency):
        self.__matrix_abcd = np.matrix([[self.__parameter_a, self.__parameter_b], [self.__admittance.get_admittance(at_frequency=at_frequency), self.__parameter_d]])

        return self.__matrix_abcd

# Definition of the class that represents the T circuit of a two-port network
class TCircuit:
    # Private class attributes
    __parameter_a: complex
    __parameter_b: complex
    __parameter_c: complex
    __parameter_d: complex
    __delta_abcd: complex
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
    def get_delta_abcd(self, at_frequency):
        parameter_a = self.__get_parameter_a(at_frequency=at_frequency)
        parameter_b = self.__get_parameter_b(at_frequency=at_frequency)
        parameter_c = self.__get_parameter_c(at_frequency=at_frequency)
        parameter_d = self.__get_parameter_d(at_frequency=at_frequency)

        self.__delta_abcd = (parameter_a * parameter_d) - (parameter_b * parameter_c)

        return  self.__delta_abcd

    def get_matrix_abcd(self, at_frequency):
        parameter_a = self.__get_parameter_a(at_frequency=at_frequency)
        parameter_b = self.__get_parameter_b(at_frequency=at_frequency)
        parameter_c = self.__get_parameter_c(at_frequency=at_frequency)
        parameter_d = self.__get_parameter_d(at_frequency=at_frequency)

        self.__matrix_abcd = np.matrix([[parameter_a, parameter_b],[parameter_c, parameter_d]])

        return self.__matrix_abcd

# Definition of the class that represents the Pi circuit of a two-port network
class PiCircuit:
    # Private class attributes
    __parameter_a: complex
    __parameter_b: complex
    __parameter_c: complex
    __parameter_d: complex
    __delta_abcd: complex
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
    def get_delta_abcd(self, at_frequency):
        self.__delta_abcd = (self.__get_parameter_a(at_frequency=at_frequency) * self.__get_parameter_d(
            at_frequency=at_frequency)) - (self.__get_parameter_b(at_frequency=at_frequency) * self.__get_parameter_c(
            at_frequency=at_frequency))

        return self.__delta_abcd

    def get_matrix_abcd(self, at_frequency):
        self.__matrix_abcd = np.matrix(
            [[self.__get_parameter_a(at_frequency=at_frequency), self.__get_parameter_b(at_frequency=at_frequency)],
             [self.__get_parameter_c(at_frequency=at_frequency), self.__get_parameter_d(at_frequency=at_frequency)]],
            dtype=complex)

        return self.__matrix_abcd