
FILE_NAME = "test-nmc.xlsx"
sheet_name = "Sheet2"


FILE_NAME = "File NMC Nurse Scrapes_Manual Effort.xlsx"
sheet_name = "Extract 1_ NMC List View"


import xlrd

# Replace 'your_file.xlsx' with the actual file path
# file_path = 'your_file.xlsx'

# Open the Excel file using xlrd
workbook = xlrd.open_workbook(FILE_NAME)

sheet = workbook.sheet_by_name(sheet_name)

# Iterate through rows in the sheet
for row_index in range(1,10):
    cell_value = sheet.cell_value(row_index, 6)

    cell_url = None

    # Check if the cell contains a hyperlink
    if sheet.hyperlink_map.get((row_index, 6)):
        cell_url = sheet.hyperlink_map.get((row_index, 6)).url_or_path

        print(cell_url)

