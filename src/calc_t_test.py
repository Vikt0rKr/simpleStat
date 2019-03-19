from scipy.stats import ttest_ind
import pandas as pd
from config import res_column_name, alpha


def calc_t_test(data_frame, pages_count,
                writer, xl_file):
    column_name = res_column_name
    # T-test is calculated for 2 result pages because they are being compared to each other
    if pages_count % 2 == 0 and column_name:
        calc_list = []
        count = 0

        for sheet_name in xl_file.sheet_names:
            calc_list.append(xl_file.parse(sheet_name=sheet_name))
        # T-test independent
        while count + 1 <= pages_count:
            if hasattr(calc_list[count], column_name):
                group_1 = calc_list[count][column_name].values
                group_2 = calc_list[count + 1][column_name].values

                t_test_ind_res, p = ttest_ind(group_1, group_2)

                data_dict = {'p_value': [p], 'null_hypothesis': [p > alpha]}
                data_dict[column_name] = [t_test_ind_res]

                df = pd.DataFrame(data=data_dict)
                df.to_excel(
                    writer, sheet_name='{page_1}-T'.format(page_1=xl_file.sheet_names[count]), engine='xlsxwriter')
            else:
                wanted_columns = calc_list[count].columns.tolist()
                # remove participants naming data
                wanted_columns.pop(0)

                for col in wanted_columns:
                    group_1 = calc_list[count][col].values
                    group_2 = calc_list[count + 1][col].values

                    t_test_ind_res, p = ttest_ind(group_1, group_2)

                    data_dict = {'p_value': [p],
                                 'null_hypothesis': [p > alpha]}
                    data_dict[col] = [t_test_ind_res]

                    df = pd.DataFrame(data=data_dict)
                    df.to_excel(
                        writer, sheet_name='{page_1}-T'.format(page_1=xl_file.sheet_names[count]), engine='xlsxwriter')
            count += 2
        return True
    else:
        print(
            'Aborting T-test calculation. You need to provide an even amount of pages and a valid results column.')
        return False
