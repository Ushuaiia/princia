import json
import random

def transform_conversation(conversations):
    prompt = "system\nYou are an AI assistant. You will be given a task. You must generate a detailed and long answer.\nuser\n"
    conversation_segments = []

    rejected_options = [
        "Je ne peux vous répondre",
        "Pouvez-vous répéter la question s'il vous plaît?",
        "Désolé, je ne vous comprends pas"
    ]

    for i in range(0, len(conversations), 2):
        if i + 1 < len(conversations) and "]" not in conversations[i]["value"]:
            user_part = conversations[i]["value"]
            gpt_part = conversations[i + 1]["value"]
            rejected = random.choice(rejected_options)
            segment = {
                'question': user_part,
                'chosen': gpt_part,
                'rejected': rejected
            }
            conversation_segments.append(segment)

    return {
        'prompt': prompt,
        'conversation': conversation_segments
    }

def transform_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in file:
            conversation = json.loads(line)
            transformed = transform_conversation(conversation["conversations"])
            json.dump(transformed, outfile, ensure_ascii=False)
            outfile.write("\n")

# Exemple d'utilisation
input_file = 'dataset_neural.jsonl'
output_file = 'cible.jsonl'
transform_data(input_file, output_file)
