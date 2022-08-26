from aiohttp import BadContentDispositionParam
import pandas as pd
import numpy as np
import random
import copy
import os 


### Name Definitions!!
DATA_PATH = "data"
DIR_TRAINER_WISHES = "trainer_files"
DIR_DATA_CLEANED_for_ANALYSIS = "data_for_analysis"
name_key_metrics = "all_key_metrics_from_all_allocations.csv"
name_all_success_rates = "all_success_rates_from_all_allocations.csv"
RESULTS_PATH = "results"
id = "ID"
start = "Start"
end = "End"
duration = "Duration"
prio_application = "Prio Application"
course_class = "Course_type"
client = "Client"
pay_rate = "Pay Rate"
number_trainers_required = "Number Trainers Required"
number_asigned_trainers = "Number Assigned Trainers"
app_success_rate = "Application Success Rate"
application = "Application"
assigned = "Assigned"
wait_list = "Wait list"
app_success_rate = "Application Success Rate"
mean = "Mean"
stand_dev = "Standard Deviation"
coef_variation = "Coefficient of Variation"
name_ratio_filled_seats = "Ratio of Assigned CourseSeats"
allocation_type = "Allocation Type"


## Function for checking and creating directory:
def check_create_dir (*a_path):
    """Thus function checks if a specific directory existis and if not it is created

    Returns:
        str: a directory in the working directory
    """
    try:
        path_exist = os.path.join("./", a_path[0], a_path[1])
    except:
        path_exist = os.path.join("./", a_path[0])
    data_analysis_dir_exists = os.path.exists(path_exist)
    if data_analysis_dir_exists:
        print(f"\nThe path {path_exist} exists")
    else:
        os.mkdir(path_exist)
        print(f"\nThe path {path_exist} did not exist and was created")
    return path_exist

# Data Processing
def trainer_app_excel_to_dict (a_path, a_name = None):
    """This function convertes all trainer excel or if a_name == None the empty course files that are structured in a specific and equal way into a json file

    Args:
        a_path (str): The path of the directory of all trainer files 
        a_name (str, optional): the name of the file without the ending.

    Returns:
        dic: A dictionary containing all trainers and their preferences. 
    """
    column_names = [id, start, end, course_class, client, pay_rate, number_trainers_required]
    if a_name == None:
        try:
            excel_df = pd.read_excel(f"{a_path}/All_courses_empty.xlsx")
        except:
            print(f"{a_path}/All_courses_empty.xlsx Does not exist pls check in the {a_path} directory")
        excel_df[assigned] = np.empty((len(excel_df),0)).tolist()
        excel_df[wait_list] = np.empty((len(excel_df),0)).tolist()
        excel_df[number_asigned_trainers] = 0
        column_names.append(number_asigned_trainers)
        column_names.append(assigned)
        column_names.append(wait_list)
        
    else:
        excel_df = pd.read_excel(f"{a_path}/{a_name}.xlsx")
        excel_df = excel_df.rename(columns= {"id": id, "start": start, "end": end, "course_type": course_class, "client": client, "pay_rate": pay_rate, "number_trainers_required": number_trainers_required, "application": application})

        column_names.append(application)
    excel_df = excel_df.rename(columns= {"Hotelbuchungsnummer": id, "Beginn": start, "Ende": end, "Bildungsprogramm": course_class, "Gruppe": client, "Tagessatz": pay_rate, "Benötigte Trainer": number_trainers_required, "Wunsch": application})
    updated_df = excel_df.copy()
    
    
    #Renaming the columns
    updated_df = updated_df[column_names]
    updated_df = updated_df.dropna(subset=[pay_rate])
    # Only parsing rows where trainer is interested in the course
    if a_name != None:
        updated_df = updated_df.dropna(subset=[application, pay_rate])
        # only neede if no prio_application submitted
        updated_df = updated_df.sample(frac=1)
        updated_df.reset_index(inplace=True, drop=True)
        updated_df[prio_application] = updated_df.index+1
    updated_df[duration] = (pd.to_datetime(updated_df[end]) - pd.to_datetime(updated_df[start])).dt.days +1
    try:
        updated_df[end] = updated_df[end].dt.strftime('%Y-%m-%d')
        updated_df[start] = updated_df[start].dt.strftime('%Y-%m-%d')
    except:
        pass
    
    
    
    if a_name == None:
        updated_df.set_index(id, inplace=True, drop=True)
        trainer_dic = updated_df.to_dict(orient= "index")
        return trainer_dic
    else:
        trainer_dic = updated_df.to_dict(orient= "records")
        return {"name": a_name, "pick_order": [], "courses": trainer_dic}

