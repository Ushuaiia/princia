import json
import pandas as pd

# Fonctions de vérification (Ces fonctions sont des placeholders et doivent être développées davantage)
def check_grammar(text):
    # À remplacer par une vraie vérification grammaticale
    return True

def check_completeness(text):
    # Vérifie si le texte est complet (non vide et se termine par un point)
    return bool(text) and text.strip().endswith('.')

def check_consistency(prompt, response):
    # À remplacer par une vraie vérification de cohérence
    return True

def check_input_positions(entry):
    input_start_correct = 'input_start' in entry and isinstance(entry['input_start'], int) and entry['input_start'] >= 0
    input_end_correct = 'input_end' in entry and isinstance(entry['input_end'], int) and entry['input_end'] >= entry['input_start']
    return input_start_correct, input_end_correct

# Chemin vers le fichier JSONL
file_path = '/mnt/data/transformed_dataset.jsonl'

# Analyser le fichier JSONL
data = []
with open(file_path, 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Créer un DataFrame pour les résultats
results = pd.DataFrame(columns=['line_number', 'prompt', 'chosen', 'grammar_error', 'completeness_error', 'consistency_error', 'input_start_error', 'input_end_error'])

# Effectuer les vérifications
for i, entry in enumerate(data):
    grammar_check = check_grammar(entry['prompt']) and check_grammar(entry['chosen'])
    completeness_check = check_completeness(entry['prompt']) and check_completeness(entry['chosen'])
    consistency_check = check_consistency(entry['prompt'], entry['chosen'])
    input_start_correct, input_end_correct = check_input_positions(entry)

    results = results.append({
        'line_number': i,
        'prompt': entry['prompt'],
        'chosen': entry['chosen'],
        'grammar_error': not grammar_check,
        'completeness_error': not completeness_check,
        'consistency_error': not consistency_check,
        'input_start_error': not input_start_correct,
        'input_end_error': not input_end_correct
    }, ignore_index=True)

# Sauvegarder les résultats dans un fichier Excel
results.to_excel('/mnt/data/dataset_check_report.xlsx', index=False)
