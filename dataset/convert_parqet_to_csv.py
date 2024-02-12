import pandas as pd

# Lire le fichier Parquet
df = pd.read_parquet('/home/brian/Documents/python/princia/dataset/train-00000-of-00001.parquet')

# Convertir le DataFrame en CSV
df.to_csv('/home/brian/Documents/python/princia/dataset/train-00000-of-00001.csv', index=False)

