import pandas as pd

# Lire un fichier Parquet
df = pd.read_parquet('/home/brian/Documents/python/princia/dataset/train-00000-of-00001.parquet')

# Afficher les premières lignes du DataFrame
print(df.head())
