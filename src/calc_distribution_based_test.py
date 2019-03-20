from scipy.stats import fisher_exact, mannwhitneyu, normaltest
import pandas as pd
from src.config import res_column_name, alpha, digital_addiction_entry_level, digital_addiction_mid_level, subj_control_level_criteria


# try to calculate Fisher exact if normal test is ok, else calculate Manna-Whitney U test
def calc_distribution_based_test(data_frame, pages_count, writer, xl_file, normal_test_results):
    column_name = res_column_name
    # F-test is calculated for 2 result pages because they are being compared to each other
    if pages_count % 2 == 0 and column_name:
        calc_list = []
        wanted_list = []
        count = 0

        for sheet_name in xl_file.sheet_names:
            calc_list.append(xl_file.parse(sheet_name=sheet_name))
            wanted_list.append(sheet_name)
        # F-test exact/ M-W U-test
        while count + 1 <= pages_count:
            if hasattr(calc_list[count], column_name):
                # in my case, first 2 pages are related to digital addiction
                group_1 = calc_list[count][column_name].values.tolist()
                group_2 = calc_list[count + 1][column_name].values.tolist()

                appropriate_stat_func = fisher_exact if normal_test_results[wanted_list[
                    count]] and normal_test_results[wanted_list[count+1]] else mannwhitneyu

                group_1_overall = {'no_addiction': len(list(filter(
                    lambda v: v < digital_addiction_entry_level, group_1))), 'entry_level': len(list(filter(
                        lambda v: digital_addiction_entry_level <= v < digital_addiction_mid_level, group_1))), 'mid_level': len(list(filter(
                            lambda v: digital_addiction_mid_level <= v, group_1)))}
                group_2_overall = {'no_addiction': len(list(filter(
                    lambda v: v < digital_addiction_entry_level, group_2))), 'entry_level': len(list(filter(
                        lambda v: digital_addiction_entry_level <= v < digital_addiction_mid_level, group_2))), 'mid_level': len(list(filter(
                            lambda v: digital_addiction_mid_level <= v, group_2)))}

                if appropriate_stat_func == fisher_exact:
                    print(
                        '[{col}:{page_1}->{page_2}] Chosen Fisher exact test for the data due to normal distribution'.format(col=column_name, page_1=wanted_list[count], page_2=wanted_list[count+1]))

                    f_test_1, p_1 = appropriate_stat_func([[group_1_overall['no_addiction'], group_1_overall['entry_level']], [
                        group_2_overall['no_addiction'], group_2_overall['entry_level']]])

                    f_test_2, p_2 = appropriate_stat_func([[group_1_overall['entry_level'], group_1_overall['mid_level']], [
                        group_2_overall['entry_level'], group_2_overall['mid_level']]])

                    f_test_3, p_3 = appropriate_stat_func([[group_1_overall['no_addiction'], group_1_overall['mid_level']], [
                        group_2_overall['no_addiction'], group_2_overall['mid_level']]])

                    data_dict = {'p_no-entry': [p_1],
                                 'null_hypothesis_no-entry': [p_1 > alpha], 'f_res_no-entry': [f_test_1], 'p_entry-mid': [p_2],
                                 'null_hypothesis_entry-mid': [p_2 > alpha], 'f_res_entry-mid': [f_test_2], 'p_no-mid': [p_3],
                                 'null_hypothesis_no-mid': [p_3 > alpha], 'f_res_no-mid': [f_test_3]}

                    df = pd.DataFrame(data=data_dict)
                    df.to_excel(
                        writer, sheet_name='{page_1}-F'.format(page_1=xl_file.sheet_names[count]), engine='xlsxwriter')
                elif appropriate_stat_func == mannwhitneyu:
                    print(
                        '[{col}:{page_1}->{page_2}] Chosen Manna-Whitney U-test because of not-normal distribution'.format(col=column_name, page_1=wanted_list[count], page_2=wanted_list[count+1]))

                    u_test, p = appropriate_stat_func(x=group_1, y=group_2)

                    data_dict = {'p': [p],
                                 'null_hypothesis': [p > alpha], 'u_res': [u_test]}

                    df = pd.DataFrame(data=data_dict)
                    df.to_excel(
                        writer, sheet_name='{page_1}-U'.format(page_1=xl_file.sheet_names[count]), engine='xlsxwriter')

            else:
                wanted_columns = calc_list[count].columns.tolist()
                # remove participants naming data
                wanted_columns.pop(0)

                for col in wanted_columns:
                    criteria = subj_control_level_criteria[col]

                    group_1 = calc_list[count][col].values.tolist()
                    group_2 = calc_list[count + 1][col].values.tolist()

                    appropriate_stat_func = fisher_exact if normal_test_results[wanted_list[
                        count]] and normal_test_results[wanted_list[count+1]] else mannwhitneyu

                    group_1_overall = {'external_locus': len(list(filter(lambda v: v < criteria[0], group_1))), 'normal_locus': len(list(filter(lambda v: criteria[0] <= v <= criteria[1], group_1))), 'internal_locus': len(
                        list(filter(lambda v: criteria[1] < v, group_1)))}
                    group_2_overall = {'external_locus': len(list(filter(lambda v: v < criteria[0], group_2))), 'normal_locus': len(list(filter(lambda v: criteria[0] <= v <= criteria[1], group_2))), 'internal_locus': len(
                        list(filter(lambda v: criteria[1] < v, group_2)))}

                    if appropriate_stat_func == fisher_exact:
                        print(
                            '[{col}:{page_1}->{page_2}] Chosen Fisher exact test for the data due to normal distribution'.format(col=col, page_1=wanted_list[count], page_2=wanted_list[count+1]))

                        f_test_1, p_1 = fisher_exact([[group_1_overall['external_locus'], group_1_overall['normal_locus']], [
                            group_2_overall['external_locus'], group_2_overall['normal_locus']]])

                        f_test_2, p_2 = fisher_exact([[group_1_overall['normal_locus'], group_1_overall['internal_locus']], [
                            group_2_overall['normal_locus'], group_2_overall['internal_locus']]])

                        f_test_3, p_3 = fisher_exact([[group_1_overall['external_locus'], group_1_overall['internal_locus']], [
                            group_2_overall['external_locus'], group_2_overall['internal_locus']]])

                        data_dict = {'p_ext-norm': [p_1],
                                     'null_hypothesis_ext-norm': [p_1 > alpha], 'f_res_ext-norm': [f_test_1], 'p_norm-int': [p_2],
                                     'null_hypothesis_norm-int': [p_2 > alpha], 'f_res_norm-int': [f_test_2], 'p_ext-int': [p_3],
                                     'null_hypothesis_ext-int': [p_3 > alpha], 'f_res_ext-int': [f_test_3]}

                        df = pd.DataFrame(data=data_dict)
                        df.to_excel(
                            writer, sheet_name='{page_1}-F'.format(page_1=xl_file.sheet_names[count]), engine='xlsxwriter')
                    elif appropriate_stat_func == mannwhitneyu:
                        print(
                            '[{col}:{page_1}->{page_2}] Chosen Manna-Whitney U-test because of not-normal distribution'.format(col=col, page_1=wanted_list[count], page_2=wanted_list[count+1]))

                        u_test, p = appropriate_stat_func(x=group_1, y=group_2)

                        data_dict = {'p': [p],
                                     'null_hypothesis': [p > alpha], 'u_res': [u_test]}

                        df = pd.DataFrame(data=data_dict)
                        df.to_excel(
                            writer, sheet_name='{page_1}-U'.format(page_1=xl_file.sheet_names[count]), engine='xlsxwriter')
            count += 2
        return True
    else:
        print(
            'Aborting F-test calculation. You need to provide an even amount of pages and a valid results column.')
        return False
