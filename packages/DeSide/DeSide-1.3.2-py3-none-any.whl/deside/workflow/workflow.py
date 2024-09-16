import os
import numpy as np
import pandas as pd
import warnings
from ..decon_cf import DeSide
from ..utility import check_dir, print_msg
from ..utility.read_file import ReadH5AD
from ..utility.compare import mean_exp_of_marker_gene, read_and_merge_result, cal_gene_signature_score
from ..plot import (compare_exp_and_cell_fraction, plot_predicted_result,
                    compare_cell_fraction_across_cancer_type, ScatterPlot, compare_y_y_pred_plot)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


def tcga_evaluation(marker_gene_file_path, total_result_dir, pred_cell_frac_tcga_dir,
                    cell_types, tcga_data_dir, outlier_file_path=None, pre_trained_model_dir=None,
                    model_name: str = None, signature_score_method: str = 'mean_exp',
                    cancer_types: list = None, update_figures=False, pathway_mask=None,
                    group_cell_types: dict = None, cell_type2subtypes: dict = None,
                    bulk_tpm: pd.DataFrame = None, sample2cancer_type: pd.DataFrame = None):
    """

    :param marker_gene_file_path:
    :param total_result_dir:
    :param pred_cell_frac_tcga_dir:
    :param cell_types:
    :param tcga_data_dir:
    :param outlier_file_path:
    :param pre_trained_model_dir: the directory of pre-trained model
    :param model_name: the model name
    :param signature_score_method:
        mean_exp (the mean or max expression of corresponding marker genes for each cell type) or
        gene_signature_score (Combes et al., 2022, Cell 185, 184-203)
    :param cancer_types: a list of cancer types
    :param update_figures: update figures or not
    :param pathway_mask: genes by pathways, 1 for genes in the pathway, 0 for genes not in the pathway
    :param group_cell_types: a dictionary of cell types, key is the group name, value is a list of cell types
    :param cell_type2subtypes: a dictionary of cell types, key is the cell type, value is a list of subtypes
    :return:
    """
    # marker_gene_file_path = marker_gene_file_path
    # pred_cell_frac_dir = pred_cell_frac_tcga_dir
    # result_dir = total_result_dir
    if cancer_types is None:
        cancer_types = ['ACC', 'BLCA', 'BRCA', 'GBM', 'HNSC', 'LGG', 'LIHC', 'LUAD', 'PAAD', 'PRAD',
                        'CESC', 'COAD', 'KICH', 'KIRC', 'KIRP', 'LUSC', 'READ', 'THCA', 'UCEC']
    # for model in model_name:
    merged_signature_score_and_cell_frac_file_path = \
        os.path.join(pred_cell_frac_tcga_dir, f'merged_all_signature_score_and_cell_fraction_by_{model_name}.csv')
    pred_cell_frac_dir_current_model = os.path.join(pred_cell_frac_tcga_dir, model_name)
    check_dir(pred_cell_frac_dir_current_model)
    all_pred_cell_frac_file_path = os.path.join(pred_cell_frac_dir_current_model,
                                                f'all_predicted_cell_fraction_by_{model_name}.csv')
    signature_score_result_dir = os.path.join(pred_cell_frac_dir_current_model, 'signature_score')
    check_dir(signature_score_result_dir)
    all_signature_score_file_path = os.path.join(signature_score_result_dir, 'all_cancer_type_signature_score.csv')
    if 'DeSide' in model_name:
        if os.path.exists(os.path.join(pre_trained_model_dir, model_name, model_name, 'genes.txt')):
            gene_list_in_model_fp = os.path.join(pre_trained_model_dir, model_name, model_name, 'genes.txt')
        else:
            gene_list_in_model_fp = os.path.join(pre_trained_model_dir, 'genes.txt')
    else:  # Scaden
        gene_list_in_model_fp = os.path.join(pre_trained_model_dir, model_name, 'm256', 'genes.txt')

    # calculate the signature score for each cancer type
    all_signature_score = None
    # if cell_type2subtypes is None:
    #     _cell_types = cell_types.copy()
    # else:
    #     _cell_types = list(cell_type2subtypes.keys())
    #     if cell_type2subtypes.get('Fibroblasts', None) is not None:
    #         _cell_types += cell_type2subtypes['Fibroblasts']
    if group_cell_types is None:
        if not os.path.exists(all_signature_score_file_path):
            if bulk_tpm is None:
                bulk_tpm = pd.read_csv(os.path.join(tcga_data_dir, 'merged_tpm.csv'), index_col=0)
            if sample2cancer_type is None:
                sample2cancer_type = pd.read_csv(os.path.join(tcga_data_dir, 'tcga_sample_id2cancer_type.csv'), index_col=0)
            gene_list_in_model = list(pd.read_csv(gene_list_in_model_fp, index_col=0, sep='\t')['0'])
            signature_scores = []
            for cancer_type in cancer_types:
                print('----------------------------------------------------')
                print(f'Deal with cancer type: {cancer_type}...')
                # tpm_file_path = os.path.join(tcga_data_dir, cancer_type, f'{cancer_type}_TPM.csv')
                current_sample_ids = sample2cancer_type.loc[sample2cancer_type['cancer_type'] == cancer_type, :].copy()
                tpm_file = bulk_tpm.loc[bulk_tpm.index.isin(current_sample_ids.index.to_list()), :].copy().T
                result_file_path = os.path.join(signature_score_result_dir, f'{cancer_type}_signature_score.csv')
                if signature_score_method == 'mean_exp':
                    current_signature_score = \
                        mean_exp_of_marker_gene(marker_gene_file_path=marker_gene_file_path,
                                                bulk_tpm_file_path=tpm_file, cell_types=cell_types.copy(),
                                                result_file_path=result_file_path, cancer_type=cancer_type,
                                                gene_list_in_model=gene_list_in_model,
                                                cell_type2subtypes=cell_type2subtypes)
                else:  # gene_signature_score
                    current_signature_score = cal_gene_signature_score(marker_gene_file_path=marker_gene_file_path,
                                                                       bulk_tpm_file_path=tpm_file,
                                                                       cell_types=cell_types.copy(),
                                                                       result_file_path=result_file_path,
                                                                       cancer_type=cancer_type)
                signature_scores.append(current_signature_score)
            # merge all mean expression (gene signature score) of marker genes together
            all_signature_score = pd.concat(signature_scores)
            if all_signature_score.shape[0] > 0:
                all_signature_score.to_csv(all_signature_score_file_path, float_format='%.3f')
        else:
            print(f'   Using the previous result of signature score of marker genes from: '
                  f'{all_signature_score_file_path}')
            all_signature_score = pd.read_csv(all_signature_score_file_path, index_col=0)

    # combine all predicted cell fractions for each cancer type together
    if not os.path.exists(all_pred_cell_frac_file_path):
        print(f'   Merge all predicted result by {model_name}...')
        _cell_type_name_mapping = dict(zip(cell_types, cell_types))
        read_and_merge_result(raw_result_dir=pred_cell_frac_dir_current_model,
                              cell_type_name_mapping=_cell_type_name_mapping,
                              algo=model_name, result_file_path=all_pred_cell_frac_file_path,
                              group_cell_types=group_cell_types)
    else:
        print(f'   Using the previous result of merged cell fractions from: {all_pred_cell_frac_file_path}.')
    all_pred_cell_fractions_df = pd.read_csv(all_pred_cell_frac_file_path, index_col='sample_id')
    if cell_type2subtypes is not None:
        for cell_type in cell_type2subtypes.keys():
            if cell_type not in all_pred_cell_fractions_df.columns:
                subtypes = cell_type2subtypes[cell_type]
                if np.all([subtype in all_pred_cell_fractions_df.columns for subtype in subtypes]):
                    all_pred_cell_fractions_df[cell_type] = all_pred_cell_fractions_df.loc[:, subtypes].sum(axis=1)
                else:
                    print(f'   Warning: {cell_type} is not in the predicted cell fractions.')

    if group_cell_types is None:
        # merge two parts together
        if not os.path.exists(merged_signature_score_and_cell_frac_file_path):
            if 'cancer_type' in all_signature_score.columns:
                all_signature_score.drop(columns=['cancer_type'], inplace=True)
            merged_df = all_signature_score.merge(all_pred_cell_fractions_df, left_index=True, right_index=True)
            merged_df.to_csv(merged_signature_score_and_cell_frac_file_path)

        # comparing mean expression of marker genes and the predicted cell fraction of corresponding cell type
        result_dir_new = os.path.join(total_result_dir, f'corr_signature_score_and_pred_cell_fraction', model_name)
        # outlier samples in correlation for each cancer type, selected manually
        # outlier_file_path = 'outlier_samples.txt'
        outlier_file_path = outlier_file_path

        if pathway_mask is None:
            cell_types_clustering = [i for i in cell_types if i != 'Cancer Cells']
            compare_exp_and_cell_fraction(merged_file_path=merged_signature_score_and_cell_frac_file_path,
                                          clustering_ct=cell_types_clustering, font_scale=1.5,
                                          cell_types=cell_types, outlier_file_path=outlier_file_path,
                                          result_dir=result_dir_new, update_figures=update_figures,
                                          signature_score_method=signature_score_method,
                                          cell_type2subtypes=cell_type2subtypes)

    print('Plot predicted cell proportion across all cancer types...')
    cell_types2max = {'B Cells': 0.1, 'CD4 T': 0.1, 'DC': 0.1, 'CD8 T': 0.1}
    across_all_dir = os.path.join(total_result_dir, 'across_all_cancer_type', model_name)
    for cell_type in cell_types:
        cell_type2max = cell_types2max.get(cell_type, 0.0)
        compare_cell_fraction_across_cancer_type(merged_cell_fraction=all_pred_cell_fractions_df,
                                                 result_dir=across_all_dir,
                                                 outlier_file_path=outlier_file_path,
                                                 ylabel=f'Predicted cell prop. of {cell_type} by {model_name}',
                                                 cell_type=cell_type, cell_type2max=cell_type2max)


