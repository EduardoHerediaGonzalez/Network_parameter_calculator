import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import pandas as pd
from openpyxl import *

from source.common_two_port_circuits import *
from source.touchstone_files.touchstone import *

excel_base_template_workbook = load_workbook(filename=os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_BASE_TEMPLATE_FILE))
excel_base_template_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))
excel_base_template_workbook.close()
del excel_base_template_workbook

excel_network_parameters_workbook = load_workbook(filename=os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))
excel_network_info_sheet = excel_network_parameters_workbook[cfg.EXCEL_NETWORK_INFO_SHEET]

excel_circuit_counter_row = cfg.EXCEL_INITIAL_ROW_NETWORK_ID
sub_networks = list()
sub_networks_interconnection = list()
frequency_range = list()
cascade_sub_networks_indexes = list()
series_sub_networks_indexes = list()
parallel_sub_networks_indexes = list()
touchstone_sub_networks_indexes = list()
touchstone_file_counter = 0

def add_touchstone_file():
    touchstone_file_path = touchstone_file_entry.get()
    global touchstone_file_counter
    global counter_of_sub_networks
    global excel_circuit_counter_row

    if os.path.exists(touchstone_file_path):
        shutil.copy2(touchstone_file_path, os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, cfg.TXT_TOUCHSTONE_FILE_NAME))

        data_frame = pd.read_csv(os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, cfg.TXT_TOUCHSTONE_FILE_NAME), sep=',')
        data_frame.to_excel(os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, cfg.EXCEL_TOUCHSTONE_FILE_NAME), index=False)
        os.remove(os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, cfg.TXT_TOUCHSTONE_FILE_NAME))

        sub_networks_counter = counter_of_sub_networks.get()
        sub_networks_counter = sub_networks_counter + 1

        excel_network_info_sheet.cell(row=excel_circuit_counter_row, column=cfg.EXCEL_COLUMN_A, value=str(sub_networks_counter))
        excel_network_info_sheet.cell(row=excel_circuit_counter_row, column=cfg.EXCEL_COLUMN_B, value=cfg.TOUCHSTONE_CONNECTION)
        excel_network_info_sheet.cell(row=excel_circuit_counter_row, column=cfg.EXCEL_COLUMN_C, value=cfg.EXCEL_TOUCHSTONE_FILE_NAME)
        excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))
        excel_touchstone_workbook = load_workbook(filename=os.path.join(os.getcwd(), cfg.FOLDER_TOUCHSTONE_FILES, cfg.EXCEL_TOUCHSTONE_FILE_NAME))
        excel_touchstone_sheet = excel_touchstone_workbook[cfg.EXCEL_DEFAULT_SHEET_NAME]

        (start_frequency_value, end_frequency_value, analysis_frequency_step_value) = get_frequency_parameters_from_touchstone_file(excel_touchstone_sheet)

        start_frequency = get_frequency_with_prefixed(start_frequency_value)
        end_frequency = get_frequency_with_prefixed(end_frequency_value)
        analysis_frequency_step = get_frequency_with_prefixed(analysis_frequency_step_value)

        start_frequency = start_frequency.split(' ')
        start_frequency_prefix = start_frequency[1]
        start_frequency = start_frequency[0]
        reset_start_frequency_entry.set(start_frequency)
        start_frequency_combobox.current(cfg.FREQUENCY_PREFIXES.index(start_frequency_prefix))

        end_frequency = end_frequency.split(' ')
        end_frequency_prefix = end_frequency[1]
        end_frequency = end_frequency[0]
        reset_end_frequency_entry.set(end_frequency)
        end_frequency_combobox.current(cfg.FREQUENCY_PREFIXES.index(end_frequency_prefix))

        analysis_frequency_step = analysis_frequency_step.split(' ')
        analysis_frequency_step_prefix = analysis_frequency_step[1]
        analysis_frequency_step = analysis_frequency_step[0]
        reset_analysis_frequency_step_entry.set(analysis_frequency_step)
        analysis_frequency_step_combobox.current(cfg.FREQUENCY_PREFIXES.index(analysis_frequency_step_prefix))

        reset_touchstone_file_entry.set('')
        counter_of_sub_networks.set(sub_networks_counter)
        touchstone_file_counter = 1

        if sub_networks_counter == 1:
            save_sub_networks_button.config(state='normal')

    else:
        messagebox.showerror(title='Error', message='Touchstone file not found. Check that the path or filename is correct.')

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
        analysis_frequency_step_combobox.config(state='normal')

    save_frequency_parameters_button.config(state='normal')