############################################################
### Function -> applying different allocation mechanisms  ####
############################################################ 

def applying_allocation_mechanism(trainer_dict, all_courses_dict, a_name, re_permutate = False, quota_per_pick = 1, random_from_applications = False, random_total = False):
    """This function implements different allocation mechanisms and returns two dictionaries one containg the allocation from the course side (dic of assigned trainers) and from trainers side - (dic of trainers and allocated courses)

    Args:
        trainer_dict (dic): a dictionary of all trainers applications (from function:trainer_app_excel_to_dict )
        all_courses_dict (dic): a dictionary of all empty courses (from function:trainer_app_excel_to_dict )
        a_name (str): a name that is moved through the function
        re_permutate (bool, optional): Specifing if the order of trainers is repermutated after each picking round. Defaults to False.
        quota_per_pick (int, optional): Number of courses that can be picked in each round. Defaults to 1.
        random_from_applications (bool, optional): If True -> allocationg from " course side" picking as much trainers as required from all trainers that applied for this course . Defaults to False.
        random_total (bool, optional): If True -> allocationg from " course side" picking as much trainers as required from all trainers in trainers dic. Defaults to False.

    Returns:
        dic: two dictionaries (dic of assigned trainers) (dic of trainers and allocated courses)
    """
    a_trainer_dict = copy.deepcopy(trainer_dict)
    a_all_courses_dict = copy.deepcopy(all_courses_dict)
    
    counter = None
    random.shuffle(a_trainer_dict) #random permutation of the picking order 
    while counter != 0:
        counter = 0
        for pick_order, trainer in enumerate(a_trainer_dict):
            trainer["pick_order"].append(pick_order+1)

            if random_from_applications == True or random_total == True:  # Allocation from course side perspective 
                for wanted_course in trainer["courses"]:
                    course = wanted_course[id]
                    if assigned not in wanted_course.keys():
                        wanted_course[assigned] = "No"
                    ## Assigning all to waitlist
                    if wanted_course[assigned] == "No":
                        counter += 1
                        a_all_courses_dict[course][wait_list].append(trainer["name"])
                        wanted_course[assigned] = wait_list
                
            elif random_from_applications == False and random_total == False:
                lowest_prio = 999
                prefered_course = None
                
                # Serial Dictatorship: all preferences of a trainer are assigned at once
                if quota_per_pick == "ALL": 
                    for wanted_course in trainer["courses"]:
                        course = wanted_course[id]
                        if assigned not in wanted_course.keys():
                            wanted_course[assigned] = "No"
                        ## Conditions for assining the most prefered course
                        if wanted_course[assigned] == "No":
                            if a_all_courses_dict[course][number_trainers_required] > a_all_courses_dict[course][number_asigned_trainers]:
                                a_all_courses_dict[course][assigned].append(trainer["name"])
                                wanted_course[assigned] = "Yes"
                                a_all_courses_dict[course][number_asigned_trainers] += 1
                            else:
                                a_all_courses_dict[course][wait_list].append(trainer["name"])
                                wanted_course[assigned] = wait_list
                else:
                    ## Round Robin implementation 
                    for i in range(quota_per_pick): # With different quotas, if 1 -> classical Round Robin
                        for wanted_course in trainer["courses"]:
                            if assigned not in wanted_course.keys():
                                wanted_course[assigned] = "No"
                            ## Conditions for assining the most prefered course
                            if wanted_course[assigned] == "No":
                                counter +=1
                            if wanted_course[prio_application] <= lowest_prio and wanted_course[assigned] == "No":
                                lowest_prio = wanted_course[prio_application]
                                prefered_course = wanted_course
                            if lowest_prio == 999:
                                continue      
                        if prefered_course != None:# and a_all_courses_dict[course]:
                            ## Assigning the trainer to the prefered course or Waitlist
                            course = prefered_course[id]
                            if a_all_courses_dict[course][number_trainers_required] > a_all_courses_dict[course][number_asigned_trainers]:
                                a_all_courses_dict[course][assigned].append(trainer["name"])
                                prefered_course[assigned] = "Yes"
                                a_all_courses_dict[course][number_asigned_trainers] += 1
                            else:
                                a_all_courses_dict[course][wait_list].append(trainer["name"])
                                prefered_course[assigned] = wait_list
                        prefered_course = None
                        lowest_prio = 999
                    
        if re_permutate == True:
            random.shuffle(a_trainer_dict) #re-permutate the picking order 
    
    ## Allocation from course side perspective 
    # Random from trainers who applied for the course
    if random_from_applications == True and random_total == False: 
        for each_course in a_all_courses_dict:
            course = a_all_courses_dict[each_course]
            interest = course[wait_list]
            random.shuffle(interest)
            needed_trainer = int(course[number_trainers_required])
            for i in range(needed_trainer):
                try:
                    course[assigned].append(interest[i])
                    course[number_asigned_trainers] += 1
                except:
                    pass
    
    # Total Random from all possible trainers
    elif random_total == True and random_from_applications == False:
        for each_course in a_all_courses_dict:
            course = a_all_courses_dict[each_course]
            pot_interest = [x["name"] for x in a_trainer_dict]
            random.shuffle(pot_interest)
            needed_trainer = int(course[number_trainers_required])
            for i in range(needed_trainer):
                if pot_interest[i] in course[wait_list]:
                    course[assigned].append(pot_interest[i])
                    course[number_asigned_trainers] += 1
                else:
                    pass
    elif random_total == True and random_from_applications == True:
        print("This specification is not possilble check the arguments of  random_total and random_from_applications must no be both TRUE")
    
    ## Returning overall picking order the smaller the number the earlier you were involved in the picking order
    for trainer in a_trainer_dict:
        trainer["pick_order"] = sum(trainer["pick_order"])/len(trainer["pick_order"])
    return a_trainer_dict, a_all_courses_dict



