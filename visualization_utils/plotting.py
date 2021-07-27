#Copyright (c) Facebook, Inc. and its affiliates.
#This source code is licensed under the MIT license found in the
#LICENSE file in the root directory of this source tree.
import itertools
import copy
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
from settings import config_plotting

def get_column_name_number(dir_addr, mode):
    column_name_number_dic = {}
    try:
        if mode == "all":
            file_name = "result_summary/FARSI_simple_run_0_1_all_reults.csv"
        else:
            file_name = "result_summary/FARSI_simple_run_0_1.csv"

        file_full_addr = os.path.join(dir_addr, file_name)
        with open(file_full_addr) as f:
            resultReader = csv.reader(f, delimiter=',', quotechar='|')
            for row in resultReader:
                for idx, el_name in enumerate(row):
                    column_name_number_dic[el_name] = idx
                break
        return column_name_number_dic
    except Exception as e:
        raise e



#


# the function to get the column information of the given category
def columnNum(dirName, fileName, cate, result):
    if result == "all":
        with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
            resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

            for i, row in enumerate(resultReader):
                if i == 0:
                    for j in range(0, len(row)):
                        if row[j] == cate:
                            return j
                    raise Exception("No such category in the list! Check the name: " + cate)
                break
    elif result == "simple":
        with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1.csv", newline='') as csvfile:
            resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

            for i, row in enumerate(resultReader):
                if i == 0:
                    for j in range(0, len(row)):
                        if row[j] == cate:
                            return j
                    raise Exception("No such category in the list! Check the name: " + cate)
                break
    else:
        raise Exception("No such result file! Check the result type! It should be either \"all\" or \"simple\"")