def save_frequency_parameters():
    start_frequency = start_frequency_entry.get()
    start_frequency_prefix = start_frequency_combobox.get()

    end_frequency = end_frequency_entry.get()
    end_frequency_prefix = end_frequency_combobox.get()

    analysis_frequency_step = analysis_frequency_step_entry.get()
    analysis_frequency_step_prefix = analysis_frequency_step_combobox.get()

    if start_frequency == '' or start_frequency_prefix == '' or end_frequency == '' or end_frequency_prefix == '' or analysis_frequency_step == '':
        messagebox.showerror(title='Error', message='One or more fields are empty')
        
    else:
        start_frequency_value = float(start_frequency) * cfg.FREQUENCY_PREFIXES_TO_VALUE[start_frequency_prefix]
        end_frequency_value = float(end_frequency) * cfg.FREQUENCY_PREFIXES_TO_VALUE[end_frequency_prefix]
        analysis_frequency_step_value = float(analysis_frequency_step) * cfg.FREQUENCY_PREFIXES_TO_VALUE[analysis_frequency_step_prefix]

        total_of_frequency_points =  round(((end_frequency_value - start_frequency_value) / analysis_frequency_step_value) + 1)

        frequency_range.append(start_frequency_value)
        current_frequency_point_value = start_frequency_value

        for frequency_point_counter in range(1, total_of_frequency_points):
            current_frequency_point_value = current_frequency_point_value + analysis_frequency_step_value
            frequency_range.append(current_frequency_point_value)

        excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW, column=cfg.EXCEL_COLUMN_B).value = start_frequency + ' ' + start_frequency_prefix
        excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 1, column=cfg.EXCEL_COLUMN_B).value = end_frequency + ' ' + end_frequency_prefix
        excel_network_info_sheet.cell(row =cfg.EXCEL_INITIAL_ROW + 2, column = cfg.EXCEL_COLUMN_B).value = analysis_frequency_step + ' ' + analysis_frequency_step_prefix
        excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))

        start_frequency_entry.config(state='disable')
        start_frequency_combobox.config(state='disable')
        end_frequency_entry.config(state='disable')
        end_frequency_combobox.config(state='disable')
        analysis_frequency_step_entry.config(state='disable')
        save_frequency_parameters_button.config(state='disable')
        calculate_parameters_button.config(state='normal')
        parameters_to_calculate_combobox.config(state='normal')

def calculate_parameters():
    global sub_networks
    global sub_networks_interconnection
    excel_abcd_parameters_sheet = excel_network_parameters_workbook[cfg.EXCEL_ABCD_PARAMETERS_SHEET]

    parameters_to_calculate = parameters_to_calculate_combobox.get()

    if parameters_to_calculate != '':
        excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 4, column=cfg.EXCEL_COLUMN_B).value = cfg.DEFAULT_NETWORK_TYPE
        excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 5, column=cfg.EXCEL_COLUMN_B).value = parameters_to_calculate
        excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))

        get_sub_networks_info()

        get_indexes_of_sub_networks_interconnection()

        row_counter = cfg.EXCEL_INITIAL_ROW

        for frequency in frequency_range:
            abcd_parameters = get_total_abcd_matrix_parameters(frequency=frequency)

            excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_A).value = frequency
            excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_B).value = str(abcd_parameters[cfg.PARAMETER_A_INDEX]).strip('()')
            excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_C).value = str(abcd_parameters[cfg.PARAMETER_B_INDEX]).strip('()')
            excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_D).value = str(abcd_parameters[cfg.PARAMETER_C_INDEX]).strip('()')
            excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_E).value = str(abcd_parameters[cfg.PARAMETER_D_INDEX]).strip('()')
            excel_network_parameters_workbook.save(os.path.join(os.getcwd(), cfg.FOLDER_EXCEL_FILES, cfg.EXCEL_NETWORK_PARAMETERS_FILE))

            row_counter = row_counter + 1
    
    else:
        messagebox.showerror(title='Error', message='Empty parameters to calculate')

def plot_parameters():
    pass

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
    global sub_networks
    global sub_networks_interconnection

    while excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_A).value is not None:
        interconnection_type = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_B).value
        sub_networks_interconnection.append(interconnection_type)

        circuit_type = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_C).value

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

    # return sub_networks, sub_networks_interconnection

