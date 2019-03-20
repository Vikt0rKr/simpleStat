from scipy.stats import normaltest
import pandas as pd
import numbers
from config import alpha


def normal_test(data_frame, page, writer, sheet_names):
    result = False
    for column in data_frame.columns:
        if column != 'ФИО':
            column_values = data_frame[column].get_values()

            for value in column_values:
                if isinstance(value, numbers.Number):
                    test_res, p = normaltest(column_values)

                    data_dict = {'p_value': [p],
                                 'null_hypothesis': [p > alpha]}
                    data_dict['normal_test'] = [test_res]

                    result = p > alpha

                    df = pd.DataFrame(data=data_dict)
                    df.to_excel(
                        writer, sheet_name='{page}-normaltest'.format(page=sheet_names[page]), engine='xlsxwriter')
    return result
