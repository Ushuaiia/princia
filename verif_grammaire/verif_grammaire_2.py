import json
import pandas as pd
import language_tool_python

# Initialiser LanguageTool
tool = language_tool_python.LanguageTool('fr')

def check_grammar(text):
    """ Vérifie la grammaire d'un texte et retourne les erreurs. """
    return tool.check(text)

def find_index(text, keyword):
    """Trouve l'indice de début du mot-clé dans le texte."""
    try:
        return text.index(keyword)
    except ValueError:
        return None

def remove_specific_phrase(text, phrase):
    """Supprime une phrase spécifique du texte."""
    return text.replace(phrase, "")

# Phrase à exclure
exclude_phrase = "You are an AI assistant that helps people find information and you always answer in French."

# Lire le fichier JSONL
file_path = '/mnt/data/transformed_dataset.jsonl'
data = []
with open(file_path, 'r') as file:
    for line in file:
        data.append(json.loads(line))

# DataFrames pour les résultats
error_count_df = pd.DataFrame(columns=['line_number', 'error_count'])
correction_suggestions_df = pd.DataFrame(columns=['line_number', 'original_text', 'suggestion', 'rule_id', 'message'])

# Boucler sur le dataset et les intervalles
for i, entry in enumerate(data):
    text = remove_specific_phrase(entry['prompt'], exclude_phrase)
    
    # Exemple d'intervalles basés sur des mots-clés
    keyword1_index = find_index(text, "<|im_start|>system")
    keyword2_index = find_index(text, "<|im_end|>")
    keyword3_index = find_index(text, "<|im_start|> user")
    keyword4_index = find_index(text, "<|im_end|>")
    keyword5_index = find_index(text, "<|im_start|>  assistant")
    keyword6_index = find_index(text, "user")
    keyword7_index = find_index(text, "assistant")
    keyword8_index = find_index(text, "chosen")
    keyword9_index = find_index(text, "<|im_end|>")
    keyword10_index = find_index(text, "rejected")
    keyword11_index = find_index(text, "<|im_end|>")

    intervals = []
    if keyword1_index is not None and keyword2_index is not None:
        intervals.append((keyword1_index + len("user"), keyword2_index))
    if keyword3_index is not None and keyword4_index is not None:
        intervals.append((keyword3_index + len("chosen"), keyword4_index))
    if keyword5_index is not None and keyword6_index is not None:
        intervals.append((keyword3_index + len("chosen"), keyword4_index))
    if keyword7_index is not None and keyword8_index is not None:
        intervals.append((keyword3_index + len("chosen"), keyword4_index))
    if keyword9_index is not None and keyword10_index is not None:
        intervals.append((keyword3_index + len("chosen"), keyword4_index))
    if keyword10_index is not None and keyword11_index is not None:
        intervals.append((keyword3_index + len("chosen"), keyword4_index))

    total_errors = 0
    for start, end in intervals:
        text_to_check = text[start:end]
        matches = check_grammar(text_to_check)
        total_errors += len(matches)

        for match in matches:
            correction_suggestions_df = pd.concat([correction_suggestions_df, pd.DataFrame({
                'line_number': [i],
                'original_text': [text_to_check],
                'suggestion': [match.replacements[0] if match.replacements else ''],
                'rule_id': [match.ruleId],
                'message': [match.message]
            })], ignore_index=True)

    error_count_df = pd.concat([error_count_df, pd.DataFrame({'line_number': [i], 'error_count': [total_errors]})], ignore_index=True)

# Enregistrement dans un fichier Excel
with pd.ExcelWriter('/mnt/data/grammar_check_report.xlsx') as writer:
    error_count_df.to_excel(writer, sheet_name='nombre_d_erreurs', index=False)
    correction_suggestions_df.to_excel(writer, sheet_name='propositions_correction', index=False)
