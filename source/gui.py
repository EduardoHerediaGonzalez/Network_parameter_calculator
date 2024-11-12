import tkinter as tk
from tkinter import ttk

from openpyxl import *
import config_parameters as cfg
from source.common_two_port_circuits import *

SUB_NETWORK_DEFAULT_CONNECTION = 'Cascade connection'

excel_base_template_workbook = load_workbook(filename=cfg.EXCEL_BASE_TEMPLATE_FILE)
excel_base_template_workbook.save(cfg.EXCEL_NETWORK_PARAMETERS_FILE)
excel_base_template_workbook.close()
del excel_base_template_workbook

excel_network_parameters_workbook = load_workbook(filename= cfg.EXCEL_NETWORK_PARAMETERS_FILE)
excel_network_info_sheet = excel_network_parameters_workbook[cfg.EXCEL_NETWORK_INFO_SHEET]

excel_circuit_counter_row = cfg.EXCEL_INITIAL_ROW_NETWORK_ID
frequency_points_to_analyzed = list()

def add_frequency_point_to_analyze():   ##################################### Hacer las frecuencias de prueba en pasaos

    number_of_frequencies = number_of_frequencies_entry.get()

    if number_of_frequencies != '':
        number_of_frequencies = int(number_of_frequencies)

        start_frequency = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW, column=cfg.EXCEL_COLUMN_B).value
        value, prefix = start_frequency.split()
        start_frequency = int(value) * cfg.FREQUENCY_PREFIXES_TO_VALUE[prefix]

        end_frequency = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 1, column=cfg.EXCEL_COLUMN_B).value
        value, prefix = end_frequency.split()
        end_frequency = int(value) * cfg.FREQUENCY_PREFIXES_TO_VALUE[prefix]

        frequency_step = (end_frequency - start_frequency) / number_of_frequencies
        frequency_point_to_analyzed = start_frequency - frequency_step
        num_str = ''
        prefix_str = ''

        for all_frequencies in range(number_of_frequencies):
            frequency_point_to_analyzed = frequency_point_to_analyzed + frequency_step
            if frequency_point_to_analyzed % 10e9 == 0


            frequency_points_to_analyzed.append(frequency_point_to_analyzed)

    else:
        pass

'''
def add_frequency_point_to_analyze():
    frequency_point_to_analyzed = frequency_point_to_analyze_entry.get()
    frequency_point_prefix = frequency_point_to_analyze_combobox.get()

    if frequency_point_to_analyzed == '' or frequency_point_prefix == '':
        pass

    else:
        frequency_point_to_analyzed = frequency_point_to_analyzed + ' ' + frequency_point_prefix
        frequency_points_to_analyzed.append(frequency_point_to_analyzed)

        reset_frequency_point_to_analyze_entry.set('')
        reset_frequency_point_to_analyze_combobox.set('')
'''

def save_frequency_parameters():
    start_frequency = start_frequency_entry.get()
    start_frequency_prefix = start_frequency_combobox.get()
    end_frequency = end_frequency_entry.get()
    end_frequency_prefix = end_frequency_combobox.get()

    if start_frequency == '' or start_frequency_prefix == '' or end_frequency == '' or end_frequency_prefix == '':
        pass
    else:
        frequency_points = ','.join(frequency_points_to_analyzed)
        excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW, column=cfg.EXCEL_COLUMN_B).value = start_frequency + ' ' + start_frequency_prefix
        excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 1, column=cfg.EXCEL_COLUMN_B).value = end_frequency + ' ' + end_frequency_prefix
        excel_network_info_sheet.cell(row =cfg.EXCEL_INITIAL_ROW + 2, column = cfg.EXCEL_COLUMN_B).value = frequency_points
        excel_network_parameters_workbook.save(cfg.EXCEL_NETWORK_PARAMETERS_FILE)

        start_frequency_entry.config(state='disable')
        start_frequency_combobox.config(state = 'disable')
        end_frequency_entry.config(state='disable')
        end_frequency_combobox.config(state='disable')
        frequency_point_to_analyze_entry.config(state='disable')
        frequency_point_to_analyze_combobox.config(state='disable')
        frequency_point_to_analyze_button.config(state='disable')
        save_frequency_parameters_button.config(state='disable')
        type_of_network_combobox.config(state='normal')
        parameters_to_calculate_combobox.config(state='normal')
        save_network_parameters_button.config(state='normal')


