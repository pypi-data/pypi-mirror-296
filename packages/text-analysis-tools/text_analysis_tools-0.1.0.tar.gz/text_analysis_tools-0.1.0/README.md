

# Text Toolkit

Text Toolkit est un package Python simple et efficace pour analyser et manipuler des chaînes de caractères. Il fournit plusieurs fonctions permettant de compter des éléments tels que les points, les points d'exclamation, les virgules, les mots, et plus encore. 

## Installation

Pour installer le package, clonez le dépôt ou utilisez une commande pip une fois le package publié sur PyPI.

pip install text_analysis_tools


## Utilisation

Voici quelques exemples d'utilisation des différentes fonctions fournies par text_analysis_tools.

### Exemple 1 : Compter le nombre de points
python
from text_analysis_tools.core import count_periods

text = "Bonjour. Comment ça va? Tout est bien."
print(count_periods(text))  # Affiche 1


### Exemple 2 : Compter le nombre de points d'exclamation
python
from text_analysis_tools.core import count_exclamations

text = "C'est incroyable! Je n'y crois pas!"
print(count_exclamations(text))  # Affiche 2


### Exemple 3 : Compter le nombre de mots
python
from text_analysis_tools.core import count_words

text = "Ceci est un exemple simple."
print(count_words(text))  # Affiche 5


### Exemple 4 : Compter le nombre de virgules
python
from text_analysis_tools.core import count_commas

text = "Le chat, le chien, et le lapin sont des animaux domestiques."
print(count_commas(text))  # Affiche 2


### Exemple 5 : Compter le nombre de phrases
python
from text_analysis_tools.core import count_sentences

text = "Bonjour! Comment vas-tu? Je vais bien."
print(count_sentences(text))  # Affiche 3


### Exemple 6 : Compter le nombre de questions
python
from text_analysis_tools.core import count_questions

text = "Qui est là? Pourquoi es-tu venu?"
print(count_questions(text))  # Affiche 2


## Fonctionnalités

- **count_periods(text)** : Retourne le nombre de points ('.') dans un texte.
- **count_exclamations(text)** : Retourne le nombre de points d'exclamation ('!') dans un texte.
- **count_words(text)** : Retourne le nombre de mots dans un texte.
- **count_commas(text)** : Retourne le nombre de virgules (',') dans un texte.
- **count_sentences(text)** : Retourne le nombre total de phrases dans un texte, basé sur les '.', '!', et '?'.
- **count_questions(text)** : Retourne le nombre de points d'interrogation ('?') dans un texte.

