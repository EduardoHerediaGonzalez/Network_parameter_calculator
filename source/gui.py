import os
import tkinter as tk
import pandas as pd
import shutil
from tkinter import ttk
from tkinter import messagebox

from openpyxl import *
import config_parameters as cfg
from source.common_two_port_circuits import *

excel_base_template_workbook = load_workbook(filename=os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_BASE_TEMPLATE_FILE))
excel_base_template_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))
excel_base_template_workbook.close()
del excel_base_template_workbook

excel_network_parameters_workbook = load_workbook(filename=os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))
excel_network_info_sheet = excel_network_parameters_workbook[cfg.EXCEL_NETWORK_INFO_SHEET]

excel_circuit_counter_row = cfg.EXCEL_INITIAL_ROW_NETWORK_ID
frequency_points_to_analyzed = list()
touchstone_file_counter = 0

def get_frequency_with_prefixed(frequency_value: float):
    frequency_value__length = len(str(int(frequency_value)))
    frequency_with_prefixed = ''

    if frequency_value__length <= cfg.THREE_DIGITS:
        frequency_value = frequency_value / cfg.FREQUENCY_PREFIXES_TO_VALUE[cfg.FREQUENCY_PREFIXES[0]]
        frequency_with_prefixed = str(round(frequency_value,2)) + ' ' + cfg.FREQUENCY_PREFIXES[0]

    elif frequency_value__length <= cfg.SIX_DIGITS:
        frequency_value = frequency_value / cfg.FREQUENCY_PREFIXES_TO_VALUE[cfg.FREQUENCY_PREFIXES[1]]
        frequency_with_prefixed = str(round(frequency_value,2)) + ' ' + cfg.FREQUENCY_PREFIXES[1]

    elif frequency_value__length <= cfg.NINE_DIGITS:
        frequency_value = frequency_value / cfg.FREQUENCY_PREFIXES_TO_VALUE[cfg.FREQUENCY_PREFIXES[2]]
        frequency_with_prefixed = str(round(frequency_value,2)) + ' ' + cfg.FREQUENCY_PREFIXES[2]

    elif frequency_value__length <= cfg.TWELVE_DIGITS:
        frequency_value = frequency_value / cfg.FREQUENCY_PREFIXES_TO_VALUE['GHz']
        frequency_with_prefixed = str(round(frequency_value,2)) + ' ' + cfg.FREQUENCY_PREFIXES[3]

    return  frequency_with_prefixed

def save_frequency_parameters():
    start_frequency = start_frequency_entry.get()
    start_frequency_prefix = start_frequency_combobox.get()

    end_frequency = end_frequency_entry.get()
    end_frequency_prefix = end_frequency_combobox.get()

    analysis_frequency_step = analysis_frequency_step_entry.get()

    if start_frequency == '' or start_frequency_prefix == '' or end_frequency == '' or end_frequency_prefix == '' or analysis_frequency_step == '':
        messagebox.showerror(title='Error', message='One or more fields are empty')
    else:
        start_frequency_value = float(start_frequency) * cfg.FREQUENCY_PREFIXES_TO_VALUE[start_frequency_prefix]
        end_frequency_value = float(end_frequency) * cfg.FREQUENCY_PREFIXES_TO_VALUE[end_frequency_prefix]
        analysis_frequency_step_value = float(analysis_frequency_step)

        """frequency_step_value = (end_frequency_value - start_frequency_value) / (analysis_frequency_step_value - 1)

        frequency_points_to_analyzed.append(get_frequency_with_prefixed(start_frequency_value))

        frequency_point_to_analyzed = start_frequency_value + frequency_step_value

        for counter in range(int(analysis_frequency_step_value - 2)):
        # while frequency_point_to_analyzed <= (analysis_frequency_step_value - 2):
            frequency_points_to_analyzed.append(get_frequency_with_prefixed(frequency_point_to_analyzed))
            frequency_point_to_analyzed = frequency_point_to_analyzed + frequency_step_value

        frequency_points_to_analyzed.append(get_frequency_with_prefixed(end_frequency_value))"""

    # ************************************ Insert Step instead of number of points ************************************* #

        frequency_point_to_analyzed = start_frequency_value

        while frequency_point_to_analyzed <= end_frequency_value:
            frequency_points_to_analyzed.append(get_frequency_with_prefixed(frequency_point_to_analyzed))
            frequency_point_to_analyzed = frequency_point_to_analyzed + analysis_frequency_step_value
    # ****************************************************************************************************************** #

    frequency_points = ','.join(frequency_points_to_analyzed)
    excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW, column=cfg.EXCEL_COLUMN_B).value = start_frequency + ' ' + start_frequency_prefix
    excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 1, column=cfg.EXCEL_COLUMN_B).value = end_frequency + ' ' + end_frequency_prefix
    excel_network_info_sheet.cell(row =cfg.EXCEL_INITIAL_ROW + 2, column = cfg.EXCEL_COLUMN_B).value = frequency_points
    excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))

    start_frequency_entry.config(state='disable')
    start_frequency_combobox.config(state='disable')
    end_frequency_entry.config(state='disable')
    end_frequency_combobox.config(state='disable')
    analysis_frequency_step_entry.config(state='disable')
    save_frequency_parameters_button.config(state='disable')
    parameters_to_calculate_combobox.config(state='normal')

