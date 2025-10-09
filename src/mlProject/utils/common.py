import os
from box.exceptions import BoxValueError
import yaml
from mlProject import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations

def read_yaml(path_to_yaml:Path)->ConfigBox:
    """
    reads yaml file and returns
    args:
        path_to_yaml: path like input
    raises:
        ValueError: if yaml file is empty
        e: empty file
    returns:
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content=yaml.safe_load(yaml_file)
            logger.info(f"yaml file:{path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations

def create_directories(path_to_directories:list,verbose=True):
    """
    create list of directories
    
    args:
    path_to_directories: list of path of directories
    ignore_log(bool,optional): ignore if multiple directories are to be created. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f"created directory at:{path}")


@ensure_annotations
def save_json(path:Path,data:dict):
    """
    save dict as json file
    args:
        path: path to save json file
        data: data to be saved
    """
    with open(path,"w") as f:
        json.dump(data,f,indent=4)
    logger.info(f"json file saved at:{path}")

@ensure_annotations
def load_json(path:Path)->ConfigBox:
    """
    load json file and returns as ConfigBox
    args:
        path: path to load json file
    returns:
        ConfigBox:data as class attributes instead of dict
    """
    with open(path)as f:
        content=json.load(f)

    logger.info(f"json file loaded successfully from:{path}")
    return ConfigBox(content)
    
@ensure_annotations
def save_bin(data:Any,path:Path):
    """
    save binary file
    args:
        data: data to be saved
        path: path to save binary file
    """
    with open(path,"wb") as file_obj:
        joblib.dump(data,file_obj)
    logger.info(f"binary file saved at:{path}")

@ensure_annotations
def load_bin(path:Path)->Any:
    """
    load binary file
    args:
        path: path to load binary file
    returns:
        data: data loaded from binary file
    """
    with open(path,"rb") as file_obj:
        data=joblib.load(file_obj)
    logger.info(f"binary file loaded from:{path}")
    return data

@ensure_annotations
def get_size(path:Path)->str:
    """
    get size in KB
    args:
        path: path to the file
    returns:
        size: size of the file in KB
    """
    size_in_kb=round(os.path.getsize(path)/1024)
    return f"~{size_in_kb} KB"