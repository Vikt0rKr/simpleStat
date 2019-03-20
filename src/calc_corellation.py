from scipy.stats import pearsonr, spearmanr
import pandas as pd
from src.config import res_column_name, alpha


# make a corellation analysis based on normal distribution -> Pearson if normal else Spearman
def calc_corellation(data_frame, pages_count, writer, xl_file, normal_test_results):
    column_name = res_column_name
    # T-test is calculated for 2 result pages because they are being compared to each other
    if pages_count % 2 == 0 and column_name:
        calc_list = []
        wanted_list = []
        count = 0

        for sheet_name in xl_file.sheet_names:
            calc_list.append(xl_file.parse(sheet_name=sheet_name))
            wanted_list.append(sheet_name)

        # Pearson corellation analysis
        while count + 3 <= pages_count:
            if hasattr(calc_list[count], column_name):
                group_1 = calc_list[count][column_name].values

                group_2_columns = calc_list[count + 2].columns.tolist()
                # remove participants naming data
                group_2_columns.pop(0)

                appropriate_stat_func = pearsonr if normal_test_results[wanted_list[
                    count]] and normal_test_results[wanted_list[count+2]] else spearmanr

                if appropriate_stat_func == pearsonr:
                    print('[Corellation:{item_1}->{item_2}] Chosen {corr_test_title} for the corellation analysis because it suits current {type} distribution.'.format(
                        item_1=wanted_list[count], item_2=wanted_list[count+2], corr_test_title='Pearson' if appropriate_stat_func == pearsonr else 'Spearman', type='normal' if appropriate_stat_func == pearsonr else 'not normal'))

                data_dict = {}

                for col in group_2_columns:
                    comparing_group = calc_list[count + 2][col].values

                    corr_test_res, p = appropriate_stat_func(
                        group_1, comparing_group)

                    data_dict['{n}_p_{col}'.format(n=count, col=col)] = [p]
                    data_dict['{n}_null_{col}'.format(n=count, col=col)] = [
                        p > alpha]
                    data_dict['{n}_{col}'.format(n=count, col=col)] = [
                        corr_test_res]

                df = pd.DataFrame(data=data_dict)
                df.to_excel(
                    writer, sheet_name='{page_1}_{corr_test_title}'.format(page_1=xl_file.sheet_names[count], corr_test_title='Pearson' if appropriate_stat_func == pearsonr else 'Spearman'), engine='xlsxwriter')
            count += 1
        return True
    else:
        print(
            'Aborting corellation analysis. You need to provide an even amount of pages and a valid results column.')
        return False
