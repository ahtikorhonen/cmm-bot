import json
from pathlib import Path


def read_json(file_name: str) -> dict:
    """
    Read json file to Python dict.
    :file_name (str): name of the json file to be read
    :return (dict): the json file as a python dict
    """
    path = Path().cwd().joinpath("config", f"{file_name}.json")
    try:
        with open(path, "r") as f:
            config = json.load(f)
            
            return config
        
    except Exception as e:
        raise Exception(f"Failed to read {file_name} - {str(e)}")