## Converting Trainersapplications -> to dataframe
def dict_trainer_to_df(a_dict):
    """This function converts a trainers dic to an pandas dataframe

    Args:
        a_dict (dic): dic from function: applying_allocation_mechanism

    Returns:
        dataframe: A dataframe of trainers applications and assignments
    """
    try:
        trainer_df = pd.json_normalize(a_dict, "courses", ["name", "pick_order"])
    except:
        trainer_df = pd.json_normalize(a_dict, "courses", ["name"])
    return trainer_df

def dict_allocation_to_df (a_dict):
    """Thus function converts a course dic to an pandas dataframe

    Args:
        a_dict (dic): dic from function: applying_allocation_mechanism

    Returns:
        dataframe: A dataframe of courses wheres assigned column is a list
    """
    df = pd.DataFrame.from_dict(a_dict, orient="index")
    return df

def df_with_lst_to_sep_rows (a_df, a_column):
    """Thus function extents an column with list as values into separate rows

    Args:
        a_df (dataframe): a dataframe from the function dict_allocation_to_df
        a_column (str): name of the column

    Returns:
        dataframe: a dataframe with separate rows for each element of a list of a column 
    """
    exploded_df = a_df.copy()
    exploded_df = exploded_df.explode(a_column)
    return exploded_df

def df_application_success_per_trainer (a_trainer_df, a_allocation_df):
    """this functions calculates the application success rate for each trainer of an allocation

    Args:
        a_trainer_df (dataframe): a dataframe from the function: dict_trainer_to_df
        a_allocation_df (dataframe ):a dataframe from the function: df_with_lst_to_sep_rows

    Returns:
        dataframe: containing the application success rate for each trainer of the allocation
    """
    try:
        trainer_sum = a_trainer_df.groupby("name").agg({"pick_order": "mean", pay_rate: "mean", duration: "sum", application: "count"})
    except:
        trainer_sum = a_trainer_df.groupby("name").agg({pay_rate: "mean", duration: "sum", application: "count"})

    trainer_sum = trainer_sum.add_prefix("applied_")
    trainer_group_assigned = a_allocation_df.groupby(assigned).agg({pay_rate: "mean", duration: "sum", assigned: "count"})
    combined_df = pd.concat([trainer_sum, trainer_group_assigned], axis=1)
    combined_df = combined_df.fillna(0)
    combined_df[app_success_rate] = combined_df[assigned]/combined_df[f"applied_{application}"]
    return combined_df

def dicts_to_application_success_rate_AND_key_metrics (a_trainer_dict, a_allocation_dict):
    """combining the different functions from trainers, allocation dict to dataframes in one step and calculates the key metrics for the research project 

    Args:
        a_trainer_df (dataframe): a dataframe from the function: dict_trainer_to_df
        a_allocation_df (dataframe ):a dataframe from the function: df_with_lst_to_sep_rows

    Returns:
        tuple: dataframe with application success rate for each trainer and tuple with coefficient of variation, mean, standard deviation and ratio of assigned course seats of the respective allocation) 
    """
    trainer_df = dict_trainer_to_df(a_trainer_dict)
    alloc_df = dict_allocation_to_df(a_allocation_dict)
    if number_asigned_trainers not in alloc_df.columns:
        alloc_df[number_asigned_trainers] = alloc_df[assigned].str.len()
    sum_required_trainers = alloc_df[number_trainers_required].sum()
    sum_filled_course_seats = alloc_df[number_asigned_trainers].sum()
    ratio_filled_seats = sum_filled_course_seats / sum_required_trainers
    alloc_explod = df_with_lst_to_sep_rows(alloc_df, assigned)
    trainer_success_rate_df = df_application_success_per_trainer(trainer_df, alloc_explod)
    mean, std = (trainer_success_rate_df[app_success_rate].mean(), trainer_success_rate_df[app_success_rate].std())
    coef_of_varia = std/mean
    return trainer_success_rate_df, (coef_of_varia, mean, std, ratio_filled_seats)
        

