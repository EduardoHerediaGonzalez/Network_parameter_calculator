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

    # Class constructors
    def __init__(self, type_of_element : str = '', element_value : float = 0):
        self.impedance = Impedance(type_of_element=type_of_element, with_value=element_value)

    # Private class methods

    # Public class methods
    def get_parameter_a(self):
        return self.__parameter_a

    def get_parameter_b(self, at_frequency):
        self.__parameter_b = self.impedance.get_impedance(at_frequency=at_frequency)
        return self.__parameter_b

    def get_parameter_c(self):
        return self.__parameter_c

    def get_parameter_d(self):
        return self.__parameter_d

    def get_delta_abcd(self, at_frequency):
        self.__parameter_b = self.impedance.get_impedance(at_frequency=at_frequency)
        self.__delta_abcd = (self.__parameter_a * self.__parameter_d) - (self.__parameter_b * self.__parameter_c)

        return  self.__delta_abcd

    def get_matrix(self, at_frequency):
        self.__parameter_b = self.impedance.get_impedance(at_frequency=at_frequency)
        self.__matrix_abcd = np.matrix([[self.__parameter_a, self.__parameter_b] , [self.__parameter_c, self.__parameter_d.real]], dtype=complex)

        return self.__matrix_abcd
