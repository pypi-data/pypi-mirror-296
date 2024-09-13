'''Writing .xlsx files'''

import os
from datetime import date
from decimal import Decimal
import xlsxwriter

class WorkSheet:
    '''Worksheet class for the workbook class
    name: name of the worksheet
    header: header of the worksheet, list[str]
    data: data of the worksheet, list[list[]]
    header_comment: comment on the headers, list[[str, str]]'''

    def __init__(self, name: str, header: list[str], data: list[list], header_comment: list = None):
        self.name: str = name
        self.header: list[str] = header
        self.data: list[list] = data
        self.header_comment: list = header_comment if header_comment else []

    def __str__(self):
        return self.name

    # Seggesting a column width with min. and max. filter
    def suggest_width(self, col: int, min_width: int = 10, max_width: int = 40):
        '''Suggesting a column width with min. and max. filter'''

        length: int = min_width
        if self.header:
            if len(str(self.header[col])) > length:
                length: int = len(str(self.header[col]))
        if self.data:
            for row in self.data:
                if len(row) > col and len(str(row[col])) > length:
                    length: int = len(str(row[col]))

        return (length if length < max_width else max_width)


class WorkBook:
    '''Workbook class
    name: name of the workbook
    content: content of the workbook, worksheet or list[worksheet]'''

    def __init__(self, name: str, content: list[WorkSheet]):
        self.name: str = name
        self.content: list[WorkSheet] = content

    def __str__(self):
        return self.name
    
    # Creating the .xlsx
    def xlsx_create(self, file_path: str = os.getcwd(), file_name: str = None) -> str:
        '''Creating the .xlsx'''

        # Creating the name of the .xlsx
        file_name: str = (self.name if file_name is None else file_name)
        if not file_name.lower().endswith(".xlsx"):
            file_name += ".xlsx"
        excel_file: str = os.path.join(file_path, file_name)

        # Creating the .xlsx
        file: xlsxwriter.workbook = xlsxwriter.Workbook(excel_file)
        bold_format = file.add_format({"bold": True})
        date_format = file.add_format({'num_format': 'yyyy.mm.dd'})
        number_format = file.add_format({'num_format': '#,##0.00'})

        # Fetching the worksheet(s)
        worksheets: list = []
        if type(self.content) != list:
            worksheets.append(self.content)
        else:
            for element in self.content:
                worksheets.append(element)

        print(f"{file_name} is {str(len(worksheets))} worksheet(s):")

        # Creating the worksheet(s)
        for wsheet in worksheets:
            print(f"\t {wsheet.name}")
            sheet = file.add_worksheet(wsheet.name)
            row: int = 0
            col: int = 0
            last_row: int = row
            last_col: int = col

            # If available, then creating a header
            if wsheet.header:
                sheet.freeze_panes(1, 0)
                for element in wsheet.header:
                    width = wsheet.suggest_width(col)
                    sheet.set_column(col, col, width)
                    sheet.write(row, col, element, bold_format)
                    # If available, then adding comments
                    if wsheet.header_comment:
                        for comment in wsheet.header_comment:
                            if element == comment[0]:
                                sheet.write_comment(row, col, comment[1])
                    col += 1
                    last_col = (col if col > last_col else last_col)

            # If available, then creating the data
            if wsheet.data:
                row += 1
                last_row = (row if row > last_row else last_row)
                for line in wsheet.data:
                    col = 0
                    for element in line:
                        # Checking for basic types
                        if isinstance(element, date):
                            try:
                                sheet.write_datetime(row, col, element, date_format)
                            except:
                                pass
                        elif isinstance(element, Decimal):
                            try:
                                sheet.write(row, col, element, number_format)
                            except:
                                pass
                        else:
                            try:
                                sheet.write(row, col, element)
                            except:
                                pass
                        col += 1
                        last_col = (col if col > last_col else last_col)
                    row += 1
                    last_row = (row if row > last_row else last_row)

            # If header is available, then adding an aoutfilter
            if wsheet.header:
                if last_col != 0:
                    last_col -= 1
                sheet.autofilter(0, 0, last_row, last_col)

        # Closing the .xlsx
        file.close()

        print(f"xlsx created: {excel_file}")

        return excel_file