def save_network_parameters():
    type_of_network = type_of_network_combobox.get()
    parameters_to_calculate = parameters_to_calculate_combobox.get()

    if type_of_network == '' or parameters_to_calculate == '':
        pass
    else:
        excel_network_info_sheet.cell(row =cfg.EXCEL_INITIAL_ROW + 4, column = cfg.EXCEL_COLUMN_B).value = type_of_network
        excel_network_info_sheet.cell(row =cfg.EXCEL_INITIAL_ROW + 5, column = cfg.EXCEL_COLUMN_B).value = parameters_to_calculate
        excel_network_parameters_workbook.save(cfg.EXCEL_NETWORK_PARAMETERS_FILE)

        type_of_network_combobox.config(state = 'disable')
        parameters_to_calculate_combobox.config(state = 'disable')
        save_network_parameters_button.config(state = 'disable')
        type_of_circuit_combobox.config(state = 'normal')
        type_of_interconnection_combobox.config(state ='normal')
        characteristic_impedance_entry.config(state = 'normal')
        element_A_combobox.config(state = 'normal')
        element_A_entry.config(state = 'normal')
        element_B_combobox.config(state = 'normal')
        element_B_entry.config(state = 'normal')
        element_C_combobox.config(state = 'normal')
        element_C_entry.config(state = 'normal')
        add_sub_network_button.config(state ='normal')  # ************************************************************

def add_sub_network():
    type_of_circuit = type_of_circuit_combobox.get()
    type_of_interconnection = type_of_interconnection_combobox.get()
    characteristic_impedance = characteristic_impedance_entry.get()  # *************************************************
    element_a = element_A_combobox.get()
    element_a_value = element_A_entry.get()
    element_b = element_B_combobox.get()
    element_b_value = element_B_entry.get()
    element_c = element_C_combobox.get()
    element_c_value = element_C_entry.get()


    if type_of_circuit == '' and ((element_a == '' and element_a_value == '') and (element_b == '' and element_b_value == '') and (element_c == '' and element_c_value == '')):
        pass
    else:
        global excel_circuit_counter_row

        counter = counter_of_sub_networks.get()
        counter = counter + 1

        if type_of_interconnection == '':
            type_of_interconnection = SUB_NETWORK_DEFAULT_CONNECTION

        excel_network_info_sheet.cell(row =  excel_circuit_counter_row, column=cfg.EXCEL_COLUMN_A, value=str(counter))
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_B, value = type_of_interconnection)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_C, value = type_of_circuit)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_D, value = element_a)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_E, value = join_value_and_prefix(element_a_value))
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_F, value = element_b)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_G, value = join_value_and_prefix(element_b_value))
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_H, value = element_c)
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_I, value = join_value_and_prefix(element_c_value))
        excel_network_info_sheet.cell(row = excel_circuit_counter_row, column = cfg.EXCEL_COLUMN_J, value = characteristic_impedance)  #**********

        excel_network_parameters_workbook.save(cfg.EXCEL_NETWORK_PARAMETERS_FILE)

        excel_circuit_counter_row = excel_circuit_counter_row + 1

        counter_of_sub_networks.set(counter)
        reset_type_of_circuit_combobox.set('')
        reset_type_of_connection_combobox.set('')
        reset_element_A_combobox.set('')
        reset_element_A_entry.set('')
        reset_element_B_combobox.set('')
        reset_element_B_entry.set('')
        reset_element_C_combobox.set('')
        reset_element_C_entry.set('')
        reset_characteristic_impedance_entry.set('')  # ****************************************************************


        if counter == 1:
            calculate_parameters_button.config(state='normal')


