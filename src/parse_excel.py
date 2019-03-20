import os
import pandas as pd
import numbers
import re
from normal_test import normal_test
from calc_t_test import calc_t_test
from calc_distribution_based_test import calc_distribution_based_test
from calc_corellation import calc_corellation


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
                        with pd.ExcelWriter('{name}.xlsx'.format(name=output_file_name if output_file_name != None else statistics)) as writer:
                            xl_file = pd.ExcelFile(file.name)
                            sheet_names = xl_file.sheet_names

                            # ask if T-test is needed
                            need_t_test = input(
                                'Do you need T-test for the data? y/n: ')
                            # ask if distribution is needed
                            need_distr_test = input(
                                'Do you need distribution test for the data? y/n: ')
                            # ask if Pearson/Spearman corellation analysis is needed
                            need_corr_test = input(
                                'Do you need corellation test for the groups? y/n: ')

                            normal_test_results = {}
                            for page in range(0, int(pages_count)):
                                data_book = pd.read_excel(file.name, page)
                                # descriptive statistics
                                data_book.describe().to_excel(
                                    writer, sheet_name='{n}-D'.format(n=sheet_names[page]), engine='xlsxwriter')
                                # normal test for each data page
                                normal_test_results[sheet_names[page]] = normal_test(data_book, page,
                                                                                     writer, sheet_names)

                            # T-test for each data page with normal distribution
                            if re.match(r'^y', need_t_test, re.IGNORECASE):
                                calc_t_test(data_book, pages_count,
                                            writer, xl_file, normal_test_results)
                            # distribution test processing
                            if re.match(r'^y', need_distr_test, re.IGNORECASE):
                                calc_distribution_based_test(data_book, pages_count,
                                                             writer, xl_file, normal_test_results)
                            # Corellation test processing
                            if re.match(r'^y', need_corr_test, re.IGNORECASE):
                                calc_corellation(data_book, pages_count,
                                                 writer, xl_file, normal_test_results)
                        print('Completed xlsx convertation')
                    else:
                        print('Cannot detect file or format is incorrect')
    else:
        print('No file name was provided')
