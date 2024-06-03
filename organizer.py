import os
import shutil
from datetime import datetime


ORGANIZED_TARGET= "organized"
FROM = "documents"
storage_directories = ["registration list", "list of served", "caseplan served", "caregivers served"]

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def initialize_directories(path):
    if not os.path.exists(path):
        os.mkdir(path)

    for directory in storage_directories:
        dir_path = os.path.join(path,directory)
        create_dir(dir_path)

    return True

def sort_document_paths(path):
    reg_list_paths = []
    list_served_paths = []
    caseplan_served_paths = []
    caregiver_served_paths = []
  
    for root,dirs,files in os.walk(path):
        for file in files:
            if "registration-list" in file.lower():
                reg_list_paths.append(file)
            elif "ovc-served" in file.lower():
                list_served_paths.append(file)
            elif "caseplan-list" in file.lower():
                caseplan_served_paths.append(file)
            elif "caregivers-list" in file.lower():
                caregiver_served_paths.append(file)
            else:
                raise Exception("Something went wrong could not sort documents")
        break
  
    return reg_list_paths, list_served_paths, caseplan_served_paths, caregiver_served_paths


def move_document_to_organized(organized_path, documents_path):
    reg_list_paths, list_served_paths, caseplan_served_paths, caregiver_served_paths = sort_document_paths(documents_path) 
    copy_to_organized(reg_list_paths,storage_directories[0],organized_path, documents_path)
    copy_to_organized(list_served_paths,storage_directories[1],organized_path, documents_path)
    copy_to_organized(caseplan_served_paths,storage_directories[2],organized_path, documents_path)
    copy_to_organized(caregiver_served_paths,storage_directories[3],organized_path, documents_path)
    return True

  

def copy_to_organized(files, storage_dir_name, organized_path, documents_path):
    path_to_store = os.path.join(organized_path, storage_dir_name)
    for file in files:
        source = os.path.join(documents_path, file)
        dest = os.path.join(path_to_store,file)
        if not os.path.exists(dest):
            shutil.copy(source, path_to_store)

def change_file_name(file_path, new_file_path):
    try:
        os.rename(file_path, new_file_path)
    except FileNotFoundError as e:
        print(e)
        raise Exception("FILE does not exist")

def update_file_names(document_path):
    path_dictionary = {}
    for root, dirs, files in os.walk(document_path):
        for file in files:
            correct_format = False
            if  "registration-list" in file.lower() or "caseplan-list" in file.lower() or "ovc-served" in file.lower() or "caregivers-list" in file.lower():
                correct_format = True
            
            if not correct_format:
                file_name_split = file.split("-")[1].split(".")
                timestamp = file_name_split[1].split(" ")
                if(len(timestamp) == 1):
                    timestamp = timestamp[0]
                else:
                    timestamp = timestamp[0]
                date = datetime.fromtimestamp(int(timestamp)).date()
                
                if "registrationlist" in file.lower():
                    new_file_name = f"registration-list-{date}"
                    change_file_name(os.path.join(document_path, file), os.path.join(document_path,new_file_name))
                elif "listofovcserved" in file.lower():
                    new_file_name = f"ovc-served-{date}"
                    change_file_name(os.path.join(document_path, file), os.path.join(document_path,new_file_name))
                elif "caseplan" in file.lower():
                    new_file_name = f"caseplan-list-{date}"
                    change_file_name(os.path.join(document_path, file), os.path.join(document_path,new_file_name))
                elif "caregivers" in file.lower():
                    new_file_name = f"caregivers-list-{date}"
                    change_file_name(os.path.join(document_path, file), os.path.join(document_path,new_file_name))
                else:
                    raise Exception("Invalid file name")



def main():
    cwd = os.getcwd()
    organized_path = os.path.join(cwd,"organized")
    documents_path = os.path.join(cwd,"documents")
    update_file_names(documents_path)
    initialize_directories(organized_path)
    move_document_to_organized(organized_path, documents_path)

if __name__ == "__main__":
    main()