def get_total_abcd_matrix_parameters(frequency: float):
    global sub_networks
    global sub_networks_interconnection

    abcd_parameters_matrix: list
    sub_networks_abcd_matrices = list()
    current_matrix_index = 0
    total_abcd_matrix = complex(0,0)
    total_of_sub_networks = len(sub_networks)
    total_of_cascade_interconnection = len(cascade_sub_networks_indexes)
    total_of_series_interconnection = len(series_sub_networks_indexes)
    total_of_parallel_interconnection = len(parallel_sub_networks_indexes)
    total_of_touchstone_interconnection = len(touchstone_sub_networks_indexes)

    #while len(sub_networks_abcd_matrices) < total_of_sub_networks:

    for sub_network in sub_networks:
        sub_networks_abcd_matrices.append(sub_network.get_matrix_abcd(at_frequency=frequency))

    if total_of_sub_networks == 1:
        total_abcd_matrix = sub_networks_abcd_matrices[current_matrix_index]
    
    else:
        if total_of_sub_networks == total_of_cascade_interconnection:
            total_abcd_matrix = sub_networks_abcd_matrices[current_matrix_index]
            current_matrix_index = current_matrix_index + 1

            while current_matrix_index < total_of_sub_networks:
                total_abcd_matrix = total_abcd_matrix * sub_networks_abcd_matrices[current_matrix_index]
                current_matrix_index = current_matrix_index + 1
        else:
            pass

    total_abcd_matrix = total_abcd_matrix.tolist()
    matrix_row_1 = total_abcd_matrix[0]
    matrix_row_2 = total_abcd_matrix[1]
    parameter_a, parameter_b = matrix_row_1
    parameter_c, parameter_d = matrix_row_2

    parameter_a = parameter_a
    parameter_b = parameter_b
    parameter_c = parameter_c
    parameter_d = parameter_d

    abcd_parameters_matrix = [parameter_a, parameter_b, parameter_c, parameter_d]

    sub_networks_abcd_matrices.clear()

    return abcd_parameters_matrix

def get_indexes_of_sub_networks_interconnection():
    global sub_networks_interconnection

    index_counter = 0

    for sub_network_interconnection in sub_networks_interconnection:
        if sub_network_interconnection == 'Series connection':
            series_sub_networks_indexes.append(index_counter)
        elif sub_network_interconnection == 'Parallel connection':
            parallel_sub_networks_indexes.append(index_counter)
        elif sub_network_interconnection == 'Cascade connection':
            cascade_sub_networks_indexes.append(index_counter)
        else:
            touchstone_sub_networks_indexes.append(index_counter)

        index_counter = index_counter + 1

mainWindow = tk.Tk()
mainWindow.title("Two-port network parameter calculator")
mainWindow.geometry('800x600')

counter_of_sub_networks = tk.IntVar(mainWindow, 0)
reset_type_of_circuit_combobox = tk.StringVar(mainWindow, '')
reset_type_of_connection_combobox = tk.StringVar(mainWindow, '')
reset_element_A_combobox = tk.StringVar(mainWindow, '')
reset_element_A_entry = tk.StringVar(mainWindow, '')
reset_element_B_combobox = tk.StringVar(mainWindow, '')
reset_element_B_entry = tk.StringVar(mainWindow, '')
reset_element_C_combobox = tk.StringVar(mainWindow, '')
reset_element_C_entry = tk.StringVar(mainWindow, '')
reset_touchstone_file_entry = tk.StringVar(mainWindow, '')
reset_start_frequency_entry = tk.StringVar(mainWindow, '')
reset_end_frequency_entry = tk.StringVar(mainWindow, '')
reset_analysis_frequency_step_entry = tk.StringVar(mainWindow, '')

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
start_frequency_entry = ttk.Entry(frame_2, state='normal', textvariable=reset_start_frequency_entry)
start_frequency_entry.grid(row=row, column=1)
start_frequency_combobox = ttk.Combobox(frame_2, state='normal', values = cfg.FREQUENCY_PREFIXES)
start_frequency_combobox.grid(row=row, column=2)

row = row + 1

end_frequency_label = ttk.Label(frame_2, text='End frequency')
end_frequency_label.grid(row=row, column=0)
end_frequency_entry = ttk.Entry(frame_2, state='normal', textvariable=reset_end_frequency_entry)
end_frequency_entry.grid(row=row, column=1)
end_frequency_combobox = ttk.Combobox(frame_2, state='normal', values=cfg.FREQUENCY_PREFIXES)
end_frequency_combobox.grid(row=row, column=2)

row = row + 1

analysis_frequency_step_label = ttk.Label(frame_2, text='Analysis frequency step')
analysis_frequency_step_label.grid(row=row, column=0)
analysis_frequency_step_entry = ttk.Entry(frame_2, state='normal', textvariable=reset_analysis_frequency_step_entry)
analysis_frequency_step_entry.grid(row=row, column=1)
analysis_frequency_step_combobox = ttk.Combobox(frame_2, state='normal', values = cfg.FREQUENCY_PREFIXES)
analysis_frequency_step_combobox.grid(row=row, column=2)

row = row + 1

spacer_5.grid(row=row, column=0)

row = row + 1

save_frequency_parameters_button = ttk.Button(frame_2, text='Save frequency parameters', state='normal', command=save_frequency_parameters)
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