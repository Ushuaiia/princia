import json
import pandas as pd
import language_tool_python

# Initialiser LanguageTool
tool = language_tool_python.LanguageTool('fr')

# Mots clés à exclure
exclude_keywords = ["prompt", "user", "assistant", "chosen", "rejected", "system", "You are an AI assistant that helps people find information and you always answer in French.","<|im_end|>", "<|im_start|>"]

def clean_text(text):
    """ Nettoie le texte en retirant les mots clés spécifiés. """
    for word in exclude_keywords:
        text = text.replace(word, "")
    return text.strip()

def check_grammar(text):
    """ Vérifie la grammaire d'un texte et retourne les erreurs. """
    return tool.check(text)

# Lire le fichier JSONL
file_path = '/home/brian/Documents/python/princia/little_transformed_dataset.jsonl'
data = []
with open(file_path, 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Préparer les DataFrames pour les résultats
error_count_df = pd.DataFrame(columns=['line_number', 'error_count'])
correction_suggestions_df = pd.DataFrame(columns=['line_number', 'original_text', 'suggestion', 'rule_id', 'message'])

# Effectuer les vérifications
for i, entry in enumerate(data):
    # Nettoyer et vérifier les textes
    prompt_text = clean_text(entry['prompt'])
    chosen_text = clean_text(entry['chosen'])

    prompt_matches = check_grammar(prompt_text)
    chosen_matches = check_grammar(chosen_text)

    total_errors = len(prompt_matches) + len(chosen_matches)
    #Ajouter les données dans le DataFrame avec pd.concat
    error_count_df = pd.concat([error_count_df, pd.DataFrame({'line_number': [i], 'error_count': [total_errors]})], ignore_index=True)

    # Ajouter les suggestions de correction
    for match in prompt_matches + chosen_matches:
        new_row = pd.DataFrame({
            'line_number': [i],
            'original_text': [prompt_text if match in prompt_matches else chosen_text],
            'suggestion': [match.replacements[0] if match.replacements else ''],
            'rule_id': [match.ruleId],
            'message': [match.message]
        })
        correction_suggestions_df = pd.concat([correction_suggestions_df, new_row], ignore_index=True)

# Créer un writer Pandas Excel et enregistrer les DataFrames dans des feuilles différentes
with pd.ExcelWriter('/home/brian/Documents/python/princia/grammar_check_report.xlsx') as writer:
    error_count_df.to_excel(writer, sheet_name='nombre_d_erreurs', index=False)
    correction_suggestions_df.to_excel(writer, sheet_name='propositions_correction', index=False)

