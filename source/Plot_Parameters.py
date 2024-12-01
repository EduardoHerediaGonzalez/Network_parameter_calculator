import matplotlib.pyplot as plt
import numpy as np
from source.network_parameter_conversions import convert_ABCD_matrix_to_S_matrix
import skrf as rf

 # **************************** Por ahora asumiendo que se calculan paráMetros ABCD ************************************
# Plot functions
def plot_magnitude_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):

    labels = {
        "ABCD": ("A", "B", "C", "D"),
        "Z": ("Z11", "Z12", "Z21", "Z22"),
        "Y": ("Y11", "Y12", "Y21", "Y22"),
        "S": ("S11", "S12", "S21", "S22")
    }

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

    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.show()

def plot_phase_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):

    phase_a = [phase_in_degrees(x) for x in parameter_a]
    phase_b = [phase_in_degrees(x) for x in parameter_b]
    phase_c = [phase_in_degrees(x) for x in parameter_c]
    phase_d = [phase_in_degrees(x) for x in parameter_d]

    labels = {
        "ABCD": ["Phase (A)", "Phase (B)", "Phase (C)", "Phase (D)"],
        "Z": ["Phase (Z11)", "Phase (Z12)", "Phase (Z21)", "Phase (Z22)"],
        "Y": ["Phase (Y11)", "Phase (Y12)", "Phase (Y21)", "Phase (Y22)"],
        "S": ["Phase (S11)", "Phase (S12)", "Phase (S21)", "Phase (S22)"]
    }

    label_a, label_b, label_c, label_d = labels[type_of_parameters]

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

    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.show()

def plot_r_i_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):

    real_a, imag_a = extract_real_imag(parameter_a)
    real_b, imag_b = extract_real_imag(parameter_b)
    real_c, imag_c = extract_real_imag(parameter_c)
    real_d, imag_d = extract_real_imag(parameter_d)

    labels = {
        "ABCD": ["Phase (A)", "Phase (B)", "Phase (C)", "Phase (D)"],
        "Z": ["Phase (Z11)", "Phase (Z12)", "Phase (Z21)", "Phase (Z22)"],
        "Y": ["Phase (Y11)", "Phase (Y12)", "Phase (Y21)", "Phase (Y22)"],
        "S": ["Phase (S11)", "Phase (S12)", "Phase (S21)", "Phase (S22)"]
    }

    label_a, label_b, label_c, label_d = labels[type_of_parameters]


    fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    fig.suptitle("Real and Imaginary Parts vs Frequency", fontsize=16)

    # Plot Parameter A
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

    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.show()

def plot_polar(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters):

    magnitude_a = np.abs(parameter_a)
    phase_a = np.angle(parameter_a, deg=True)

    magnitude_b = np.abs(parameter_b)
    phase_b = np.angle(parameter_b, deg=True)

    magnitude_c = np.abs(parameter_c)
    phase_c = np.angle(parameter_c, deg=True)

    magnitude_d = np.abs(parameter_d)
    phase_d = np.angle(parameter_d, deg=True)

    labels = {
        "ABCD": ["Parameter A", "Parameter B", "Parameter C", "Parameter D"],
        "Z": ["Z11", "Z12", "Z21", "Z22"],
        "Y": ["Y11", "Y12", "Y21", "Y22"],
        "S": ["S11", "S12", "S21", "S22"]
    }

    label_a, label_b, label_c, label_d = labels[type_of_parameters]

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

    plt.tight_layout(rect=(0, 0, 1, 0.95))
    plt.show()

def plot_smith_chart(frequencies, parameter_a, parameter_b, parameter_c, parameter_d, type_of_parameters, z_0=50):

    s_parameters_a = []
    s_parameters_b = []
    s_parameters_c = []
    s_parameters_d = []

    if type_of_parameters != "S":
        for a, b, c, d in zip(parameter_a, parameter_b, parameter_c, parameter_d):
            matrix_abcd = np.matrix([[a, b], [c, d]])
            s_matrix = convert_ABCD_matrix_to_S_matrix(matrix_abcd, z_0)

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

    labels = {
        "ABCD": ["S11 (A)", "S12 (B)", "S21 (C)", "S22 (D)"],
        "Z": ["S11 (Z11)", "S12 (Z12)", "S21 (Z21)", "S22 (Z22)"],
        "Y": ["S11 (Y11)", "S12 (Y12)", "S21 (Y21)", "S22 (Y22)"],
        "S": ["S11", "S12", "S21", "S22"]
    }

    label_a, label_b, label_c, label_d = labels[type_of_parameters]

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

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

 # Get values for functions
def magnitude_in_db(parameter):
    return 20 * np.log10(np.abs(parameter))

def phase_in_degrees(parameter):

    real_part = np.real(parameter)
    imag_part = np.imag(parameter)
    phase_radians = np.arctan2(imag_part, real_part)
    phase_degrees = (180*(phase_radians)) / np.pi

    return phase_degrees

def extract_real_imag(parameter):
    real_part = [np.real(x) for x in parameter]
    imag_part = [np.imag(x) for x in parameter]
    return real_part, imag_part

'''
def generate_smith_chart():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_title("Smith Chart", fontsize=16)

    # Unit circumference
    theta = np.linspace(0, 2 * np.pi, 500)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=0.8)

    # Resistance Axes
    ax.axhline(0, color='k', linewidth=0.5, linestyle='--')

    # Resistance values
    resistances = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                   10, 12, 14, 16, 18, 20]
    for r in resistances:
        center_x = r / (1 + r)
        radius = 1 / (1 + r)
        theta_resistance = np.linspace(0, 2 * np.pi, 500)
        x_res = center_x + radius * np.cos(theta_resistance)
        y_res = radius * np.sin(theta_resistance)

        # Cut edge and plot
        mask = x_res ** 2 + y_res ** 2 <= 1
        ax.plot(x_res[mask], y_res[mask], color='grey', linewidth=0.5)

    # Reactance values
    reactances = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                  10, 12, 14, 16, 18, 20]
    for x in reactances:
        # Inductance Reactance
        center_x = 1
        center_y = 1 / x
        radius = np.abs(center_y)
        theta_react = np.linspace(-np.pi / 2, np.pi / 2, 500)
        x_pos = center_x - radius * np.cos(theta_react)
        y_pos = center_y - radius * np.sin(theta_react)

        # Cut edge and plot
        mask_pos = x_pos ** 2 + y_pos ** 2 <= 1
        ax.plot(x_pos[mask_pos], y_pos[mask_pos], color='grey', linewidth=0.5)

        # Capacitive reactance
        center_y = -1 / x
        y_neg = center_y + radius * np.sin(theta_react)

        # Cut edge and plot
        mask_neg = x_pos ** 2 + y_neg ** 2 <= 1
        ax.plot(x_pos[mask_neg], y_neg[mask_neg], color='grey', linewidth=0.5)

    ax.text(0, 1.05, "Resistance and Reactance Normalized Values", fontsize=12, ha="center", color="black")

    for i, r in enumerate(resistances):
        ax.text(1.05, 1 - (i * 0.075), f"{r}", color='black', fontsize=8, ha="left")

    ax.text(1.05, 1 - (len(resistances) * 0.075), "From left to right", color='black', fontsize=7, ha="left",
            verticalalignment="top")

    ax.grid(False)
    ax.axis('off')
    ax.legend(loc='upper left', fontsize=10)
    plt.show()
'''