def calculate_parameters():
    sub_network_id_counter = cfg.EXCEL_INITIAL_ROW_NETWORK_ID
    sub_networks = []
    sub_networks_interconnection = []
    sub_networks_matrixes = []
    excel_abcd_parameters_sheet = excel_network_parameters_workbook[cfg.EXCEL_ABCD_PARAMETERS_SHEET]

    while excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_A).value is not None:
        # sub_network_id = excel_network_info_sheet.cell(row=sub_network_id_counter, column=cfg.EXCEL_COLUMN_A).value
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


    start_frequency = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW, column=cfg.EXCEL_COLUMN_B).value
    value, prefix = start_frequency.split()
    start_frequency = int(value) * cfg.FREQUENCY_PREFIXES_TO_VALUE[prefix]

    end_frequency = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 1, column=cfg.EXCEL_COLUMN_B).value
    value, prefix = end_frequency.split()
    end_frequency = int(value) * cfg.FREQUENCY_PREFIXES_TO_VALUE[prefix]

    frequency_points_to_be_analyzed = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 2, column=cfg.EXCEL_COLUMN_B).value

    if len(frequency_points_to_be_analyzed) != 0:
        frequency_points_to_be_analyzed = frequency_points_to_be_analyzed.split(',')

    frequency_points_to_be_analyzed = get_total_frequency_points(start_frequency, frequency_points_to_be_analyzed, end_frequency)

    parameters_to_calculate = excel_network_info_sheet.cell(row=cfg.EXCEL_INITIAL_ROW + 5, column=cfg.EXCEL_COLUMN_B).value

    row_counter = cfg.EXCEL_INITIAL_ROW

    for frequency_to_analyzed in frequency_points_to_be_analyzed:
        for sub_network in sub_networks:
            sub_networks_matrixes.append(sub_network.get_matrix_abcd(at_frequency=frequency_to_analyzed))

        # Algorithm for multiply all the matrixes
        total_of_matrixes = len(sub_networks_matrixes)
        next_matrix_index = 2
        # global matrix
        if total_of_matrixes > 1:
            matrix = sub_networks_matrixes[0] * sub_networks_matrixes[1]
        else:
            matrix = sub_networks_matrixes[0]

        while next_matrix_index < total_of_matrixes:
            matrix = matrix * sub_networks_matrixes[next_matrix_index]

        matrix = matrix.tolist()
        matrix_row_1 = matrix[0]
        matrix_row_2 = matrix[1]
        parameter_a, parameter_b = matrix_row_1
        parameter_c, parameter_d = matrix_row_2

        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_A).value = frequency_to_analyzed
        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_B).value = str(parameter_a)
        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_C).value = str(parameter_b)
        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_D).value = str(parameter_c)
        excel_abcd_parameters_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_E).value = str(parameter_d)
        excel_network_parameters_workbook.save(cfg.EXCEL_NETWORK_PARAMETERS_FILE)

        row_counter = row_counter + 1

        sub_networks_matrixes.clear()



def get_total_frequency_points(start_frequency, frequency_points, end_frequency):
    frequency_points_temp = []
    frequency_range = []

    for frequency_point in frequency_points:
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


mainWindow = tk.Tk()
mainWindow.title("Network parameter calculator")
mainWindow.geometry('800x600')

counter_of_sub_networks = tk.IntVar(mainWindow, 0)
reset_frequency_point_to_analyze_entry = tk.StringVar(mainWindow, '')
reset_frequency_point_to_analyze_combobox = tk.StringVar(mainWindow, '')
reset_type_of_circuit_combobox = tk.StringVar(mainWindow, '')
reset_type_of_connection_combobox = tk.StringVar(mainWindow, '')
reset_element_A_combobox = tk.StringVar(mainWindow, '')
reset_element_A_entry = tk.StringVar(mainWindow, '')
reset_element_B_combobox = tk.StringVar(mainWindow, '')
reset_element_B_entry = tk.StringVar(mainWindow, '')
reset_element_C_combobox = tk.StringVar(mainWindow, '')
reset_element_C_entry = tk.StringVar(mainWindow, '')
reset_characteristic_impedance_entry = tk.StringVar(mainWindow, '') # ********************************************