def run_step3(evaluation_dataset2path, log_file_path, result_dir, model_dir,
              all_cell_types, one_minus_alpha=False, pathway_mask=None,
              method_adding_pathway='add_to_end', hyper_params: dict = None,
              group_cell_types: dict = None):
    """
    Step3: Predicting cell fractions of test set and evaluation
    :param evaluation_dataset2path: dict, key: dataset name, value: file path
    :param log_file_path: str, log file path
    :param result_dir: str, result directory
    :param model_dir: str, model directory
    :param all_cell_types: list, all cell types
    :param one_minus_alpha: bool, whether to use 1-alpha as the predicted cell fraction for all cell types
    :param pathway_mask: dataframe, pathway mask, genes by pathways
    :param method_adding_pathway: str, method for adding pathway, 'add_to_end' or 'convert'
    :param hyper_params: dict, hyper parameters for DNN model
    :param group_cell_types: dict, group cell types
    """
    # Step3, evaluation on test set
    print_msg('Step3: Predicting cell fractions of test set and evaluation...',
              log_file_path=log_file_path)

    for dataset_name, file_path in evaluation_dataset2path.items():
        # if 'Test_set' in dataset_name:
        print(f'   Evaluating on dataset {dataset_name}...')
        predicted_result_dir = os.path.join(result_dir, dataset_name)
        check_dir(predicted_result_dir)
        predicted_cell_frac_file_path = os.path.join(predicted_result_dir,
                                                     f'{dataset_name}_pred_cell_frac.csv')

        generated_bulk_gep_fp = file_path
        if dataset_name == 'Pre_Test_set':
            generated_bulk_gep_fp = './datasets/simulated_bulk_cell_dataset/test_set_nbase3_7ds/' \
                                    'simu_bulk_exp_Test_set2_log2cpm1p.h5ad'
        generated_cell_frac = ReadH5AD(generated_bulk_gep_fp).get_cell_fraction()
        if group_cell_types is not None:
            for g, cell_types in group_cell_types.items():
                if len(cell_types) > 1:
                    generated_cell_frac[g] = generated_cell_frac[cell_types].sum(axis=1)
                    generated_cell_frac.drop(columns=cell_types, inplace=True)

        if not os.path.exists(predicted_cell_frac_file_path):
            deside_model = DeSide(model_dir=model_dir)
            deside_model.predict(input_file=generated_bulk_gep_fp,
                                 output_file_path=predicted_cell_frac_file_path,
                                 exp_type='log_space', scaling_by_sample=False,
                                 scaling_by_constant=True, one_minus_alpha=one_minus_alpha,
                                 pathway_mask=pathway_mask, method_adding_pathway=method_adding_pathway,
                                 hyper_params=hyper_params)
        print('   > Comparing cell frac between y_true and y_pred...')
        s_plot = ScatterPlot(x=predicted_cell_frac_file_path,
                             y=generated_cell_frac)
        for cell_type in s_plot.x.columns.to_list():
            s_plot.postfix = f'pred_y_y_{cell_type}'
            s_plot.plot(show_columns={'x': cell_type, 'y': cell_type}, fig_size=(8, 8),
                        result_file_dir=predicted_result_dir, show_mae=True,
                        show_rmse=True, show_diag=True,
                        show_corr=True,
                        x_label='y_pred by DeSide', y_label=f'y_true of {dataset_name}',
                        show_reg_line=False)
        # plot all cell types in one figure
        compare_y_y_pred_plot(y_true=generated_cell_frac,
                              y_pred=predicted_cell_frac_file_path,
                              show_columns=all_cell_types, result_file_dir=predicted_result_dir,
                              model_name=f'DeSide', show_metrics=True,
                              y_label=f'y_pred')


