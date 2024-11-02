import numpy as np

# Definition of the class that represents the series impedance circuit of
# a two-port network
##from openpyxl.descriptors import String
class SeriesImpedanceCircuit:
    # Class variables
    __parameter_A = 1
    parameter_B = []
    __parameter_C = 0
    __parameter_D = 1
    __delta_ABCD = 0

    # Class constructors
    def __init__(self, type_of_element : str, element_value : float, frecuencies : list):
        self.type_of_element = type_of_element
        self.element_value = element_value
        self.frecuencies = frecuencies

    # Private class methods
    def __calculate_impedances(self):
        impedance = 0

        for frecuency in self.frecuencies:
            if self.type_of_element == 'Inductor':
                impedance = 2 * np.pi * int(frecuency) * self.element_value
                self.parameter_B.append(impedance)

            elif self.type_of_element == 'Capacitor':
                impedance = 1 / (2 * np.pi * int(frecuency) * self.element_value)
                self.parameter_B.append(impedance)

            else:
                self.parameter_B = 1

    # Public class methods
    def get_type_of_element(self):
        return self.type_of_element

    def get_element_value(self):
        return self.element_value

    def get_frecuencies_list(self):
        return self.frecuencies


network_A = SeriesImpedanceCircuit(type_of_element='Resistor', element_value=100, frecuencies=['100','200','500'])
print(network_A.get_type_of_element())
print(network_A.get_element_value())
print(network_A.parameter_B)