# __init__.py

import pandas as pd
from pathlib import Path

def load_r25kg_rare_dataset():
    """
    Load the R25KG-Rare dataset from a TSV file.
    
    Returns:
    pandas.DataFrame: The loaded R25KG-Rare dataset.
    """
    file_path = Path(__file__).parent / "data" / "R25KG-Rare.tsv"
    return pd.read_csv(file_path, sep='\t')

def load_r25kg_Gene_dataset():
    #"""
    #Load the R25KG-Common dataset from a TSV file.
    
    #Returns:
    #pandas.DataFrame: The loaded R25KG-Common dataset.
    """
    file_path = Path(__file__).parent / "data" / "R25KG-Rare-Gene.tsv"
    return pd.read_csv(file_path, sep='\t')

class R25KGDataset:
   
    def __init__(self):
        self.rare = load_r25kg_rare_dataset()
        self.common = load_r25kg_gene_dataset()

    def get_rare(self):
        """Return the R25KG-Rare dataset."""
        return self.rare

    def get_common(self):
        """Return the R25KG-gene dataset."""
        return self.common

    def get_combined(self):
        """Return a combined dataset of both rare and common."""
        return pd.concat([self.rare, self.common], ignore_index=True)

# Make these functions and the class available when the package is imported
__all__ = ['load_r25kg_rare_dataset', 'load_r25kg_gene_dataset', 'R25KGDataset']

