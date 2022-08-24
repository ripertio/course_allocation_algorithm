# This Script establish the ground truth for this project analysis,
# it process the raw excel files from trainers and empty courses into two json files 
# (all_courses_empty.json // trainer_applications.json)

# Importing Moduls:
import glob
import regex
import json
from data_parsing_functions import *

if __name__ == '__main__':
    # ------------------------------------------------------------------------------------
    # Check if all required directory exists:
    check_create_dir(DATA_PATH)
    path_trainer_applications = check_create_dir(DATA_PATH, DIR_TRAINER_WISHES)    
    
    # ------------------------------------------------------------------------------------
    # Parsing Raw Excel files to JSON - GROUND TRUTH:
    parsing_trainer_applications = input("Do you want to parse trainers application and empty courses and store them as json file? \nif YES enter Y/y \nif not enter any other key: ")
    if parsing_trainer_applications.lower() in ["y", "yes"]:
        ALL_trainers_applications = []
        trainer_files = glob.glob(path_trainer_applications+"/*")

        for i in trainer_files:
            trainer_name_file = regex.sub(rf"^{path_trainer_applications}/","",i)
            trainer_name = regex.sub(r".xlsx","",trainer_name_file)
            trainer_dic = trainer_app_excel_to_dict(path_trainer_applications, trainer_name)
            ALL_trainers_applications.append(trainer_dic)
        
        with open(f"{DATA_PATH}/trainer_applications.json", "w") as outfile:
            json.dump(ALL_trainers_applications, outfile)
        print(f"All Trainer Applications are parsed and stored in {DATA_PATH}/trainer_applications.json")  

        empty_courses = trainer_app_excel_to_dict("./data")
        with open(f"{DATA_PATH}/all_courses_empty.json", "w") as outfile:
            json.dump(empty_courses, outfile)
            print(f"All empty courses are parsed and stored in {DATA_PATH}/all_courses_empty.json")  
    else:
        print("NO raw excel files are parsed")
        