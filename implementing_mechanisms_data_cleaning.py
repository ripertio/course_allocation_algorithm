# This Script allocates trainers and course seats based on the GT created by the script rawdata_to_GT.py

# Importing Moduls:
import json
from data_parsing_functions import *


if __name__ == '__main__':
    # ------------------------------------------------------------------------------------
    # Check if all required directory exists:
    check_create_dir(DATA_PATH)
    path_trainer_applications = check_create_dir(DATA_PATH, DIR_TRAINER_WISHES)
    path_data_analysis = check_create_dir(DATA_PATH, DIR_DATA_CLEANED_for_ANALYSIS)
    path_results = check_create_dir(RESULTS_PATH)

    #### DICT of all Trainer Applications:
    with open(f"{DATA_PATH}/trainer_applications.json", "r") as in_file:
        all_trainers = json.load(in_file)
    
    #### DICT of all courses:
    with open(f"{DATA_PATH}/all_courses_empty.json", "r") as in_file:
        all_empty_courses = json.load(in_file)
    
    
    #### DICT of MANUAL course Allocation:
    with open(f"{DATA_PATH}/manual_allocation.json", "r") as in_file:
        manu_allocation = json.load(in_file)

    ######### Applying all implemented allocation mechanisms with re-allocating several times
    rounds= 100
    best_allocation_threshold = 999
    overall_best_allocation = None
        
    lst_all_key_metrics = []
    list_all_sucess_rates = []
    ## Name , how many times repeating allocation , re permutate true/false, quota per pick, random application from interested trainers, random application from set of trainers
    for all_type in [("Random from applications", rounds, False, 1, True, False),
                    ("Serial Dictatorship", rounds,False, "ALL" ,False, False),
                    ("Round Robin", rounds, False, 5 ,False, False),
                    ("Round Robin", rounds, False, 2 ,False, False),
                    ("Round Robin", rounds, False, 1 ,False, False),                 
                    ("Round Robin", rounds, True, 1 ,False, False),
                    ]:
        ## Performing and cleaning all allocation mechanisms
        df_key_metrics, df_success_rate, best_allocation = repeat_allocation_return_df(all_trainers, all_empty_courses, all_type[0], all_type[1], re_permutate=all_type[2], quota_per_pick=all_type[3],random_from_applications=all_type[4], random_total=all_type[5])
        lst_all_key_metrics.append(df_key_metrics)
        list_all_sucess_rates.append(df_success_rate)
        print("The best allocation for the mechanisms ",best_allocation[0], f"yields to {coef_variation} of: ", best_allocation[1])
        if best_allocation[1] < best_allocation_threshold:
            overall_best_allocation = best_allocation
            best_allocation_threshold = best_allocation[1]
     
    ## Parsing manual Allocation to other allocations:
    manual_application_succcess_rate, manual_stats = dicts_to_application_success_rate_AND_key_metrics(all_trainers, manu_allocation)    
    manual_application_succcess_rate[allocation_type]  = "Manual Allocation"
    manual_stats = [manual_stats]
    df_manual_stats = pd.DataFrame(manual_stats, columns=[coef_variation, mean, stand_dev, name_ratio_filled_seats])
    df_manual_stats[allocation_type] = "Manual Allocation"

    lst_all_key_metrics.append(df_manual_stats)
    list_all_sucess_rates.append(manual_application_succcess_rate)

    # ------------------------------------------------------------------------------------
    # Combining clean dataframes of all allocation mechanisms
    all_key_metrics = pd.concat(lst_all_key_metrics, ignore_index = True)
    all_sucess_rates = pd.concat(list_all_sucess_rates, axis=0, ignore_index = True)

    # ------------------------------------------------------------------------------------
    # Saving cleaned dataframes to csv files
    all_key_metrics.to_csv(f"{path_data_analysis}/{name_key_metrics}", index = False)
    all_sucess_rates.to_csv(f"{path_data_analysis}/{name_all_success_rates}", index = False)

    # ------------------------------------------------------------------------------------
    # Storing best allocation as
    with open(f"{path_results}/best_allocation_with_{overall_best_allocation[0]}.json", "w") as outfile:
            json.dump(overall_best_allocation[3], outfile)
            print(f"All empty courses are parsed and stored in {DATA_PATH}/all_courses_empty.json")
    overall_best_allocation[2].to_csv(f"{path_results}/best_allocation_{app_success_rate}.csv", index = False)
    
    df_best_allo = dict_allocation_to_df(overall_best_allocation[3])
    df_best_allo.to_excel(f"{RESULTS_PATH}/Beste Einteilung.xlsx")
    
    print("\nDONE!")
    