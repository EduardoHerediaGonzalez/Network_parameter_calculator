import matplotlib.pyplot as plt
import skrf as rf

from source.network_parameter_conversions import *

labels = {"ABCD": ("A", "B", "C", "D"),
          "Z": ("z11", "z12", "z21", "z22"),
          "Y": ("y11", "y12", "y21", "y22"),
          "S": ("s11", "s12", "s21", "s22")}

smith_labels = {"ABCD": ["s11 (A)", "s12 (B)", "s21 (C)", "s22 (D)"],
                "Z": ["s11 (z11)", "s12 (z12)", "s21 (z21)", "s22 (z22)"],
                "Y": ["s11 (y11)", "s12 (y12)", "s21 (y21)", "s22 (y22)"],
                "S": ["s11", "s12", "s21", "s22"]}

def plot_magnitude_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):
    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    parameter_a_db = [magnitude_in_db(A) for A in parameter_a]
    parameter_b_db = [magnitude_in_db(B) for B in parameter_b]
    parameter_c_db = [magnitude_in_db(C) for C in parameter_c]
    parameter_d_db = [magnitude_in_db(D) for D in parameter_d]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    fig.suptitle(f"Magnitude in dB vs Frequency ({type_of_parameters} Parameters)", fontsize=16)

    axs[0, 0].plot(frequencies, parameter_a_db, label=f"Magnitude ({label_a})", color="blue")
    axs[0, 0].set_title(f"{label_a}")
    axs[0, 0].set_ylabel("Magnitude (dB)")
    axs[0, 0].grid()

    axs[0, 1].plot(frequencies, parameter_b_db, label=f"Magnitude ({label_b})", color="orange")
    axs[0, 1].set_title(f"{label_b}")
    axs[0, 1].grid()

    axs[1, 0].plot(frequencies, parameter_c_db, label=f"Magnitude ({label_c})", color="green")
    axs[1, 0].set_title(f"{label_c}")
    axs[1, 0].set_xlabel("Frequency (Hz)")
    axs[1, 0].set_ylabel("Magnitude (dB)")
    axs[1, 0].grid()

    axs[1, 1].plot(frequencies, parameter_d_db, label=f"Magnitude ({label_d})", color="red")
    axs[1, 1].set_title(f"{label_d}")
    axs[1, 1].set_xlabel("Frequency (Hz)")
    axs[1, 1].grid()

    plt.show()

def plot_phase_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):
    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    phase_a = [phase_in_degrees(x) for x in parameter_a]
    phase_b = [phase_in_degrees(x) for x in parameter_b]
    phase_c = [phase_in_degrees(x) for x in parameter_c]
    phase_d = [phase_in_degrees(x) for x in parameter_d]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    fig.suptitle("Phase in Degrees vs Frequency", fontsize=16)

    axs[0, 0].plot(frequencies, phase_a, label=f"Phase ({label_a})", color="blue")
    axs[0, 0].set_title(f"{label_a}")
    axs[0, 0].set_ylabel("Phase (°)")
    axs[0, 0].grid()

    axs[0, 1].plot(frequencies, phase_b, label=f"Phase ({label_b})", color="orange")
    axs[0, 1].set_title(f"{label_b}")
    axs[0, 1].grid()

    axs[1, 0].plot(frequencies, phase_c, label=f"Phase ({label_c})", color="green")
    axs[1, 0].set_title(f"{label_c}")
    axs[1, 0].set_xlabel("Frequency (Hz)")
    axs[1, 0].set_ylabel("Phase (°)")
    axs[1, 0].grid()

    axs[1, 1].plot(frequencies, phase_d, label=f"Phase ({label_d})", color="red")
    axs[1, 1].set_title(f"{label_d}")
    axs[1, 1].set_xlabel("Frequency (Hz)")
    axs[1, 1].grid()

    plt.show()

