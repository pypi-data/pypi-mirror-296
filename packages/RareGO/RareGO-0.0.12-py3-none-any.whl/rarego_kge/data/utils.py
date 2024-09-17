import pandas as pd
from importlib import resources

def list_csv_files():
    csv_files = []
    package_dir = resources.files('rarego_kge.data')
    for file in package_dir.iterdir():
        if file.suffix == '.csv':
            csv_files.append(file.name)
    return csv_files

def read_csv_file(filename):
    if not filename.endswith('.csv'):
        raise ValueError("File must be a CSV")
    
    package_dir = resources.files('cpykg.data')
    file_path = package_dir / filename
    
    with file_path.open('r') as file:
        df = pd.read_csv(file,index_col=0)
    return df