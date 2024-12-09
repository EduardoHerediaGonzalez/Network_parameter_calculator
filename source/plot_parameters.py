import matplotlib.pyplot as plt
import skrf as rf
import source.config_parameters as cfg

from source.network_parameter_conversions import *

labels = {"ABCD": ["A", "B", "C", "D"],
          "Z": ["Z(1,1)", "Z(1,2)", "Z(2,1)", "Z(2,2)"],
          "Y": ["Y(1,1)", "Y(1,2)", "Y(2,1)", "Y(2,2)"],
          "S": ["S(1,1)", "S(1,2)", "S(2,1)", "S(2,2)"]}

def plot_dB_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):
    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    parameter_a_db = [magnitude_in_db(A) for A in parameter_a]
    parameter_b_db = [magnitude_in_db(B) for B in parameter_b]
    parameter_c_db = [magnitude_in_db(C) for C in parameter_c]
    parameter_d_db = [magnitude_in_db(D) for D in parameter_d]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"dB vs Freq ({type_of_parameters} Parameters)", fontsize=16)

    axs[0, 0].plot(frequencies, parameter_a_db, color="red")
    axs[0, 0].set_ylabel(f"dB({label_a})")
    axs[0, 0].set_xlabel("Freq, Hz")
    axs[0, 0].grid()

    axs[0, 1].plot(frequencies, parameter_b_db, color="red")
    axs[0, 1].set_ylabel(f"dB({label_b})")
    axs[0, 1].set_xlabel("Freq, Hz")
    axs[0, 1].grid()

    axs[1, 0].plot(frequencies, parameter_c_db, color="red")
    axs[1, 0].set_ylabel(f"dB({label_c})")
    axs[1, 0].set_xlabel("Freq, Hz")
    axs[1, 0].grid()

    axs[1, 1].plot(frequencies, parameter_d_db, color="red")
    axs[1, 1].set_ylabel(f"dB({label_d})")
    axs[1, 1].set_xlabel("Freq, Hz")
    axs[1, 1].grid()

    parameter_a_db.clear()
    parameter_b_db.clear()
    parameter_c_db.clear()
    parameter_d_db.clear()

    plt.show()

def plot_phase_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):
    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    phase_a = [phase_in_degrees(x) for x in parameter_a]
    phase_b = [phase_in_degrees(x) for x in parameter_b]
    phase_c = [phase_in_degrees(x) for x in parameter_c]
    phase_d = [phase_in_degrees(x) for x in parameter_d]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Phase vs Freq ({type_of_parameters} Parameters)", fontsize=16)

    axs[0, 0].plot(frequencies, phase_a, color="red")
    axs[0, 0].set_ylabel(f"Phase({label_a})")
    axs[0, 0].set_xlabel("Freq, Hz")
    axs[0, 0].grid()

    axs[0, 1].plot(frequencies, phase_b, color="red")
    axs[0, 1].set_ylabel(f"Phase ({label_b})")
    axs[0, 1].set_xlabel("Freq, Hz")
    axs[0, 1].grid()

    axs[1, 0].plot(frequencies, phase_c, color="red")
    axs[1, 0].set_ylabel(f"Phase ({label_c})")
    axs[1, 0].set_xlabel("Freq, Hz")
    axs[1, 0].grid()

    axs[1, 1].plot(frequencies, phase_d, color="red")
    axs[1, 1].set_ylabel(f"Phase ({label_d})")
    axs[1, 1].set_xlabel("Freq, Hz")
    axs[1, 1].grid()

    phase_a.clear()
    phase_b.clear()
    phase_c.clear()
    phase_d.clear()

    plt.show()

def plot_real_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):
    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    real_a = extract_real_part(parameter_a)
    real_b = extract_real_part(parameter_b)
    real_c = extract_real_part(parameter_c)
    real_d = extract_real_part(parameter_d)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Real vs Freq ({type_of_parameters} Parameters)", fontsize=16)

    axs[0, 0].plot(frequencies, real_a, color="red")
    axs[0, 0].set_ylabel(f"Real({label_a})")
    axs[0, 0].set_xlabel("Freq, Hz")
    axs[0, 0].grid()

    axs[0, 1].plot(frequencies, real_b, color="red")
    axs[0, 1].set_ylabel(f"Real({label_b})")
    axs[0, 1].set_xlabel("Freq, Hz")
    axs[0, 1].grid()

    axs[1, 0].plot(frequencies, real_c, color="red")
    axs[1, 0].set_ylabel(f"Real({label_c})")
    axs[1, 0].set_xlabel("Freq, Hz")
    axs[1, 0].grid()

    axs[1, 1].plot(frequencies, real_d, color="red")
    axs[1, 1].set_ylabel(f"Real({label_d})")
    axs[1, 1].set_xlabel("Freq, Hz")
    axs[1, 1].grid()

    real_a.clear()
    real_b.clear()
    real_c.clear()
    real_d.clear()

    plt.show()

def plot_imag_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):
    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    imag_a = extract_imag_part(parameter_a)
    imag_b = extract_imag_part(parameter_b)
    imag_c = extract_imag_part(parameter_c)
    imag_d = extract_imag_part(parameter_d)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Imag vs Freq ({type_of_parameters} Parameters)", fontsize=16)

    axs[0, 0].plot(frequencies, imag_a, color="red")
    axs[0, 0].set_ylabel(f"Imag({label_a})")
    axs[0, 0].set_xlabel("Freq, Hz")
    axs[0, 0].grid()

    axs[0, 1].plot(frequencies, imag_b, color="red")
    axs[0, 1].set_ylabel(f"Imag({label_b})")
    axs[0, 1].set_xlabel("Freq, Hz")
    axs[0, 1].grid()

    axs[1, 0].plot(frequencies, imag_c, color="red")
    axs[1, 0].set_ylabel(f"Imag({label_c})")
    axs[1, 0].set_xlabel("Freq, Hz")
    axs[1, 0].grid()

    axs[1, 1].plot(frequencies, imag_d, color="red")
    axs[1, 1].set_ylabel(f"Imag({label_d})")
    axs[1, 1].set_xlabel("Freq, Hz")
    axs[1, 1].grid()

    imag_a.clear()
    imag_b.clear()
    imag_c.clear()
    imag_d.clear()

    plt.show()