def save_network_parameters():
    parameters_to_calculate = parameters_to_calculate_combobox.get()

    excel_network_info_sheet.cell(row =cfg.EXCEL_INITIAL_ROW + 5, column = cfg.EXCEL_COLUMN_B).value = parameters_to_calculate
    excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))

    parameters_to_calculate_combobox.config(state = 'disable')
    type_of_circuit_combobox.config(state = 'normal')
    type_of_interconnection_combobox.config(state ='normal')
    element_A_combobox.config(state = 'normal')
    element_A_entry.config(state = 'normal')
    element_B_combobox.config(state = 'normal')
    element_B_entry.config(state = 'normal')
    element_C_combobox.config(state = 'normal')
    element_C_entry.config(state = 'normal')
    add_sub_network_button.config(state ='normal')

def add_sub_network():
    type_of_circuit = type_of_circuit_combobox.get()
    type_of_interconnection = type_of_interconnection_combobox.get()
    element_a = element_A_combobox.get()
    element_a_value = element_A_entry.get()
    element_b = element_B_combobox.get()
    element_b_value = element_B_entry.get()
    element_c = element_C_combobox.get()
    element_c_value = element_C_entry.get()


    if type_of_circuit == '':
        messagebox.showerror(title='Error', message='Type of circuit is empty')

    elif element_a == '' and element_b == '' and element_c == '':
        messagebox.showerror(title='Error', message='No element selected')

    elif element_a_value == '' and element_b_value == '' and element_c_value == '':
        messagebox.showerror(title='Error', message='No element value')

    else:
        global excel_circuit_counter_row

        sub_networks_counter = counter_of_sub_networks.get()
        sub_networks_counter = sub_networks_counter + 1

        if type_of_interconnection == '':
            type_of_interconnection = cfg.SUB_NETWORK_DEFAULT_CONNECTION

        excel_network_info_sheet.cell(row=excel_circuit_counter_row, column=cfg.EXCEL_COLUMN_A, value=str(sub_networks_counter))
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_B, value = type_of_interconnection)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_C, value = type_of_circuit)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_D, value = element_a)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_E, value = join_value_and_prefix(element_a_value))
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_F, value = element_b)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_G, value = join_value_and_prefix(element_b_value))
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_H, value = element_c)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_I, value = join_value_and_prefix(element_c_value))
        excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))

        excel_circuit_counter_row = excel_circuit_counter_row + 1

        counter_of_sub_networks.set(sub_networks_counter)
        reset_type_of_circuit_combobox.set('')
        reset_type_of_connection_combobox.set('')
        reset_element_A_combobox.set('')
        reset_element_A_entry.set('')
        reset_element_B_combobox.set('')
        reset_element_B_entry.set('')
        reset_element_C_combobox.set('')
        reset_element_C_entry.set('')
        reset_characteristic_impedance_entry.set('')

        if sub_networks_counter == 1:
            save_sub_networks_button.config(state='normal')


