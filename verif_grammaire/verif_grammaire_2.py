import json
import pandas as pd
import language_tool_python

# Initialiser LanguageTool
tool = language_tool_python.LanguageTool('fr')

def check_grammar(text):
    """ Vérifie la grammaire d'un texte et retourne les erreurs. """
    return tool.check(text)

# Lire le fichier JSONL
file_path = '/mnt/data/transformed_dataset.jsonl'
data = []
with open(file_path, 'r') as file:
    for line in file:
        data.append(json.loads(line))

# DataFrames pour les résultats
error_count_df = pd.DataFrame(columns=['line_number', 'error_count'])
correction_suggestions_df = pd.DataFrame(columns=['line_number', 'original_text', 'suggestion', 'rule_id', 'message'])

# Définir les intervalles de texte à vérifier (exemple)
for i, entry in enumerate(data):
    # Supposons que vous avez déterminé les indices pour extraire le texte
    start_index = ...  # Début de l'intervalle
    end_index = ...    # Fin de l'intervalle

    text_to_check = entry['prompt'][start_index:end_index]  # Exemple d'extraction
    matches = check_grammar(text_to_check)

    # Ajout des résultats dans les DataFrames
    error_count_df = pd.concat([error_count_df, pd.DataFrame({'line_number': [i], 'error_count': [len(matches)]})], ignore_index=True)
    for match in matches:
        correction_suggestions_df = pd.concat([correction_suggestions_df, pd.DataFrame({
            'line_number': [i],
            'original_text': [text_to_check],
            'suggestion': [match.replacements[0] if match.replacements else ''],
            'rule_id': [match.ruleId],
            'message': [match.message]
        })], ignore_index=True)

# Enregistrement dans un fichier Excel
with pd.ExcelWriter('/mnt/data/grammar_check_report.xlsx') as writer:
    error_count_df.to_excel(writer, sheet_name='nombre_d_erreurs', index=False)
    correction_suggestions_df.to_excel(writer, sheet_name='propositions_correction', index=False)

