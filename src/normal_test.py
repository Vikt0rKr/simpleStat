from scipy.stats import normaltest
import pandas as pd
import numbers


def normal_test(data_frame, page, writer, sheet_names):
    for column in data_frame.columns:
        if column != 'ФИО':
            alpha = 1e-3
            column_values = data_frame[column].get_values()

            for value in column_values:
                if not isinstance(value, numbers.Number):
                    return False

            test_res, p = normaltest(column_values)

            data_dict = {'p_value': [p], 'null_hypothesis': [p > alpha]}
            data_dict['normal_test'] = [test_res]

            df = pd.DataFrame(data=data_dict)
            df.to_excel(
                writer, sheet_name='{page}-normaltest'.format(page=sheet_names[page]), engine='xlsxwriter')
    return True