def repeat_allocation_return_df (trainer_dict, empty_course_dict, name_of_mechanism, num_allocations = 100 ,re_permutate=False, quota_per_pick = 1, random_from_applications = False, random_total = False):
    """This function combines all the implementing and cleaning functions from abaove in one step, furthermore it integrates the possiblity the repeat the allocation as often as wanted 

    Args:
        trainer_dict (dic): a dictionary of all trainers applications (from function:trainer_app_excel_to_dict )
        all_courses_dict (dic): a dictionary of all empty courses (from function:trainer_app_excel_to_dict )
        name_of_mechanism (str): a name that is moved through the function
        num_allocations (int): the number of times the allocation is to be repeated
        re_permutate (bool, optional): Specifing if the order of trainers is repermutated after each picking round. Defaults to False.
        quota_per_pick (int, optional): Number of courses that can be picked in each round. Defaults to 1.
        random_from_applications (bool, optional): If True -> allocationg from " course side" picking as much trainers as required from all trainers that applied for this course . Defaults to False.
        random_total (bool, optional): If True -> allocationg from " course side" picking as much trainers as required from all trainers in trainers dic. Defaults to False.

    Returns:
        a dataframe of all keymetrics of all allocation of this type of allocation 
        // a dataframe of all application success rates for all allocations 
        // the most efficiant allocaiton of this time (measured by the coefficient of variation)   (name of allocation, coef_variation, dataframe of application success rate, allocation as dict)
    """
    best_allocation_threshold = 999
    best_allocation = None
    
    finding_optimum_lst = []
    df_sucess_rate_lst = []
    for i in range(num_allocations):
        trainers, course_all = applying_allocation_mechanism(trainer_dict, empty_course_dict, name_of_mechanism, re_permutate=re_permutate, quota_per_pick = quota_per_pick, random_from_applications = random_from_applications, random_total = random_total)
        tmp_df , tmp_key_metrics = dicts_to_application_success_rate_AND_key_metrics(trainers, course_all)
        tmp_df.reset_index(inplace=True)
        if tmp_key_metrics[0] < best_allocation_threshold:
            best_allocation = [tmp_key_metrics[0], tmp_df, course_all]
            best_allocation_threshold = tmp_key_metrics[0]
        finding_optimum_lst.append(tmp_key_metrics)
        df_sucess_rate_lst.append(tmp_df)
    df_optimum = pd.DataFrame(finding_optimum_lst, columns=[coef_variation, mean, stand_dev, name_ratio_filled_seats])
    
    df_all_app_success_rates =  pd.concat(df_sucess_rate_lst, ignore_index = True)
    if quota_per_pick == 1:
        quota = ""
    elif quota_per_pick == "ALL":
        quota = " Picking all at once"
    else:
        quota = f" Quota {str(quota_per_pick)}"
    if re_permutate == False:
        re_perm = ""
    elif re_permutate == True and quota_per_pick == "ALL":
        re_perm = ""
    elif re_permutate == True:
        re_perm = " re-permutated"
    df_all_app_success_rates[allocation_type] = f"{name_of_mechanism}{re_perm}{quota}"
    df_optimum[allocation_type] = f"{name_of_mechanism}{re_perm}{quota}"
    best_allocation.insert(0, f"{name_of_mechanism}{re_perm}{quota}")
    return df_optimum, df_all_app_success_rates, best_allocation

def stand_df(a_df, a_name_colum=None):
    """Thus function standardizes an dataframe (mean = 0) if value > +/-1 --> value more than 1std from mean away 

    Args:
        a_df (dataframe): a dataframe
        a_name_colum (str, optional): Name of column to standardize . Defaults to None.

    Returns:
        dataframe: df with standardized values
    """

    vnames = [name for name in globals() if globals()[name] is a_df]
    #Normalizing data 
    print(f"Standardizing the dataframe {vnames}")
    stand_df = a_df.copy()
    for name in a_df:
        if name == a_name_colum:
            continue
        stand_df[name] = (a_df[name] - stand_df[name].mean())/stand_df[name].std()
    return stand_df
