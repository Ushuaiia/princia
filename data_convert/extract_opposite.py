import json

def extract_from_gpt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line_num, line in enumerate(infile, 1):
            try:
                data = json.loads(line)
                conversations = data.get('conversations', [])
                for conversation in conversations:
                    if conversation.get('from') == 'gpt':
                        from_gpt_value = conversation.get('value', '')
                        outfile.write(from_gpt_value + '\n')
            except json.JSONDecodeError as e:
                print(f"Erreur lors du décodage de la ligne {line_num}: {e}")

# Utiliser le script
input_jsonl_file = 'datatset_neural (copy).jsonl'  # Remplacez par le nom de votre fichier .jsonl
output_text_file = 'output.txt'             # Le fichier texte de sortie

extract_from_gpt(input_jsonl_file, output_text_file)
