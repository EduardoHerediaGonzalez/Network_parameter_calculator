import numpy as np
from numpy.matrixlib.defmatrix import matrix

def get_parameters_and_delta_from_matrix(x_matrix: matrix):
    _matrix = x_matrix.tolist()
    matrix_row_1 = _matrix[0]
    matrix_row_2 = _matrix[1]

    parameter_11 = matrix_row_1[0]
    parameter_12 = matrix_row_1[1]
    parameter_21 = matrix_row_2[0]
    parameter_22 = matrix_row_2[1]

    delta = (parameter_11 * parameter_22) - (parameter_12 * parameter_21)

    return parameter_11, parameter_12, parameter_21, parameter_22, delta

def convert_ABCD_matrix_to_Z_matrix(abcd_matrix: matrix):
    parameter_a, parameter_b, parameter_c, parameter_d, delta_abcd = get_parameters_and_delta_from_matrix(abcd_matrix)

    parameter_z11 = parameter_a / parameter_c
    parameter_z12 = delta_abcd / parameter_c
    parameter_z21 = 1 / parameter_c
    parameter_z22 = parameter_d / parameter_c

    Z_matrix = np.matrix([[parameter_z11, parameter_z12],[parameter_z21, parameter_z22]])

    return Z_matrix

def convert_ABCD_matrix_to_Y_matrix(abcd_matrix: matrix):
    parameter_a, parameter_b, parameter_c, parameter_d, delta_abcd = get_parameters_and_delta_from_matrix(abcd_matrix)

    parameter_y11 = parameter_d / parameter_b
    parameter_y12 = -delta_abcd / parameter_b
    parameter_y21 = -1 / parameter_b
    parameter_y22 = parameter_a / parameter_b

    Y_matrix = np.matrix([[parameter_y11, parameter_y12], [parameter_y21, parameter_y22]])

    return Y_matrix

def convert_ABCD_matrix_to_S_matrix(abcd_matrix: matrix, z_0: complex):
    parameter_a, parameter_b, parameter_c, parameter_d, delta_abcd = get_parameters_and_delta_from_matrix(abcd_matrix)
    psi = parameter_a + (parameter_b / z_0) + (parameter_c * z_0) + parameter_d

    parameter_s11 =  (parameter_a + (parameter_b / z_0) - (parameter_c * z_0) - parameter_d) / psi
    parameter_s12 =  (2 * delta_abcd) / psi
    parameter_s21 =  2 / psi
    parameter_s22 = (-parameter_a + (parameter_b / z_0) - (parameter_c * z_0) + parameter_d) / psi

    S_matrix = np.matrix([[parameter_s11, parameter_s12], [parameter_s21, parameter_s22]])

    return S_matrix

def convert_Z_matrix_to_ABCD_matrix(z_matrix: matrix):
    parameter_z11, parameter_z12, parameter_z21, parameter_z22, delta_z = get_parameters_and_delta_from_matrix(z_matrix)

    parameter_a =  parameter_z11 / parameter_z21
    parameter_b =  delta_z / parameter_z21
    parameter_c =  1 / parameter_z21
    parameter_d = parameter_z22 / parameter_z21

    ABCD_matrix = np.matrix([[parameter_a, parameter_b], [parameter_c, parameter_d]])

    return ABCD_matrix

def convert_Y_matrix_to_ABCD_matrix(y_matrix: matrix):
    parameter_y11, parameter_y12, parameter_y21, parameter_y22, delta_y = get_parameters_and_delta_from_matrix(y_matrix)

    parameter_a =  -parameter_y22 / parameter_y21
    parameter_b =  -1 / parameter_y21
    parameter_c =  -delta_y / parameter_y21
    parameter_d = -parameter_y11 / parameter_y21

    abcd_matrix = np.matrix([[parameter_a, parameter_b], [parameter_c, parameter_d]])

    return abcd_matrix