import pandas as pd

# Tester avec une petite partie du fichier Parquet
df = pd.read_parquet('/home/brian/Documents/python/princia/dataset/train-00000-of-00001.parquet', nrows=100)

# Convertir en CSV
df.to_csv('/home/brian/Documents/python/princia/dataset/nouveau_fichier.csv', index=False)

