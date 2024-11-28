import numpy as np
from numpy.matrixlib.defmatrix import matrix

def get_parameters_and_delta(matrix_x: matrix):
    _matrix = matrix_x.tolist()
    matrix_row_1 = _matrix[0]
    matrix_row_2 = _matrix[1]

    parameter_11 = matrix_row_1[0]
    parameter_12 = matrix_row_1[1]
    parameter_21 = matrix_row_2[0]
    parameter_22 = matrix_row_2[1]

    delta = (parameter_11 * parameter_22) - (parameter_12 * parameter_21)

    return parameter_11, parameter_12, parameter_21, parameter_22, delta

def convert_abcd_parameters_to_z_parameters(matrix_abcd: matrix):
    parameter_a, parameter_b, parameter_c, parameter_d, delta_abcd = get_parameters_and_delta(matrix_abcd)

    parameter_z11 = parameter_a / parameter_c
    parameter_z12 = delta_abcd / parameter_c
    parameter_z21 = 1 / parameter_c
    parameter_z22 = parameter_d / parameter_c

    z_parameters_matrix = np.matrix([[parameter_z11, parameter_z12],[parameter_z21, parameter_z22]])

    return z_parameters_matrix

def convert_abcd_parameters_to_y_parameters(matrix_abcd: matrix):
    parameter_a, parameter_b, parameter_c, parameter_d, delta_abcd = get_parameters_and_delta(matrix_abcd)

    parameter_y11 = parameter_d / parameter_b
    parameter_y12 = -delta_abcd / parameter_b
    parameter_y21 = -1 / parameter_b
    parameter_y22 = parameter_a / parameter_d

    y_parameters_matrix = np.matrix([[parameter_y11, parameter_y12], [parameter_y21, parameter_y22]])

    return y_parameters_matrix

def convert_abcd_parameters_to_s_parameters(matrix_abcd: matrix, z_0: complex):
    parameter_a, parameter_b, parameter_c, parameter_d, delta_abcd = get_parameters_and_delta(matrix_abcd)
    psi = parameter_a + (parameter_b / z_0) + (parameter_c * z_0) + parameter_d

    parameter_s11 =  (parameter_a + (parameter_b / z_0) - (parameter_c * z_0) - parameter_d) / psi
    parameter_s12 =  (2 * delta_abcd) / psi
    parameter_s21 =  2 / psi
    parameter_s22 = (-parameter_a + (parameter_b / z_0) - (parameter_c * z_0) + parameter_d) / psi

    s_parameters_matrix = np.matrix([[parameter_s11, parameter_s12], [parameter_s21, parameter_s22]])

    return s_parameters_matrix

def convert_z_parameters_to_abcd_parameters(z_matrix: matrix):
    parameter_z11, parameter_z12, parameter_z21, parameter_z22, delta_z = get_parameters_and_delta(z_matrix)

    parameter_a =  parameter_z11 / parameter_z21
    parameter_b =  delta_z / parameter_z21
    parameter_c =  1 / parameter_z21
    parameter_d = parameter_z22 / parameter_z21

    abcd_parameters_matrix = np.matrix([[parameter_a, parameter_b], [parameter_c, parameter_d]])

    return abcd_parameters_matrix

def convert_y_parameters_to_abcd_parameters(y_matrix: matrix):
    parameter_y11, parameter_y12, parameter_y21, parameter_y22, delta_y = get_parameters_and_delta(y_matrix)

    parameter_a =  -parameter_y22 / parameter_y21
    parameter_b =  -1 / parameter_y21
    parameter_c =  -delta_y / parameter_y21
    parameter_d = -parameter_y11 / parameter_y21

    abcd_parameters_matrix = np.matrix([[parameter_a, parameter_b], [parameter_c, parameter_d]])

    return abcd_parameters_matrix

def convert_series_sub_networks(sub_networks: list, series_sub_networks_indexes: list, frequency: float):
    z_parameters_matrix = np.matrix[[0, 0],[0, 0]]

    for series_sub_network_index in series_sub_networks_indexes:
        abcd_matrix = sub_networks[series_sub_network_index].get_matrix_abcd(at_frequency=frequency)
        abcd_to_z_matrix = convert_abcd_parameters_to_z_parameters(abcd_matrix)
        z_parameters_matrix = z_parameters_matrix + abcd_to_z_matrix

    abcd_parameters_matrix = convert_z_parameters_to_abcd_parameters(z_parameters_matrix)

    return abcd_parameters_matrix

def convert_parallel_sub_networks(sub_networks: list, parallel_sub_networks_indexes: list, frequency: float):
    y_parameters_matrix = np.matrix[[0, 0], [0, 0]]

    for parallel_sub_network_index in parallel_sub_networks_indexes:
        abcd_matrix = sub_networks[parallel_sub_network_index].get_matrix_abcd(at_frequency=frequency)
        abcd_to_y_matrix = convert_abcd_parameters_to_z_parameters(abcd_matrix)
        y_parameters_matrix = y_parameters_matrix + abcd_to_y_matrix

    abcd_parameters_matrix = convert_y_parameters_to_abcd_parameters(y_parameters_matrix)

    return abcd_parameters_matrix
