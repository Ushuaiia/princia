import json

def save_partial_results(data, filepath):
    """Sauvegarde les résultats partiels dans un fichier."""
    with open(filepath, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Chemin vers votre fichier .jsonl
file_path = 'datatset_neural.jsonl'
output_path = 'converted_dataset.json'

new_dataset = []

try:
    with open(file_path, 'r') as file:
        for line in file:
            conversation = json.loads(line)

            for exchange in conversation.get('conversations', []):
                if exchange['from'] == 'human':
                    question = exchange['value']
                elif exchange['from'] == 'gpt':
                    response = exchange['value']

                    print(f"Question: {question}")
                    system_input = input("Entrez le contenu pour 'system': ")

                    print(f"Réponse: {response}")
                    rejected_input = input("Entrez le contenu pour 'rejected': ")

                    new_entry = {
                        'system': system_input,
                        'user': question,
                        'assistant': '',
                        'chosen': response,
                        'rejected': rejected_input,
                        'variables': conversation.get('variables', {}),
                        'id': conversation.get('id', '')
                    }
                    new_dataset.append(new_entry)

                    # Sauvegarder après chaque entrée traitée
                    save_partial_results(new_dataset, output_path)

except KeyboardInterrupt:
    print("\nInterruption détectée, sauvegarde des données jusqu'à présent...")
    save_partial_results(new_dataset, output_path)

# Enregistrer le dataset complet à la fin du traitement
save_partial_results(new_dataset, output_path)
print("Traitement terminé et données sauvegardées.")