row = 0

start_frequency_label = ttk.Label(mainWindow, text = 'Start frequency')
start_frequency_label.grid(row=row, column=0)
start_frequency_entry = ttk.Entry(mainWindow)
start_frequency_entry.grid(row=row, column=1)
start_frequency_combobox = ttk.Combobox(mainWindow, values = cfg.FREQUENCY_PREFIXES)
start_frequency_combobox.grid(row=row, column=2)

row = row + 1

end_frequency_label = ttk.Label(mainWindow, text='End frequency')
end_frequency_label.grid(row=row, column=0)
end_frequency_entry = ttk.Entry(mainWindow)
end_frequency_entry.grid(row=row, column=1)
end_frequency_combobox = ttk.Combobox(mainWindow, values=cfg.FREQUENCY_PREFIXES)
end_frequency_combobox.grid(row=row, column=2)

row = row + 1

"""""
frequency_point_to_analyze_label = ttk.Label(mainWindow, text='Frequency point to analyze')
frequency_point_to_analyze_label.grid(row=row, column=0)
frequency_point_to_analyze_entry = ttk.Entry(mainWindow, textvariable=reset_frequency_point_to_analyze_entry)
frequency_point_to_analyze_entry.grid(row=row, column=1)
frequency_point_to_analyze_combobox = ttk.Combobox(mainWindow, values=cfg.FREQUENCY_PREFIXES, textvariable=reset_frequency_point_to_analyze_combobox)
frequency_point_to_analyze_combobox.grid(row=row, column=2)
frequency_point_to_analyze_button = ttk.Button(mainWindow, text='Add', command=add_frequency_point_to_analyze)
frequency_point_to_analyze_button.grid(row=row, column=3)

row = row + 1
"""
# *************************************************************************************************************** Insertar numero de freq
number_of_frequencies_label = ttk.Label(mainWindow, text='Number of frequencies to analyze')
number_of_frequencies_label.grid(row=row, column=0)
number_of_frequencies_entry = ttk.Entry(mainWindow, textvariable=reset_frequency_point_to_analyze_entry)
number_of_frequencies_entry.grid(row=row, column=1)

row = row + 1

spacer_1 = ttk.Label(mainWindow)
spacer_1.grid(row=row, column=0)

row = row + 1

save_frequency_parameters_button = ttk.Button(mainWindow, text='Save frequency parameters',
                                              command=save_frequency_parameters)
save_frequency_parameters_button.grid(row=row, column=2)

row = row + 1

spacer_1 = ttk.Label(mainWindow)
spacer_1.grid(row=row, column=0)

row = row + 1

type_of_network_label = ttk.Label(mainWindow, text='Type of network')
type_of_network_label.grid(row=row, column=0)
type_of_network_combobox = ttk.Combobox(mainWindow, values=cfg.NETWORK_TYPES, state='disable')
type_of_network_combobox.grid(row=row, column=1)

row = row + 1

spacer_1 = ttk.Label(mainWindow)
spacer_1.grid(row=row, column=0)

row = row + 1

parameters_to_calculate_label = ttk.Label(mainWindow, text='Parameters to calculate')
parameters_to_calculate_label.grid(row=row, column=0)
parameters_to_calculate_combobox = ttk.Combobox(mainWindow, values=cfg.NETWORK_PARAMETERS, state='disable')
parameters_to_calculate_combobox.grid(row=row, column=1)

#In case of N-port uncomment the next lines
#total_of_ports_label = ttk.Label(mainWindow, text='Total of ports')
#total_of_ports_label.grid(row=row, column=2)
#total_of_ports_entry = ttk.Entry(mainWindow)
#total_of_ports_entry.grid(row=row, column=3)
#total_of_ports_entry.config(state='normal')

row = row + 1

spacer_1 = ttk.Label(mainWindow)
spacer_1.grid(row=row, column=0)

row = row + 1

save_network_parameters_button = ttk.Button(mainWindow, text='Save network parameters', state='disable', command=save_network_parameters)
save_network_parameters_button.grid(row=row, column=2)

