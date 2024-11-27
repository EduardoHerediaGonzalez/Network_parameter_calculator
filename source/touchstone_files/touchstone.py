import source.config_parameters as cfg

def get_frequency_parameters_from_touchstone_file(excel_touchstone_sheet):
    row_counter = 1

    symbol = excel_touchstone_sheet.cell(row=row_counter, column= cfg.EXCEL_COLUMN_A).value
    symbol = symbol.split()
    symbol = symbol[0]

    while symbol != '#':

        row_counter = row_counter + 1
        symbol = excel_touchstone_sheet.cell(row=row_counter, column=cfg.EXCEL_COLUMN_A).value
        symbol = symbol.split()
        symbol = symbol[0]

    start_frequency_row = row_counter + 1
    start_frequency = excel_touchstone_sheet.cell(row=start_frequency_row, column= cfg.EXCEL_COLUMN_A).value
    start_frequency = start_frequency.split()
    start_frequency = start_frequency[0]
    start_frequency = float(start_frequency)

    next_frequency_row = start_frequency_row + 1
    next_frequency = excel_touchstone_sheet.cell(row=next_frequency_row, column= cfg.EXCEL_COLUMN_A).value
    next_frequency = next_frequency.split()
    next_frequency = next_frequency[0]
    next_frequency = float(next_frequency)

    analysis_frequency_step = next_frequency - start_frequency

    end_frequency_row = excel_touchstone_sheet.max_row
    end_frequency = excel_touchstone_sheet.cell(row=end_frequency_row, column= cfg.EXCEL_COLUMN_A).value
    end_frequency = end_frequency.split()
    end_frequency = end_frequency[0]
    end_frequency = float(end_frequency)

    return start_frequency, end_frequency, analysis_frequency_step

def read_touchstone_file():
    pass

def write_touchstone_file():
    pass