from openpyxl.styles import Border, Side, Alignment

def apply_border_to_excel_sheet(start_cell: str, end_cell: str, to_sheet):
    cell_range = to_sheet[start_cell:end_cell]

    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'),
                    bottom=Side(style='thin'))

    for row in cell_range:
        for cell in row:
            cell.border = border

def adjust_columns_width_of_excel_sheet(columns: list, columns_width: list, to_sheet):
    column_width_index = 0

    for column in columns:
       to_sheet.column_dimensions[column].width = columns_width[column_width_index]
       column_width_index = column_width_index + 1

def apply_cell_text_alignment(start_cell: str, end_cell: str, type_of_alignment: str, to_sheet):
    cell_range = to_sheet[start_cell:end_cell]

    for row in cell_range:
        for cell in row:
            cell = str(cell)
            cell = cell.split('.')
            cell = cell[1]
            cell = cell.replace('>', '')
            to_sheet[cell].alignment = Alignment(horizontal=type_of_alignment)
