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

    z_parameters_matrix = np.matrix[[parameter_z11, parameter_z12],[parameter_z21, parameter_z22]]

    return z_parameters_matrix

def convert_abcd_parameters_to_y_parameters(matrix_abcd: matrix, delta: complex):
    parameter_a, parameter_b, parameter_c, parameter_d, delta_abcd = get_parameters_and_delta(matrix_abcd)

    parameter_y11 = parameter_d / parameter_b
    parameter_y12 = -delta_abcd / parameter_b
    parameter_y21 = -1 / parameter_b
    parameter_y22 = parameter_a / parameter_d

    y_parameters_matrix = np.matrix[[parameter_y11, parameter_y12], [parameter_y21, parameter_y22]]

    return y_parameters_matrix

def convert_abcd_parameters_to_s_parameters(matrix_abcd: matrix, z_0: complex):
    parameter_a, parameter_b, parameter_c, parameter_d, delta_abcd = get_parameters_and_delta(matrix_abcd)
    psi = parameter_a + (parameter_b / z_0) + (parameter_c * z_0) + parameter_d

    parameter_s11 =  (parameter_a + (parameter_b / z_0) - (parameter_c * z_0) - parameter_d) / psi
    parameter_s12 =  (2 * delta_abcd) / psi
    parameter_s21 =  2 / psi
    parameter_s22 = (-parameter_a + (parameter_b / z_0) - (parameter_c * z_0) + parameter_d) / psi

    s_parameters_matrix = np.matrix[[parameter_s11, parameter_s12], [parameter_s21, parameter_s22]]

    return s_parameters_matrix