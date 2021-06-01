#Copyright (c) Facebook, Inc. and its affiliates.
#This source code is licensed under the MIT license found in the
#LICENSE file in the root directory of this source tree.

from specs.LW_cl import *
from specs.parse_libraries.parse_library import  *


# -----------
# Functionality:
#      split tasks to what can run in parallel and
#      what should run in serial
# Variables:
#      task_name_intensity_type: list of tuples : (task name, intensity (memory intensive, comp intensive))
# -----------
def cluster_tasks(task_name_intensity_type, avg_parallelism):
    task_names = [task_name for task_name, intensity in task_name_intensity_type]
    task_name_position = []
    state = "par"
    pos_ctr = 0
    state_ctr = avg_parallelism
    for idx, task in enumerate(task_names):
        if state == "par" and state_ctr > 0:
            state_ctr -= 1
        elif state == "par" and state_ctr == 0:
            state = "ser"
            pos_ctr += 1
        elif state == "ser":
            state = "par"
            state_ctr = avg_parallelism
            state_ctr -= 1
            pos_ctr += 1
        task_name_position.append((task, pos_ctr))
    return task_name_position


# -----------
# Functionality:
#      generate synthetic work (instructions, bytes) for tasks
# Variables:
#      task_name_intensity_type: list of tuples : (task name, intensity (memory intensive, comp intensive))
# -----------
def generate_synthetic_work(task_exec_intensity_type):
    general_task_type_char = {}
    general_task_type_char["memory_intensive"] = {}
    general_task_type_char["comp_intensive"] = {}
    general_task_type_char["memory_intensive"]["exec"] = 50000
    general_task_type_char["comp_intensive"]["exec"] = 10000000
    work_dict = {}
    for task, intensity in task_exec_intensity_type:
        if "siink" in task or "souurce" in task:
            work_dict[task] = 0
        else:
            work_dict[task] = general_task_type_char[intensity]["exec"]

    return work_dict


# -----------
# Functionality:
#      generate synthetic datamovement between tasks
# Variables:
#      task_exec_intensity_type: memory or computational intensive
#      average number of tasks that can run in parallel
# -----------
def generate_synthetic_datamovement(task_exec_intensity_type, avg_parallelism):
    # hardcoded data.
    # TODO: move these into a config file later
    general_task_type_char = {}
    general_task_type_char["memory_intensive"] = {}
    general_task_type_char["comp_intensive"] = {}
    general_task_type_char["memory_intensive"]["read_bytes"] = 100000
    general_task_type_char["memory_intensive"]["write_bytes"] = 100000 # hardcoded, delete later
    general_task_type_char["comp_intensive"]["read_bytes"] = 100
    general_task_type_char["comp_intensive"]["write_bytes"] = 100

    general_task_type_char["memory_intensive"]["exec"] = 100
    general_task_type_char["comp_intensive"]["exec"] = 10000000

    # find a family task (parent, child or sibiling)
    def find_family(task_name_position, task_name, relationship):
        task_position = [position for task, position in task_name_position if task == task_name][0]
        if relationship == "parent":
            parents = [task_name for task_name, position in task_name_position if position ==(task_position -1)]
            return parents
        elif relationship == "child":
            children = [task_name for task_name, position in task_name_position if position ==(task_position +1)]
            return children
        else:
            print('relationsihp ' + relationship + " is not defined")
            exit(0)



    data_movement = {}
    task_name_position = cluster_tasks(task_exec_intensity_type, avg_parallelism)
    task_name_position.insert(0,("synthetic_souurce", -1))
    task_name_position.append(("synthetic_siink", max([pos for el, pos in task_name_position])+1))
    task_exec_intensity_type.insert(0, ("synthetic_souurce", (task_exec_intensity_type[0])[1]))
    task_exec_intensity_type.append(("synthetic_siink", task_exec_intensity_type[0][1]))

    for task,_ in task_name_position:
        data_movement[task] = {}
        tasks_parents = find_family(task_name_position, task, "parent")
        tasks_children = find_family(task_name_position, task, "child")
        for child in tasks_children:
            exec_intensity = [intensity  for task_, intensity in task_exec_intensity_type if task_== task][0]
            #if child == "synthetic_siink":  # hardcoded delete later
            #    data_movement[task][child] = 1
            #else:
            data_movement[task][child] = general_task_type_char[exec_intensity]["write_bytes"]

    return data_movement


