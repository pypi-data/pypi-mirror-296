import pykeen
from pykeen.triples import TriplesFactory
from pykeen.datasets import PathDataset
import torch
import pandas as pd



#print(torch.cuda.is_available())


def triple_factory_from_csv(csvpath):
    if isinstance(csvpath, pd.DataFrame):
        # If csvpath is a DataFrame, convert it to triples
        triples = csvpath.values.tolist()
        return TriplesFactory.from_labeled_triples(triples, create_inverse_triples=False)
    else:
        # If csvpath is a string (file path), use the original method
        return TriplesFactory.from_path(csvpath, create_inverse_triples=False)

def train_test_val_split_from_csv(csvpath, splits_ratio=[0.8, 0.1, 0.1]):
    kg = triple_factory_from_csv(csvpath)
    train, test, val = kg.split(splits_ratio)
    return train, test, val

def pykeen_dataset_from_csv(csvpath):
    if isinstance(csvpath, pd.DataFrame):
        # If csvpath is a DataFrame, create a dataset from triples
        triples = csvpath.values.tolist()
        return Dataset(triples=triples)
    else:
        # If csvpath is a string (file path), use the original method
        return PathDataset.from_path(csvpath)

def data_process(csvpath, splits_ratio=[0.8, 0.1, 0.1]):
    # Load the dataset as a TriplesFactory
    triples_factory = triple_factory_from_csv(csvpath)
    
    # Load the dataset for grid search
    dataset = pykeen_dataset_from_csv(csvpath)
    
    # Split the dataset
    train, test, val = train_test_val_split_from_csv(csvpath, splits_ratio)
    
    return triples_factory, dataset, train, test, val



