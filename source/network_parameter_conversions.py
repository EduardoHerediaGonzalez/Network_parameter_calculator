import numpy as np
from numpy.matrixlib.defmatrix import matrix

def convert_abcd_parameters_to_z_parameters(matrix_abcd: matrix, delta: complex):
    matrix_abcd = matrix_abcd.tolist()
    matrix_abcd_row_1 = matrix_abcd[0]
    matrix_abcd_row_2 = matrix_abcd[1]

    parameter_a = matrix_abcd_row_1[0]
    parameter_c = matrix_abcd_row_2[0]
    parameter_d = matrix_abcd_row_2[1]

    parameter_z11 = parameter_a / parameter_c
    parameter_z12 = delta / parameter_c
    parameter_z21 = 1 / parameter_c
    parameter_z22 = parameter_d / parameter_c

    z_parameters_matrix = np.matrix[[parameter_z11, parameter_z12],[parameter_z21, parameter_z22]]

    return z_parameters_matrix

def convert_abcd_parameters_to_y_parameters(matrix_abcd: matrix, delta: complex):
    matrix_abcd = matrix_abcd.tolist()
    matrix_abcd_row_1 = matrix_abcd[0]
    matrix_abcd_row_2 = matrix_abcd[1]

    parameter_a = matrix_abcd_row_1[0]
    parameter_b = matrix_abcd_row_1[1]
    parameter_d = matrix_abcd_row_2[1]

    parameter_y11 = parameter_d / parameter_b
    parameter_y12 = -delta / parameter_b
    parameter_y21 = -1 / parameter_b
    parameter_y22 = parameter_a / parameter_d

    y_parameters_matrix = np.matrix[[parameter_y11, parameter_y12], [parameter_y21, parameter_y22]]

    return y_parameters_matrix

def convert_abcd_parameters_to_s_parameters(matrix_abcd: matrix, delta: complex, z_0: complex):
    matrix_abcd = matrix_abcd.tolist()
    matrix_abcd_row_1 = matrix_abcd[0]
    matrix_abcd_row_2 = matrix_abcd[1]

    parameter_a = matrix_abcd_row_1[0]
    parameter_b = matrix_abcd_row_1[1]
    parameter_c = matrix_abcd_row_2[0]
    parameter_d = matrix_abcd_row_2[1]

    parameter_s11 = (parameter_a * z_0 + parameter_b - parameter_c * z_0 ** 2 - parameter_d * z_0) / (parameter_a * z_0 + parameter_b + parameter_c * z_0 ** 2 + parameter_d * z_0)
    parameter_s12 = (2 * delta * z_0) / (parameter_a * z_0 + parameter_b + parameter_c * z_0 ** 2 + parameter_d * z_0)
    parameter_s21 = 2 * z_0 / (parameter_a * z_0 + parameter_b + parameter_c * z_0 ** 2 + parameter_d * z_0)
    parameter_s22 = (- parameter_a * z_0 + parameter_b - parameter_c * z_0 ** 2 + parameter_d * z_0) / (parameter_a * z_0 + parameter_b + parameter_c * z_0 ** 2 + parameter_d * z_0)

    s_parameters_matrix = np.matrix[[parameter_s11, parameter_s12], [parameter_s21, parameter_s22]]

    return s_parameters_matrix