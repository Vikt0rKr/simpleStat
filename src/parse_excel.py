import os
import pandas as pd
import numbers
import re


def parse_excel_file():
    path = os.getcwd()
    # query user parameters
    name = input('Enter file name to parse workbook from: ')
    pages_count = int(input('What number of pages should i use?: '))
    output_file_name = input('Enter file name for the output: ')

    if name:
        # scan cwd for files and open matching file
        with os.scandir(path) as file_list:
            for file in file_list:
                # currently, only xlsx format is supported -> TODO
                if file.is_file() and file.name == '{file_name}.xlsx'.format(file_name=name):
                    if pages_count != None and isinstance(int(pages_count), numbers.Number):
                        # # ask if T-test is needed
                        # need_t_test = str(
                        #     input('Make a T-test? y/n:'))

                        # if re.match(r'^y', need_t_test, re.IGNORECASE):
                        #     print('processing T-test...')
                        # # ask if F-test is needed
                        # need_f_test = str(
                        #     input('Make a Fisher F-criteria test? y/n:'))

                        # if re.match(r'^y', need_f_test, re.IGNORECASE):
                        #     print('processing Fisher F-criteria test...')

                        # # ask if Pearson is needed
                        # need_pearson_test = str(
                        #     input('Make a Pearson test? y/n:'))

                        # if re.match(r'^y', need_pearson_test, re.IGNORECASE):
                        #     print('processing Pearson test...')
                        # # ask if Spearman is needed
                        # need_spearman_test = str(
                        #     input('Make a Spearman test? y/n:'))

                        # if re.match(r'^y', need_pearson_test, re.IGNORECASE):
                        #     print('processing Spearman test...')
                        with pd.ExcelWriter('{name}.xlsx'.format(name=output_file_name if output_file_name != None else statistics)) as writer:
                            xl_file = pd.ExcelFile(file.name)
                            sheet_names = xl_file.sheet_names
                            for page in range(0, int(pages_count)):
                                data_book = pd.read_excel(file.name, page)
                                # descriptive statistics
                                data_book.describe().to_excel(
                                    writer, sheet_name=sheet_names[page], engine='xlsxwriter')
                                # other statistics processing
                        print('Completed xlsx convertation')
                    else:
                        print('Cannot detect file or format is incorrect')
    else:
        print('No file name was provided')