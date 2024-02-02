import xml.etree.ElementTree as ET

def parse_xml_to_dialogues(file_path):
    dialogues = []

    # Charger le fichier XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Parcourir les différents chapitres et extraire les titres et paragraphes
    for chapitre in root.findall('.//Chapitre'):
        # Utiliser le titre du chapitre comme question
        question = chapitre.find('.//Titre/Paragraphe').text if chapitre.find('.//Titre/Paragraphe') is not None else "Question non trouvée"

        # Utiliser les paragraphes comme réponse
        reponse = " ".join([p.text for p in chapitre.findall('.//Paragraphe') if p.text])

        if reponse:
            dialogues.append({"question": question, "reponse": reponse})

    return dialogues

# Emplacement de votre fichier XML
file_path = '/home/brian/Documents/python/princia/dataset/F34328.xml'  # Remplacez par le chemin réel de votre fichier XML

# Exécuter le script et afficher les dialogues
dialogues = parse_xml_to_dialogues(file_path)
for dialogue in dialogues:
    print("Question:", dialogue["question"])
    print("Réponse:", dialogue["reponse"])
    print("---")