# we generate very simple scenarios for now.
def generate_synthetic_task_graphs(num_of_tasks, avg_parallelism, exec_intensity):
    assert(num_of_tasks > avg_parallelism)

    tasksL: List[TaskL] = []

    # generate a list of task names and their exec intensity (i.e., compute or memory intensive)
    task_exec_intensity = []
    for idx in range(0, num_of_tasks - 2):
        task_exec_intensity.append(("synthetic_"+str(idx), exec_intensity))

    # collect data movement data
    task_graph_dict = generate_synthetic_datamovement(task_exec_intensity, avg_parallelism)

    # collect number of instructions for each tasks
    work_dict = generate_synthetic_work(task_exec_intensity)

    for task_name_, values in task_graph_dict.items():
        task_ = TaskL(task_name=task_name_, work=work_dict[task_name_])
        task_.add_task_work_distribution([(work_dict[task_name_], 1)])
        tasksL.append(task_)

    for task_name_, values in task_graph_dict.items():
        task_ = [taskL for taskL in tasksL if taskL.task_name == task_name_][0]
        for child_task_name, data_movement in values.items():
            child_task = [taskL for taskL in tasksL if taskL.task_name == child_task_name][0]
            task_.add_child(child_task, data_movement, "real")  # eye_tracking_soource t glint_mapping
            task_.add_task_to_child_work_distribution(child_task, [(data_movement, 1)])  # eye_tracking_soource t glint_mapping

    return tasksL,task_graph_dict, work_dict

# generate a synthetic hardware library to generate systems from
def generate_synthetic_hardware_library(task_work_dict, library_dir, Block_char_file_name):

    blocksL: List[BlockL] = []  # collection of all the blocks
    pe_mapsL: List[TaskToPEBlockMapL] = []
    pe_schedulesL: List[TaskScheduleL] = []

    gpps = parse_block_based_on_types(library_dir, Block_char_file_name, ("pe", "gpp"))
    gpp_names = list(gpps.keys())
    mems = parse_block_based_on_types(library_dir, Block_char_file_name, ("mem", "mem"))
    ics  = parse_block_based_on_types(library_dir, Block_char_file_name, ("ic", "ic"))


    hardware_library_dict = {}
    for task_name in task_work_dict.keys():
        for IP_name in gpp_names:
            if IP_name in hardware_library_dict.keys():
                hardware_library_dict[IP_name]["mappable_tasks"].append(task_name)
                continue
            hardware_library_dict[IP_name] = {}
            if IP_name in gpps:
                hardware_library_dict[IP_name]["work_rate"] = float(gpps[IP_name]['Freq'])*float(gpps[IP_name]["dhrystone_IPC"])
                hardware_library_dict[IP_name]["work_over_energy"] = float(gpps[IP_name]['Inst_per_joul'])
                hardware_library_dict[IP_name]["work_over_area"] = 1/float(gpps[IP_name]['Gpp_area'])
                hardware_library_dict[IP_name]["mappable_tasks"] = [task_name]
                hardware_library_dict[IP_name]["type"] = "pe"
                hardware_library_dict[IP_name]["sub_type"] = "gpp"
                #print("taskname: " + str(task_name) + ", subtype: gpp, power is"+ str(hardware_library_dict[IP_name]["work_rate"]/hardware_library_dict[IP_name]["work_over_energy"] ))

    for blck_name, blck_value in mems.items():
        hardware_library_dict[blck_value['Name']] = {}
        hardware_library_dict[blck_value['Name']]["work_rate"] = float(blck_value['BitWidth'])*float(blck_value['Freq'])
        hardware_library_dict[blck_value['Name']]["work_over_energy"] = float(blck_value['Byte_per_joul'])
        hardware_library_dict[blck_value['Name']]["work_over_area"] =  float(blck_value['Byte_per_m'])
        hardware_library_dict[blck_value['Name']]["mappable_tasks"] = 'all'
        hardware_library_dict[blck_value['Name']]["type"] = "mem"
        hardware_library_dict[blck_value['Name']]["sub_type"] = "mem"

    for blck_name, blck_value in ics.items():
        hardware_library_dict[blck_value['Name']] = {}
        hardware_library_dict[blck_value['Name']]["work_rate"] = float(blck_value['BitWidth'])*float(blck_value['Freq'])
        hardware_library_dict[blck_value['Name']]["work_over_energy"] = float(blck_value['Byte_per_joul'])
        hardware_library_dict[blck_value['Name']]["work_over_area"] =  float(blck_value['Byte_per_m'])
        hardware_library_dict[blck_value['Name']]["mappable_tasks"] = 'all'
        hardware_library_dict[blck_value['Name']]["type"] = "ic"
        hardware_library_dict[blck_value['Name']]["sub_type"] = "ic"


    block_suptype = "gpp"  # default.
    for IP_name, values in hardware_library_dict.items():
        block_subtype = values['sub_type']
        block_type = values['type']
        blocksL.append(
            BlockL(block_instance_name=IP_name, block_type=block_type, block_subtype=block_subtype,
                   peak_work_rate_distribution = {hardware_library_dict[IP_name]["work_rate"]:1},
                   work_over_energy_distribution = {hardware_library_dict[IP_name]["work_over_energy"]:1},
                   work_over_area_distribution = {hardware_library_dict[IP_name]["work_over_area"]:1},
                   one_over_area_distribution = {1/hardware_library_dict[IP_name]["work_over_area"]:1}))

        if block_type == "pe":
            for mappable_tasks in hardware_library_dict[IP_name]["mappable_tasks"]:
                task_to_block_map_ = TaskToPEBlockMapL(task_name=mappable_tasks, pe_block_instance_name=IP_name)
                pe_mapsL.append(task_to_block_map_)

    return blocksL, pe_mapsL, pe_schedulesL