def save_sub_networks():
    type_of_circuit_combobox.config(state='disable')
    type_of_interconnection_combobox.config(state='disable')
    element_A_combobox.config(state='disable')
    element_A_entry.config(state='disable')
    element_B_combobox.config(state='disable')
    element_B_entry.config(state='disable')
    element_C_combobox.config(state='disable')
    element_C_entry.config(state='disable')
    touchstone_file_button.config(state='disable')
    touchstone_file_entry.config(state='disable')
    add_sub_network_button.config(state='disable')
    save_sub_networks_button.config(state='disable')

    if touchstone_file_counter == 0:
        start_frequency_entry.config(state='normal')
        start_frequency_combobox.config(state='normal')
        end_frequency_entry.config(state='normal')
        end_frequency_combobox.config(state='normal')

    analysis_frequency_step_entry.config(state='normal')
    save_frequency_parameters_button.config(state='normal')

def calculate_parameters():
    _sub_networks = []
    _sub_networks_interconnection = []
    excel_abcd_parameters_sheet = excel_network_parameters_workbook[cfg.EXCEL_ABCD_PARAMETERS_SHEET]

    _parameters_to_calculate = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 5, column=cfg.EXCEL_COLUMN_B).value

    _sub_networks, _sub_networks_interconnection = get_sub_networks_info()

    frequency_range = get_frequency_range()

    row_counter = cfg.EXCEL_INITIAL_ROW

    for frequency in frequency_range:
        abcd_parameters = get_total_abcd_matrix_parameters(sub_networks=_sub_networks, frequency=frequency)

        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_A).value = frequency
        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_B).value = abcd_parameters[cfg.PARAMETER_A_INDEX]
        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_C).value = abcd_parameters[cfg.PARAMETER_B_INDEX]
        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_D).value = abcd_parameters[cfg.PARAMETER_C_INDEX]
        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_E).value = abcd_parameters[cfg.PARAMETER_D_INDEX]
        excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))

        row_counter = row_counter + 1

def plot_parameters():

    excel_abcd_parameters_sheet = excel_network_parameters_workbook[cfg.EXCEL_ABCD_PARAMETERS_SHEET]

    frequencies = []
    parameter_a = []
    parameter_b = []
    parameter_c = []
    parameter_d = []

    for row in range(cfg.EXCEL_INITIAL_ROW, excel_abcd_parameters_sheet.max_row + 1):
        frequencies.append(excel_abcd_parameters_sheet.cell(row=row, column=cfg.EXCEL_COLUMN_A).value)
        parameter_a.append(excel_abcd_parameters_sheet.cell(row=row, column=cfg.EXCEL_COLUMN_B).value)
        parameter_b.append(excel_abcd_parameters_sheet.cell(row=row, column=cfg.EXCEL_COLUMN_C).value)
        parameter_c.append(excel_abcd_parameters_sheet.cell(row=row, column=cfg.EXCEL_COLUMN_D).value)
        parameter_d.append(excel_abcd_parameters_sheet.cell(row=row, column=cfg.EXCEL_COLUMN_E).value)

    return frequencies, parameter_a, parameter_b, parameter_c, parameter_d

    format_to_plot = plot_parameters_in_format_combobox.get()

    if format_to_plot == 'Rectangular (Magnitude vs Freq)':
        plot_magnitude_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d)

    elif format_to_plot == 'Rectangular (Phase vs Freq)':
        plot_phase_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d)

    elif format_to_plot == 'Rectangular (RI vs Freq)':
        plot_r_i_vs_frequency(frequencies, parameter_a, parameter_b, parameter_c, parameter_d)

    elif format_to_plot == 'Polar':
        plot_polar(frequencies, parameter_a, parameter_b, parameter_c, parameter_d)

    elif format_to_plot == 'Smith chart':
        plot_smith_chart(frequencies, parameter_a, parameter_b, parameter_c, parameter_d)

