from scipy.stats import pearsonr
import pandas as pd
from config import res_column_name, alpha


def calc_pearson(data_frame, pages_count, writer, xl_file):
    column_name = res_column_name
    # T-test is calculated for 2 result pages because they are being compared to each other
    if pages_count % 2 == 0 and column_name:
        calc_list = []
        count = 0

        for sheet_name in xl_file.sheet_names:
            calc_list.append(xl_file.parse(sheet_name=sheet_name))

        # Pearson corellation analysis
        while count + 3 <= pages_count:
            if hasattr(calc_list[count], column_name):
                group_1 = calc_list[count][column_name].values

                group_2_columns = calc_list[count + 2].columns.tolist()
                # remove participants naming data
                group_2_columns.pop(0)

                data_dict = {}

                for col in group_2_columns:
                    comparing_group = calc_list[count + 2][col].values

                    pearson_test_res, p = pearsonr(group_1, comparing_group)

                    data_dict['{n}_p_{col}'.format(n=count, col=col)] = [p]
                    data_dict['{n}_null_{col}'.format(n=count, col=col)] = [
                        p > alpha]
                    data_dict['{n}_{col}'.format(n=count, col=col)] = [
                        pearson_test_res]

                df = pd.DataFrame(data=data_dict)
                df.to_excel(
                    writer, sheet_name='{page_1}_Pearson'.format(page_1=xl_file.sheet_names[count]), engine='xlsxwriter')
            count += 1
        return True
    else:
        print(
            'Aborting Pearson corellation calculation. You need to provide an even amount of pages and a valid results column.')
        return False
