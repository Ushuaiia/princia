import pandas as pd

def convert_parquet_to_text(parquet_file_path, text_file_path):
    # Lire le fichier Parquet
    df = pd.read_parquet(parquet_file_path)

    # Convertir chaque ligne du DataFrame en une chaîne de caractères
    with open(text_file_path, 'w', encoding='utf-8') as file:
        for index, row in df.iterrows():
            # Convertir la ligne en chaîne de caractères
            line = row.to_string() + '\n\n'
            # Écrire la ligne dans le fichier texte
            file.write(line)

# Chemins des fichiers
parquet_file_path = '/home/brian/Documents/python/princia/dataset/train-00000-of-00001.parquet'  # Remplacer par le chemin de votre fichier Parquet
text_file_path = '/home/brian/Documents/python/princia/dataset/train-00000-of-00001.txt'       # Remplacer par le chemin de destination souhaité

# Exécuter la fonction de conversion
convert_parquet_to_text(parquet_file_path, text_file_path)