def get_total_frequency_points(start_frequency, frequency_points_to_be_analyzed, end_frequency):
    frequency_points_temp = []
    frequency_range = []

    for frequency_point in frequency_points_to_be_analyzed:
        value, prefix = frequency_point.split()
        frequency_point = int(value) * cfg.FREQUENCY_PREFIXES_TO_VALUE[prefix]

        frequency_points_temp.append(frequency_point)

    frequency_points = frequency_points_temp

    frequency_range.append(start_frequency)

    for frequency in frequency_points:
        frequency_range.append(frequency)

    frequency_range.append(end_frequency)

    return frequency_range

def convert_string_to_value(string_value):
    num_str = ''
    prefix_str = ''

    for character_value in string_value:
        if character_value.isdigit() or character_value == '.':
            num_str = num_str + character_value
        else:
            prefix_str = prefix_str + character_value

    prefix_str = prefix_str[0]

    prefix_value = cfg.MAGNITUDES_PREFIXES_TO_VALUE[prefix_str]
    num_value = float(num_str)

    value = num_value * prefix_value

    return value

def join_value_and_prefix(value: str):
    num_str = ''
    prefix_str = ''

    for character_value in value:
        if character_value.isdigit() or character_value == '.':
            num_str = num_str + character_value
        else:
            if character_value != ' ':
                if character_value == 'f' or character_value == 'h' or character_value == 'k':
                    character_value = character_value.title()

                prefix_str = prefix_str + character_value

    value = num_str + prefix_str

    return value

def get_sub_networks_info():
    sub_network_id_counter = cfg.EXCEL_INITIAL_ROW_NETWORK_ID
    sub_networks = []
    sub_networks_interconnection = []
    sub_networks_matrixes = []
    excel_abcd_parameters_sheet = excel_network_parameters_workbook[cfg.EXCEL_ABCD_PARAMETERS_SHEET]
    characteristic_impedance_list = []

    while excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_A).value is not None:
        interconnection_type = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_B).value
        sub_networks_interconnection.append(interconnection_type)
        characteristic_impedance = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_J).value
        characteristic_impedance = int(characteristic_impedance)
        characteristic_impedance_list.append(characteristic_impedance)

        circuit_type = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_C).value
        print(characteristic_impedance_list)

        if circuit_type == 'Series impedance':
            element = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_D).value
            element_value = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_E).value

            sub_network = SeriesImpedanceCircuit(type_of_element=element, element_value=convert_string_to_value(element_value))
            sub_networks.append(sub_network)

        elif circuit_type == 'Shunt impedance':
            element = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_D).value
            element_value = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_E).value

            sub_network = ShuntImpedanceCircuit(type_of_element=element, element_value=convert_string_to_value(element_value))
            sub_networks.append(sub_network)

        elif circuit_type == 'T':
            element_a = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_D).value
            element_a_value = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_E).value
            element_b = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_F).value
            element_b_value = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_G).value
            element_c = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_H).value
            element_c_value = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_I).value

            sub_network = TCircuit(type_of_element_a=element_a, element_a_value=convert_string_to_value(element_a_value),
                                   type_of_element_b=element_b, element_b_value=convert_string_to_value(element_b_value),
                                   type_of_element_c=element_c, element_c_value=convert_string_to_value(element_c_value))
            sub_networks.append(sub_network)

        elif circuit_type == 'Pi':
            element_a = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_D).value
            element_a_value = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_E).value
            element_b = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_F).value
            element_b_value = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_G).value
            element_c = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_H).value
            element_c_value = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_I).value

            sub_network = PiCircuit(type_of_element_a=element_a, element_a_value=convert_string_to_value(element_a_value),
                                   type_of_element_b=element_b, element_b_value=convert_string_to_value(element_b_value),
                                   type_of_element_c=element_c, element_c_value=convert_string_to_value(element_c_value))
            sub_networks.append(sub_network)

        sub_network_id_counter = sub_network_id_counter + 1

    return sub_networks, sub_networks_interconnection