row = row + 1

spacer_4 = ttk.Label(mainWindow)
spacer_4.grid(row=row, column=0)

row = row + 1

type_of_circuit_label = ttk.Label(mainWindow, text='Type of circuit')
type_of_circuit_label.grid(row=row, column=0)
type_of_circuit_combobox = ttk.Combobox(mainWindow, values=cfg.CIRCUIT_TYPES, state='disable', textvariable=reset_type_of_circuit_combobox)
type_of_circuit_combobox.grid(row=row, column=1)

total_of_circuits_label = ttk.Label(mainWindow, text='Total of sub-networks:')
total_of_circuits_label.grid(row=row, column=2)
total_of_circuits_label = ttk.Label(mainWindow, textvariable=counter_of_sub_networks)
total_of_circuits_label.grid(row=row, column=3)

row = row + 1

type_of_interconnection_label = ttk.Label(mainWindow, text='Type of interconnection')
type_of_interconnection_label.grid(row=row, column=0)
type_of_interconnection_combobox = ttk.Combobox(mainWindow, values=cfg.INTERCONNECTION_TYPES, state='disable', textvariable=reset_type_of_connection_combobox)
type_of_interconnection_combobox.grid(row=row, column=1)

row = row + 1

# *********** AQUI ES DONDE MOVI ***************************************************************************************
characteristic_impedance_label = ttk.Label(mainWindow, text='Characteristic Impedance')
characteristic_impedance_label.grid(row=row, column=0)
characteristic_impedance_entry = ttk.Entry(mainWindow, state='disable', textvariable=reset_characteristic_impedance_entry)
characteristic_impedance_entry.grid(row=row, column=1)

row = row + 1
# **********************************************************************************************************************

spacer_5 = ttk.Label(mainWindow)
spacer_5.grid(row=row, column=0)

row = row + 1

element_A_label = ttk.Label(mainWindow, text='Element A')
element_A_label.grid(row=row, column=0)
element_A_combobox = ttk.Combobox(mainWindow, values=cfg.ELEMENT_TYPES, state='disable', textvariable=reset_element_A_combobox)
element_A_combobox.grid(row=row, column=1)
element_A_value_label = ttk.Label(mainWindow, text='Value')
element_A_value_label.grid(row=row, column=2)
element_A_entry = ttk.Entry(mainWindow, state='disable', textvariable=reset_element_A_entry)
element_A_entry.grid(row=row, column=3)

row = row + 1

element_B_label = ttk.Label(mainWindow, text='Element B')
element_B_label.grid(row=row, column=0)
element_B_combobox = ttk.Combobox(mainWindow, values=cfg.ELEMENT_TYPES, state='disable', textvariable=reset_element_B_combobox)
element_B_combobox.grid(row=row, column=1)
element_B_value_label = ttk.Label(mainWindow, text='Value')
element_B_value_label.grid(row=row, column=2)
element_B_entry = ttk.Entry(mainWindow, state='disable', textvariable=reset_element_B_entry)
element_B_entry.grid(row=row, column=3)

row = row + 1

element_C_label = ttk.Label(mainWindow, text='Element C')
element_C_label.grid(row=row, column=0)
element_C_combobox = ttk.Combobox(mainWindow, values=cfg.ELEMENT_TYPES, state='disable', textvariable=reset_element_C_combobox)
element_C_combobox.grid(row=row, column=1)
element_C_value_label = ttk.Label(mainWindow, text='Value')
element_C_value_label.grid(row=row, column=2)
element_C_entry = ttk.Entry(mainWindow, state='disable', textvariable=reset_element_C_entry)
element_C_entry.grid(row=row, column=3)

row = row + 1

add_sub_network_button = ttk.Button(mainWindow, text='Add sub-network', state='disable', command=add_sub_network)
add_sub_network_button.grid(row=row, column=2)

row = row + 1

calculate_parameters_button = ttk.Button(mainWindow, text='Calculate parameters', state='normal', command=calculate_parameters)
calculate_parameters_button.grid(row=row, column=2)

mainWindow.mainloop()
