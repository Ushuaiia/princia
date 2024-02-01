import language_tool_python

# Créer un objet LanguageTool pour le français
tool = language_tool_python.LanguageTool('fr')

# Texte à vérifier
text = "Ce texte a un faute."

# Effectuer la vérification
matches = tool.check(text)

# Afficher les résultats
print("Nombre d'erreurs trouvées :", len(matches))
for match in matches:
    print(match)