def get_frequency_range():
    start_frequency = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW, column=cfg.EXCEL_COLUMN_B).value
    value, prefix = start_frequency.split()
    start_frequency = int(value) * cfg.FREQUENCY_PREFIXES_TO_VALUE[prefix]

    end_frequency = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 1, column=cfg.EXCEL_COLUMN_B).value
    value, prefix = end_frequency.split()
    end_frequency = int(value) * cfg.FREQUENCY_PREFIXES_TO_VALUE[prefix]

    frequency_points_to_be_analyzed = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 2, column=cfg.EXCEL_COLUMN_B).value

    if len(frequency_points_to_be_analyzed) != 0:
        frequency_points_to_be_analyzed = frequency_points_to_be_analyzed.split(',')

    frequency_range = get_total_frequency_points(start_frequency, frequency_points_to_be_analyzed, end_frequency)

    return  frequency_range

def simplify_value_result(value: complex):
    real_part = value.real
    imaginary_part = value.imag
    simplify_result = ''

    if real_part != 0:
        real_part = str(real_part)
        simplify_result = simplify_result + real_part

    if imaginary_part != 0:
        imaginary_part = str(imaginary_part)
        simplify_result = simplify_result + imaginary_part + 'j'

    if real_part == 0 and imaginary_part == 0:
        simplify_result = '0'

    return simplify_result

def get_total_abcd_matrix_parameters(sub_networks: list, frequency: int):
    total_of_matrices: int
    total_abcd_matrix: complex
    abcd_parameters: list
    sub_networks_matrices = []

    for sub_network in sub_networks:
        sub_networks_matrices.append(sub_network.get_matrix_abcd(at_frequency=frequency))

    total_of_matrices = len(sub_networks_matrices)
    next_matrix_index = 2

    if total_of_matrices > 1:
        total_abcd_matrix = sub_networks_matrices[0] * sub_networks_matrices[1]
    else:
        total_abcd_matrix = sub_networks_matrices[0]

    while next_matrix_index < total_of_matrices:
        total_abcd_matrix = total_abcd_matrix * sub_networks_matrices[next_matrix_index]

    total_abcd_matrix = total_abcd_matrix.tolist()
    matrix_row_1 = total_abcd_matrix[0]
    matrix_row_2 = total_abcd_matrix[1]
    parameter_a, parameter_b = matrix_row_1
    parameter_c, parameter_d = matrix_row_2

    parameter_a = simplify_value_result(value=parameter_a)
    parameter_b = simplify_value_result(value=parameter_b)
    parameter_c = simplify_value_result(value=parameter_c)
    parameter_d = simplify_value_result(value=parameter_d)

    abcd_parameters = [parameter_a, parameter_b, parameter_c, parameter_d]

    sub_networks_matrices.clear()

    return abcd_parameters

def add_touchstone_file():
    touchstone_file_path = touchstone_file_entry.get()
    global touchstone_file_counter
    global counter_of_sub_networks
    global excel_circuit_counter_row

    if os.path.exists(touchstone_file_path):
        touchstone_file_counter = touchstone_file_counter + 1
        touchstone_txt_file_name = cfg.TOUCHSTONE_FILE_NAME + str(touchstone_file_counter) + cfg.TXT_EXTENSION
        shutil.copy2(touchstone_file_path, os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, touchstone_txt_file_name))

        touchstone_excel_file_name = cfg.TOUCHSTONE_FILE_NAME + str(touchstone_file_counter) + cfg.EXCEL_EXTENSION
        data_frame = pd.read_csv(os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, touchstone_txt_file_name), sep=',')
        data_frame.to_excel(os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, touchstone_excel_file_name), index=False)
        os.remove(os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, touchstone_txt_file_name))

        sub_networks_counter = counter_of_sub_networks.get()
        sub_networks_counter = sub_networks_counter + 1

        excel_network_info_sheet.cell(row=excel_circuit_counter_row, column=cfg.EXCEL_COLUMN_A, value=str(sub_networks_counter))
        excel_network_info_sheet.cell(row=excel_circuit_counter_row, column=cfg.EXCEL_COLUMN_C, value=touchstone_excel_file_name)
        excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))

        reset_touchstone_file_entry.set('')
        sub_networks_counter = counter_of_sub_networks.get()
        sub_networks_counter = sub_networks_counter + 1
        counter_of_sub_networks.set(sub_networks_counter)

        if sub_networks_counter == 1:
            save_sub_networks_button.config(state='normal')

    else:
        messagebox.showerror(title='Error', message='Touchstone file not found. Check that the path or filename is correct.')