def plot_polar(parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):
    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    magnitude_a = np.abs(parameter_a)
    phase_a = np.angle(parameter_a, deg=True)

    magnitude_b = np.abs(parameter_b)
    phase_b = np.angle(parameter_b, deg=True)

    magnitude_c = np.abs(parameter_c)
    phase_c = np.angle(parameter_c, deg=True)

    magnitude_d = np.abs(parameter_d)
    phase_d = np.angle(parameter_d, deg=True)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8), subplot_kw={'projection': 'polar'})
    fig.suptitle(f"Polar ({type_of_parameters} Parameters)", fontsize=16)

    axs[0, 0].plot(np.radians(phase_a), magnitude_a, color="red")
    axs[0, 0].set_ylabel(f"{label_c}")
    axs[0, 0].grid(True)


    axs[0, 1].plot(np.radians(phase_b), magnitude_b, color="red")
    axs[0, 1].set_ylabel(f"{label_b}")
    axs[0, 1].grid(True)

    axs[1, 0].plot(np.radians(phase_c), magnitude_c, color="red")
    axs[1, 0].set_ylabel(f"{label_c}")
    axs[1, 0].grid(True)

    axs[1, 1].plot(np.radians(phase_d), magnitude_d, color="red")
    axs[1, 1].set_ylabel(f"{label_d}")
    axs[1, 1].grid(True)

    plt.show()

def plot_smith_chart(parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters, z_0=cfg.CHARACTERISTIC_IMPEDANCE_50_OHMS):
    s_parameters_a = parameter_a
    s_parameters_b = parameter_b
    s_parameters_c = parameter_c
    s_parameters_d = parameter_d

    if type_of_parameters != "S":
        for a, b, c, d in zip(parameter_a, parameter_b, parameter_c, parameter_d):

            if type_of_parameters == "ABCD":
                matrix_abcd = np.matrix([[a, b], [c, d]])
                s_matrix = convert_ABCD_matrix_to_S_matrix(matrix_abcd, z_0)

                s_parameters_a.append(s_matrix[0, 0])  # S11
                s_parameters_b.append(s_matrix[0, 1])  # S12
                s_parameters_c.append(s_matrix[1, 0])  # S21
                s_parameters_d.append(s_matrix[1, 1])  # S22

            elif type_of_parameters == "Z":
                matrix_z = np.matrix([[a, b], [c, d]])
                abcd_matrix = convert_Z_matrix_to_ABCD_matrix(matrix_z)
                s_matrix = convert_ABCD_matrix_to_S_matrix(abcd_matrix, z_0)

                s_parameters_a.append(s_matrix[0, 0])  # S11
                s_parameters_b.append(s_matrix[0, 1])  # S12
                s_parameters_c.append(s_matrix[1, 0])  # S21
                s_parameters_d.append(s_matrix[1, 1])  # S22

            elif type_of_parameters == "Y":
                matrix_y = np.matrix([[a, b], [c, d]])
                abcd_matrix = convert_Y_matrix_to_ABCD_matrix(matrix_y)
                s_matrix = convert_ABCD_matrix_to_S_matrix(abcd_matrix, z_0)

                s_parameters_a.append(s_matrix[0, 0])  # S11
                s_parameters_b.append(s_matrix[0, 1])  # S12
                s_parameters_c.append(s_matrix[1, 0])  # S21
                s_parameters_d.append(s_matrix[1, 1])  # S22

    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Smith Chart ({type_of_parameters} Parameters)", fontsize=16)

    ax = axs[0, 0]
    rf.plotting.plot_smith(s=np.array(s_parameters_a), ax=ax, color="red", x_label='', y_label='', title='')
    axs[0, 0].set_ylabel(f"{label_a}")

    ax = axs[0, 1]
    rf.plotting.plot_smith(s=np.array(s_parameters_b), ax=ax, color="red", x_label='', y_label='', title='')
    axs[0, 1].set_ylabel(f"{label_b}")

    ax = axs[1, 0]
    rf.plotting.plot_smith(s=np.array(s_parameters_c), ax=ax, color="red", x_label='', y_label='', title='')
    axs[1, 0].set_ylabel(f"{label_c}")

    ax = axs[1, 1]
    rf.plotting.plot_smith(s=np.array(s_parameters_d), ax=ax, color="red", x_label='', y_label='', title='')
    axs[1, 1].set_ylabel(f"{label_d}")

    plt.show()

def magnitude_in_db(parameter):
    return 20 * np.log10(np.abs(parameter))

def phase_in_degrees(parameter):
    real_part = np.real(parameter)
    imag_part = np.imag(parameter)
    phase_radians = np.arctan2(imag_part, real_part)
    phase_degrees = (180 * phase_radians) / np.pi

    return phase_degrees

def extract_real_part(parameter):
    real_part = [np.real(x) for x in parameter]

    return real_part

def extract_imag_part(parameter):
    imag_part = [np.imag(x) for x in parameter]

    return imag_part