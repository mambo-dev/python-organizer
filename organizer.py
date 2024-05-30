import os
import shutil


ORGANIZED_TARGET= "organized"
FROM = "documents"
storage_directories = ["registration list", "list of served", "caseplan served"]

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def initialize_directories(path):
    for directory in storage_directories:
        dir_path = os.path.join(path,directory)
        create_dir(dir_path)

    return True

def sort_document_paths(path):
    reg_list_paths = []
    list_served_paths = []
    caseplan_served_paths = []
  
    for root,dirs,files in os.walk(path):
        for file in files:
            if "registrationlist" in file.lower():
                reg_list_paths.append(file)
            elif "listofovcserved" in file.lower():
                list_served_paths.append(file)
            elif "caseplan" in file.lower():
                caseplan_served_paths.append(file)
            else:
                raise Exception("Something went wrong could not sort documents")
        break
  
    return reg_list_paths, list_served_paths, caseplan_served_paths


def move_document_to_organized(organized_path, documents_path):
    reg_list_paths, list_served_paths, caseplan_served_paths = sort_document_paths(documents_path) 
    copy_to_organized(reg_list_paths,storage_directories[0],organized_path, documents_path)
    copy_to_organized(list_served_paths,storage_directories[1],organized_path, documents_path)
    copy_to_organized(caseplan_served_paths,storage_directories[2],organized_path, documents_path)
    return True

  

def copy_to_organized(files, storage_dir_name, organized_path, documents_path):
    path_to_store = os.path.join(organized_path, storage_dir_name)
    for file in files:
        source = os.path.join(documents_path, file)
        dest = os.path.join(path_to_store,file)
        if not os.path.exists(dest):
            shutil.copy(source, path_to_store)




def main():
    cwd = os.getcwd()
    organized_path = os.path.join(cwd,"organized")
    documents_path = os.path.join(cwd,"documents")
    initialize_directories(organized_path)
    move_document_to_organized(organized_path, documents_path)
if __name__ == "__main__":
    main()