mainWindow = tk.Tk()
mainWindow.title("Two-port network parameter calculator")
mainWindow.geometry('800x600')

counter_of_sub_networks = tk.IntVar(mainWindow, 0)
reset_analysis_frequency_step_entry = tk.StringVar(mainWindow, '')
reset_frequency_point_to_analyze_combobox = tk.StringVar(mainWindow, '')
reset_type_of_circuit_combobox = tk.StringVar(mainWindow, '')
reset_type_of_connection_combobox = tk.StringVar(mainWindow, '')
reset_element_A_combobox = tk.StringVar(mainWindow, '')
reset_element_A_entry = tk.StringVar(mainWindow, '')
reset_element_B_combobox = tk.StringVar(mainWindow, '')
reset_element_B_entry = tk.StringVar(mainWindow, '')
reset_element_C_combobox = tk.StringVar(mainWindow, '')
reset_element_C_entry = tk.StringVar(mainWindow, '')
reset_characteristic_impedance_entry = tk.StringVar(mainWindow, '')
reset_touchstone_file_entry = tk.StringVar(mainWindow, '')

# Start of frame 1 #
row = 0

frame_1 = ttk.Frame(mainWindow)
frame_1.grid(row=row, column=0)

spacer_1 = ttk.Label(frame_1)
spacer_2 = ttk.Label(frame_1)
spacer_3 = ttk.Label(frame_1)
spacer_4 = ttk.Label(frame_1)

type_of_circuit_label = ttk.Label(frame_1, text='Type of circuit')
type_of_circuit_label.grid(row=row, column=0)
type_of_circuit_combobox = ttk.Combobox(frame_1, values=cfg.CIRCUIT_TYPES, state='normal', textvariable=reset_type_of_circuit_combobox)
type_of_circuit_combobox.grid(row=row, column=1)

total_of_circuits_label = ttk.Label(frame_1, text='Total of sub-networks:')
total_of_circuits_label.grid(row=row, column=2)
total_of_circuits_label = ttk.Label(frame_1, textvariable=counter_of_sub_networks)
total_of_circuits_label.grid(row=row, column=3)

row = row + 1

type_of_interconnection_label = ttk.Label(frame_1, text='Type of interconnection')
type_of_interconnection_label.grid(row=row, column=0)
type_of_interconnection_combobox = ttk.Combobox(frame_1, values=cfg.INTERCONNECTION_TYPES, state='normal', textvariable=reset_type_of_connection_combobox)
type_of_interconnection_combobox.grid(row=row, column=1)
type_of_interconnection_combobox.current()

row = row + 1

spacer_1.grid(row=row, column=0)

row = row + 1

element_A_label = ttk.Label(frame_1, text='Element A')
element_A_label.grid(row=row, column=0)
element_A_combobox = ttk.Combobox(frame_1, values=cfg.ELEMENT_TYPES, state='normal', textvariable=reset_element_A_combobox)
element_A_combobox.grid(row=row, column=1)
element_A_value_label = ttk.Label(frame_1, text='Value')
element_A_value_label.grid(row=row, column=2)
element_A_entry = ttk.Entry(frame_1, state='normal', textvariable=reset_element_A_entry)
element_A_entry.grid(row=row, column=3)

row = row + 1

element_B_label = ttk.Label(frame_1, text='Element B')
element_B_label.grid(row=row, column=0)
element_B_combobox = ttk.Combobox(frame_1, values=cfg.ELEMENT_TYPES, state='normal', textvariable=reset_element_B_combobox)
element_B_combobox.grid(row=row, column=1)
element_B_value_label = ttk.Label(frame_1, text='Value')
element_B_value_label.grid(row=row, column=2)
element_B_entry = ttk.Entry(frame_1, state='normal', textvariable=reset_element_B_entry)
element_B_entry.grid(row=row, column=3)

row = row + 1