def plot_r_i_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):
    label_a, label_b, label_c, label_d = labels[type_of_parameters]

    real_a, imag_a = extract_real_imag(parameter_a)
    real_b, imag_b = extract_real_imag(parameter_b)
    real_c, imag_c = extract_real_imag(parameter_c)
    real_d, imag_d = extract_real_imag(parameter_d)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    fig.suptitle("Real and Imaginary Parts vs Frequency", fontsize=16)

    axs[0, 0].plot(frequencies, real_a, label="Real", color="blue")
    axs[0, 0].plot(frequencies, imag_a, label="Imag", color="red", linestyle="--")
    axs[0, 0].set_title(f"{label_a}")
    axs[0, 0].legend()
    axs[0, 0].grid()

    axs[0, 1].plot(frequencies, real_b, label="Real", color="blue")
    axs[0, 1].plot(frequencies, imag_b, label="Imag", color="red", linestyle="--")
    axs[0, 1].set_title(f"{label_b}")
    axs[0, 1].legend()
    axs[0, 1].grid()

    axs[1, 0].plot(frequencies, real_c, label="Real", color="blue")
    axs[1, 0].plot(frequencies, imag_c, label="Imag", color="red", linestyle="--")
    axs[1, 0].set_title(f"{label_c}")
    axs[1, 0].legend()
    axs[1, 0].grid()

    axs[1, 1].plot(frequencies, real_d, label="Real", color="blue")
    axs[1, 1].plot(frequencies, imag_d, label="Imag", color="red", linestyle="--")
    axs[1, 1].set_title(f"{label_d}")
    axs[1, 1].legend()
    axs[1, 1].grid()

    for ax in axs.flat:
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Amplitude")

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

    fig, axs = plt.subplots(2, 2, figsize=(12, 12), subplot_kw={'projection': 'polar'})
    fig.suptitle(f"Polar Plots of {type_of_parameters} Parameters", fontsize=16)

    axs[0, 0].plot(np.radians(phase_a), magnitude_a, label=f"({label_a})", color="blue")
    axs[0, 0].set_title(f"({label_a})")
    axs[0, 0].grid(True)

    axs[0, 1].plot(np.radians(phase_b), magnitude_b, label=f"({label_b})", color="green")
    axs[0, 1].set_title(f"({label_b})")
    axs[0, 1].grid(True)

    axs[1, 0].plot(np.radians(phase_c), magnitude_c, label=f"({label_c})", color="red")
    axs[1, 0].set_title(f"({label_c})")
    axs[1, 0].grid(True)

    axs[1, 1].plot(np.radians(phase_d), magnitude_d, label=f"({label_d})", color="purple")
    axs[1, 1].set_title(f"({label_d})")
    axs[1, 1].grid(True)

    plt.show()

def plot_smith_chart(parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters, z_0=50):
    s_parameters_a = parameter_a
    s_parameters_b = parameter_b
    s_parameters_c = parameter_c
    s_parameters_d = parameter_c

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

        print("Enters conversion to S")

    else:
        s_parameters_a = parameter_a
        s_parameters_b = parameter_b
        s_parameters_c = parameter_c
        s_parameters_d = parameter_d
        print("Does not enter conversion to S")

    label_a, label_b, label_c, label_d = smith_labels[type_of_parameters]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Smith Chart for {type_of_parameters} Parameters", fontsize=16)

    ax = axs[0, 0]
    rf.plotting.plot_smith(s=np.array(s_parameters_a), ax=ax, label=f"({label_a})", color="blue")
    ax.set_title(f"({label_a})")
    ax.legend()

    ax = axs[0, 1]
    rf.plotting.plot_smith(s=np.array(s_parameters_b), ax=ax, label=f"({label_b})", color="orange")
    ax.set_title(f"({label_b})")
    ax.legend()

    ax = axs[1, 0]
    rf.plotting.plot_smith(s=np.array(s_parameters_c), ax=ax, label=f"({label_c})", color="green")
    ax.set_title(f"({label_c})")
    ax.legend()

    ax = axs[1, 1]
    rf.plotting.plot_smith(s=np.array(s_parameters_d), ax=ax, label=f"({label_d})", color="red")
    ax.set_title(f"({label_d})")
    ax.legend()

    plt.show()

def magnitude_in_db(parameter):
    return 20 * np.log10(np.abs(parameter))

def phase_in_degrees(parameter):
    real_part = np.real(parameter)
    imag_part = np.imag(parameter)
    phase_radians = np.arctan2(imag_part, real_part)
    phase_degrees = (180 * phase_radians) / np.pi

    return phase_degrees

def extract_real_imag(parameter):
    real_part = [np.real(x) for x in parameter]
    imag_part = [np.imag(x) for x in parameter]

    return real_part, imag_part