# the function to plot the frequency of all comm_comp in the pie chart
def plotCommCompAll(dirName, fileName, all_res_column_name_number):
    colNum = all_res_column_name_number["comm_comp"]
    truNum = all_res_column_name_number["move validity"]

    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        commNum = 0
        compNum = 0

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i > 1:
                if row[colNum] == "comm":
                    commNum += 1
                elif row[colNum] == "comp":
                    compNum += 1
                else:
                    raise Exception("comm_comp is not giving comm or comp! The new type: " + row[colNum])

        plt.figure()
        plt.pie([commNum, compNum], labels = ["comm", "comp"])
        plt.title("comm_comp: Frequency")
        plt.savefig(dirName + fileName + "/comm-compFreq-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot the frequency of all high level optimizations in the pie chart
def plothighLevelOptAll(dirName, fileName, all_res_column_name_number):
    colNum = all_res_column_name_number["high level optimization name"]
    truNum = all_res_column_name_number["move validity"]

    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        topoNum = 0
        tunNum = 0
        mapNum = 0
        idenOptNum = 0

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i > 1:
                if row[colNum] == "topology":
                    topoNum += 1
                elif row[colNum] == "customization":
                    tunNum += 1
                elif row[colNum] == "mapping":
                    mapNum += 1
                elif row[colNum] == "identity":
                    idenOptNum += 1
                else:
                    raise Exception("high level optimization name is not giving topology or customization or mapping or identity! The new type: " + row[colNum])
        
        plt.figure()
        plt.pie([topoNum, tunNum, mapNum, idenOptNum], labels = ["topology", "customization", "mapping", "identity"])
        plt.title("High Level Optimization: Frequency")
        plt.savefig(dirName + fileName + "/highLevelOpt-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot the frequency of all architectural variables to improve in the pie chart
def plotArchVarImpAll(dirName, fileName, colNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        parazNum = 0
        custNum = 0
        localNum = 0
        idenImpNum = 0

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i > 1:
                if row[colNum] == "parallelization":
                    parazNum += 1
                elif row[colNum] == "customization":
                    custNum += 1
                elif row[colNum] == "locality":
                    localNum += 1
                elif row[colNum] == "identity":
                    idenImpNum += 1                
                else:
                    raise Exception("architectural principle is not parallelization or customization or locality or identity! The new type: " + row[colNum])

        plt.figure()
        plt.pie([parazNum, custNum, localNum, idenImpNum], labels = ["parallelization", "customization", "locality", "identity"])
        plt.title("Architectural Principle: Frequency")
        plt.savefig(dirName + fileName + "/archVarImp-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot simulation time vs. system block count
def plotSimTimeVSblk(dirName, fileName, blkColNum, simColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        sysBlkCount = []
        simTime = []

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i > 1:
                sysBlkCount.append(int(row[blkColNum]))
                simTime.append(float(row[simColNum]))

        plt.figure()
        plt.plot(sysBlkCount, simTime)
        plt.xlabel("System Block Count")
        plt.ylabel("Simulation Time")
        plt.title("Simulation Time vs. Sytem Block Count")
        plt.savefig(dirName + fileName + "/simTimeVSblk-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot move generation time vs. system block count
def plotMoveGenTimeVSblk(dirName, fileName, blkColNum, movColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        sysBlkCount = []
        moveGenTime = []

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i > 1:
                sysBlkCount.append(int(row[blkColNum]))
                moveGenTime.append(float(row[movColNum]))
        
        plt.figure()
        plt.plot(sysBlkCount, moveGenTime)
        plt.xlabel("System Block Count")
        plt.ylabel("Move Generation Time")
        plt.title("Move Generation Time vs. System Block Count")
        plt.savefig(dirName + fileName + "/moveGenTimeVSblk-" + fileName + ".png")
        # plt.show()
        plt.close('all')

def get_experiments_workload(all_res_column_name):
    latency_budget =  all_res_column_name_number["latency budget"][:-1]
    workload_latency = latency_budget.split(";")
    workloads = []
    for workload_latency in workload_latency:
        workloads.append(workload_latency.split("=")[0])
    return workloads

def get_experiments_name(file_full_addr, all_res_column_name_number):
    with open(file_full_addr, newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row1 = next(resultReader)
        row2 = next(resultReader)
        latency_budget =  row2[all_res_column_name_number["latency_budget"]]
        power_budget =  row2[all_res_column_name_number["power_budget"]]
        area_budget =  row2[all_res_column_name_number["area_budget"]]
        try:
            transformation_selection_mode =  row2[all_res_column_name_number["transformation_selection_mode"]]
        except:
            transformation_selection_mode =  ""


        workload_latency = latency_budget[:-1].split(';')
        latency_budget_refined =""
        for workload_latency in workload_latency:
            latency_budget_refined +="_" + (workload_latency.split("=")[0][0]+workload_latency.split("=")[1])

        return latency_budget_refined[1:]+"_" + power_budget + "_" + area_budget+"_"+transformation_selection_mode

def get_all_col_values_of_a_file(file_full_addr, all_res_column_name_number, column_name):
    column_number = all_res_column_name_number[column_name]
    all_values = []
    with open(file_full_addr, newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        experiment_name = get_experiments_name(file_full_addr, all_res_column_name_number)
        for i, row in enumerate(resultReader):
            if i > 1:
                if not row[column_number] == '':
                    value =row[column_number]
                    values = value.split(";") # if mutiple values
                    for val in values:
                        if "=" in val:
                            val_splitted = val.split("=")
                            all_values.append(val_splitted[0])
                        else:
                            all_values.append(val)

    return all_values

def get_all_col_values_of_a_folders(input_dir_names, input_all_res_column_name_number, column_name):
    all_values = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        all_values.extend(get_all_col_values_of_a_file(file_full_addr, input_all_res_column_name_number, column_name))

    # get rid of duplicates
    all_values_rid_of_duplicates = list(set(all_values))
    return all_values_rid_of_duplicates

def extract_latency_values(values_):
    print("")


def plot_codesign_rate_efficacy_cross_workloads_updated(input_dir_names, res_column_name_number):
    #itrColNum = all_res_column_name_number["iteration cnt"]
    #distColNum = all_res_column_name_number["dist_to_goal_non_cost"]
    trueNum  =  all_res_column_name_number["move validity"]
    move_name_number =  all_res_column_name_number["move name"]

    # experiment_names
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        file_full_addr_list.append(file_full_addr)

    axis_font = {'fontname': 'Arial', 'size': '4'}
    x_column_name = "iteration cnt"
    #y_column_name_list = ["high level optimization name", "exact optimization name", "architectural principle", "comm_comp"]
    y_column_name_list = ["exact optimization name",  "architectural principle", "comm_comp", "workload"]

    #y_column_name_list = ["high level optimization name", "exact optimization name", "architectural principle", "comm_comp"]



    column_co_design_cnt = {}
    column_non_co_design_cnt = {}
    column_co_design_rate = {}
    column_non_co_design_rate = {}
    column_co_design_efficacy_avg = {}
    column_non_co_design_efficacy_rate = {}
    column_non_co_design_efficacy = {}
    column_co_design_dist= {}
    column_co_design_dist_avg= {}
    column_co_design_improvement = {}
    experiment_name_list = []
    last_col_val = ""
    for file_full_addr in file_full_addr_list:
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        experiment_name_list.append(experiment_name)
        column_co_design_dist_avg[experiment_name] = {}
        column_co_design_efficacy_avg[experiment_name] = {}

        column_co_design_cnt = {}
        for y_column_name in y_column_name_list:
            y_column_number = res_column_name_number[y_column_name]
            x_column_number = res_column_name_number[x_column_name]


            dis_to_goal_column_number = res_column_name_number["dist_to_goal_non_cost"]
            ref_des_dis_to_goal_column_number = res_column_name_number["ref_des_dist_to_goal_non_cost"]
            column_co_design_cnt[y_column_name] = []
            column_non_co_design_cnt[y_column_name] = []

            column_non_co_design_efficacy[y_column_name] = []
            column_co_design_dist[y_column_name] = []
            column_co_design_improvement[y_column_name] = []
            column_co_design_rate[y_column_name] = []

            all_values = get_all_col_values_of_a_folders(input_dir_names, all_res_column_name_number, y_column_name)

            last_row_change = ""
            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                rows = list(resultReader)
                for i, row in enumerate(rows):
                    if i >= 1:
                        last_row = rows[i - 1]
                        if row[y_column_number] not in all_values or row[move_name_number]=="identity":
                            continue

                        col_value = row[y_column_number]
                        col_values = col_value.split(";")
                        for idx, col_val in enumerate(col_values):


                            # only for improvement
                            if float(row[ref_des_dis_to_goal_column_number]) - float(row[dis_to_goal_column_number]) < 0:
                                continue

                            delta_x_column = (float(row[x_column_number]) - float(last_row[x_column_number]))/len(col_values)
                            delta_improvement = (float(last_row[dis_to_goal_column_number]) - float(row[dis_to_goal_column_number]))/(float(last_row[dis_to_goal_column_number])*len(col_values))


                            if not col_val == last_col_val and i > 1:
                                if not last_row_change == "":
                                    distance_from_last_change =  float(last_row[x_column_number]) - float(last_row_change[x_column_number]) + idx * delta_x_column
                                    column_co_design_dist[y_column_name].append(distance_from_last_change)
                                    improvement_from_last_change =  (float(last_row[dis_to_goal_column_number]) - float(row[dis_to_goal_column_number]))/float(last_row[dis_to_goal_column_number])  + idx *delta_improvement
                                    column_co_design_improvement[y_column_name].append(improvement_from_last_change)

                                last_row_change = copy.deepcopy(last_row)


                            last_col_val = col_val



            # co_des cnt
            # we ignore the first element as the first element distance is always zero
            co_design_dist_sum = 0
            co_design_efficacy_sum = 0
            avg_ctr = 1
            co_design_dist_selected = column_co_design_dist[y_column_name]
            co_design_improvement_selected = column_co_design_improvement[y_column_name]
            for idx,el in enumerate(column_co_design_dist[y_column_name]):
                if idx == len(co_design_dist_selected) - 1:
                    break
                co_design_dist_sum += (column_co_design_dist[y_column_name][idx] + column_co_design_dist[y_column_name][idx+1])
                co_design_efficacy_sum += (column_co_design_improvement[y_column_name][idx] + column_co_design_improvement[y_column_name][idx+1])
                #/(column_co_design_dist[y_column_name][idx] + column_co_design_dist[y_column_name][idx+1])
                avg_ctr+=1

            column_co_design_improvement = {}
            column_co_design_dist_avg[experiment_name][y_column_name]= co_design_dist_sum/avg_ctr
            column_co_design_efficacy_avg[experiment_name][y_column_name] = co_design_efficacy_sum/avg_ctr

        #result = {"rate":{}, "efficacy":{}}
        #rate_column_co_design = {}

    plt.figure()
    plotdata = pd.DataFrame(column_co_design_dist_avg, index=y_column_name_list)
    fontSize = 10
    plotdata.plot(kind='bar', fontsize=fontSize)
    plt.xticks(fontsize=fontSize, rotation=6)
    plt.yticks(fontsize=fontSize)
    plt.xlabel("co design parameter", fontsize=fontSize)
    plt.ylabel("co design distance", fontsize=fontSize)
    plt.title("co desgin distance of different parameters",  fontsize=fontSize)

    # dump in the top folder
    output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
    output_dir = os.path.join(output_base_dir, "cross_workloads/co_design_rate")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(os.path.join(output_dir,"_".join(experiment_name_list) +"_"+"co_design_avg_dist"+'_'.join(y_column_name_list)+".png"))
    plt.close('all')


    plt.figure()
    plotdata = pd.DataFrame(column_co_design_efficacy_avg, index=y_column_name_list)
    fontSize = 10
    plotdata.plot(kind='bar', fontsize=fontSize)
    plt.xticks(fontsize=fontSize, rotation=6)
    plt.yticks(fontsize=fontSize)
    plt.xlabel("co design parameter", fontsize=fontSize)
    plt.ylabel("co design dis", fontsize=fontSize)
    plt.title("co desgin efficacy of different parameters",  fontsize=fontSize)

    # dump in the top folder
    output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
    output_dir = os.path.join(output_base_dir, "cross_workloads/co_design_rate")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(os.path.join(output_dir,"_".join(experiment_name_list) +"_"+"co_design_efficacy"+'_'.join(y_column_name_list)+".png"))
    plt.close('all')

def plot_codesign_rate_efficacy_per_workloads(input_dir_names, res_column_name_number):
    #itrColNum = all_res_column_name_number["iteration cnt"]
    #distColNum = all_res_column_name_number["dist_to_goal_non_cost"]
    trueNum  =  all_res_column_name_number["move validity"]
    move_name_number =  all_res_column_name_number["move name"]

    # experiment_names
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        file_full_addr_list.append(file_full_addr)

    axis_font = {'fontname': 'Arial', 'size': '4'}
    x_column_name = "iteration cnt"
    #y_column_name_list = ["high level optimization name", "exact optimization name", "architectural principle", "comm_comp"]
    y_column_name_list = ["exact optimization name",  "architectural principle", "comm_comp", "workload"]

    #y_column_name_list = ["high level optimization name", "exact optimization name", "architectural principle", "comm_comp"]



    column_co_design_cnt = {}
    column_non_co_design_cnt = {}
    column_co_design_rate = {}
    column_non_co_design_rate = {}
    column_co_design_efficacy_rate = {}
    column_non_co_design_efficacy_rate = {}
    column_non_co_design_efficacy = {}
    column_co_design_efficacy= {}
    last_col_val = ""
    for file_full_addr in file_full_addr_list:
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        column_co_design_cnt = {}
        for y_column_name in y_column_name_list:
            y_column_number = res_column_name_number[y_column_name]
            x_column_number = res_column_name_number[x_column_name]


            dis_to_goal_column_number = res_column_name_number["dist_to_goal_non_cost"]
            ref_des_dis_to_goal_column_number = res_column_name_number["ref_des_dist_to_goal_non_cost"]
            column_co_design_cnt[y_column_name] = []
            column_non_co_design_cnt[y_column_name] = []

            column_non_co_design_efficacy[y_column_name] = []
            column_co_design_efficacy[y_column_name] = []

            all_values = get_all_col_values_of_a_folders(input_dir_names, all_res_column_name_number, y_column_name)

            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                rows = list(resultReader)
                for i, row in enumerate(rows):
                    if i >= 1:
                        last_row = rows[i - 1]
                        if row[y_column_number] not in all_values or row[trueNum] == "False" or row[move_name_number]=="identity":
                            continue

                        col_value = row[y_column_number]
                        col_values = col_value.split(";")
                        for idx, col_val in enumerate(col_values):
                            delta_x_column = (float(row[x_column_number]) - float(last_row[x_column_number]))/len(col_values)

                            value_to_add_1 = (float(last_row[x_column_number]) + idx * delta_x_column, 1)
                            value_to_add_0 = (float(last_row[x_column_number]) + idx * delta_x_column, 0)

                            # only for improvement
                            if float(row[ref_des_dis_to_goal_column_number]) - float(row[dis_to_goal_column_number]) < 0:
                                continue

                            if not col_val == last_col_val:

                                column_co_design_cnt[y_column_name].append(value_to_add_1)
                                column_non_co_design_cnt[y_column_name].append(value_to_add_0)
                                column_co_design_efficacy[y_column_name].append((float(row[ref_des_dis_to_goal_column_number]) - float(row[dis_to_goal_column_number]))/float(row[ref_des_dis_to_goal_column_number]))
                                column_non_co_design_efficacy[y_column_name].append(0)
                            else:
                                column_co_design_cnt[y_column_name].append(value_to_add_0)
                                column_non_co_design_cnt[y_column_name].append(value_to_add_1)
                                column_co_design_efficacy[y_column_name].append(0)
                                column_non_co_design_efficacy[y_column_name].append((float(row[ref_des_dis_to_goal_column_number]) - float(row[dis_to_goal_column_number]))/float(row[ref_des_dis_to_goal_column_number]))

                            last_col_val = col_val



            # co_des cnt
            x_values_co_design_cnt = [el[0] for el in column_co_design_cnt[y_column_name]]
            y_values_co_design_cnt = [el[1] for el in column_co_design_cnt[y_column_name]]
            y_values_co_design_cnt_total =sum(y_values_co_design_cnt)
            total_iter = x_values_co_design_cnt[-1]

            # non co_des cnt
            x_values_non_co_design_cnt = [el[0] for el in column_non_co_design_cnt[y_column_name]]
            y_values_non_co_design_cnt = [el[1] for el in column_non_co_design_cnt[y_column_name]]
            y_values_non_co_design_cnt_total =sum(y_values_non_co_design_cnt)

            column_co_design_rate[y_column_name] = y_values_co_design_cnt_total/total_iter
            column_non_co_design_rate[y_column_name] = y_values_non_co_design_cnt_total/total_iter

            # co_des efficacy
            y_values_co_design_efficacy =  column_co_design_efficacy[y_column_name]
            y_values_co_design_efficacy_total =sum(y_values_co_design_efficacy)


            # non co_des efficacy
            y_values_non_co_design_efficacy = column_non_co_design_efficacy[y_column_name]
            y_values_non_co_design_efficacy_total =sum(y_values_non_co_design_efficacy)

            column_co_design_efficacy_rate[y_column_name] = y_values_co_design_efficacy_total/(y_values_non_co_design_efficacy_total + y_values_co_design_efficacy_total)
            column_non_co_design_efficacy_rate[y_column_name] = y_values_non_co_design_efficacy_total/(y_values_non_co_design_efficacy_total + y_values_co_design_efficacy_total)


        result = {"rate":{}, "efficacy":{}}
        rate_column_co_design = {}

        result["rate"] =  {"co_design":column_co_design_rate, "non_co_design": column_non_co_design_rate}
        result["efficacy_rate"] =  {"co_design":column_co_design_efficacy_rate, "non_co_design": column_non_co_design_efficacy_rate}
        # prepare for plotting and plot


        plt.figure()
        plotdata = pd.DataFrame(result["rate"], index=y_column_name_list)
        fontSize = 10
        plotdata.plot(kind='bar', fontsize=fontSize, stacked=True)
        plt.xticks(fontsize=fontSize, rotation=6)
        plt.yticks(fontsize=fontSize)
        plt.xlabel("co design parameter", fontsize=fontSize)
        plt.ylabel("co design rate", fontsize=fontSize)
        plt.title("co desgin rate of different parameters",  fontsize=fontSize)

        # dump in the top folder
        output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
        output_dir = os.path.join(output_base_dir, "single_workload/co_design_rate")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.savefig(os.path.join(output_dir,experiment_name +"_"+"co_design_rate_"+'_'.join(y_column_name_list)+".png"))
        plt.close('all')


        plt.figure()
        plotdata = pd.DataFrame(result["efficacy_rate"], index=y_column_name_list)
        fontSize = 10
        plotdata.plot(kind='bar', fontsize=fontSize, stacked=True)
        plt.xticks(fontsize=fontSize, rotation=6)
        plt.yticks(fontsize=fontSize)
        plt.xlabel("co design parameter", fontsize=fontSize)
        plt.ylabel("co design efficacy rate", fontsize=fontSize)
        plt.title("co design efficacy rate of different parameters", fontsize=fontSize)

        # dump in the top folder
        output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
        output_dir = os.path.join(output_base_dir, "single_workload/co_design_rate")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.savefig(os.path.join(output_dir,experiment_name+"_"+"co_design_efficacy_rate_"+'_'.join(y_column_name_list)+".png"))
        plt.close('all')



def plot_codesign_progression_per_workloads(input_dir_names, res_column_name_number):
    #itrColNum = all_res_column_name_number["iteration cnt"]
    #distColNum = all_res_column_name_number["dist_to_goal_non_cost"]
    trueNum  =  all_res_column_name_number["move validity"]

    # experiment_names
    experiment_names = []
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        file_full_addr_list.append(file_full_addr)
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        experiment_names.append(experiment_name)

    axis_font = {'size': '20'}
    x_column_name = "iteration cnt"
    y_column_name_list = ["high level optimization name", "exact optimization name", "architectural principle", "comm_comp"]


    experiment_column_value = {}
    for file_full_addr in file_full_addr_list:
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        for y_column_name in y_column_name_list:
            y_column_number = res_column_name_number[y_column_name]
            x_column_number = res_column_name_number[x_column_name]
            experiment_column_value[experiment_name] = []
            all_values = get_all_col_values_of_a_folders(input_dir_names, all_res_column_name_number, y_column_name)
            all_values_encoding = {}
            for idx, val in enumerate(all_values):
                all_values_encoding[val] = idx

            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                rows = list(resultReader)
                for i, row in enumerate(rows):
                    #if row[trueNum] != "True":
                    #    continue
                    if i >= 1:
                        if row[y_column_number] not in all_values:
                            continue

                        col_value = row[y_column_number]
                        col_values = col_value.split(";")
                        for idx, col_val in enumerate(col_values):
                            last_row =  rows[i-1]
                            delta_x_column = (float(row[x_column_number]) - float(last_row[x_column_number]))/len(col_values)
                            value_to_add = (float(last_row[x_column_number])+ idx*delta_x_column, col_val)
                            experiment_column_value[experiment_name].append(value_to_add)



            # prepare for plotting and plot
            axis_font = {'size': '20'}
            fontSize = 20

            fig = plt.figure(figsize=(12, 8))
            plt.rc('font', **axis_font)
            ax = fig.add_subplot(111)
            x_values = [el[0] for el in experiment_column_value[experiment_name]]
            #y_values = [all_values_encoding[el[1]] for el in experiment_column_value[experiment_name]]
            y_values = [el[1] for el in experiment_column_value[experiment_name]]

            #ax.set_title("experiment vs system implicaction")
            ax.tick_params(axis='both', which='major', labelsize=fontSize, rotation=60)
            ax.set_xlabel(x_column_name, fontsize=20)
            ax.set_ylabel(y_column_name, fontsize=20)
            ax.plot(x_values, y_values, label=y_column_name, linewidth=2)
            ax.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize=fontSize)

            # dump in the top folder
            output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
            output_dir = os.path.join(output_base_dir, "single_workload/progression")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            plt.tight_layout()
            fig.savefig(os.path.join(output_dir,experiment_name+"_progression_"+'_'.join(y_column_name_list)+".png"))
            # plt.show()
            plt.close('all')

            fig = plt.figure(figsize=(12, 8))
            plt.rc('font', **axis_font)
            ax = fig.add_subplot(111)
            x_values = [el[0] for el in experiment_column_value[experiment_name]]
            # y_values = [all_values_encoding[el[1]] for el in experiment_column_value[experiment_name]]
            y_values = [el[1] for el in experiment_column_value[experiment_name]]

            # ax.set_title("experiment vs system implicaction")
            ax.tick_params(axis='both', which='major', labelsize=fontSize, rotation=60)
            ax.set_xlabel(x_column_name, fontsize=20)
            ax.set_ylabel(y_column_name, fontsize=20)
            ax.plot(x_values, y_values, label=y_column_name, linewidth=2)
            ax.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize=fontSize)

            # dump in the top folder
            output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
            output_dir = os.path.join(output_base_dir, "single_workload/progression")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            plt.tight_layout()
            fig.savefig(os.path.join(output_dir, experiment_name + "_progression_" + y_column_name + ".png"))
            # plt.show()
            plt.close('all')


def plot_3d(input_dir_names, res_column_name_number):
    # experiment_names
    experiment_names = []
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1.csv")
        file_full_addr_list.append(file_full_addr)
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        experiment_names.append(experiment_name)

    axis_font = {'size': '10'}
    fontSize = 10
    column_value = {}
    # initialize the dictionary
    column_name_list = ["budget_scaling_power", "budget_scaling_area","budget_scaling_latency"]

    under_study_vars =["iteration cnt",
                       "local_bus_avg_theoretical_bandwidth", "local_bus_max_actual_bandwidth",
                       "local_bus_avg_actual_bandwidth",
                       "system_bus_avg_theoretical_bandwidth", "system_bus_max_actual_bandwidth",
                       "system_bus_avg_actual_bandwidth", "global_total_traffic", "local_total_traffic",
                       "global_memory_total_area", "local_memory_total_area", "ips_total_area",
                       "gpps_total_area","ip_cnt", "max_accel_parallelism", "avg_accel_parallelism",
                       "gpp_cnt", "max_gpp_parallelism", "avg_gpp_parallelism"]




    # get all the data
    for file_full_addr in file_full_addr_list:
        with open(file_full_addr, newline='') as csvfile:
            resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            experiment_name = get_experiments_name( file_full_addr, res_column_name_number)

            for i, row in enumerate(resultReader):
                #if row[trueNum] != "True":
                #    continue
                if i >= 1:
                    for column_name in column_name_list + under_study_vars:
                        if column_name not in column_value.keys() :
                            column_value[column_name] = []
                        column_number = res_column_name_number[column_name]
                        col_value = row[column_number]
                        col_values = col_value.split(";")
                        if "=" in col_values[0]:
                            column_value[column_name].append(float((col_values[0]).split("=")[1]))
                        else:
                            column_value[column_name].append(float(col_values[0]))


    for idx,under_study_var in enumerate(under_study_vars):
        fig_budget_blkcnt = plt.figure(figsize=(12, 12))
        plt.rc('font', **axis_font)
        ax_blkcnt = fig_budget_blkcnt.add_subplot(projection='3d')
        img = ax_blkcnt.scatter3D(column_value["budget_scaling_power"], column_value["budget_scaling_area"], column_value["budget_scaling_latency"],
                                  c=column_value[under_study_var], cmap="bwr", s=80, label="System Block Count")
        for idx,_ in enumerate(column_value[under_study_var]):
            coordinate = column_value[under_study_var][idx]
            coord_in_scientific_notatio = "{:.2e}".format(coordinate)

            ax_blkcnt.text(column_value["budget_scaling_power"][idx], column_value["budget_scaling_area"][idx], column_value["budget_scaling_latency"][idx], '%s' % coord_in_scientific_notatio, size=fontSize)

        ax_blkcnt.set_xlabel("Power Budget", fontsize=fontSize)
        ax_blkcnt.set_ylabel("Area Budget", fontsize=fontSize)
        ax_blkcnt.set_zlabel("Latency Budget", fontsize=fontSize)
        ax_blkcnt.legend()
        cbar = fig_budget_blkcnt.colorbar(img, aspect=40)
        cbar.set_label("System Block Count", rotation=270)
        #plt.title("{Power Budget, Area Budget, Latency Budget} VS System Block Count: " + subDirName)
        plt.tight_layout()

        output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
        output_dir = os.path.join(output_base_dir, "3D/case_studies")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.savefig(os.path.join(output_dir, under_study_var+ ".png"))
        # plt.show()
        plt.close('all')


def plot_convergence_per_workloads(input_dir_names, res_column_name_number):
    #itrColNum = all_res_column_name_number["iteration cnt"]
    #distColNum = all_res_column_name_number["dist_to_goal_non_cost"]
    trueNum  =  all_res_column_name_number["move validity"]
    move_name_number =  all_res_column_name_number["move name"]


    # experiment_names
    experiment_names = []
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        file_full_addr_list.append(file_full_addr)
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        experiment_names.append(experiment_name)

    color_values = ["r","b","y","black","brown","purple"]
    column_name_color_val_dict = {"best_des_so_far_power":"purple", "power_budget":"purple","best_des_so_far_area_non_dram":"blue", "area_budget":"blue",
                                  "latency_budget_hpvm_cava":"orange", "latency_budget_audio_decoder":"yellow", "latency_budget_edge_detection":"red",
                                  "best_des_so_far_latency_hpvm_cava":"orange", "best_des_so_far_latency_audio_decoder": "yellow","best_des_so_far_latency_edge_detection": "red",
                                  "latency_budget":"white"
                                  }

    axis_font = {'size': '20'}
    fontSize = 20
    x_column_name = "iteration cnt"
    y_column_name_list = ["power", "area_non_dram", "latency", "latency_budget", "power_budget","area_budget"]

    experiment_column_value = {}
    for file_full_addr in file_full_addr_list:
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        experiment_column_value[experiment_name] = {}
        for y_column_name in y_column_name_list:
            if "budget"  in y_column_name:
                prefix = ""
            else:
                prefix = "best_des_so_far_"
            y_column_name = prefix+y_column_name
            y_column_number = res_column_name_number[y_column_name]
            x_column_number = res_column_name_number[x_column_name]
            #dis_to_goal_column_number = res_column_name_number["dist_to_goal_non_cost"]
            #ref_des_dis_to_goal_column_number = res_column_name_number["ref_des_dist_to_goal_non_cost"]

            if not y_column_name == prefix+"latency":
                experiment_column_value[experiment_name][y_column_name] = []


            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for i, row in enumerate(resultReader):
                    if i > 1:
                        if row[trueNum] == "FALSE" or row[move_name_number]=="identity":
                            continue
                        col_value = row[y_column_number]
                        if ";" in col_value:
                            col_value = col_value[:-1]
                        col_values = col_value.split(";")
                        for col_val in col_values:
                            if "=" in col_val:
                                val_splitted = col_val.split("=")
                                value_to_add = (float(row[x_column_number]), (val_splitted[0], val_splitted[1]))
                            else:
                                value_to_add = (float(row[x_column_number]), col_val)

                            if y_column_name in [prefix+"latency", prefix+"latency_budget"] :
                                new_tuple = (value_to_add[0], 1000*float(value_to_add[1][1]))
                                if y_column_name+"_"+value_to_add[1][0] not in experiment_column_value[experiment_name].keys():
                                    experiment_column_value[experiment_name][y_column_name + "_" + value_to_add[1][0]] = []
                                experiment_column_value[experiment_name][y_column_name+"_"+value_to_add[1][0]].append(new_tuple)
                            if y_column_name in [prefix+"power", prefix+"power_budget"]:
                               new_tuple = (value_to_add[0], float(value_to_add[1])*1000)
                               experiment_column_value[experiment_name][y_column_name].append(new_tuple)
                            elif y_column_name in [prefix+"area_non_dram", prefix+"area_budget"]:
                                new_tuple = (value_to_add[0], float(value_to_add[1]) * 1000000)
                                experiment_column_value[experiment_name][y_column_name].append(new_tuple)

            # prepare for plotting and plot
            fig = plt.figure(figsize=(15, 8))
            ax = fig.add_subplot(111)
            for column, values in experiment_column_value[experiment_name].items():
                x_values = [el[0] for el in values]
                y_values = [el[1] for el in values]
                ax.set_yscale('log')
                if "budget" in column:
                    marker = 'x'
                    alpha_ = .3
                else:
                    marker = "_"
                    alpha_ = 1
                ax.plot(x_values, y_values, label=column, c=column_name_color_val_dict[column], marker=marker, alpha=alpha_)

            #ax.set_title("experiment vs system implicaction")
            ax.set_xlabel(x_column_name, fontsize=fontSize)
            y_axis_name = "_".join(list(experiment_column_value[experiment_name].keys()))
            ax.set_ylabel(y_axis_name, fontsize=fontSize)
            ax.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize=fontSize)
            plt.tight_layout()

            # dump in the top folder
            output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
            output_dir = os.path.join(output_base_dir, "single_workload/convergence")
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            fig.savefig(os.path.join(output_dir,experiment_name+"_convergence.png"))
            # plt.show()
            plt.close('all')

def plot_convergence_vs_time(input_dir_names, res_column_name_number):
    PA_time_scaling_factor = 10
    #itrColNum = all_res_column_name_number["iteration cnt"]
    #distColNum = all_res_column_name_number["dist_to_goal_non_cost"]
    trueNum  =  all_res_column_name_number["move validity"]

    # experiment_names
    experiment_names = []
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        file_full_addr_list.append(file_full_addr)
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        experiment_names.append(experiment_name)

    axis_font = {'size': '15'}
    fontSize = 20
    x_column_name = "exploration_plus_simulation_time"
    y_column_name_list = ["best_des_so_far_dist_to_goal_non_cost"]

    PA_column_experiment_value = {}
    FARSI_column_experiment_value = {}

    #column_name = "move name"
    for k, file_full_addr in enumerate(file_full_addr_list):
        for y_column_name in y_column_name_list:
            # get all possible the values of interest
            y_column_number = res_column_name_number[y_column_name]
            x_column_number = res_column_name_number[x_column_name]
            PA_column_experiment_value[y_column_name] = []
            FARSI_column_experiment_value[y_column_name] = []
            PA_last_time = 0
            FARSI_last_time = 0
            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                experiment_name = get_experiments_name( file_full_addr, res_column_name_number)
                for i, row in enumerate(resultReader):
                    #if row[trueNum] != "True":
                    #    continue
                    if i >= 1:
                        FARSI_last_time += float(row[x_column_number])
                        FARSI_value_to_add = (float(FARSI_last_time), row[y_column_number])
                        FARSI_column_experiment_value[y_column_name].append(FARSI_value_to_add)

                        PA_last_time = FARSI_last_time*PA_time_scaling_factor
                        PA_value_to_add = (float(PA_last_time), row[y_column_number])
                        PA_column_experiment_value[y_column_name].append(PA_value_to_add)

                # prepare for plotting and plot
                fig = plt.figure(figsize=(12, 12))
                plt.rc('font', **axis_font)
                ax = fig.add_subplot(111)
                fontSize = 20
                #plt.tight_layout()
                x_values = [el[0] for el in FARSI_column_experiment_value[y_column_name]]
                y_values = [str(float(el[1]) * 100 // 1 / 100.0) for el in FARSI_column_experiment_value[y_column_name]]
                x_values.reverse()
                y_values.reverse()
                ax.scatter(x_values, y_values, label="FARSI time to completion", marker="_")
                # ax.set_yscale('log')

                x_values = [el[0] for el in PA_column_experiment_value[y_column_name]]
                y_values = [str(float(el[1]) * 100 // 1 / 100.0) for el in PA_column_experiment_value[y_column_name]]
                x_values.reverse()
                y_values.reverse()
                ax.scatter(x_values, y_values, label="PA time to completion", marker="_")
                #ax.set_xscale('log')

               #ax.set_title("experiment vs system implicaction")
                ax.legend(loc="upper right")#bbox_to_anchor=(1, 1), loc="upper left")
                ax.set_xlabel(x_column_name, fontsize=fontSize)
                ax.set_ylabel(y_column_name, fontsize=fontSize)
                plt.tight_layout()

                # dump in the top folder
                output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
                output_dir = os.path.join(output_base_dir, "single_workload/progression")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                fig.savefig(os.path.join(output_dir,str(k)+"_" + y_column_name+"_vs_"+x_column_name+"_FARSI_vs_PA.png"))
                plt.show()
                plt.close('all')


def plot_convergence_cross_workloads(input_dir_names, res_column_name_number):
    #itrColNum = all_res_column_name_number["iteration cnt"]
    #distColNum = all_res_column_name_number["dist_to_goal_non_cost"]
    trueNum  =  all_res_column_name_number["move validity"]

    # experiment_names
    experiment_names = []
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        file_full_addr_list.append(file_full_addr)
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        experiment_names.append(experiment_name)

    axis_font = {'size': '20'}
    x_column_name = "iteration cnt"
    y_column_name_list = ["best_des_so_far_dist_to_goal_non_cost", "dist_to_goal_non_cost"]

    column_experiment_value = {}
    #column_name = "move name"
    for y_column_name in y_column_name_list:
        # get all possible the values of interest
        y_column_number = res_column_name_number[y_column_name]
        x_column_number = res_column_name_number[x_column_name]

        column_experiment_value[y_column_name] = {}
        # initialize the dictionary
        # get all the data
        for file_full_addr in file_full_addr_list:
            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                experiment_name = get_experiments_name( file_full_addr, res_column_name_number)
                column_experiment_value[y_column_name][experiment_name] = []

                for i, row in enumerate(resultReader):
                    #if row[trueNum] != "True":
                    #    continue
                    if i >= 1:
                        value_to_add = (float(row[x_column_number]), max(float(row[y_column_number]),.01))
                        column_experiment_value[y_column_name][experiment_name].append(value_to_add)

        # prepare for plotting and plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #plt.tight_layout()
        for experiment_name, values in column_experiment_value[y_column_name].items():
            x_values = [el[0] for el in values]
            y_values = [el[1] for el in values]
            ax.scatter(x_values, y_values, label=experiment_name[1:])

        #ax.set_title("experiment vs system implicaction")
        ax.set_yscale('log')
        ax.legend(bbox_to_anchor=(1, 1), loc="best")
        ax.set_xlabel(x_column_name)
        ax.set_ylabel(y_column_name)
        plt.tight_layout()

        # dump in the top folder
        output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
        output_dir = os.path.join(output_base_dir, "cross_workloads/convergence")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        fig.savefig(os.path.join(output_dir,x_column_name+"_"+y_column_name+".png"))
        # plt.show()
        plt.close('all')

def plot_system_implication_analysis(input_dir_names, res_column_name_number, case_study):
    # experiment_names
    experiment_names = []
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1.csv")
        file_full_addr_list.append(file_full_addr)
        experiment_name = get_experiments_name(file_full_addr, res_column_name_number)
        experiment_names.append(experiment_name)

    axis_font = {'size': '10'}

    column_name_list = list(case_study.values())[0]

    column_experiment_value = {}
    #column_name = "move name"
    for column_name in column_name_list:
        # get all possible the values of interest
        column_number = res_column_name_number[column_name]

        column_experiment_value[column_name] = {}
        # initialize the dictionary
        column_experiment_number_dict = {}
        experiment_number_dict = {}

        # get all the data
        for file_full_addr in file_full_addr_list:
            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                experiment_name = get_experiments_name( file_full_addr, res_column_name_number)

                for i, row in enumerate(resultReader):
                    #if row[trueNum] != "True":
                    #    continue
                    if i >= 1:
                        col_value = row[column_number]
                        col_values = col_value.split(";")
                        for col_val in col_values:
                            column_experiment_value[column_name][experiment_name] = float(col_val)

    # prepare for plotting and plot
    # plt.figure()
    index = experiment_names
    plotdata = pd.DataFrame(column_experiment_value, index=index)
    if list(case_study.keys())[0] in ["bandwidth_analysis","traffic_analysis"]:
        plotdata.plot(kind='bar', fontsize=9, rot=5, log=True)
    else:
        plotdata.plot(kind='bar', fontsize=9, rot=5)

    plt.legend(loc="best", fontsize="9")
    plt.xlabel("experiments", fontsize="10")
    plt.ylabel("system implication")
    #plt.title("experiment vs system implicaction")
    # dump in the top folder
    output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
    output_dir = os.path.join(output_base_dir, "cross_workloads/system_implications")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #plt.tight_layout()
    plt.savefig(os.path.join(output_dir,list(case_study.keys())[0]+".png"))
    plt.close('all')



def plot_co_design_nav_breakdown_post_processing(input_dir_names, column_column_value_experiment_frequency_dict):
    column_name_list = [("exact optimization name", "neighbouring design space size", "div")]
    #column_name = "move name"
    for n, column_name_tuple in enumerate(column_name_list):
        first_column =  column_name_tuple[0]
        second_column =  column_name_tuple[1]
        operation =   column_name_tuple[2]
        new_column_name = first_column+"_"+operation+"_"+second_column

        first_column_value_experiment_frequency_dict = column_column_value_experiment_frequency_dict[first_column]
        second_column_value_experiment_frequency_dict = column_column_value_experiment_frequency_dict[second_column]
        modified_column_value_experiment_frequency_dict = {}

        experiment_names = []
        for column_val, experiment_freq  in first_column_value_experiment_frequency_dict.items():
            if column_val == "unknown":
                continue
            modified_column_value_experiment_frequency_dict[column_val] = {}
            for experiment, freq in  experiment_freq.items():
                if(second_column_value_experiment_frequency_dict[column_val][experiment]) < .000001:
                    modified_column_value_experiment_frequency_dict[column_val][experiment] = 0
                else:
                    modified_column_value_experiment_frequency_dict[column_val][experiment] = first_column_value_experiment_frequency_dict[column_val][experiment]/max(second_column_value_experiment_frequency_dict[column_val][experiment],.0000000000001)
                experiment_names.append(experiment)

        axis_font = {'size': '22'}
        fontSize = 22
        experiment_names =  list(set(experiment_names))
        # prepare for plotting and plot
        # plt.figure(n)
        plt.rc('font', **axis_font)
        index = experiment_names
        plotdata = pd.DataFrame(modified_column_value_experiment_frequency_dict, index=index)
        plotdata.plot(kind='bar', stacked=True, figsize=(13, 8))
        plt.xlabel("experiments", **axis_font)
        plt.ylabel(new_column_name, **axis_font)
        plt.xticks(fontsize=fontSize, rotation=45)
        plt.yticks(fontsize=fontSize)
        plt.title("experiment vs " + new_column_name, **axis_font)
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize=fontSize)
        # dump in the top folder
        output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
        output_dir = os.path.join(output_base_dir, "cross_workloads/nav_breakdown")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # plt.tight_layout()
        plt.savefig(os.path.join(output_dir,'_'.join(new_column_name.split(" "))+".png"), bbox_inches='tight')
        plt.tight_layout()
        # plt.show()
        plt.close('all')



# navigation breakdown
def plot_codesign_nav_breakdown_per_workload(input_dir_names, input_all_res_column_name_number):
    trueNum = input_all_res_column_name_number["move validity"]

    # experiment_names
    experiment_names = []
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        file_full_addr_list.append(file_full_addr)
        experiment_name = get_experiments_name(file_full_addr, input_all_res_column_name_number)
        experiment_names.append(experiment_name)


    axis_font = {'size': '20'}
    fontSize = 20
    column_name_list = ["transformation_metric", "comm_comp", "workload"]#, "architectural principle", "high level optimization name", "exact optimization name"]
    #column_name_list = ["architectural principle", "exact optimization name"]

    #column_name = "move name"
    # initialize the dictionary
    column_column_value_experiment_frequency_dict = {}
    for file_full_addr in file_full_addr_list:
        column_column_value_frequency_dict = {}
        for column_name in column_name_list:
            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                experiment_name = get_experiments_name(file_full_addr, input_all_res_column_name_number)
                #column_column_value_frequency_dict[column_name] = {}
                # get all possible the values of interest
                all_values = get_all_col_values_of_a_folders(input_dir_names, input_all_res_column_name_number, column_name)
                columne_number = all_res_column_name_number[column_name]
                for column in all_values:
                    column_column_value_frequency_dict[column] = {}
                    column_column_value_frequency_dict[column][column_name] = 0
                for i, row in enumerate(resultReader):
                    if row[trueNum] != "True":
                        continue
                    if i > 1:
                        col_value = row[columne_number]
                        col_values = col_value.split(";")
                        for col_val in col_values:
                            if "=" in col_val:
                                val_splitted = col_val.split("=")
                                column_column_value_frequency_dict[val_splitted[0]][column_name] += float(val_splitted[1])
                            else:
                                column_column_value_frequency_dict[col_val][column_name] += 1

        index = column_name_list
        total_cnt = 0
        for val in column_column_value_frequency_dict[column].values():
            total_cnt += val

        for col_val, column_name_val in column_column_value_frequency_dict.items():
            for column_name, val in column_name_val.items():
                column_column_value_frequency_dict[col_val][column_name] /= max(total_cnt,1)

        plotdata = pd.DataFrame(column_column_value_frequency_dict, index=index)
        plotdata.plot(kind='bar', stacked=True, figsize=(10, 10))
        plt.rc('font', ** axis_font)
        plt.xlabel("experiments", **axis_font)
        plt.ylabel(column_name, **axis_font)
        plt.xticks(fontsize=fontSize, rotation=45)
        plt.yticks(fontsize=fontSize)
        plt.title("experiment vs " + column_name, **axis_font)
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize=fontSize)
        # dump in the top folder
        output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
        output_dir = os.path.join(output_base_dir, "single_workload/nav_breakdown")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir,"__".join(column_name_list)+".png"), bbox_inches='tight')
        # plt.show()
        plt.close('all')
        #column_column_value_experiment_frequency_dict[column_name] = copy.deepcopy(column_column_value_frequency_dict)

    return column_column_value_experiment_frequency_dict




def plot_codesign_nav_breakdown_cross_workload(input_dir_names, input_all_res_column_name_number):
    trueNum = input_all_res_column_name_number["move validity"]

    # experiment_names
    experiment_names = []
    file_full_addr_list = []
    for dir_name in input_dir_names:
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        file_full_addr_list.append(file_full_addr)
        experiment_name = get_experiments_name(file_full_addr, input_all_res_column_name_number)
        experiment_names.append(experiment_name)

    axis_font = {'size': '20'}
    fontSize = 20
    column_name_list = ["transformation_metric", "transformation_block_type", "move name", "comm_comp", "architectural principle", "high level optimization name", "exact optimization name", "neighbouring design space size"]
    #column_name_list = ["transformation_metric", "move name"]#, "comm_comp", "architectural principle", "high level optimization name", "exact optimization name", "neighbouring design space size"]
    #column_name = "move name"
    # initialize the dictionary
    column_column_value_experiment_frequency_dict = {}
    for column_name in column_name_list:
        column_value_experiment_frequency_dict = {}
        # get all possible the values of interest
        all_values = get_all_col_values_of_a_folders(input_dir_names, input_all_res_column_name_number, column_name)
        columne_number = all_res_column_name_number[column_name]
        for column in all_values:
            column_value_experiment_frequency_dict[column] = {}

        # get all the data
        for file_full_addr in file_full_addr_list:
            with open(file_full_addr, newline='') as csvfile:
                resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
                experiment_name = get_experiments_name( file_full_addr, input_all_res_column_name_number)
                for column_value in all_values:
                    column_value_experiment_frequency_dict[column_value][experiment_name] = 0

                for i, row in enumerate(resultReader):
                    #if row[trueNum] != "True":
                    #    continue
                    if i > 1:
                        try:
                            col_value = row[columne_number]
                            col_values = col_value.split(";")
                            for col_val in col_values:
                                if "=" in col_val:
                                    val_splitted = col_val.split("=")
                                    column_value_experiment_frequency_dict[val_splitted[0]][experiment_name] += float(val_splitted[1])
                                else:
                                    column_value_experiment_frequency_dict[col_val][experiment_name] += 1
                        except:
                            print("what")

        total_cnt = {}
        for el in column_value_experiment_frequency_dict.values():
            for exp, values in el.items():
                if exp not in total_cnt.keys():
                    total_cnt[exp] = 0
                total_cnt[exp] += values

        for col_val, exp_vals in column_value_experiment_frequency_dict.items():
            for exp, values in exp_vals.items():
                column_value_experiment_frequency_dict[col_val][exp] /= total_cnt[exp]

        # prepare for plotting and plot
        # plt.figure(figsize=(10, 8))
        index = experiment_names
        plotdata = pd.DataFrame(column_value_experiment_frequency_dict, index=index)
        plotdata.plot(kind='bar', stacked=True, figsize=(12, 10))
        plt.rc('font', **axis_font)
        plt.xlabel("experiments", **axis_font)
        plt.ylabel(column_name, **axis_font)
        plt.xticks(fontsize=fontSize, rotation=45)
        plt.yticks(fontsize=fontSize)
        plt.title("experiment vs " + column_name, **axis_font)
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize=fontSize)
        # dump in the top folder
        output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
        output_dir = os.path.join(output_base_dir, "cross_workloads/nav_breakdown")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir,'_'.join(column_name.split(" "))+".png"), bbox_inches='tight')
        # plt.show()
        plt.close('all')
        column_column_value_experiment_frequency_dict[column_name] = copy.deepcopy(column_value_experiment_frequency_dict)

    """
    # multi-stack plot here
    index = experiment_names
    plotdata = pd.DataFrame(column_column_value_experiment_frequency_dict, index=index)

    df_g = plotdata.groupby(["transformation_metric", "move name"])
    plotdata.plot(kind='bar', stacked=True, figsize=(12, 10))
    plt.rc('font', **axis_font)
    plt.xlabel("experiments", **axis_font)
    plt.ylabel(column_name, **axis_font)
    plt.xticks(fontsize=fontSize, rotation=45)
    plt.yticks(fontsize=fontSize)
    plt.title("experiment vs " + column_name, **axis_font)
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize=fontSize)
    # dump in the top folder
    output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
    output_dir = os.path.join(output_base_dir, "cross_workloads/nav_breakdown")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,'column____'.join(column_name.split(" "))+".png"), bbox_inches='tight')
    # plt.show()
    plt.close('all')
    """
    return column_column_value_experiment_frequency_dict




# the function to plot distance to goal vs. iteration cnt
def plotDistToGoalVSitr(input_dir_names, all_res_column_name_number):
    itrColNum = all_res_column_name_number["iteration cnt"]
    distColNum = all_res_column_name_number["dist_to_goal_non_cost"]
    trueNum  =  all_res_column_name_number["move validity"]

    experiment_itr_dist_to_goal_dict = {}
    # iterate through directories, get data and store in a dictionary
    for dir_name in input_dir_names:
        itr = []
        distToGoal = []
        file_full_addr = os.path.join(dir_name, "result_summary/FARSI_simple_run_0_1_all_reults.csv")
        with open(file_full_addr, newline='') as csvfile:
            resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            experiment_name = get_experiments_name(file_full_addr, all_res_column_name_number)
            for i, row in enumerate(resultReader):
                if row[trueNum] != "True":
                    continue
                if i > 1:
                    itr.append(int(row[itrColNum]))
                    distToGoal.append(float(row[distColNum]))

            experiment_itr_dist_to_goal_dict[experiment_name] = (itr[:], distToGoal[:])

    plt.figure()
    # iterate and plot
    for experiment_name, value in experiment_itr_dist_to_goal_dict.items():
        itr, distToGoal = value[0], value[1]
        if len(itr) == 0 or len(distToGoal) == 0: # no valid move
            continue
        plt.plot(itr, distToGoal, label=experiment_name)
        plt.xlabel("Iteration Cnt")
        plt.ylabel("Distance to Goal")
        plt.title("Distance to Goal vs. Iteration Cnt")

    # decide on the output dir
    if len(input_dir_names) == 1:
        output_dir = input_dir_names[0]
    else:
        # dump in the top folder
        output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
        output_dir  = os.path.join(output_base_dir, "cross_workloads")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    plt.savefig(os.path.join(output_dir, "distToGoalVSitr.png"))
    # plt.show()
    plt.close('all')


# the function to plot distance to goal vs. iteration cnt
def plotRefDistToGoalVSitr(dirName, fileName, itrColNum, refDistColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        itr = []
        refDistToGoal = []

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i > 1:
                itr.append(int(row[itrColNum]))
                refDistToGoal.append(float(row[refDistColNum]))

        plt.figure()
        plt.plot(itr, refDistToGoal)
        plt.xlabel("Iteration Cnt")
        plt.ylabel("Reference Design Distance to Goal")
        plt.title("Reference Design Distance to Goal vs. Iteration Cnt")
        plt.savefig(dirName + fileName + "/refDistToGoalVSitr-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to do the zonal partitioning
def zonalPartition(comparedValue, zoneNum, maxValue):
    unit = maxValue / zoneNum

    if comparedValue > maxValue:
        return zoneNum - 1
    
    if comparedValue < 0:
        return 0

    for i in range(0, zoneNum):
        if comparedValue <= unit * (i + 1):
            return i

    raise Exception("zonalPartition is fed by a strange value! maxValue: " + str(maxValue) + "; comparedValue: " + str(comparedValue))

# the function to plot simulation time vs. move name in a zonal format
def plotSimTimeVSmoveNameZoneDist(dirName, fileName, zoneNum, moveColNum, distColNum, simColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        splitSwapSim = np.zeros(zoneNum, dtype = float)
        splitSim = np.zeros(zoneNum, dtype = float)
        migrateSim = np.zeros(zoneNum, dtype = float)
        swapSim = np.zeros(zoneNum, dtype = float)
        tranSim = np.zeros(zoneNum, dtype = float)
        routeSim = np.zeros(zoneNum, dtype = float)
        identitySim = np.zeros(zoneNum, dtype = float)

        maxDist = 0

        index = []
        for i in range(0, zoneNum):
            index.append(i)

        for i, row in enumerate(resultReader):
            # print('"' + row[trueNum] + '"\t"' + row[moveColNum] + '"\t"' + row[distColNum] + '"\t"' + row[simColNum] + '"')
            if row[trueNum] != "True":
                continue

            if i == 2:
                maxDist = float(row[distColNum])

            if i > 1:
                if row[moveColNum] == "split_swap":
                    splitSwapSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[moveColNum] == "split":
                    splitSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[moveColNum] == "migrate":
                    migrateSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[moveColNum] == "swap":
                    swapSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[moveColNum] == "transfer":
                    tranSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[moveColNum] == "routing":
                    routeSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[moveColNum] == "identity":
                    identitySim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                else:
                    raise Exception("move name is not split_swap or split or migrate or swap or transfer or routing or identity! The new type: " + row[moveColNum])
        
        # plt.figure()
        plotdata = pd.DataFrame({
            "split_swap":splitSwapSim,
            "split":splitSim,
            "migrate":migrateSim,
            "swap":swapSim,
            "transfer":tranSim,
            "routing":routeSim,
            "identity":identitySim
        }, index = index
        )
        plotdata.plot(kind = 'bar', stacked = True)
        plt.xlabel("Zone decided by the max distance to goal")
        plt.ylabel("Simulation Time")
        plt.title("Simulation Time in Each Zone based on Move Name")
        plt.savefig(dirName + fileName + "/simTimeVSmoveNameZoneDist-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot move generation time vs. move name in a zonal format
def plotMovGenTimeVSmoveNameZoneDist(dirName, fileName, zoneNum, moveColNum, distColNum, movGenColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        splitSwapMov = np.zeros(zoneNum, dtype = float)
        splitMov = np.zeros(zoneNum, dtype = float)
        migrateMov = np.zeros(zoneNum, dtype = float)
        swapMov = np.zeros(zoneNum, dtype = float)
        tranMov = np.zeros(zoneNum, dtype = float)
        routeMov = np.zeros(zoneNum, dtype = float)
        identityMov = np.zeros(zoneNum, dtype = float)

        maxDist = 0

        index = []
        for i in range(0, zoneNum):
            index.append(i)

        for i, row in enumerate(resultReader):
            # print('"' + row[trueNum] + '"\t"' + row[moveColNum] + '"\t"' + row[distColNum] + '"\t"' + row[movGenColNum] + '"')
            if row[trueNum] != "True":
                continue

            if i == 2:
                maxDist = float(row[distColNum])

            if i > 1:
                if row[moveColNum] == "split_swap":
                    splitSwapMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[moveColNum] == "split":
                    splitMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[moveColNum] == "migrate":
                    migrateMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[moveColNum] == "swap":
                    swapMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[moveColNum] == "transfer":
                    tranMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[moveColNum] == "routing":
                    routeMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[moveColNum] == "identity":
                    identityMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                else:
                    raise Exception("move name is not split_swap or split or migrate or swap or transfer of routing or identity! The new type: " + row[moveColNum])
        
        # plt.figure()
        plotdata = pd.DataFrame({
            "split_swap":splitSwapMov,
            "split":splitMov,
            "migrate":migrateMov,
            "swap":swapMov,
            "transfer":tranMov,
            "routing":routeMov,
            "identity":identityMov
        }, index = index
        )
        plotdata.plot(kind = 'bar', stacked = True)
        plt.xlabel("Zone decided by the max distance to goal")
        plt.ylabel("Move Generation Time")
        plt.title("Move Generation Time in Each Zone based on Move Name")
        plt.savefig(dirName + fileName + "/movGenTimeVSmoveNameZoneDist-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot simulation time vs. comm_comp in a zonal format
def plotSimTimeVScommCompZoneDist(dirName, fileName, zoneNum, commcompColNum, distColNum, simColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        commSim = np.zeros(zoneNum, dtype = float)
        compSim = np.zeros(zoneNum, dtype = float)

        maxDist = 0
        index = []
        for i in range(0, zoneNum):
            index.append(i)

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i == 2:
                maxDist = float(row[distColNum])

            if i > 1:
                if row[commcompColNum] == "comm":
                    commSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[commcompColNum] == "comp":
                    compSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                else:
                    raise Exception("comm_comp is not giving comm or comp! The new type: " + row[colNum])
        
        # plt.figure()
        plotdata = pd.DataFrame({
            "comm":commSim,
            "comp":compSim
        }, index = index
        )
        plotdata.plot(kind = 'bar', stacked = True)
        plt.xlabel("Zone decided by the max distance to goal")
        plt.ylabel("Simulation Time")
        plt.title("Simulation Time in Each Zone based on comm_comp")
        plt.savefig(dirName + fileName + "/simTimeVScommCompZoneDist-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot simulation time vs. comm_comp in a zonal format
def plotMovGenTimeVScommCompZoneDist(dirName, fileName, zoneNum, commcompColNum, distColNum, movGenColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        commMov = np.zeros(zoneNum, dtype = float)
        compMov = np.zeros(zoneNum, dtype = float)

        maxDist = 0
        index = []
        for i in range(0, zoneNum):
            index.append(i)

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i == 2:
                maxDist = float(row[distColNum])

            if i > 1:
                if row[commcompColNum] == "comm":
                    commMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[commcompColNum] == "comp":
                    compMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                else:
                    raise Exception("comm_comp is not giving comm or comp! The new type: " + row[colNum])
        
        # plt.figure()
        plotdata = pd.DataFrame({
            "comm":commMov,
            "comp":compMov
        }, index = index
        )
        plotdata.plot(kind = 'bar', stacked = True)
        plt.xlabel("Zone decided by the max distance to goal")
        plt.ylabel("Move Generation Time")
        plt.title("Move Generation Time in Each Zone based on comm_comp")
        plt.savefig(dirName + fileName + "/movGenTimeVScommCompZoneDist-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot simulation time vs. high level optimization name in a zonal format
def plotSimTimeVShighLevelOptZoneDist(dirName, fileName, zoneNum, optColNum, distColNum, simColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        topoSim = np.zeros(zoneNum, dtype = float)
        tunSim = np.zeros(zoneNum, dtype = float)
        mapSim = np.zeros(zoneNum, dtype = float)
        idenOptSim = np.zeros(zoneNum, dtype = float)

        maxDist = 0
        index = []
        for i in range(0, zoneNum):
            index.append(i)

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i == 2:
                maxDist = float(row[distColNum])

            if i > 1:
                if row[optColNum] == "topology":
                    topoSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[optColNum] == "customization":
                    tunSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[optColNum] == "mapping":
                    mapSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[optColNum] == "identity":
                    idenOptSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                else:
                    raise Exception("high level optimization name is not giving topology or customization or mapping or identity! The new type: " + row[optColNum])
        
        # plt.figure()
        plotdata = pd.DataFrame({
            "topology":topoSim,
            "customization":tunSim,
            "mapping":mapSim,
            "identity":idenOptSim
        }, index = index
        )
        plotdata.plot(kind = 'bar', stacked = True)
        plt.xlabel("Zone decided by the max distance to goal")
        plt.ylabel("Simulation Time")
        plt.title("Simulation Time in Each Zone based on Optimation Name")
        plt.savefig(dirName + fileName + "/simTimeVShighLevelOptZoneDist-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot simulation time vs. high level optimization name in a zonal format
def plotMovGenTimeVShighLevelOptZoneDist(dirName, fileName, zoneNum, optColNum, distColNum, movGenColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        topoMov = np.zeros(zoneNum, dtype = float)
        tunMov = np.zeros(zoneNum, dtype = float)
        mapMov = np.zeros(zoneNum, dtype = float)
        idenOptMov = np.zeros(zoneNum, dtype = float)

        maxDist = 0
        index = []
        for i in range(0, zoneNum):
            index.append(i)

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i == 2:
                maxDist = float(row[distColNum])

            if i > 1:
                if row[optColNum] == "topology":
                    topoMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[optColNum] == "customization":
                    tunMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[optColNum] == "mapping":
                    mapMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[optColNum] == "identity":
                    idenOptMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                else:
                    raise Exception("high level optimization name is not giving topology or customization or mapping or identity! The new type: " + row[optColNum])
        
        # plt.figure()
        plotdata = pd.DataFrame({
            "topology":topoMov,
            "customization":tunMov,
            "mapping":mapMov,
            "identity":idenOptMov
        }, index = index
        )
        plotdata.plot(kind = 'bar', stacked = True)
        plt.xlabel("Zone decided by the max distance to goal")
        plt.ylabel("Transformation Generation Time")
        plt.title("Transformation Generation Time in Each Zone based on Optimization Name")
        plt.savefig(dirName + fileName + "/movGenTimeVShighLevelOptZoneDist-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot simulation time vs. architectural principle in a zonal format
def plotSimTimeVSarchVarImpZoneDist(dirName, fileName, zoneNum, archColNum, distColNum, simColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        paraSim = np.zeros(zoneNum, dtype = float)
        custSim = np.zeros(zoneNum, dtype = float)
        localSim = np.zeros(zoneNum, dtype = float)
        idenImpSim = np.zeros(zoneNum, dtype = float)

        maxDist = 0
        index = []
        for i in range(0, zoneNum):
            index.append(i)

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i == 2:
                maxDist = float(row[distColNum])

            if i > 1:
                if row[archColNum] == "parallelization":
                    paraSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[archColNum] == "customization":
                    custSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[archColNum] == "locality":
                    localSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                elif row[archColNum] == "identity":
                    idenImpSim[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[simColNum])
                else:
                    raise Exception("architectural principle is not giving parallelization or customization or locality or identity! The new type: " + row[archColNum])
        
        # plt.figure()
        plotdata = pd.DataFrame({
            "parallelization":paraSim,
            "customization":custSim,
            "locality":localSim,
            "identity":idenImpSim
        }, index = index
        )
        plotdata.plot(kind = 'bar', stacked = True)
        plt.xlabel("Zone decided by the max distance to goal")
        plt.ylabel("Simulation Time")
        plt.title("Simulation Time in Each Zone based on Architectural Principle")
        plt.savefig(dirName + fileName + "/simTimeVSarchVarImpZoneDist-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot simulation time vs. architectural principle in a zonal format
def plotMovGenTimeVSarchVarImpZoneDist(dirName, fileName, zoneNum, archColNum, distColNum, movGenColNum, trueNum):
    with open(dirName + fileName + "/result_summary/FARSI_simple_run_0_1_all_reults.csv", newline='') as csvfile:
        resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')

        paraMov = np.zeros(zoneNum, dtype = float)
        custMov = np.zeros(zoneNum, dtype = float)
        localMov = np.zeros(zoneNum, dtype = float)
        idenImpMov = np.zeros(zoneNum, dtype = float)

        maxDist = 0
        index = []
        for i in range(0, zoneNum):
            index.append(i)

        for i, row in enumerate(resultReader):
            if row[trueNum] != "True":
                continue

            if i == 2:
                maxDist = float(row[distColNum])

            if i > 1:
                if row[archColNum] == "parallelization":
                    paraMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[archColNum] == "customization":
                    custMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[archColNum] == "locality":
                    localMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                elif row[archColNum] == "identity":
                    idenImpMov[zonalPartition(float(row[distColNum]), zoneNum, maxDist)] += float(row[movGenColNum])
                else:
                    raise Exception("architectural principle is not giving parallelization or customization or locality or identity! The new type: " + row[archColNum])
        
        # plt.figure()
        plotdata = pd.DataFrame({
            "parallelization":paraMov,
            "customization":custMov,
            "locality":localMov,
            "identity":idenImpMov
        }, index = index
        )
        plotdata.plot(kind = 'bar', stacked = True)
        plt.xlabel("Zone decided by the max distance to goal")
        plt.ylabel("Tranformation Generation Time")
        plt.title("Tranformation Generation Time in Each Zone based on Architectural Principle")
        plt.savefig(dirName + fileName + "/movGenTimeVSarchVarImpZoneZoneDist-" + fileName + ".png")
        # plt.show()
        plt.close('all')

# the function to plot convergence vs. iteration cnt, system block count, and routing complexity in 3d
def plotBudgets3d(dirName, subDirName):
    newDirName = dirName + "/"+ subDirName + "/"
    if os.path.exists(newDirName + "/figures"):
        shutil.rmtree(newDirName + "/figures")
    resultList = os.listdir(newDirName)
    latBudgets = []
    powBudgets = []
    areaBudgets = []
    itrValues = []
    cntValues = []
    routingValues = []
    workloads = []
    for j, fileName in enumerate(resultList):
        with open(newDirName + fileName + "/result_summary/FARSI_simple_run_0_1.csv", newline='') as csvfile:
            resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for i, row in enumerate(resultReader):
                if i == 1:
                    itrValues.append(int(row[columnNum(newDirName, fileName, "iteration cnt", "simple")]))
                    cntValues.append(int(row[columnNum(newDirName, fileName, "system block count", "simple")]))
                    routingValues.append(float(row[columnNum(newDirName, fileName, "routing complexity", "simple")]))
                    powBudgets.append(float(row[columnNum(newDirName, fileName, "power_budget", "simple")]))
                    areaBudgets.append(float(row[columnNum(newDirName, fileName, "area_budget", "simple")]))
                    lat = row[int(columnNum(newDirName, fileName, "latency_budget", "simple"))][:-1]
                    latDict = dict(item.split("=") for item in lat.split(";"))
                    if j == 0:
                        for k in range(0, len(latDict)):
                            latBudgets.append([])
                            workloads.append(list(latDict.keys())[k])
                    latList = list(latDict.values())
                    for k in range(0, len(latList)):
                        latBudgets[k].append(float(latList[k]))

    m = ['o', 'x', '^', 's', 'd', '+', 'v', '<', '>']
    axis_font = {'size': '10'}
    fontSize = 10
    os.mkdir(newDirName + "figures")
    fig_budget_itr = plt.figure(figsize=(12, 12))
    plt.rc('font', **axis_font)
    ax_itr = fig_budget_itr.add_subplot(projection='3d')
    for i in range(0, len(latBudgets)):
        img = ax_itr.scatter3D(powBudgets, areaBudgets, latBudgets[i], c=itrValues, cmap="bwr", marker=m[i], s=80, label='{0}'.format(workloads[i]))
        for j in range(0, len(latBudgets[i])):
            coordinate = str(itrValues[j])
            ax_itr.text(powBudgets[j], areaBudgets[j], latBudgets[i][j], '%s' % coordinate, size=fontSize)
        break
    ax_itr.set_xlabel("Power Budget")
    ax_itr.set_ylabel("Area Budget")
    ax_itr.set_zlabel("Latency Budget")
    ax_itr.legend()
    cbar_itr = fig_budget_itr.colorbar(img, aspect = 40)
    cbar_itr.set_label("Number of Iterations", rotation = 270)
    plt.title("{Power Budget, Area Budget, Latency Budget} VS Iteration Cnt: " + subDirName)
    plt.tight_layout()
    plt.savefig(newDirName + "figures/budgetVSitr-" + subDirName + ".png")
    # plt.show()
    plt.close('all')

    fig_budget_blkcnt = plt.figure(figsize=(12, 12))
    plt.rc('font', **axis_font)
    ax_blkcnt = fig_budget_blkcnt.add_subplot(projection='3d')
    for i in range(0, len(latBudgets)):
        img = ax_blkcnt.scatter3D(powBudgets, areaBudgets, latBudgets[i], c=cntValues, cmap="bwr", marker=m[i], s=80, label='{0}'.format(workloads[i]))
        for j in range(0, len(latBudgets[i])):
            coordinate = str(cntValues[j])
            ax_blkcnt.text(powBudgets[j], areaBudgets[j], latBudgets[i][j], '%s' % coordinate, size=fontSize)
        break
    ax_blkcnt.set_xlabel("Power Budget")
    ax_blkcnt.set_ylabel("Area Budget")
    ax_blkcnt.set_zlabel("Latency Budget")
    ax_blkcnt.legend()
    cbar = fig_budget_blkcnt.colorbar(img, aspect=40)
    cbar.set_label("System Block Count", rotation=270)
    plt.title("{Power Budget, Area Budget, Latency Budget} VS System Block Count: " + subDirName)
    plt.tight_layout()
    plt.savefig(newDirName + "figures/budgetVSblkcnt-" + subDirName + ".png")
    # plt.show()
    plt.close('all')

    fig_budget_routing = plt.figure(figsize=(12, 12))
    plt.rc('font', **axis_font)
    ax_routing = fig_budget_routing.add_subplot(projection='3d')
    for i in range(0, len(latBudgets)):
        img = ax_routing.scatter3D(powBudgets, areaBudgets, latBudgets[i], c=cntValues, cmap="bwr", marker=m[i], s=80, label='{0}'.format(workloads[i]))
        for j in range(0, len(latBudgets[i])):
            coordinate = str(routingValues[j])
            ax_routing.text(powBudgets[j], areaBudgets[j], latBudgets[i][j], '%s' % coordinate, size=fontSize)
        break
    ax_routing.set_xlabel("Power Budget")
    ax_routing.set_ylabel("Area Budget")
    ax_routing.set_zlabel("Latency Budget")
    ax_routing.legend()
    cbar = fig_budget_routing.colorbar(img, aspect=40)
    cbar.set_label("System Block Count", rotation=270)
    plt.title("{Power Budget, Area Budget, Latency Budget} VS System Block Count: " + subDirName)
    plt.tight_layout()
    plt.savefig(newDirName + "figures/budgetVSroutingComplexity-" + subDirName + ".png")
    # plt.show()
    plt.close('all')

def get_experiment_dir_list(run_folder_name):
    workload_set_folder_list = os.listdir(run_folder_name)

    experiment_full_addr_list = []
    #  iterate and generate plots
    for workload_set_folder in workload_set_folder_list:
        # ignore irelevant files
        if workload_set_folder in config_plotting.ignore_file_names:
            continue

        # get experiment folder
        workload_set_full_addr = os.path.join(run_folder_name,workload_set_folder)
        folder_list = os.listdir(workload_set_full_addr)
        for experiment_name_relative_addr in folder_list:
            if experiment_name_relative_addr in config_plotting.ignore_file_names:
                continue
            experiment_full_addr_list.append(os.path.join(workload_set_full_addr, experiment_name_relative_addr))

    return experiment_full_addr_list


def find_the_most_recent_directory(top_dir):
    dirs = [os.path.join(top_dir, el) for el in os.listdir(top_dir)]
    dirs = list(filter(os.path.isdir, dirs))
    dirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return dirs


def get_experiment_full_file_addr_list(experiment_full_dir_list):
    file_name = "result_summary/FARSI_simple_run_0_1.csv"
    results = []
    for el in experiment_full_dir_list:
        results.append(os.path.join(el, file_name))

    return results

######### RADHIKA PANDAS PLOTS ############

def grouped_barplot_varying_x(df, metric, metric_ylabel, varying_x, varying_x_labels, ax):
    # [[bar heights, errs for varying_x1], [heights, errs for varying_x2]...]
    grouped_stats_list = []
    for x in varying_x:
        grouped_x = df.groupby([x])
        stats = grouped_x[metric].agg([np.mean, np.std])
        grouped_stats_list.append(stats)

    start_loc = 0
    bar_width = 0.15
    offset = 0.03
    # [[bar locations for varying_x1], [bar locs for varying_x2]...]
    grouped_bar_locs_list = []
    for x in varying_x:
        n_unique_varying_x = df[x].nunique()
        bound = n_unique_varying_x * (bar_width+offset)
        end_loc = start_loc+bound
        bar_locs = np.linspace(start_loc, end_loc, n_unique_varying_x)
        grouped_bar_locs_list.append(bar_locs)
        start_loc = end_loc + 2*bar_width

    print(grouped_bar_locs_list)

    for x_i,x in enumerate(varying_x):
        ax.bar(
            grouped_bar_locs_list[x_i],
            grouped_stats_list[x_i]["mean"],
            width=bar_width,
            yerr=grouped_stats_list[x_i]["std"]
            #label=metric_ylabel
        )

    cat_xticks = []
    cat_xticklabels = []

    xticks = []
    xticklabels = []
    for x_i,x in enumerate(varying_x):
        xticklabels.extend(grouped_stats_list[x_i].index.astype(float))
        xticks.extend(grouped_bar_locs_list[x_i])

        xticks_cat = grouped_bar_locs_list[x_i]
        xticks_cat_start = xticks_cat[0]
        xticks_cat_end = xticks_cat[-1]
        xticks_cat_mid = xticks_cat_start + (xticks_cat_end - xticks_cat_start) / 2

        cat_xticks.append(xticks_cat_mid)
        cat_xticklabels.append("\n\n" + varying_x_labels[x_i])

    xticks.extend(cat_xticks)
    xticklabels.extend(cat_xticklabels)

    ax.set_ylabel(metric_ylabel)
    #ax.set_xlabel(xlabel)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)

    return ax


def pandas_plots(all_results_files):
    df = pd.concat((pd.read_csv(f) for f in all_results_files))

    #df = raw_df.loc[(raw_df["move validity"] == True)]
    #df["dist_to_goal_non_cost_delta"] = df["ref_des_dist_to_goal_non_cost"] - df["dist_to_goal_non_cost"]
    df["local_traffic_ratio"] = np.divide(df["local_total_traffic"], df["local_total_traffic"] + df["global_total_traffic"])

    print(df["local_traffic_ratio"])

    fig, ax = plt.subplots(1)

    #metric = "global_memory_avg_freq"
    #metric_ylabel = "Global memory avg freq"
    metric = "local_traffic_ratio"
    metric_ylabel = "Local traffic ratio"
    varying_x = [
            "budget_scaling_latency",
            "budget_scaling_power",
            "budget_scaling_area",
    ]
    varying_x_labels = [
            "Budget scaling latency",
            "Budget scaling power",
            "Budget scaling area",
    ]

    grouped_barplot_varying_x(
            df,
            metric, metric_ylabel,
            varying_x, varying_x_labels,
            ax
    )
    fig.tight_layout(rect=[0, 0, 1, 1])
    fig.savefig("/Users/behzadboro/Project_FARSI_dir/Project_FARSI_with_channels/data_collection/data/simple_run/27_point_coverage_zad/bleh.png")
    plt.close(fig)

def get_budget_optimality(input_dir_names,all_result_files, summary_res_column_name_number):
    workload_results = {}
    for file in all_result_files:
        with open(file, newline='') as csvfile:
            resultReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for i, row in enumerate(resultReader):
                if i == 1:
                    blah = summary_res_column_name_number["workload_set"]
                    workload_set_name = row[summary_res_column_name_number["workload_set"]]
                    if workload_set_name not in workload_results.keys():
                        workload_results[workload_set_name] = []
                    latency = ((row[summary_res_column_name_number["latency"]].split(";"))[0].split("="))[1]
                    latency_budget = ((row[summary_res_column_name_number["latency_budget"]].split(";"))[0].split("="))[1]
                    if float(latency)  > float(latency_budget):
                        continue

                    power = row[summary_res_column_name_number["power"]]
                    area = row[summary_res_column_name_number["area"]]
                    workload_results[workload_set_name].append((float(power),float(area)))

    workload_pareto_points = {}
    for workload, points in workload_results.items():
        workload_pareto_points[workload] = find_pareto_points(list(set(points)))

    """" 
    # combine the results
    combined_area_power = []
    for results_combined in itertools.product(*list(workload_pareto_points.values())):
        combined_power_area_tuple = [0,0]
        for el in results_combined:
            combined_power_area_tuple[0] += el[0]
            combined_power_area_tuple[1] += el[1]
        combined_area_power.append(combined_power_area_tuple[:])
    """


    all_points = []
    for workload, points in workload_results.items():
        for point in points:
            all_points.append(point)


    combined_area_power = []
    for results_combined in itertools.product(all_points):
        combined_power_area_tuple = [0,0]
        for el in results_combined:
            combined_power_area_tuple[0] += el[0]
            combined_power_area_tuple[1] += el[1]
        combined_area_power.append((combined_power_area_tuple[0],combined_power_area_tuple[1]))

    combined_area_power_pareto = find_pareto_points(list(set(combined_area_power)))

    # prepare for plotting and plot
    fig = plt.figure(figsize=(12, 12))
    #plt.rc('font', **axis_font)
    ax = fig.add_subplot(111)
    fontSize = 20
    # plt.tight_layout()
    x_values = [el[0] for el in combined_area_power_pareto]
    y_values = [el[1] for el in combined_area_power_pareto]
    x_values.reverse()
    y_values.reverse()
    ax.scatter(x_values, y_values, label="pareto front of sweep",marker="x")


    x_values = [el[0] for el in all_points]
    y_values = [el[1] for el in all_points]
    x_values.reverse()
    y_values.reverse()
    ax.scatter(x_values, y_values, label="all points",marker="_")

    # ax.set_title("experiment vs system implicaction")
    ax.legend(loc="upper right")  # bbox_to_anchor=(1, 1), loc="upper left")
    ax.set_xlabel("power", fontsize=fontSize)
    ax.set_ylabel("area", fontsize=fontSize)
    plt.tight_layout()

    # dump in the top folder
    output_base_dir = '/'.join(input_dir_names[0].split("/")[:-2])
    output_dir = os.path.join(output_base_dir, "budget_optimality/")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    fig.savefig(os.path.join(output_dir, "budget_optimality.png"))
    plt.show()
    plt.close('all')


def find_pareto_points(points):
    efficients = is_pareto_efficient_dumb(np.array(points))
    pareto_points_array = [points[idx] for idx, el in enumerate(efficients) if el]

    return pareto_points_array

    pareto_points = []
    for el in pareto_points_array:
        list_ = []
        for el_ in el:
            list.append(el)
        pareto_points.append(list_)

    return pareto_points


def is_pareto_efficient_dumb(costs):
    is_efficient = np.ones(costs.shape[0], dtype = bool)
    for i, c in enumerate(costs):
        is_efficient[i] = np.all(np.any(costs[:i]>c, axis=1)) and np.all(np.any(costs[i+1:]>c, axis=1))
    return is_efficient



###########################################

# the main function. comment out the plots if you do not need them
if __name__ == "__main__":
    # populate parameters
    run_folder_name =  config_plotting.run_folder_name
    if  config_plotting.run_folder_name == "":
        run_folder_name = find_the_most_recent_directory(config_plotting.top_result_folder)[0]

    zoneNum = config_plotting.zoneNum
    # get all the experiments under the run folder
    print(run_folder_name)
    experiment_full_addr_list = get_experiment_dir_list(run_folder_name)

    # according to the plot type, plot
    all_res_column_name_number = get_column_name_number(experiment_full_addr_list[0], "all")
    all_results_files = get_experiment_full_file_addr_list(experiment_full_addr_list)
    summary_res_column_name_number = get_column_name_number(experiment_full_addr_list[0], "simple")
    case_studies = {}
    case_studies["bandwidth_analysis"] = ["local_bus_avg_theoretical_bandwidth", "local_bus_max_actual_bandwidth", "local_bus_avg_actual_bandwidth",
                                          "system_bus_avg_theoretical_bandwidth", "system_bus_max_actual_bandwidth", "system_bus_avg_actual_bandwidth"]
    case_studies["traffic_analysis"] = ["global_total_traffic", "local_total_traffic"]
    case_studies["area_analysis"] = ["global_memory_total_area", "local_memory_total_area", "ips_total_area",
                                     "gpps_total_area"]
    case_studies["accel_paral_analysis"] = ["ip_cnt","max_accel_parallelism", "avg_accel_parallelism",
                                            "gpp_cnt", "max_gpp_parallelism", "avg_gpp_parallelism"]
    case_studies["system_complexity"] = ["system block count", "routing complexity", "system PE count",
                                         "local_mem_cnt", "local_bus_cnt"]  # , "channel_cnt"]

    case_studies["heterogenity"] = ["local_bus_freq_coeff_var", "local_bus_bus_width_coeff_var",
                                    "local_memory_freq_coeff_var", "local_memory_area_coeff_var",
                                    "ips_freq_coeff_var", "ips_area_coeff_var",
                                    "pes_freq_coeff_var", "pes_area_coeff_var"]

    if "budget_optimality":
        get_budget_optimality(experiment_full_addr_list, all_results_files, summary_res_column_name_number)

    if "cross_workloads" in config_plotting.plot_list:
        # get column orders (assumption is that the column order doesn't change between experiments)
        plot_convergence_cross_workloads(experiment_full_addr_list, all_res_column_name_number)
        column_column_value_experiment_frequency_dict = plot_codesign_nav_breakdown_cross_workload(experiment_full_addr_list, all_res_column_name_number)

        for key, val in case_studies.items():
            case_study = {key:val}
            plot_system_implication_analysis(experiment_full_addr_list, summary_res_column_name_number, case_study)
        plot_co_design_nav_breakdown_post_processing(experiment_full_addr_list, column_column_value_experiment_frequency_dict)
        plot_codesign_rate_efficacy_cross_workloads_updated(experiment_full_addr_list, all_res_column_name_number)

    if "single_workload" in config_plotting.plot_list:
        #single workload
        plot_codesign_progression_per_workloads(experiment_full_addr_list, all_res_column_name_number)
        _ = plot_codesign_nav_breakdown_per_workload(experiment_full_addr_list, all_res_column_name_number)
        plot_convergence_per_workloads(experiment_full_addr_list, all_res_column_name_number)
        plot_convergence_vs_time(experiment_full_addr_list, all_res_column_name_number)

    if "plot_3d" in config_plotting.plot_list:
        plot_3d(experiment_full_addr_list, summary_res_column_name_number)

    if "pandas_plots" in config_plotting.plot_list:
        pandas_plots(all_results_files)

    # get the the workload_set folder
    # each workload_set has a bunch of experiments underneath it
    workload_set_folder_list = os.listdir(run_folder_name)

    #  iterate and generate plots
    for workload_set_folder in workload_set_folder_list:
        # ignore irelevant files
        if workload_set_folder in config_plotting.ignore_file_names:
            continue

        # start plotting
        #plotBudgets3d(run_folder_name, workload_set_folder)


        """
        # get experiment folder
        workload_set_full_addr = os.path.join(run_folder_name,workload_set_folder)
        folder_list = os.listdir(workload_set_full_addr)
        for experiment_name_relative_addr in folder_list:
            print(experiment_name_relative_addr)
            if experiment_name_relative_addr in config_plotting.ignore_file_names:
                continue
            experiment_full_addr = os.path.join(workload_set_full_addr, experiment_name_relative_addr)

            all_res_column_name_number = get_column_name_number(experiment_full_addr, "all")
            summary_res_column_name_number = get_column_name_number(experiment_full_addr, "simple")

            workload_set_full_addr +="/" # this is because you didn't use join
            commcompColNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "comm_comp", "all")
            trueNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "move validity", "all")
            optColNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "high level optimization name", "all")
            archColNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "architectural principle", "all")
            sysBlkNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "system block count", "all")
            simColNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "simulation time", "all")
            movGenColNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "transformation generation time", "all")
            movColNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "move name", "all")
            itrNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "iteration cnt", "all")
            distColNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "dist_to_goal_non_cost", "all")
            refDistColNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "ref_des_dist_to_goal_non_cost", "all")
            latNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "latency", "all")
            powNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "power", "all")
            areaNum = columnNum(workload_set_full_addr, experiment_name_relative_addr, "area", "all")

            # comment or uncomment the following functions for your plottings
            plotDistToGoalVSitr([experiment_full_addr], all_res_column_name_number)
            plotCommCompAll(workload_set_full_addr, experiment_name_relative_addr, all_res_column_name_number)
            plothighLevelOptAll(workload_set_full_addr, experiment_name_relative_addr, all_res_column_name_number)
            plotArchVarImpAll(workload_set_full_addr, experiment_name_relative_addr, archColNum, trueNum)
            plotSimTimeVSblk(workload_set_full_addr, experiment_name_relative_addr, sysBlkNum, simColNum, trueNum)
            plotMoveGenTimeVSblk(workload_set_full_addr, experiment_name_relative_addr, sysBlkNum, movGenColNum, trueNum)
            plotRefDistToGoalVSitr(workload_set_full_addr, experiment_name_relative_addr, itrNum, refDistColNum, trueNum)
            plotSimTimeVSmoveNameZoneDist(workload_set_full_addr, experiment_name_relative_addr, zoneNum, movColNum, distColNum, simColNum, trueNum)
            plotMovGenTimeVSmoveNameZoneDist(workload_set_full_addr, experiment_name_relative_addr, zoneNum, movColNum, distColNum, movGenColNum, trueNum)
            plotSimTimeVScommCompZoneDist(workload_set_full_addr, experiment_name_relative_addr, zoneNum, commcompColNum, distColNum, simColNum, trueNum)
            plotMovGenTimeVScommCompZoneDist(workload_set_full_addr, experiment_name_relative_addr, zoneNum, commcompColNum, distColNum, movGenColNum, trueNum)
            plotSimTimeVShighLevelOptZoneDist(workload_set_full_addr, experiment_name_relative_addr, zoneNum, optColNum, distColNum, simColNum, trueNum)
            plotMovGenTimeVShighLevelOptZoneDist(workload_set_full_addr, experiment_name_relative_addr, zoneNum, optColNum, distColNum, movGenColNum, trueNum)
            plotSimTimeVSarchVarImpZoneDist(workload_set_full_addr, experiment_name_relative_addr, zoneNum, archColNum, distColNum, simColNum, trueNum)
            plotMovGenTimeVSarchVarImpZoneDist(workload_set_full_addr, experiment_name_relative_addr, zoneNum, archColNum, distColNum, movGenColNum, trueNum)
        """
