import pykeen
from pykeen.triples import TriplesFactory
from pykeen.datasets import PathDataset
import pandas as pd

def process_input(csvpath):
    if isinstance(csvpath, pd.DataFrame):
        return csvpath
    elif isinstance(csvpath, str):
        return pd.read_csv(csvpath)
    else:
        raise TypeError("Input must be a pandas DataFrame or a file path string")

def triple_factory_from_csv(csvpath):
    data = process_input(csvpath)
    if isinstance(csvpath, str):
        return TriplesFactory.from_path(csvpath, create_inverse_triples=False)
    else:
        return TriplesFactory.from_labeled_triples(data.values, create_inverse_triples=False)

"""
Saving dataset as triples factory

Args:
    csvpath_or_data: the file path of the dataset or a pandas DataFrame

Returns:
    triples factory dataset from csv path or DataFrame.
    create_inverse_triples(str): Either true or False the default is False
"""

def pykeen_dataset_from_csv(csvpath):
    if isinstance(csvpath, str):
        return PathDataset.from_path(csvpath)
    else:
        data = process_input(csvpath)
        return PathDataset(triples=data.values)

"""
Loading own dataset for grid search process

Args:
    csvpath_or_data: the file path of the dataset or a pandas DataFrame
Returns:
    PathDataset from csv path or DataFrame.  
"""

def train_test_val_split_from_csv(csvpath, splits_ratio=[0.8, 0.1, 0.1]):
    kg = triple_factory_from_csv(csvpath)
    train, test, val = kg.split(splits_ratio)
    return train, test, val

"""
The splitting process of dataset for training

Args:
    csvpath_or_data: the file path of the dataset or a pandas DataFrame
    splits_ratio: The splitting of 80,10,10 which is default.
Returns:
    test, train, val sets.  
"""

def data_process(csvpath, splits_ratio=[0.8, 0.1, 0.1]):
    # Load the dataset as a TriplesFactory
    triples_factory = triple_factory_from_csv(csvpath)
    
    # Load the dataset for grid search
    dataset = pykeen_dataset_from_csv(csvpath)
    
    # Split the dataset
    train, test, val = train_test_val_split_from_csv(csvpath, splits_ratio)
    
    return triples_factory, dataset, train, test, val

