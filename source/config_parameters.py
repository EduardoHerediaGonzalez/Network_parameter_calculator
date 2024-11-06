NETWORK_TYPES = ['Two-port', 'N-port']
CIRCUIT_TYPES = ['Series impedance', 'Shunt impedance', 'T', 'Pi'] #['Series impedance', 'Shunt impedance', 'T', 'Pi', 'Transmission line', 'Transformer']
INTERCONNECTION_TYPES = ['Series connection', 'Parallel connection']
ELEMENT_TYPES = ['Resistor', 'Capacitor', 'Inductor']
FREQUENCY_PREFIXES = ['Hz', 'KHz', 'MHz', 'GHz']
RESISTOR_PREFIXES = ['\u03A9', 'K\u03A9', 'M\u03A9', 'G\u03A9']
CAPACITOR_PREFIXES = ['pF', 'nF', 'uF', 'F']
INDUCTOR_PREFIXES = ['uH', 'mH', 'H']
NETWORK_PARAMETERS = ['Z', 'Y', 'ABCD', 'S']
FREQUENCY_PREFIXES_TO_VALUE = {'Hz': 1, 'KHz': 1000, 'MHz': 1e6, 'GHz': 1e9}
MAGNITUDES_PREFIXES_TO_VALUE = {'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'K': 1e3, 'M': 1e6, 'G': 1e9, 'F': 1, 'H': 1}
EXCEL_BASE_TEMPLATE_FILE = 'Base template.xlsx'
EXCEL_NETWORK_PARAMETERS_FILE = 'Network parameters.xlsx'
EXCEL_NETWORK_INFO_SHEET = 'Network info'
EXCEL_NETWORK_Z_PARAMETERS_SHEET = 'Z-parameters'
EXCEL_NETWORK_Y_PARAMETERS_SHEET = 'Y-parameters'
EXCEL_NETWORK_S_PARAMETERS_SHEET = 'S-parameters'
EXCEL_NETWORK_ABCD_PARAMETERS_SHEET = 'ABCD-parameters'
EXCEL_COLUMN_A = 1
EXCEL_COLUMN_B = 2
EXCEL_COLUMN_C = 3
EXCEL_COLUMN_D = 4
EXCEL_COLUMN_E = 5
EXCEL_COLUMN_F = 6
EXCEL_COLUMN_G = 7
EXCEL_COLUMN_H = 8
EXCEL_COLUMN_I = 9
EXCEL_INITIAL_ROW = 3
EXCEL_INITIAL_ROW_NETWORK_ID = 11
