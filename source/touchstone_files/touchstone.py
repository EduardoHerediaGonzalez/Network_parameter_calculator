import source.config_parameters as cfg

def get_start_and_end_frequencies(excel_touchstone_sheet):
    row_counter = 1

    end_frequency_row = excel_touchstone_sheet.max_row

    end_frequency = excel_touchstone_sheet.cell(row=end_frequency_row, column= cfg.EXCEL_COLUMN_A).value
    end_frequency = end_frequency.split()
    end_frequency = end_frequency[0]
    end_frequency = float(end_frequency)

    x_value = excel_touchstone_sheet.cell(row=row_counter, column= cfg.EXCEL_COLUMN_A).value
    x_value = x_value.split()
    x_value = x_value[0]

    while x_value != '#':

        row_counter = row_counter + 1
        x_value = excel_touchstone_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_A).value
        x_value = x_value.split()
        x_value = x_value[0]

    start_frequency_row = row_counter + 1

    start_frequency = excel_touchstone_sheet.cell(row=start_frequency_row, column= cfg.EXCEL_COLUMN_A).value
    start_frequency = start_frequency.split()
    start_frequency = start_frequency[0]
    start_frequency = float(start_frequency)

    analysis_frequency_step = (int(end_frequency_row) - int(start_frequency_row)) + 1

    return start_frequency, end_frequency, analysis_frequency_step

def read_touchstone_file():
    pass

def write_touchstone_file():
    pass