def run_step4(tcga_data_dir: str, cancer_types: list, log_file_path: str, model_dir: str,
              marker_gene_file_path: str, result_dir: str, pred_cell_frac_tcga_dir: str,
              cancer_purity_file_path: str, all_cell_types: list, model_names: list,
              signature_score_method: str, one_minus_alpha: bool = False,
              update_figures: bool = False, outlier_file_path: str = None, pathway_mask: pd.DataFrame = None,
              method_adding_pathway: str = 'add_to_end', hyper_params: dict = None, cell_type2subtypes: dict = None,
              group_cell_types: dict = None, sample2cancer_type_file_path: str = None,
              bulk_tpm_file_path: str = None):
    """
    Step4: Predicting cell fractions of TCGA
    :param tcga_data_dir: str, TCGA data directory
    :param cancer_types: list, cancer types
    :param log_file_path: str, log file path
    :param model_dir: str, model directory
    :param marker_gene_file_path: str, marker gene file path
    :param result_dir: str, result directory
    :param pred_cell_frac_tcga_dir: str, predicted cell fraction of TCGA directory
    :param cancer_purity_file_path: str, cancer purity file path
    :param all_cell_types: list, all cell types
    :param model_names: list, model names
    :param signature_score_method: str, signature score method
    :param one_minus_alpha: bool, whether to use 1-alpha as the predicted cell fraction for all cell types
    :param update_figures: bool, whether to update figures
    :param outlier_file_path: str, outlier file path
    :param pathway_mask: dataframe, pathway mask, genes by pathways
    :param method_adding_pathway: str, method for adding pathway, 'add_to_end' or 'convert'
    :param hyper_params: dict, hyper parameters for DNN model
    :param cell_type2subtypes: dict, cell type to subtypes
    :param group_cell_types: dict, group cell types
    :param sample2cancer_type_file_path: str, sample to cancer type file path
    :param bulk_tpm_file_path: str, bulk tpm file path
    """
    # TCGA
    print_msg("Step 4: Predict cell fraction of TCGA...", log_file_path=log_file_path)
    # model_name = 'DeSide'
    for model_name in model_names:
        if bulk_tpm_file_path is None:
            bulk_tpm = pd.read_csv(os.path.join(tcga_data_dir, 'merged_tpm.csv'), index_col=0)
        else:
            bulk_tpm = pd.read_csv(bulk_tpm_file_path, index_col=0)
        if sample2cancer_type_file_path is None:
            sample2cancer_type = pd.read_csv(os.path.join(tcga_data_dir, 'tcga_sample_id2cancer_type.csv'), index_col=0)
        else:
            sample2cancer_type = pd.read_csv(sample2cancer_type_file_path, index_col=0)
        for cancer_type in cancer_types:
            current_sample_ids = sample2cancer_type.loc[sample2cancer_type['cancer_type'] == cancer_type, :].copy()
            current_bulk_tpm = bulk_tpm.loc[bulk_tpm.index.isin(current_sample_ids.index.to_list()), :].copy()
            print(f'current_bulk_tpm: {current_bulk_tpm.shape}')
            current_result_dir = os.path.join(pred_cell_frac_tcga_dir, model_name, cancer_type)
            check_dir(current_result_dir)
            y_pred_file_path = os.path.join(current_result_dir, 'y_predicted_result.csv')
            if not os.path.exists(y_pred_file_path):
                print(f'Predicting cell fractions of {cancer_type} samples by model {model_name}...')
                deside_model = DeSide(model_dir=model_dir)
                deside_model.predict(input_file=current_bulk_tpm, output_file_path=y_pred_file_path,
                                     exp_type='TPM', scaling_by_constant=True,
                                     scaling_by_sample=False, one_minus_alpha=one_minus_alpha,
                                     pathway_mask=pathway_mask, method_adding_pathway=method_adding_pathway,
                                     hyper_params=hyper_params)
            else:
                print(f'   Previous result existed: {y_pred_file_path}')
            print(f'   Plot and compare predicted result...')
            # y_pred_file_path = os.path.join(current_result_dir, 'y_predicted_result.csv')
            plot_predicted_result(cell_frac_result_fp=y_pred_file_path, bulk_exp_fp=current_bulk_tpm.T,
                                  cancer_type=cancer_type, model_name=model_name, result_dir=current_result_dir,
                                  cancer_purity_fp=cancer_purity_file_path, update_figures=update_figures,
                                  cell_type2subtypes=cell_type2subtypes)

        tcga_evaluation(marker_gene_file_path=marker_gene_file_path, total_result_dir=result_dir,
                        pred_cell_frac_tcga_dir=pred_cell_frac_tcga_dir,
                        cell_types=all_cell_types.copy(), tcga_data_dir=tcga_data_dir,
                        pre_trained_model_dir=model_dir, model_name=model_name,
                        signature_score_method=signature_score_method, cancer_types=cancer_types,
                        update_figures=update_figures, outlier_file_path=outlier_file_path,
                        pathway_mask=pathway_mask, group_cell_types=group_cell_types,
                        cell_type2subtypes=cell_type2subtypes, bulk_tpm=bulk_tpm, sample2cancer_type=sample2cancer_type)

        # calculate the distribution of predicted cell proportions in TCGA
        # model_name = 'DeSide'
        all_pred_cell_frac_file_path = os.path.join(pred_cell_frac_tcga_dir, model_name,
                                                    f'all_predicted_cell_fraction_by_{model_name}.csv')
        pred_cell_frac = pd.read_csv(all_pred_cell_frac_file_path, index_col=0)
        pred_cell_frac = pred_cell_frac.loc[:, all_cell_types].copy()
        cell_type2cell_prop_dis = {}
        bins = np.linspace(0, 1, 11)
        pred_cell_prop_dis_file_path = os.path.join(pred_cell_frac_tcga_dir, model_name,
                                                    'pred_cell_frac_distribution.csv')
        if not os.path.exists(pred_cell_prop_dis_file_path):
            for ct in all_cell_types:
                current_cp = pred_cell_frac[ct].values
                hist, bin_edges = np.histogram(current_cp, bins=bins)
                cell_type2cell_prop_dis[ct] = hist / len(current_cp)
            cell_type2cell_prop_dis_df = pd.DataFrame.from_dict(cell_type2cell_prop_dis, orient='index')
            cell_type2cell_prop_dis_df.to_csv(pred_cell_prop_dis_file_path, float_format='%g')