element_C_label = ttk.Label(frame_1, text='Element C')
element_C_label.grid(row=row, column=0)
element_C_combobox = ttk.Combobox(frame_1, values=cfg.ELEMENT_TYPES, state='normal', textvariable=reset_element_C_combobox)
element_C_combobox.grid(row=row, column=1)
element_C_value_label = ttk.Label(frame_1, text='Value')
element_C_value_label.grid(row=row, column=2)
element_C_entry = ttk.Entry(frame_1, state='normal', textvariable=reset_element_C_entry)
element_C_entry.grid(row=row, column=3)

row = row + 1

spacer_2.grid(row=row, column=0)

row = row + 1

touchstone_file_button = ttk.Button(frame_1, text='Add touchstone file', command=add_touchstone_file)
touchstone_file_button.grid(row=row, column=0)
touchstone_file_entry = ttk.Entry(frame_1, textvariable=reset_touchstone_file_entry)
touchstone_file_entry.grid(row=row, column=1)

row = row + 1

spacer_3.grid(row=row, column=0)

row = row + 1

add_sub_network_button = ttk.Button(frame_1, text='Add sub-network', state='normal', command=add_sub_network)
add_sub_network_button.grid(row=row, column=2)

row = row + 1

save_sub_networks_button = ttk.Button(frame_1, text='Save sub-networks', state='disable', command=save_sub_networks)
save_sub_networks_button.grid(row=row, column=2)

row = row + 1

spacer_4.grid(row=row, column=0)

# Start of frame 2 #
row = row + 1

frame_2 = ttk.Frame(mainWindow)
frame_2.grid(row=row, column=0)

spacer_5 = ttk.Label(frame_2)
spacer_6 = ttk.Label(frame_2)

row = row + 1

start_frequency_label = ttk.Label(frame_2, text = 'Start frequency')
start_frequency_label.grid(row=row, column=0)
start_frequency_entry = ttk.Entry(frame_2, state='disable')
start_frequency_entry.grid(row=row, column=1)
start_frequency_combobox = ttk.Combobox(frame_2, state='disable', values = cfg.FREQUENCY_PREFIXES)
start_frequency_combobox.grid(row=row, column=2)

row = row + 1

end_frequency_label = ttk.Label(frame_2, text='End frequency')
end_frequency_label.grid(row=row, column=0)
end_frequency_entry = ttk.Entry(frame_2, state='disable')
end_frequency_entry.grid(row=row, column=1)
end_frequency_combobox = ttk.Combobox(frame_2, state='disable', values=cfg.FREQUENCY_PREFIXES)
end_frequency_combobox.grid(row=row, column=2)

row = row + 1

analysis_frequency_step_label = ttk.Label(frame_2, text='Analysis frequency step')
analysis_frequency_step_label.grid(row=row, column=0)
analysis_frequency_step_entry = ttk.Entry(frame_2, state='disable', textvariable=reset_analysis_frequency_step_entry)
analysis_frequency_step_entry.grid(row=row, column=1)

row = row + 1

spacer_5.grid(row=row, column=0)

row = row + 1

save_frequency_parameters_button = ttk.Button(frame_2, text='Save frequency parameters', state='disable', command=save_frequency_parameters)
save_frequency_parameters_button.grid(row=row, column=0)

row = row + 1

spacer_6.grid(row=row, column=0)

row = row + 1

calculate_parameters_button = ttk.Button(frame_2, text='Calculate parameters', state='disable', command=calculate_parameters)
calculate_parameters_button.grid(row=row, column=0)
parameters_to_calculate_combobox = ttk.Combobox(frame_2, values=cfg.NETWORK_PARAMETERS, state='disable')
parameters_to_calculate_combobox.grid(row=row, column=1)

row = row + 1

plot_parameters_button = ttk.Button(frame_2, text='Plot parameters', state='disable', command=plot_parameters)
plot_parameters_button.grid(row=row, column=0)
plot_parameters_in_format_combobox = ttk.Combobox(frame_2, values=cfg.PLOT_FORMATS, state='disable')
plot_parameters_in_format_combobox.grid(row=row, column=1)

mainWindow.mainloop()